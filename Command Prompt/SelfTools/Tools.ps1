[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# 檢查是否有管理員權限
function IsAdmin {
    # 創建 WindowsPrincipal 對象
    $principal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

if (-not (IsAdmin)) {
    # 提升權限重啟腳本
    Start-Process powershell -ArgumentList "& '$PSCommandPath'" -Verb RunAs
    exit
}

function Print { # 打印文本
    param (
        [string]$text,
        [string]$foregroundColor = 'White',
        [string]$backgroundColor = 'Black'
    )

    # 設置颜色
    $Host.UI.RawUI.ForegroundColor = [ConsoleColor]::$foregroundColor
    $Host.UI.RawUI.BackgroundColor = [ConsoleColor]::$backgroundColor
    
    # 打印文本 (粗體)
    Write-Host "[1m$text"
}

function Input { # 輸入文字
    param (
        [string]$text,
        [string]$foregroundColor = 'default'
    )

    if ($foregroundColor -eq 'default') {
        return Read-Host "`n[37m[7m[1m$text[27m"
    } else {
        $Host.UI.RawUI.ForegroundColor = [ConsoleColor]::$foregroundColor
        $Host.UI.RawUI.BackgroundColor = [ConsoleColor]::'Black'
        return Read-Host "`n[1m$text"
    }
}

<#
    Todo PowerShell 不支援的 =>
    * 文字效果 : 1m(粗體) 3m(斜體) 23m(正體) 4m(底線) 53m(上划線) 22m(雙底線) 9m(刪除線) 7m(背景色與文字色反轉) 27m(復原背景色與文字色)
    * 背景色 : 49m(透明底)

    ~ 文字色
    & 灰黑色 (30m)：DarkGray
    & 紅色 (31m)：Red
    & 綠色 (32m)：Green
    & 黃色 (33m)：Yellow
    & 藍色 (34m)：Blue
    & 紫色 (35m)：Magenta
    & 青藍色 (36m)：Cyan
    & 白色 (37m)：White
    & 黑色 (40m)：Black
#>

class Main {
    static [int]$InitIndex = 0 # 菜單的索引計數
    static [string]$Temp = $env:Temp # 配置路徑

    # 等待返回菜單
    [void]WaitBack() {
        Input "Enter 返回選單"
        $this.Menu()
    }

    # 運行 CMD 指令並打印出來, 命令, 是否確認後返回首頁
    [void]CMD([string]$command, [bool]$back) {
        Start-Process cmd.exe -ArgumentList "/c $command" -NoNewWindow -Wait
        if ($back) {
            $this.WaitBack()
        }
    }

    # 關閉進程 (傳入要關閉的進程名稱)
    [void]StopProcess([object]$Process) {
        $ProcessList = Get-Process
        if ($Process -is [string]) { # 傳入的是字串
            Stop-Process -Name $Process -Force -ErrorAction SilentlyContinue
        } elseif ($Process -is [array] -and $Process[0] -is [string]) { # 傳入的是一維列表
            $Process | ForEach-Object {
                Stop-Process -Name $_ -Force -ErrorAction SilentlyContinue
            }
        }
    }

    # 獲取遠端授權代碼
    [void]Authorize([string]$DL_Path, [string]$DL_URL) {
        Print "===== 獲取最新版本 授權程式 =====`n"
        if (Test-Path $DL_Path) { Remove-Item $DL_Path -Force } # 先刪除舊文件
        Invoke-WebRequest -Uri $DL_URL -OutFile $DL_Path
        if (-not (Test-Path $DL_Path)) {
            Print "獲取失敗" 'Red'
            $this.WaitBack()
        }
        $this.CMD($DL_Path, $true)
    }

    # 註冊預設值 (特殊函數)
    [void]__RegistSpecial([string]$Path, [string]$Name, [object]$Value, [object]$FollowParent, [bool]$Delete) {
        if ($null -eq $FollowParent -and -not (Test-Path $Path)) {
            New-Item -Path $Path -Force
        }

        try {
            if (-not($Delete)) { # 當刪除是 true, 那他的反就不會觸發這邊
                throw [System.Exception]::new("不刪除")
            }

            if ($null -ne $FollowParent) {
                if (Test-Path $FollowParent) {
                    throw [System.Exception]::new("父母存在 進行註冊")
                }
            } else {
                Get-ItemProperty -Path $Path -Name $Name -ErrorAction Stop
                Remove-Item -Path $Path -Recurse -Force
            }

            Print "已刪除: $Name" 'Red'
        } catch {
            if ($null -ne $FollowParent -and -not (Test-Path $Path)) {
                New-Item -Path $Path -Force
            }

            Set-ItemProperty -Path $Path -Name $Name -Value $Value
            Print "已註冊: $Name" 'Green'
        }
    }
    # 註冊值 (不應該直接調用)
    [void]__RegistNormal([string]$Path, [string]$Name, [string]$Type, [object]$Value, [object]$FollowParent, [bool]$Delete) {
        if ($null -eq $FollowParent -and -not (Test-Path $Path)) {
            New-Item -Path $Path -Force # 路徑添加
        }
        try { # 檢查註冊表值是否存在
            if (-not($Delete)) { # 跳過刪除
                throw [System.Exception]::new("不刪除")
            }

            if ($null -ne $FollowParent) {
                if (Test-Path $FollowParent) {
                    throw [System.Exception]::new("父母存在 進行註冊")
                }
            } else {
                Get-ItemProperty -Path $Path -Name $Name -ErrorAction Stop
                Remove-Item -Path $Path -Recurse -Force
            }

            Print "已移除: $Name" 'Red'
        } catch {
            if ($null -ne $FollowParent -and -not (Test-Path $Path)) {
                New-Item -Path $Path -Force
            }

            New-ItemProperty -Path $Path -Name $Name -PropertyType $Type -Value $Value -Force # 不存在就添加
            Print "已註冊: $Name" 'Green'
        }
    }
    <#
        註冊表操作 (非 reg add)

        參數 1 設置註冊表
        參數 2 是否需要反選 觸發 刪除

        $this.RegistItem(@(path, name, type, value), $true)

        $this.RegistItem(@(
            @(path, name, type, value),
            @(path, name, type, value)
        ), $true)

        $this.RegistItem(@{path=1; name=2; type=3; value=4}, $true)
    #>
    [void]RegistItem([System.Object]$Items, [bool]$Delete) {
        if ($Items -is [array] -and $Items[0] -is [string]) { # 一維數組
            $this.__RegistNormal($Items[0], $Items[1], $Items[2], $Items[3], $null, $Delete)
        } elseif ($Items -is [array] -and $Items[0] -is [array]) { # 二維數組
            $Items | ForEach-Object {
                $this.__RegistNormal($_[0], $_[1], $_[2], $_[3], $null, $Delete)
            }
        } elseif ($Items -is [array] -and $Items[0] -is [System.Collections.Hashtable]) { # 一維是數組 二維是 哈希表
            $Items | ForEach-Object {
                if ($null -ne $_.type) { # parent 會讓該項目已他作為檢查值, 只要父項存在就是無條件創建, 只要父項不存在, 就是無條件刪除
                    $this.__RegistNormal($_.path, $_.name, $_.type, $_.value, $_.parent, $Delete)
                } else {
                    $this.__RegistSpecial($_.path, $_.name, $_.value, $_.parent, $Delete)
                }
            }
        } else {
            Print "不支援的註冊格式: $Items" 'Red'
        }
    }

    # 字串轉 MD5
    [string]MD5([string]$string) {
        $MD5 = [System.Security.Cryptography.MD5]::Create()
        $FileByte = [System.Text.Encoding]::UTF8.GetBytes($string)
        $HashByte = $MD5.ComputeHash($FileByte)
        $HashString = [BitConverter]::ToString($HashByte) -replace '-'
        $LowerString = $HashString.ToLower()
        return $LowerString.Substring(8, 24)
    }

    [void]Menu() {
        # 獲取防火牆狀態並提取狀態
        $firewallStatus = netsh advfirewall show allprofiles state | Select-String "State" | 
        ForEach-Object { $_.ToString().Trim() -replace 'State\s+', '' } | 
        Select-Object -First 1

        # 根據防火牆狀態設置 display 變量
        $display = if ($firewallStatus -eq "ON") {
            "[[32m啟用[37m]"
        } else {
            "[[31m禁用[37m]"
        }

        [Main]::InitIndex = 0 # 每次調用會重設
        function Index { # 根據調用次數累加索引值
            param (
                [string]$param = ""
            )

            if ($param -eq "") {
                [Main]::InitIndex++
                return "[[31m$([Main]::InitIndex)[37m]"
            } else {
                return "[[31m$param[37m]"
            }
        }

        Clear-Host

        # 打印菜单内容
        $P_ = "縮排用方便自己觀看 (不會打印出來)"
        Print "========================================================================================================================" 'Red'
        Print "                                              - 工具箱v2 Versions 0.0.1 -" 'Magenta'
        Print "========================================================================================================================" 'White'
        $P_
        Print "   Windows 系統開關機 :" 'Cyan'
        $P_
        Print "   $(Index) 睡眠    $(Index) 重啟    $(Index) 關機`n" 'White'
        $P_
        Print "   Windows 防火牆開關 :" 'Cyan'
        $P_
        Print "   $(Index) 開啟防火牆    $(Index) 關閉防火牆    [33m當前狀態:[37m $display`n" 'White'
        $P_
        Print "   Windows 優化相關 :" 'Cyan'
        $P_
        Print "   $(Index) .NET安裝    $(Index) Visual C++ (x64)安裝    $(Index) 關閉UAC安全通知" 'White'
        $P_
        Print "   $(Index) Windows 一鍵優化    $(Index) Windows 恢復不適用優化    $(Index) Win11 檔案總管優化 (再次運行恢復)`n" 'White'
        $P_
        Print "   瀏覽器設置 :" 'Cyan'
        $P_
        Print "   $(Index) Google 變更緩存位置    $(Index) Google 一鍵優化設置    $(Index) Google 重置受機構管理" 'White'
        $P_
        Print "   $(Index) Edge 變更緩存位置    $(Index) Edge 一鍵優化設置    $(Index) Edge 重置受組織管理`n" 'White'
        $P_
        Print "   授權啟用 :" 'Cyan'
        $P_
        Print "   $(Index) RAR 授權     $(Index) IDM 授權    $(Index) Windows 啟用授權    $(Index) Office 啟用授權`n" 'White'
        $P_
        Print "   進程操作 :" 'Cyan'
        $P_
        Print "   $(Index) Google 結束進程    $(Index) Edge 結束進程    $(Index) Adobe 結束進程`n" 'White'
        $P_
        Print "   服務操作 :" 'Cyan'
        $P_
        Print "   $(Index) Surfshark 運行    $(Index) Surfshark 終止`n" 'White'
        $P_
        Print "   特殊功能 :" 'Cyan'
        $P_
        Print "   $(Index) 網路重置    $(Index) 自動配置 DNS" 'White'
        Print "------------------------------------------------------------------------------------------------------------------------" 'Red'
        Print "                                             - 系統指令操作 (不分大小寫) -" 'Magenta'
        Print "------------------------------------------------------------------------------------------------------------------------" 'Red'
        Print "   $(Index 'CT') 系統控制台    $(Index 'GP') 本機群組原則    $(Index 'RD') 登入編輯程式    $(Index 'UG') 使用者群組    $(Index 'DX') DX診斷工具    $(Index 'MF') 系統開機設置" 'White'
        $P_
        Print "   $(Index 'WS') 電腦啟用狀態    $(Index 'SI') 查看系統資訊    $(Index 'MSI') 查看完整系統資訊    $(Index 'NV') 查看顯卡驅動版本    $(Index 'HW') 查看電腦機器碼" 'White'
        $P_
        Print "   $(Index 'IP') 查看電腦IP位置    $(Index 'RS') 查看遠端分享    $(Index 'MC') MAC地址查詢    $(Index 'SV') 查看運行中的服務    $(Index 'MRT') 惡意軟體移除工具" 'White'
        $P_
        Print "   $(Index 'WF') 顯示已連接過的wifi    $(Index 'DV') 修復驅動安裝問題    $(Index 'SR') 系統錯誤修復" 'White'
        Print "========================================================================================================================" 'White'
        Print "                                    $(Index 'H') 工具說明     $(Index '0') 離開程式     $(Index 'V') 更新資訊" 'White'
        Print "========================================================================================================================" 'Red'

        $this.Choice()
    }

    [void]Choice() {
        $choice = Input "輸入功能 [代號]"
        Clear-Host

        switch ($choice) {
            0 {exit} # 離開
            "V" { # 更新資訊
                Print "----------------------------"
                Print ""
                Print "  Versions 0.0.1 更新:"
                Print ""
                Print "      1. 首次發佈"
                Print ""
                Print "----------------------------"
                $this.WaitBack()
            }
            "H" { # 使用說明
                Print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
                Print ""
                Print " - 使用說明:"
                Print ""
                Print " 1. 需操作的程式 , 必須都安裝在預設的路徑上 , 才可成功運行"
                Print ""
                Print " 2. 授權啟用工具 , 由網路下載資源(有時候下載比較慢) 請等待"
                Print ""
                Print " 3. 請注意某些特別的設置(優化之類的) , 這是以本人的電腦製作的 , 不一定適用於所有人"
                Print ""
                Print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
                $this.WaitBack()
            }
            "CT" { # 系統控制台
                Control
                $this.Menu()
            }
            "GP" { # 本機群組原則
                gpedit.msc
                $this.Menu()
            }
            "RD" { # 登入編輯程式
                regedit
                $this.Menu()
            }
            "UG" { # 使用者群組
                lusrmgr.msc
                $this.Menu()
            }
            "DX" { # DX診斷工具
                dxdiag
                $this.Menu()
            }
            "MF" { # 系統開機設置
                msconfig
                $this.Menu()
            }
            "WS" { # 電腦啟用狀態
                slmgr.vbs -xpr
                $this.Menu()
            }
            "SI" { # 查看系統資訊
                Print "請稍等...`n"
                $this.CMD("systeminfo", $true)
            }
            "MSI" { # 查看完整系統資訊
                MSInfo32
                $this.Menu()
            }
            "NV" { # 查看顯卡驅動版本
                $this.CMD("nvidia-smi", $true)
            }
            "HW" { # 查看機器碼
                Print "[92m===============================[93m"
                Print "[91m        作業系統"
                Print "[92m===============================[93m"
                $this.CMD("wmic Os get caption", $false)

                Print "[94m===============================[93m"
                Print "[91m      主機板資訊"
                Print "[94m===============================[93m"
                $this.CMD("wmic baseboard get product,manufacturer,serialnumber", $false)

                Print "[95m===============================[93m"
                Print "[91m       CPU資訊"
                Print "[95m===============================[93m"
                $this.CMD("wmic cpu get name,processorid,serialnumber", $false)

                Print "[96m===============================[93m"
                Print "[91m       硬碟資訊"
                Print "[96m===============================[93m"
                $this.CMD("wmic diskdrive get model,serialnumber,size", $false)

                Print "[92m===============================[93m"
                Print "[91m       RAM資訊"
                Print "[92m===============================[93m"
                $this.CMD("wmic memorychip get PartNumber, SerialNumber,speed", $false)

                Print "[94m===============================[93m"
                Print "[91m       GPU資訊"
                Print "[94m===============================[93m"
                $this.CMD("wmic Path win32_videocontroller get name,Description,PNPDeviceID", $false)

                Print "[95m===============================[93m"
                Print "[91m       BIOS資訊"
                Print "[95m===============================[93m"
                $this.CMD("wmic bios get serialnumber,Manufacturer,Name", $false)

                Print "[96m===============================[93m"
                Print "[91m       BIOS資訊 UUID"
                Print "[96m===============================[93m"
                $this.CMD("wmic csproduct get uuid", $false)

                Print "[92m===============================[93m"
                Print "[91m       網路卡資訊"
                Print "[92m===============================[93m"
                $this.CMD("wmic Nic get caption", $false)

                Print "[94m===============================[93m"
                Print "[91m       MAC 地址"
                Print "[94m===============================[93m"
                $this.CMD("getmac", $true)
            }
            "IP" { # 查看 IP 和網卡資訊
                $this.CMD("ipconfig /all", $true)
            }
            "RS" { # 查看遠端分享
                $this.CMD("net share", $true)
            }
            "MC" { # MAC地址查詢
                $this.CMD("getmac /fo table /v", $true)
            }
            "SV" { # 查看運行中的服務
                $this.CMD("net start", $true)
            }
            "MRT" { # 惡意軟體移除工具
                mrt
                $this.Menu()
            }
            "WF" { # 顯示已連接過的wifi
                $this.CMD("netsh wlan show profiles", $true)
            }
            "DV" { # 修復驅動安裝問題
                msdt.exe -id DeviceDiagnostic
                $this.Menu()
            }
            "SR" { # 系統錯誤修復
                Print "準備修復 請稍後...`n" 'Yellow'

                $this.CMD("Dism /Online /Cleanup-Image /ScanHealth", $false)
                $this.CMD("Dism /Online /Cleanup-Image /CheckHealth", $false)
                $this.CMD("DISM /Online /Cleanup-image /RestoreHealth", $false)
                $this.CMD("sfc /scannow", $true)
            }
            1 { # 睡眠
                rundll32.exe powrprof.dll,SetSuspendState 0,1,0
            }
            2 { # 重啟
                Restart-Computer -Force
            }
            3 { # 關機
                Stop-Computer -Force
            }
            4 { # 開啟防火牆
                Print "===== 啟用中 =====`n"
                netsh advfirewall set allprofiles state on
                netsh advfirewall firewall set rule all new enable=yes
                $this.Menu()
            }
            5 { # 關閉防火牆
                Print "===== 禁用中 =====`n"
                netsh advfirewall set allprofiles state off
                netsh advfirewall firewall set rule all new enable=no
                $this.Menu()
            }
            6 { # .NET安裝
                # winget search Microsoft.DotNet.SDK

                $this.CMD("winget install Microsoft.DotNet.SDK.6", $false)
                $this.CMD("winget install Microsoft.DotNet.SDK.7", $false)
                $this.CMD("winget install Microsoft.DotNet.SDK.8", $true)
            }
            7 { # Visual C++ (x64)安裝
                # https://learn.microsoft.com/zh-tw/cpp/windows/latest-supported-vc-redist?view=msvc-170
                # https://www.techpowerup.com/download/visual-c-redistributable-runtime-package-all-in-one/

                $DownloadPath = "$([Main]::Temp)\Visual.tar"
                $DownloadURL = "https://raw.githubusercontent.com/Canaan-HS/Implementation-Project/Main/Command Prompt/Visual C++/Visual.tar"

                $InstallPackage = @( # 安裝包 與 安裝指令
                    @{ package = "vcredist2005_x64.exe"; Order = "/q" },
                    @{ package = "vcredist2008_x64.exe"; Order = "/qb" },
                    @{ package = "vcredist2010_x64.exe"; Order = "/passive /norestart" },
                    @{ package = "vcredist2012_x64.exe"; Order = "/passive /norestart" },
                    @{ package = "vcredist2013_x64.exe"; Order = "/passive /norestart" },
                    @{ package = "vcredist2015_2017_2019_2022_x64.exe"; Order = "/passive /norestart" }
                )

                # 有重複的先進行刪除
                if (Test-Path $DownloadPath) { Remove-Item $DownloadPath -Force }

                Print "檔案較大請稍後 - 安裝包日期 : 2024 年 05 月"
                Print "`n===== Visual C++ 開始下載 ====="

                # 請求數據
                Invoke-WebRequest -Uri $DownloadURL -OutFile $DownloadPath
                if (Test-Path $DownloadPath) { # 避免意外在檢測是否存在

                    tar -xvf $DownloadPath -C $env:Temp
                    Remove-Item $DownloadPath -Force # 解壓後刪除

                    # 遍歷安裝程式
                    Print "`n===== 開始安裝 ====="
                    foreach ($install in $InstallPackage) {
                        $Path = "$([Main]::Temp)\$($install.package)" # 合併路徑
                        if (Test-Path $Path) {
                            Start-Process -FilePath $Path -ArgumentList $install.Order -Wait -NoNewWindow
                            Remove-Item $Path -Force # 安裝完成刪除
                        }
                    }

                    $this.Menu()
                } else {
                    Print "`n下載失敗"
                    $this.WaitBack()
                }
            }
            8 { # 關閉UAC安全通知
                $this.RegistItem(@(
                    "HKLM:\Software\Microsoft\Windows\CurrentVersion\Policies\System", "EnableLUA", "DWORD", 0
                ), $false)
                Print "`n電腦重啟後生效"
                $this.WaitBack()
            }
            9 { # Windows 一鍵優化
                $this.RegistItem(@(
                    # 關機清除分頁文件
                    @("HKLM:\System\CurrentControlSet\Control\Session Manager\Memory Management", "ClearPageFileAtShutdown", "DWORD", 1),
                    # 禁用對執行文件（executable files）的分頁
                    @("HKLM:\System\CurrentControlSet\Control\Session Manager\Memory Management", "DisablePagingExecutive", "DWORD", 1),
                    # 使用大型系統高速緩存
                    @("HKLM:\System\CurrentControlSet\Control\Session Manager\Memory Management", "LargeSystemCache", "DWORD", 1),
                    # 設置記憶體使用大小 1920x1080 / 6 | 2560x1440 / 12 | 3840x2160 / 24
                    @("HKLM:\System\CurrentControlSet\Control\Session Manager\Memory Management", "SessionPoolSize", "DWORD", 12),

                    # 設為1，那麼當您使用遊戲列(Win+G)來錄製全螢幕模式下的遊戲時，系統會自動將遊戲切換到全螢幕視窗化模式，以提高錄製的效能和品質
                    @("HKCU:\System\GameConfigStore", "GameDVR_DXGIHonorFSEWindowsCompatible", "DWORD", 1),
                    # 設定全螢幕模式下的遊戲錄製品質。可能的值有0、1或2，分別代表高、中或低品質
                    @("HKCU:\System\GameConfigStore", "GameDVR_EFSEFeatureFlags", "DWORD", 0),
                    # 設定全螢幕模式下的遊戲錄製行為。可能的值有0、1或2，分別代表停用、全螢幕視窗化或全螢幕專屬模式
                    @("HKCU:\System\GameConfigStore", "GameDVR_FSEBehaviorMode", "DWORD", 2),
                    # 螢幕錄製功能啟用
                    @("HKCU:\System\GameConfigStore", "GameDVR_Enabled", "DWORD", 2),
                    # 啟用全螢幕錄製行為
                    @("HKCU:\System\GameConfigStore", "GameDVR_HonorUserFSEBehaviorMode", "DWORD", 1),

                    # 動畫效果最佳化
                    @("HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects", "VisualFXSetting", "DWORD", 2),
                    # 去除螢幕字形毛邊
                    @("HKCU:\Control Panel\Desktop", "FontSmoothing", "String", 2),
                    # 設置字體平滑的程度 (3高平滑)
                    @("HKCU:\Control Panel\Desktop", "FontSmoothingSize", "DWORD", 3),
                    # 使用平滑的動畫來滾動內容
                    @("HKCU:\Control Panel\Desktop", "SmoothScroll", "DWORD", 3),
                    # 允許使用更豐富的顏色來顯示圖形
                    @("HKCU:\Control Panel\Desktop", "ExtendedColors", "DWORD", 256),

                    # 雙緩衝 圖形渲染到兩個緩衝區中，一個用於顯示，另一個用於繪製
                    @("HKCU:\Control Panel\Desktop", "Doublebuffer", "DWORD", 1),
                    # 使用專用硬體來渲染圖形，從而提高性能
                    @("HKCU:\Control Panel\Desktop", "GraphicsAcceleration", "DWORD", 1),
                    # 允許在移動滑鼠指針到窗口時看到窗口的標題欄和邊框
                    @("HKCU:\Control Panel\Desktop", "HotTracking", "DWORD", 1),
                    # 自動結束未使用的程式
                    @("HKCU:\Control Panel\Desktop", "AutoEndTasks", "DWORD", 1),
                    # 光標閃爍速度
                    @("HKCU:\Control Panel\Desktop", "CursorBlinkingRate", "DWORD", 0)
                ), $false)

                Print "`n等待記憶體設置操作...`n"

                # 頁面合併
                Disable-MMAgent -PageCombining
                # 應用程式預讀取
                Disable-MMAgent -ApplicationPreLaunch

                # 記憶體壓縮
                Enable-MMAgent -MemoryCompression
                # 操作 API 調用時允許的最大文件數
                Set-MMAgent -MaxOperationAPIFiles 2048

                Print "`n========== 後續自行設置視覺效果 ==========`n"
                $this.CMD("control sysdm.cpl,,3", $false)

                Print "設置完成後 重啟 或 登出 應用效果"
                $this.WaitBack()
            }
            10 { # Windows 恢復不適用優化
                $this.RegistItem(@(
                    "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects", "VisualFXSetting", "DWORD", 0
                ), $false)
                $this.WaitBack()
            }
            11 { # Win11 檔案總管優化
                $pathA = "HKCU:\Software\Classes\CLSID\{2aa9162e-c906-4dd9-ad0b-3d24a8eef5a0}"
                $pathB = "HKCU:\Software\Classes\CLSID\{6480100b-5a83-4d1e-9f69-8ae5a88e9a33}"
                $dll = "C:\Windows\System32\Windows.UI.FileExplorer.dll_"

                $this.RegistItem(@(
                    # 以下為將檔案總管變回 win 10 的方式
                    @{path=$pathA; name="(default)"; value="CLSID_ItemsViewAdapter"},
                    @{path="$pathA\InProcServer32"; name="(default)"; value=$dll; parent=$pathA},
                    @{path="$pathA\InProcServer32"; name="ThreadingModel"; type="String"; value="Apartment"; parent=$pathA},

                    @{path=$pathB; name="(default)"; value="File Explorer Xaml Island View Adapter"},
                    @{path="$pathB\InProcServer32"; name="(default)"; value=$dll; parent=$pathB},
                    @{path="$pathB\InProcServer32"; name="ThreadingModel"; type="String"; value="Apartment"; parent=$pathB}
                ), $true)

                $this.RegistItem(@(
                    # 避免大量運算 檔案類型
                    @("HKCU:\Software\Classes\Local Settings\Software\Microsoft\Windows\Shell\Bags\AllFolders\Shell", "FolderType", "String", "NotSpecified")
                ), $true)

                $this.RegistItem(@(
                    @{path="HKCU:\Software\Microsoft\Internet Explorer\Toolbar\ShellBrowser"; name="ITBar7Layout"; value=[byte[]]@(
                        0x13,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x20,0x00,0x00,0x00,
                        0x10,0x00,0x01,0x00,0x00,0x00,0x00,0x00,0x01,0x00,0x00,0x00,0x01,0x07,0x00,0x00,
                        0x5e,0x01,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
                        0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
                        0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
                        0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
                        0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
                        0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
                        0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
                        0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
                        0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00
                    )}
                ), $false)

                Print "`n===== 重新啟動後應用 ====="

                $this.WaitBack()
            }
            12 { # Google 變更緩存位置

                # 創建 Shell.Application COM 物件
                $shellApp = New-Object -ComObject Shell.Application

                Print "這將會改變 Google 的緩存位置！"
                Print "`n===== 選擇要設置的路徑位置 ====="

                # 顯示選擇文件夾選擇器
                $folder = $shellApp.BrowseForFolder(0, "選擇設置路徑", 0, 0)

                if ($null -ne $folder) {
                    $folderPath = $folder.Self.Path

                    $this.RegistItem(@(
                        "HKLM:\Software\Policies\Google\Chrome", "DiskCacheDir", "String", "$($folderPath)GoogleCache"
                    ), $false)

                    Print "修改成功！緩存目錄已設置為： $($folderPath)GoogleCache" 'Green'
                } else {
                    Print "未選擇任何路徑，修改取消。" 'Red'
                }

                $this.WaitBack()
            }
            13 { # Google 一鍵優化設置

            }
            14 { # Google 重置受機構管理

            }
            15 { # Edge 變更緩存位置

                $shellApp = New-Object -ComObject Shell.Application

                Print "這將會改變 Edge 的緩存位置！"
                Print "`n===== 選擇要設置的路徑位置 ====="

                # 顯示選擇文件夾選擇器
                $folder = $shellApp.BrowseForFolder(0, "選擇設置路徑", 0, 0)

                if ($null -ne $folder) {
                    $folderPath = $folder.Self.Path

                    $this.RegistItem(@(
                        "HKLM:\Software\Policies\Microsoft\Edge", "DiskCacheDir", "String", "$($folderPath)EdgeCache"
                    ), $false)

                    Print "修改成功！緩存目錄已設置為： $($folderPath)EdgeCache" 'Green'
                } else {
                    Print "未選擇任何路徑，修改取消。" 'Red'
                }

                $this.WaitBack()
            }
            16 { # Edge 一鍵優化設置

            }
            17 { # Edge 重置受組織管理

            }
            18 { # RAR 授權
                Print "===== 獲取授權 =====`n"
                $RegistPath = "C:\Program Files\WinRAR\Rarreg.key"

                if (-not (Test-Path $RegistPath)) {
                    $DownloadURL = "https://raw.githubusercontent.com/Canaan-HS/Implementation-Project/Main/Command Prompt/Rar/Rarreg.key"
                    Invoke-WebRequest -Uri $DownloadURL -OutFile $RegistPath

                    if (Test-Path $RegistPath) {
                        Print "授權完成" 'Green'
                    } else {
                        Print "授權失敗" 'Red'
                    }

                } else {
                    Print "已擁有授權" 'Green'
                }

                $this.WaitBack()
            }
            19 { # IDM 授權
                # https://github.com/lstprjct/IDM-Activation-Script
                $this.Authorize(
                    "$([Main]::Temp)\$($this.MD5("IAS")).cmd",
                    "https://raw.githubusercontent.com/lstprjct/IDM-Activation-Script/main/IAS.cmd"
                )
            }
            20 { # Windows 啟用授權
                # https://github.com/massgravel/Microsoft-Activation-Scripts/tree/master/MAS/All-In-One-Version
                $this.Authorize(
                    "$([Main]::Temp)\$($this.MD5("MAS_AIO-CRC32_31F7FD1E")).cmd",
                    "https://raw.githubusercontent.com/massgravel/Microsoft-Activation-Scripts/master/MAS/All-In-One-Version/MAS_AIO-CRC32_31F7FD1E.cmd"
                )
            }
            21 { # Office 啟用授權 (他會導致回到菜單時歪掉)
                $this.Authorize(
                    "$([Main]::Temp)\$($this.MD5("KMS_VL_ALL_AIO")).cmd",
                    "https://raw.githubusercontent.com/abbodi1406/KMS_VL_ALL_AIO/master/KMS_VL_ALL_AIO.cmd"
                )
            }
            22 { # Google 結束進程
                $this.StopProcess("chrome")
                $this.Menu()
            }
            23 { # Edge 結束進程
                $this.StopProcess("msedge")
                $this.Menu()
            }
            24 { # Adobe 結束進程
                $this.StopProcess(
                    @("node", "CCLibrary", "AdobeIPCBroker", "OfficeClickToRun")
                )
                $this.Menu()
            }
            25 { # Surfshark 運行
                Print "===== Surfshark 啟動中 ====="
                $Path = "C:\Program Files (x86)\Surfshark\Surfshark.exe"

                if (Test-Path $Path) {
                    # 啟動服務
                    Start-Service -Name "Surfshark Service" -ErrorAction SilentlyContinue
                    Start-Process -FilePath $Path
                    $this.Menu()
                } else {
                    Print "找不到啟動程序: $Path" 'Red'
                    Print "下載連結: https://surfshark.com/zh-tw/download" 'Green'
                    $this.WaitBack()
                }
            }
            26 { # Surfshark 終止
                $this.StopProcess(
                    @("Surfshark", "Surfshark.Service")
                )
                # 關閉服務
                # Stop-Service -Name "Surfshark Service" -Force -ErrorAction SilentlyContinue
                Get-Service | Where-Object { $_.Name -eq "Surfshark Service" } | ForEach-Object { Stop-Service -Name $_.Name -Force }
                $this.Menu()
            }
            27 { # 網路重置
                Print "網路重置中..."
                # 釋放 IP 配置
                ipconfig /release
                # 清除 DNS 緩存
                Clear-DnsClientCache
                # 重置 IP 設定
                netsh int ip reset
                # 重置 TCP/IP 堆疊
                netsh int tcp reset
                # 重置 Winsock
                netsh winsock reset
                # 重置 Windows 防火牆
                netsh advfirewall reset
                # 更新 IP 配置
                ipconfig /renew
                $this.Menu()
            }
            28 { # 自動配置 DNS
                $pingResults = @{} # 存儲每個 DNS 伺服器的平均延遲

                $dnsServers = ( # 要測試的 DNS 伺服器列表
                    @{name="Cloudflare DNS"; dns="1.1.1.1"},
                    @{name="Cloudflare DNS"; dns="1.0.0.1"},
                    @{name="Google DNS"; dns="8.8.8.8"},
                    @{name="Google DNS"; dns="8.8.4.4"},
                    @{name="Comodo Secure DNS"; dns="8.26.56.26"},
                    @{name="Comodo Secure DNS"; dns="8.20.247.20"},
                    @{name="IBM DNS"; dns="9.9.9.9"},
                    @{name="IBM DNS"; dns="9.9.9.10"},
                    @{name="德國 DNS Watch"; dns="84.200.69.80"},
                    @{name="德國 DNS Watch"; dns="84.200.70.40"},
                    @{name="AdGuard DNS"; dns="94.140.14.14"},
                    @{name="AdGuard DNS"; dns="94.140.15.15"},
                    @{name="臺灣網路資訊中心 DNS"; dns="101.101.101.101"},
                    @{name="臺灣網路資訊中心 DNS"; dns="101.102.103.104"},
                    @{name="種花電信"; dns="168.95.1.1"},
                    @{name="種花電信"; dns="168.95.192.1"},
                    @{name="CleanBrowsing 安全過濾 DNS"; dns="185.228.168.9"},
                    @{name="CleanBrowsing 安全過濾 DNS"; dns="185.228.169.9"},
                    @{name="Open DNS"; dns="208.67.222.222"},
                    @{name="Open DNS"; dns="208.67.220.220"},
                    @{name="Level3 DNS"; dns="209.244.0.3"},
                    @{name="Level3 DNS"; dns="209.244.0.4"},
                    @{name="Ali DNS"; dns="223.5.5.5"},
                    @{name="Ali DNS"; dns="223.6.6.6"}
                )

                Print " =========================================== "
                Print "自動開始配置時 建議不要有消耗網路流量的操作" "Cyan"
                Print "根據環境不同 可能出現延遲顯示都是 0 這是正常的" "Cyan"
                Print " =========================================== "

                $y = Input "輸入 y 確認操作" 'Yellow'
                switch ($y) {
                    "y" {
                        Print "`n這個操作需要一些時間 請稍後...`n"
                        Start-Sleep -Seconds 1
                    }
                    Default {
                        Print "`n確認失敗 返回首頁..." 'Red'
                        Start-Sleep -Seconds 1.3
                        $this.Menu()
                    }
                }

                Print "===== 開始測試延遲 ======`n"
                $dnsServers | ForEach-Object {
                    $totalTime = 0
                    $successCount = 0

                    for ($i = 0; $i -lt 15; $i++) { # ping dns 伺服器 15 次
                        $pingResult = Test-Connection -ComputerName $_.dns -Count 1 -ErrorAction SilentlyContinue
                        if ($pingResult) {
                            $successCount++
                            $totalTime += $pingResult.ResponseTime
                            Start-Sleep -Milliseconds 100 # 延遲 100 毫秒
                        }
                    }

                    if ($successCount -gt 0) {
                        $averageTime = $totalTime / $successCount
                        $pingResults[@($_.name, $_.dns)] = $averageTime
                        Print "$($_.name) | $($_.dns) | $averageTime ms" "Yellow"
                    }
                }

                # 按平均延遲排序，選出最短的兩個 DNS 伺服器
                $sortedResults = $pingResults.GetEnumerator() | Sort-Object Value

                # 取出慣用和其他的結果
                $idiomaticResults = $sortedResults[0].Key
                $otherResults = $sortedResults[1].Key

                # 獲取 dns 項
                $idiomaticDNS = $idiomaticResults[1]
                $otherDNS = $otherResults[1]

                Clear-DnsClientCache # 清除 DNS 緩存
                $interfaceIndex = (Get-NetAdapter | Where-Object { $_.Status -eq "Up" }).ifIndex
                Set-DnsClientServerAddress -InterfaceIndex $interfaceIndex -ServerAddresses ($idiomaticDNS, $otherDNS)

                Print "`n===== 完成配置 ======`n"

                Print "慣用配置: $($idiomaticResults[0]) | $idiomaticDNS" "Green"
                Print "其他配置: $($otherResults[0]) | $otherDNS" "Green"

                $this.WaitBack()
            }
            Default {
                Print "無效的代號" 'Red'
                Start-Sleep -Seconds 1.3
                $this.Menu()
            }
        }
    }
}

<# ------------------------------ #>

[Main]::new().Menu() # 首次調用菜單
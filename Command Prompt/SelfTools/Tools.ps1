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

class Main {
    static [int]$InitIndex = 0
    static [string]$Temp = $env:Temp

    # 等待返回菜單
    [void]WaitBack() {
        Read-Host "`n[37m[7m[1mEnter返回選單[27m"
        $this.Menu()
    }

    # 運行 CMD 指令並打印出來, 命令, 是否確認後返回首頁
    [void]CMD([string]$command, [bool]$back) {
        Start-Process cmd.exe -ArgumentList "/c $command" -NoNewWindow -Wait
        if ($back) {
            $this.WaitBack()
        }
    }

    # 註冊 (不應該直接調用)
    [void]__Regist([string]$path, [string]$name, [string]$type, [object]$value, [bool]$del) {
        if (-not (Test-Path $path)) {
            New-Item -Path $path -Force # 路徑添加
        }
        try { # 檢查註冊表值是否存在
            if (-not($del)) {
                throw [System.Exception]::new()
            }

            Get-ItemProperty -Path $path -Name $name -ErrorAction Stop
            Remove-ItemProperty -Path $path -Name $name -Force # 存在就刪除
            Print "已刪除值: $name" 'Red'
        } catch {
            New-ItemProperty -Path $path -Name $name -PropertyType $type -Value $value -Force # 不存在就添加
            Print "已註冊值: $name" 'Green'
        }
    }
    <#
        註冊表操作 (非 reg add)

        參數 1 設置註冊表
        參數 2 設置是否刪除

        $this.RegistItem(@(
            @(path, name, type, value),
            @(path, name, type, value)
        ), true)
    #>
    [void]RegistItem([array]$Items, [bool]$Delete) {
        if ($Items.Length -gt 0 -and $Items[0] -is [array]) { # 二維數組註冊
            $Items | ForEach-Object {
                $this.__Regist($_[0], $_[1], $_[2], $_[3], $Delete)
            }
        } else { # 一維數組註冊
            $this.__Regist($Items[0], $Items[1], $Items[2], $Items[3], $Delete)
        }
    }

    [void]Menu() {
        # 獲取防火牆狀態並提取狀態
        $firewallStatus = netsh advfirewall show allprofiles state | Select-String "State" | 
        ForEach-Object { $_.ToString().Trim() -replace 'State\s+', '' } | 
        Select-Object -First 1

        # 根據防火牆狀態設置 display 變量
        $display = if ($firewallStatus -eq "ON") {
            "防火牆已 [[32m啟用[37m]"
        } else {
            "防火牆已 [[31m禁用[37m]"
        }

        [Main]::InitIndex = 0 # 每次調用會重設
        $index = { # 根據調用次數累加索引值
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

        # 打印菜单内容
        $P_ = "" # 換行用, 方便自己觀看 (不會打印出來)
        Print "========================================================================================================================" 'Red'
        Print "                                         - 工具箱v2 Versions 0.0.1 2024/1/1 -" 'Magenta'
        Print "========================================================================================================================" 'White'
        $P_
        Print "   Windows 系統開關機 :" 'Cyan'
        $P_
        Print "   $(& $index) 睡眠    $(& $index) 重啟    $(& $index) 關機`n" 'White'
        $P_
        Print "   Windows 防火牆開關 :" 'Cyan'
        $P_
        Print "   $(& $index) 開啟防火牆    $(& $index) 關閉防火牆    $display`n" 'White'
        $P_
        Print "   Windows 優化相關 :" 'Cyan'
        $P_
        Print "   $(& $index) .NET安裝    $(& $index) Visual C++ (x64)安裝    $(& $index) 關閉UAC安全通知" 'White'
        $P_
        Print "   $(& $index) Windows 一鍵優化    $(& $index) Windows 恢復不適用優化    $(& $index) Win11 檔案總管優化 (再次運行恢復)`n" 'White'
        $P_
        Print "   瀏覽器設置 :" 'Cyan'
        $P_
        Print "   $(& $index) Google 變更緩存位置    $(& $index) Google 一鍵優化設置    $(& $index) Google 重置受機構管理" 'White'
        $P_
        Print "   $(& $index) Edge 變更緩存位置    $(& $index) Edge 一鍵優化設置    $(& $index) Edge 重置受組織管理`n" 'White'
        $P_
        Print "   授權啟用 :" 'Cyan'
        $P_
        Print "   $(& $index) RAR 授權     $(& $index) IDM 授權    $(& $index) Windows 啟用授權    $(& $index) Office 啟用授權`n" 'White'
        $P_
        Print "   進程操作 :" 'Cyan'
        $P_
        Print "   $(& $index) Google 結束進程    $(& $index) Edge 結束進程    $(& $index) Adobe 結束進程      $(& $index) AnLink 結束進程`n" 'White'
        $P_
        Print "   服務操作 :" 'Cyan'
        $P_
        Print "   $(& $index) 開啟服務 (Surfshark運行)    $(& $index) 關閉服務 (Surfshark終止)`n" 'White'
        $P_
        Print "   特殊功能 :" 'Cyan'
        $P_
        Print "   $(& $index) 網路重置" 'White'
        Print "------------------------------------------------------------------------------------------------------------------------" 'Red'
        Print "                                          - 系統指令操作 (不分大小寫) -" 'Magenta'
        Print "------------------------------------------------------------------------------------------------------------------------" 'Red'
        Print "   $(& $index 'CT') 系統控制台    $(& $index 'GP') 本機群組原則    $(& $index 'RD') 登入編輯程式    $(& $index 'UG') 使用者群組    $(& $index 'DX') DX診斷工具    $(& $index 'MF') 系統開機設置" 'White'
        $P_
        Print "   $(& $index 'WS') 電腦啟用狀態    $(& $index 'SI') 查看系統資訊    $(& $index 'MSI') 查看完整系統資訊    $(& $index 'NV') 查看顯卡驅動版本    $(& $index 'HW') 查看電腦機器碼" 'White'
        $P_
        Print "   $(& $index 'IP') 查看電腦IP位置    $(& $index 'RS') 查看遠端分享    $(& $index 'MC') MAC地址查詢    $(& $index 'SV') 查看運行中的服務    $(& $index 'MRT') 惡意軟體移除工具" 'White'
        $P_
        Print "   $(& $index 'WF') 顯示已連接過的wifi    $(& $index 'DV') 修復驅動安裝問題    $(& $index 'SR') 系統錯誤修復" 'White'
        Print "========================================================================================================================" 'White'
        Print "                                   $(& $index 'H') 工具說明     $(& $index '0') 離開程式     $(& $index 'V') 更新資訊" 'White'
        Print "========================================================================================================================`n" 'Red'

        $this.Choice()
    }

    [void]Choice() {
        $choice = Read-Host "[37m[7m[1m輸入功能 [代號][27m"
        Clear-Host

        switch ($choice) {
            0 {exit} # 離開
            "V" { # 更新資訊
                Print "------------------------------------"
                Print ""
                Print "  Versions 0.0.1 更新:"
                Print ""
                Print "   1. 首次發佈"
                Print ""
                Print "------------------------------------"
                pause
                $this.Menu()
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
                pause
                $this.Menu()
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
                Print "準備修復 請稍後...`n"

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
                Print "啟用中...`n"
                netsh advfirewall set allprofiles state on
                netsh advfirewall firewall set rule all new enable=yes
                $this.Menu()
            }
            5 { # 關閉防火牆
                Print "禁用中...`n"
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
                Invoke-WebRequest -Uri $DownloadURL -OutFile $DownloadPath -Resume -HttpVersion 3.0 -SkipCertificateCheck -SkipHeaderValidation
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
                $this.RegistItem(@(
                    # 恢復 win 10 菜單
                    @("HKCU:\Software\Classes\Local Settings\Software\Microsoft\Windows\Shell\Bags\AllFolders\Shell", "FolderType", "String", "NotSpecified"),
                    # 避免大量運算 檔案類型
                    @("HKLM:\Software\Microsoft\Windows\CurrentVersion\Shell Extensions\Blocked", "{e2bf9676-5f8f-435c-97eb-11607a5bedf7}", "String", "")
                ), $true)
                $this.WaitBack()
            }
            12 {}
            13 {}
            14 {}
            15 {}
            16 {}
            17 {}
            18 {}
            19 {}
            20 {}
            21 {}
            22 {}
            23 {}
            24 {}
            25 {}
            26 {}
            27 {}
            28 {}
            29 {}
            Default {
                Print "無效的代號"
                Start-Sleep -Seconds 1.5
                $this.Menu()
            }
        }
    }
}

<# ------------------------------ #>

$MainInstance = [Main]::new()
$MainInstance.Menu() # 首次調用菜單
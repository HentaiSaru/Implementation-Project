[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
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

# 檢查管理員權限
function IsAdmin {
    return ([bool](New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
    ).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator))
}

# 檢查網路連線
function CheckNetwork {
    try {
        Test-Connection -ComputerName "8.8.8.8" -Count 1 -ErrorAction Stop
        return $true
    } catch {
        return $false
    }
}

# 打印文本
function Print {
    param (
        [string]$text,
        [string]$foregroundColor = 'White',
        [string]$backgroundColor = 'Black'
    )

    # 設置颜色
    $Host.UI.RawUI.ForegroundColor = [ConsoleColor]::$foregroundColor
    $Host.UI.RawUI.BackgroundColor = [ConsoleColor]::$backgroundColor
    
    # 打印粗體
    Write-Host "[1m$text"
}

# 輸入文本
function Input {
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

# 啟動器由 Invoke-Expression 調用該代碼, 運行時會有清除不乾淨的問題, 等待後續研究
function _Cls {
    Clear-Host
}

class Main {
    static [int]$InitIndex = 0 # 菜單的索引計數
    static [string]$Temp = $env:Temp # 配置路徑

    # 等待返回菜單
    [void]WaitBack() {
        Input "Enter 返回選單"
        $this.Menu()
    }

    # 檢查網路狀態
    [void]NetworkState() {
        if (-not(CheckNetwork)) {
            Print "操作失敗: 沒有網路無法運行" 'Red'
            $this.WaitBack()
        }
    }

    # 獲取遠端授權代碼
    [void]Authorize([string]$Name, [string]$DL_URL) {
        Print "===== 獲取最新版本 授權程式 =====`n"
        $this.NetworkState()

        $DL_Path = "$([Main]::Temp)\$($this.MD5($Name)).cmd" # 獲取文件保存路徑
        if (Test-Path $DL_Path) { Remove-Item $DL_Path -Force } # 先刪除舊文件
        Invoke-WebRequest -Uri $DL_URL -OutFile $DL_Path
        if (-not (Test-Path $DL_Path)) {
            Print "獲取失敗" 'Red'
            $this.WaitBack()
        }
        $this.CMD($DL_Path, $true)
    }

    # 二次確認操作
    [void]DoubleConfirm([scriptblock]$confirm) {
        $y = Input "輸入 Y 確認操作" 'Yellow'
        switch ($y) {
            "y" {
                & $confirm
            }
            Default {
                Print "`n確認失敗 返回首頁..." 'Red'
                Start-Sleep -Seconds 1.3
                $this.Menu()
            }
        }
    }

    # 用於合成指令 (沒有管理權限時)
    [string]Composite([object]$obj) {
        $merge = ""
        for ($i = 0; $i -lt $obj.Length; $i++) {
            $merge += $obj[$i]
            if ($i -lt ($obj.Length - 1)) {$merge += " & "}
        }
        return $merge
    }

    # 運行 CMD 指令並打印出來, 命令, 是否確認後返回首頁
    [void]CMD([string]$command, [bool]$back) {
        if (IsAdmin) {
            Start-Process cmd.exe -ArgumentList "/c $command" -NoNewWindow -Wait
        } else {
            Start-Process cmd.exe -ArgumentList "/c $command" -Verb RunAs -Wait
        }

        if ($back) { $this.WaitBack() }
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

    # 關閉進程 (傳入要關閉的進程名稱)
    [void]StopProcess([object]$Process) {
        if ($Process -is [string]) { # 傳入的是字串
            Stop-Process -Name $Process -Force -ErrorAction SilentlyContinue
        } elseif ($Process -is [array] -and $Process[0] -is [string]) { # 傳入的是一維列表
            $Process | ForEach-Object {
                Stop-Process -Name $_ -Force -ErrorAction SilentlyContinue
            }
        }
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
                Remove-Item -Path $Path -Recurse -Force # 他刪除的是整個資料夾
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
                Remove-ItemProperty -Path $Path -Name $Name -ErrorAction Stop # 他刪除的是單個項目
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

        _Cls
        # 打印菜单内容
        $P_ = "縮排 方便自己觀看 (不會顯示)"
        Print "========================================================================================================================" 'Red'
        Print "                                                     - 工具箱 v2 -" 'Magenta'
        Print "========================================================================================================================" 'White'
        $P_
        Print "   Windows 系統開關機 :" 'Cyan'
        $P_
        Print "   $(Index) 睡眠    $(Index) 重啟    $(Index) 關機`n" 'White'
        $P_
        Print "   Windows 防火牆 :" 'Cyan'
        $P_
        Print "   $(Index) 開啟防火牆    $(Index) 關閉防火牆    [33m當前狀態:[37m $display`n" 'White'
        $P_
        Print "   Windows 設置 :" 'Cyan'
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
        Print "   授權操作 :" 'Cyan'
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
        Print "   網路操作 :" 'Cyan'
        $P_
        Print "   $(Index) 網路重置    $(Index) 網路優化    $(Index) 自動配置 DNS    $(Index) 取得網域 IP" 'White'
        Print "------------------------------------------------------------------------------------------------------------------------" 'Red'
        Print "                                              - 系統指令操作 (不分大小寫) -" 'Magenta'
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

        [Main]::InitIndex = 0 # 每次調用會重設
        function index {return [int](++[Main]::InitIndex)}

        _Cls
        switch ($choice) {
            0 {exit} # 離開
            "V" { # 更新資訊
                Print "----------------------------"
                Print ""
                Print "  更新資訊:"
                Print ""
                Print "   1. 授權檔案更新"
                Print "----------------------------"
                $this.WaitBack()
            }
            "H" { # 使用說明
                Print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
                Print ""
                Print " - 程式資訊 -"
                Print ""
                Print " 作者: Canaan HS"
                Print " 程式名: ToolBox V2"
                Print " 程式描述: 集成個人常用功能的程式"
                Print ""
                Print " - 使用問題 -"
                Print ""
                Print " 1. 操作的程式 , 必須安裝在預設的路徑上 , 才可成功運行"
                Print " 2. 優化之類的設置 , 是以個人環境製作的 , 不一定適用於所有人"
                Print " 3. 為了避免多餘操作 , 啟動器運行方式會導致 , 有時返回菜單時 上方會有殘留操作訊息 (不要看就好)"
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
                if (-not(IsAdmin)) {
                    Print "該功能需要管理員權限" 'Red'
                    $this.WaitBack()
                }

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
                # Get-NetAdapter
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

                if (IsAdmin) {
                    $this.CMD("DISM /Online /Cleanup-Image /ScanHealth", $false)
                    $this.CMD("DISM /Online /Cleanup-Image /CheckHealth", $false)
                    $this.CMD("DISM /Online /Cleanup-image /RestoreHealth", $false)
                    $this.CMD("sfc /scannow", $true)
                } else {
                    $this.CMD($this.Composite(@(
                        "DISM /Online /Cleanup-Image /ScanHealth"
                        "DISM /Online /Cleanup-Image /CheckHealth"
                        "DISM /Online /Cleanup-image /RestoreHealth"
                        "sfc /scannow"
                        "pause"
                    )), $true)
                }
            }
            (index) { # 睡眠
                rundll32.exe powrprof.dll,SetSuspendState 0,1,0
            }
            (index) { # 重啟
                Restart-Computer -Force
            }
            (index) { # 關機
                Stop-Computer -Force
            }
            (index) { # 開啟防火牆
                Print "啟用中 =>`n" 'Green'
                netsh advfirewall set allprofiles state on
                netsh advfirewall firewall set rule all new enable=yes
                $this.Menu()
            }
            (index) { # 關閉防火牆
                Print "禁用中 =>`n" 'Red'
                netsh advfirewall set allprofiles state off
                netsh advfirewall firewall set rule all new enable=no
                $this.Menu()
            }
            (index) { # .NET安裝
                # winget search Microsoft.DotNet.SDK
                $this.NetworkState()
                if (IsAdmin) {
                    $this.CMD("winget install Microsoft.DotNet.SDK.6", $false)
                    $this.CMD("winget install Microsoft.DotNet.SDK.7", $false)
                    $this.CMD("winget install Microsoft.DotNet.SDK.8", $true)
                } else {
                    $this.CMD($this.Composite(@(
                        "winget install Microsoft.DotNet.SDK.6"
                        "winget install Microsoft.DotNet.SDK.7"
                        "winget install Microsoft.DotNet.SDK.8"
                    )), $true)
                }
            }
            (index) { # Visual C++ (x64)安裝
                # https://learn.microsoft.com/zh-tw/cpp/windows/latest-supported-vc-redist?view=msvc-170
                # https://www.techpowerup.com/download/visual-c-redistributable-runtime-package-all-in-one/
                $this.NetworkState()

                $DownloadPath = "$([Main]::Temp)\Visual.tar"
                $DownloadURL = "https://raw.githubusercontent.com/Canaan-HS/Implementation-Project/Main/Command Prompt/Visual C++/Visual.tar"

                $InstallPackage = @( # 安裝包 與 安裝指令
                    @{ package = "vcredist2005_x64.exe"; Order = "/q" }
                    @{ package = "vcredist2008_x64.exe"; Order = "/qb" }
                    @{ package = "vcredist2010_x64.exe"; Order = "/passive /norestart" }
                    @{ package = "vcredist2012_x64.exe"; Order = "/passive /norestart" }
                    @{ package = "vcredist2013_x64.exe"; Order = "/passive /norestart" }
                    @{ package = "vcredist2015_2017_2019_2022_x64.exe"; Order = "/passive /norestart" }
                )

                # 有重複的先進行刪除
                if (Test-Path $DownloadPath) { Remove-Item $DownloadPath -Force }

                Print "檔案較大請稍後 - 安裝包日期 : 2024 年 10 月"
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
            (index) { # 關閉UAC安全通知
                $this.RegistItem(@(
                    "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System", "EnableLUA", "DWORD", 0
                ), $false)
                Print "`n電腦重啟後生效"
                $this.WaitBack()
            }
            (index) { # Windows 一鍵優化
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
            (index) { # Windows 恢復不適用優化
                $this.RegistItem(@(
                    "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects", "VisualFXSetting", "DWORD", 0
                ), $false)
                $this.WaitBack()
            }
            (index) { # Win11 檔案總管優化
                $pathA = "HKCU:\Software\Classes\CLSID\{2aa9162e-c906-4dd9-ad0b-3d24a8eef5a0}"
                $pathB = "HKCU:\Software\Classes\CLSID\{6480100b-5a83-4d1e-9f69-8ae5a88e9a33}"
                $dll = "C:\Windows\System32\Windows.UI.FileExplorer.dll_"

                $this.RegistItem(@(
                    # 以下為將檔案總管變回 win 10 的方式
                    @{path=$pathA; name="(default)"; value="CLSID_ItemsViewAdapter"}
                    @{path="$pathA\InProcServer32"; name="(default)"; value=$dll; parent=$pathA}
                    @{path="$pathA\InProcServer32"; name="ThreadingModel"; type="String"; value="Apartment"; parent=$pathA}

                    @{path=$pathB; name="(default)"; value="File Explorer Xaml Island View Adapter"}
                    @{path="$pathB\InProcServer32"; name="(default)"; value=$dll; parent=$pathB}
                    @{path="$pathB\InProcServer32"; name="ThreadingModel"; type="String"; value="Apartment"; parent=$pathB}

                    # 以下為 避免大量運算 檔案類型
                    @{path="HKCU:\Software\Classes\Local Settings\Software\Microsoft\Windows\Shell\Bags\AllFolders\Shell"; name="FolderType"; type="String"; value="NotSpecified"; parent=$pathA}
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
            (index) { # Google 變更緩存位置
                # 創建 Shell.Application COM 物件
                $shellApp = New-Object -ComObject Shell.Application

                Print "這將會改變 Google 的緩存位置！"
                Print "`n===== 選擇要設置的路徑位置 ====="

                # 顯示選擇文件夾選擇器
                $folder = $shellApp.BrowseForFolder(0, "選擇設置路徑", 0, 0)

                if ($null -ne $folder) {
                    $folderPath = $folder.Self.Path

                    $this.RegistItem(@(
                        "HKLM:\SOFTWARE\Policies\Google\Chrome", "DiskCacheDir", "String", "$($folderPath)GoogleCache"
                    ), $false)

                    Print "修改成功！緩存目錄已設置為： $($folderPath)GoogleCache" 'Green'
                } else {
                    Print "未選擇任何路徑，修改取消。" 'Red'
                }

                $this.WaitBack()
            }
            (index) { # Google 一鍵優化設置
                # 原則說明文件
                # https://admx.help/?Category=Chrome&Language=zh-tw
                $this.RegistItem(@(
                    # 緩存大小
                    @("HKLM:\SOFTWARE\Policies\Google\Chrome", "DiskCacheSize", "String", "2000000000")

                    # 安全瀏覽功能防護等級 0 關閉 1 預設 2強化防護
                    @("HKLM:\SOFTWARE\Policies\Google\Chrome", "SafeBrowsingProtectionLevel", "DWORD", 2)
                    # 下載檔案安全限制 0 ~ 4 , 0 無特別限制
                    @("HKLM:\SOFTWARE\Policies\Google\Chrome", "DownloadRestrictions", "DWORD", 0)
                    # 為已輸入的憑證啟用資料外洩偵測功能
                    @("HKLM:\SOFTWARE\Policies\Google\Chrome", "PasswordLeakDetectionEnabled", "DWORD", 1)
                    # 密碼在網路詐騙網頁上遭到重複使用時，會觸發密碼保護警告
                    @("HKLM:\SOFTWARE\Policies\Google\Chrome", "PasswordProtectionWarningTrigger", "DWORD", 2)
                    # 啟用預設搜尋引擎
                    @("HKLM:\SOFTWARE\Policies\Google\Chrome", "DefaultSearchProviderEnabled", "DWORD", 1)
                    # 使用 POST 傳遞搜尋參數
                    @("HKLM:\SOFTWARE\Policies\Google\Chrome", "DefaultSearchProviderSearchURLPostParams", "String", "q={searchTerms}&client=chrome&sourceid=chrome&ie=UTF-8")
                    @("HKLM:\SOFTWARE\Policies\Google\Chrome", "DefaultSearchProviderSuggestURLPostParams", "String", "q={searchTerms}&client=chrome&sourceid=chrome&ie=UTF-8&oe=UTF-8")

                    # 將這項政策設為 Disabled，則表示除非使用者停用 PDF 外掛程式，否則系統一律會使用 PDF 外掛程式開啟 PDF 檔案
                    @("HKLM:\SOFTWARE\Policies\Google\Chrome", "AlwaysOpenPdfExternally", "DWORD", 1)
                    # 信用卡的自動填入功能
                    @("HKLM:\SOFTWARE\Policies\Google\Chrome", "AutofillCreditCardEnabled", "DWORD", 1)
                    # 地址的自動填入功能
                    @("HKLM:\SOFTWARE\Policies\Google\Chrome", "AutofillAddressEnabled", "DWORD", 1)
                    # 啟用搜尋建議
                    @("HKLM:\SOFTWARE\Policies\Google\Chrome", "SearchSuggestEnabled", "DWORD", 1)
                    # 顯示完整網址
                    @("HKLM:\SOFTWARE\Policies\Google\Chrome", "ShowFullUrlsInAddressBar", "DWORD", 1)

                    # 啟用剪貼簿共用功能
                    @("HKLM:\SOFTWARE\Policies\Google\Chrome", "SharedClipboardEnabled", "DWORD", 1)
                    # 拼字檢查網路服務
                    @("HKLM:\SOFTWARE\Policies\Google\Chrome", "SpellCheckServiceEnabled", "DWORD", 0)
                    # 0 無論使用任何網路連線，皆預測網路動作
                    @("HKLM:\SOFTWARE\Policies\Google\Chrome", "NetworkPredictionOptions", "DWORD", 0)
                    # 關閉 Google Chrome 關閉時繼續執行背景應用程式
                    @("HKLM:\SOFTWARE\Policies\Google\Chrome", "BackgroundModeEnabled", "DWORD", 0)

                    # 第一次執行時從預設瀏覽器匯入已儲存的密碼
                    @("HKLM:\SOFTWARE\Policies\Google\Chrome", "ImportSavedPasswords", "DWORD", 1)
                    # 第一次執行時從預設瀏覽器匯入搜尋引擎
                    @("HKLM:\SOFTWARE\Policies\Google\Chrome", "ImportSearchEngine", "DWORD", 1)
                    # 第一次執行時從預設瀏覽器匯入搜尋書籤
                    @("HKLM:\SOFTWARE\Policies\Google\Chrome", "ImportBookmarks", "DWORD", 1)
                    # 第一次執行時從預設瀏覽器匯入瀏覽記錄
                    @("HKLM:\SOFTWARE\Policies\Google\Chrome", "ImportHistory", "DWORD", 1)
                    # 第一次執行時從預設瀏覽器匯入自動填入表單資料
                    @("HKLM:\SOFTWARE\Policies\Google\Chrome", "ImportAutofillFormData", "DWORD", 1)

                    # Quic通訊
                    @("HKLM:\SOFTWARE\Policies\Google\Chrome", "QuicAllowed", "DWORD", 1)
                    # 登入攔截功能
                    @("HKLM:\SOFTWARE\Policies\Google\Chrome", "SigninInterceptionEnabled", "DWORD", 0)
                    # 允許音訊程式在 Windows 系統上以高於一般優先順序的次序執行
                    @("HKLM:\SOFTWARE\Policies\Google\Chrome", "AudioProcessHighPriorityEnabled", "DWORD", 1)
                    # 禁止顯示侵入式廣告
                    @("HKLM:\SOFTWARE\Policies\Google\Chrome", "AdsSettingForIntrusiveAdsSites", "DWORD", 2)
                    # 輸入網址匿名資料收集功能
                    @("HKLM:\SOFTWARE\Policies\Google\Chrome", "UrlKeyedAnonymizedDataCollectionEnabled", "DWORD", 0)
                    # 啟用視窗遮蔽功能
                    @("HKLM:\SOFTWARE\Policies\Google\Chrome", "WindowOcclusionEnabled", "DWORD", 1)
                    # YouTube 嚴格篩選模式
                    @("HKLM:\SOFTWARE\Policies\Google\Chrome", "ForceYouTubeRestrict", "DWORD", 0)
                    # 允許使用無頭
                    @("HKLM:\SOFTWARE\Policies\Google\Chrome", "HeadlessMode", "DWORD", 1)
                    # 加入進階保護計畫的使用者啟用額外防護功能
                    @("HKLM:\SOFTWARE\Policies\Google\Chrome", "AdvancedProtectionAllowed", , 1)
                ), $true)

                Print "`n===== 重新啟動後應用 ====="
                $this.WaitBack()
            }
            (index) { # Google 重置受機構管理
                Print " ============================================== "
                Print "          無特別需求不建議使用該功能" 'Red'
                Print "        該功能會重置先前所有優化註冊項目" 'Red'
                Print "  如只想重置 (一鍵優化設置) 可再次運行 (一鍵優化設置)`n" 'Red'
                Print "     重置包含: (變更緩存位置) (一鍵優化設置)"
                Print "     重置不包含: 瀏覽器設定, 與任何保存數據"
                Print " ============================================== "

                $this.DoubleConfirm({
                    Remove-Item -Path "HKLM:\SOFTWARE\Policies\Google" -Recurse -Force
                    Print "已重置 Google 受機構管理" 'Green'
                    $this.WaitBack()
                })
            }
            (index) { # Edge 變更緩存位置
                $shellApp = New-Object -ComObject Shell.Application

                Print "這將會改變 Edge 的緩存位置！"
                Print "`n===== 選擇要設置的路徑位置 ====="

                # 顯示選擇文件夾選擇器
                $folder = $shellApp.BrowseForFolder(0, "選擇設置路徑", 0, 0)

                if ($null -ne $folder) {
                    $folderPath = $folder.Self.Path

                    $this.RegistItem(@(
                        "HKLM:\SOFTWARE\Policies\Microsoft\Edge", "DiskCacheDir", "String", "$($folderPath)EdgeCache"
                    ), $false)

                    Print "修改成功！緩存目錄已設置為： $($folderPath)EdgeCache" 'Green'
                } else {
                    Print "未選擇任何路徑，修改取消。" 'Red'
                }

                $this.WaitBack()
            }
            (index) { # Edge 一鍵優化設置
                # 原則說明文件
                # https://admx.help/?Category=EdgeChromium&Language=zh-tw
                # 功能查詢
                # https://learn.microsoft.com/zh-tw/DeployEdge/microsoft-edge-policies
                $this.RegistItem(@(
                    # 設置快取大小
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "DiskCacheSize", "String", "2000000000")
                    # 可讓螢幕助讀程式使用者取得網頁上未標記影像的描述
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "AccessibilityImageLabelsEnabled", "DWORD", 1)
                    # 搜尋不到時 , 提供類似頁面
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "AlternateErrorPagesEnabled", "DWORD", 1)
                    # 可讓啟用應用程式防護的 Microsoft Edge 電腦/裝置將我的最愛從主機同步處理到容器
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "ApplicationGuardFavoritesSyncEnabled", "DWORD", 1)
                    # 啟用此原則，使用者將無法在應用程式防護中上傳檔案
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "ApplicationGuardUploadBlockingEnabled", "DWORD", 0)
                    # 允許音訊處理程式在 Windows 上以高於正常優先順序執行
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "AudioProcessHighPriorityEnabled", "DWORD", 1)
                    # 允許匯入表單資訊
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "ImportAutofillFormData", "DWORD", 1)
                    # 允許匯入瀏覽器設定
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "ImportBrowserSettings", "DWORD", 1)
                    # 允許匯入 Cookie
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "ImportCookies", "DWORD", 1)
                    # 允許匯入擴充功能
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "ImportExtensions", "DWORD", 1)
                    # 允許匯入 [我的最愛]
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "ImportFavorites", "DWORD", 1)
                    # 允許匯入歷史紀錄
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "ImportHistory", "DWORD", 1)
                    # 允許匯入首頁設定
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "ImportHomepage", "DWORD", 1)
                    # 允許匯入已開啟的索引標籤
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "ImportOpenTabs", "DWORD", 1)
                    # 允許匯入付款資訊
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "ImportPaymentInfo", "DWORD", 1)
                    # 允許匯入已儲存的密碼
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "ImportSavedPasswords", "DWORD", 1)
                    # 允許匯入搜尋引擎設定
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "ImportSearchEngine", "DWORD", 1)
                    # 允許匯入捷徑
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "ImportShortcuts", "DWORD", 1)
                    # 允許匯入設置
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "ImportStartupPageSettings", "DWORD", 1)
                    # 允許執行音訊沙箱
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "AudioSandboxEnabled", "DWORD", 1)
                    # 如果您啟用此原則，使用者就可以看到 edge://compat 頁面上的 Enterprise Mode Site List Manager 的瀏覽按鈕，以瀏覽到該工具並加以使用。
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "EnterpriseModeSiteListManagerAllowed", "DWORD", 0)
                    # 可用時便使用硬體加速
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "HardwareAccelerationModeEnabled", "DWORD", 1)
                    #  封鎖含有干擾廣告的網站上的廣告
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "AdsSettingForIntrusiveAdsSites", "DWORD", 2)
                    # 自動完成地址資訊
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "AutofillAddressEnabled", "DWORD", 1)
                    # 自動完成信用卡資訊
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "AutofillCreditCardEnabled", "DWORD", 1)
                    # 首次執行時，自動匯入其他瀏覽器的資料和設定 (0) = 從預設的瀏覽器自動匯入 , (1) = 從 Internet Explorer 自動匯入 , (2) = 從 Google Chrome 自動匯入 , (3) = 從 Safari 自動匯入 , (4) = 已停用自動匯入 , (5) = 從 Mozilla Firefox 自動匯入
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "AutoImportAtFirstRun", "DWORD", 2)
                    # 關閉後繼續執行背景應用程式
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "BackgroundModeEnabled", "DWORD", 0)
                    # 封鎖 Bing 搜尋結果中的所有廣告
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "BingAdsSuppression", "DWORD", 1)
                    # 使用內建 DNS 用戶端
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "BuiltInDnsClientEnabled", "DWORD", 1)
                    # 封鎖使用者的網頁瀏覽活動追蹤 (0) = 關閉 , (1) = 基本 , (2) = 平衡 , (3) = 嚴格
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "TrackingPrevention", "DWORD", 3)
                    # 傳送不要追蹤
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "ConfigureDoNotTrack", "DWORD", 1)
                    # 防止 Microsoft 收集使用者的 Microsoft Edge 瀏覽歷程記錄
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "PersonalizationReportingEnabled", "DWORD", 0)
                    # (1) = 允許網站追蹤使用者的實體位置 , (2) = 不允許任何網站追蹤使用者的實體位置 , (3) = 每當網站想要追蹤使用者的實體位置時詢問
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "DefaultGeolocationSetting", "DWORD", 2)
                    # 關閉家長監護
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "FamilySafetySettingsEnabled", "DWORD", 0)
                    # 設置是否可以利用「線上文字轉語音」語音字型
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "ConfigureOnlineTextToSpeech", "DWORD", 1)
                    # 移轉時刪除舊版瀏覽器資料
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "DeleteDataOnMigration", "DWORD", 1)
                    # 設定 Microsoft Edge 是否可以自動增強影像
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "EdgeEnhanceImagesEnabled", "DWORD", 1)
                    # 啟用工作區功能
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "EdgeWorkspacesEnabled", "DWORD", 1)
                    # 啟用效率模式 (主要是筆電)
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "EfficiencyModeEnabled", "DWORD", 1)
                    # 啟用密碼顯示按紐
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "PasswordRevealEnabled", "DWORD", 1)
                    # 啟用儲存密碼
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "PasswordManagerEnabled", "DWORD", 1)
                    # 啟用性能檢測
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "PerformanceDetectorEnabled", "DWORD", 1)
                    # 啟動提昇 (啟用了話 , 會在關閉程式後 , 背景進程繼續運行)
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "StartupBoostEnabled", "DWORD", 0)
                    # 啟用睡眠標籤
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "SleepingTabsEnabled", "DWORD", 1)
                    # 標籤睡眠時間
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge\Recommended", "SleepingTabsTimeout", "DWORD", 30)
                    # 禁止新分頁頁面上的 Microsoft 新聞內容
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "NewTabPageContentEnabled", "DWORD", 0)
                    # 新的索引標籤頁面隱藏預設熱門網站
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "NewTabPageHideDefaultTopSites", "DWORD", 1)
                    # 啟用域名檢測器
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "TyposquattingCheckerEnabled", "DWORD", 1)
                    # 可讓使用者比較他們所查看的產品價格、從所在網站獲得優待卷，或在結帳時自動套用優待卷。
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "EdgeShoppingAssistantEnabled", "DWORD", 1)
                    # 啟用搜尋建議
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "SearchSuggestEnabled", "DWORD", 1)
                    # 視窗閉塞 偵測視窗是否被其他視窗覆蓋，而且將暫停工作繪製像素。
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "WindowOcclusionEnabled", "DWORD", 1)
                    # 控制 DNS 預先擷取、TCP 和 SSL 預先連線和預先轉譯網頁 (0) = 預測任何網路連線上的網路動作 , (2) = 不要預測任何網路連線的網路動作
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge\Recommended", "NetworkPredictionOptions", "DWORD", 0)
                    # 將不相容的網站從 Internet Explorer 重新導向至 Microsoft Edge
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "RedirectSitesFromInternetExplorerRedirectMode", "DWORD", 1)
                    # 允許來自裝置上建議提供者 (本地提供者) 的建議，例如 Microsoft Edge 的網址列和自動建議清單中的 [我的最愛] 和 [瀏覽歷程記錄]。
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "LocalProvidersEnabled", "DWORD", 1)
                    # 下載限制 (0) = 沒有特殊限制 , (1) = 封鎖危險下載內容 , (2) = 封鎖有潛在危險或垃圾下載項目 , (3) = 封鎖所有下載
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "DownloadRestrictions", "DWORD", 0)
                    # 啟動時動作 (5) = 開啟新索引標籤 , (1) = 還原上次工作階段 , (4) = 開啟 URL 清單
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "RestoreOnStartup", "DWORD", 5)
                    # 檢查下載源安全性
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "SmartScreenForTrustedDownloadsEnabled", "DWORD", 0)
                    # 是否可以接收 Microsoft 服務的自訂背景影像和文字、建議、通知及提示
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "SpotlightExperiencesAndRecommendationsEnabled", "DWORD", 0)
                    # 啟用 Microsoft Defender SmartScreen
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "SmartScreenEnabled", "DWORD", 1)
                    # 允許使用者從 HTTPS 警告頁面繼續
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "SSLErrorOverrideAllowed", "DWORD", 1)
                    # 在 Microsoft Edge 沈浸式閱讀程式內啟用文法工具功能
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "ImmersiveReaderGrammarToolsEnabled", "DWORD", 1)
                    # Microsoft Edge 中沈浸式閱讀程式內的圖片字典功能
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "ImmersiveReaderPictureDictionaryEnabled", "DWORD", 1)
                    # 控制是否允許網站對更多私人網路端點提出要求
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "InsecurePrivateNetworkRequestsAllowed", "DWORD", 1)
                    # 啟用新索引標籤頁面的預先載入
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "NewTabPagePrerenderEnabled", "DWORD", 1)
                    # 禁用限制可在密碼管理員中儲存的密碼長度
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "PasswordManagerRestrictLengthEnabled", "DWORD", 1)
                    # 啟用密碼不安全的提示
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "PasswordMonitorAllowed", "DWORD", 1)
                    # 啟用此設定，則使用者將無法忽略 Microsoft Defender SmartScreen 警告，且會讓使用者無法繼續瀏覽該網站。
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "PreventSmartScreenPromptOverride", "DWORD", 0)
                    # 如果啟用此原則，則您組織中的使用者將無法忽略 Microsoft Defender SmartScreen 警告，且會讓使用者無法完成未驗證的下載。
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "PreventSmartScreenPromptOverrideForFiles", "DWORD", 0)
                    # 允許 QUIC 通訊協定
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "QuicAllowed", "DWORD", 1)
                    # 顯示微軟獎勵
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "ShowMicrosoftRewards", "DWORD", 0)
                    # 顯示使用edge作為默認pdf開啟
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "ShowPDFDefaultRecommendationsEnabled", "DWORD", 0)
                    # 允許來自 Microsoft Edge 的功能建議和瀏覽器協助通知
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "ShowRecommendationsEnabled", "DWORD", 0)
                    # 允許從進程管理關閉edge
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "TaskManagerEndProcessEnabled", "DWORD", 1)
                    # 限制 WebRTC 暴露本地 IP 位址
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "WebRtcLocalhostIpHandling", "String", "default_public_interface_only"),
                    # Microsoft Edge 關閉時清除快取圖片與檔案
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge\Recommended", "ClearCachedImagesAndFilesOnExit", "DWORD", 1)
                    # 允許 Microsoft Edge 發出無資料連線至 Web 服務，以探查網路連線狀況
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge\Recommended", "ResolveNavigationErrorsUseWebService", "DWORD", 1)
                    # DNS 攔截檢查的本機交換器
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "DNSInterceptionChecksEnabled", "DWORD", 1)
                    # 允許凍結背景索引標籤
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "TabFreezingEnabled", "DWORD", 1)
                    # 控制是否已啟用 Microsoft Edge 管理
                    @("HKLM:\SOFTWARE\Policies\Microsoft\Edge", "EdgeManagementEnabled", "DWORD", 0)
                ), $true)

                Print "`n===== 重新啟動後應用 ====="
                $this.WaitBack()
            }
            (index) { # Edge 重置受組織管理
                Print " ============================================== "
                Print "          無特別需求不建議使用該功能" 'Red'
                Print "        該功能會重置先前所有優化註冊項目" 'Red'
                Print "  如只想重置 (一鍵優化設置) 可再次運行 (一鍵優化設置)`n" 'Red'
                Print "     重置包含: (變更緩存位置) (一鍵優化設置)"
                Print "     重置不包含: 瀏覽器設定, 與任何保存數據"
                Print " ============================================== "

                $this.DoubleConfirm({
                    Remove-Item -Path "HKLM:\SOFTWARE\Policies\Microsoft\Edge" -Recurse -Force
                    Remove-Item -Path "HKLM:\SOFTWARE\Policies\Microsoft\MicrosoftEdge" -Recurse -Force
                    Print "已重置 Edge 受組織管理" 'Green'
                    $this.WaitBack()
                })
            }
            (index) { # RAR 授權
                Print "===== 獲取授權 =====`n"

                $this.NetworkState()
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
            (index) { # IDM 授權
                # https://github.com/oop7/IDM-Activator
                $this.Authorize(
                    "script", "https://raw.githubusercontent.com/oop7/IDM-Activator/refs/heads/main/script.bat"
                )
            }
            (index) { # Windows 啟用授權
                # https://github.com/massgravel/Microsoft-Activation-Scripts
                $this.Authorize(
                    "MAS_AIO",
                    "https://raw.githubusercontent.com/massgravel/Microsoft-Activation-Scripts/refs/heads/master/MAS/All-In-One-Version-KL/MAS_AIO.cmd"
                )
            }
            (index) { # Office 啟用授權 (他會導致回到菜單時歪掉)
                # https://github.com/abbodi1406/KMS_VL_ALL_AIO
                $this.Authorize(
                    "KMS_VL_ALL_AIO", "https://raw.githubusercontent.com/abbodi1406/KMS_VL_ALL_AIO/refs/heads/master/KMS_VL_ALL_AIO.cmd"
                )
            }
            (index) { # Google 結束進程
                $this.StopProcess("chrome")
                $this.Menu()
            }
            (index) { # Edge 結束進程
                $this.StopProcess("msedge")
                $this.Menu()
            }
            (index) { # Adobe 結束進程
                $this.StopProcess(
                    @("node", "CCLibrary", "AdobeIPCBroker", "OfficeClickToRun")
                )
                $this.Menu()
            }
            (index) { # Surfshark 運行
                Print "===== Surfshark 啟動中 ====="
                $Path1 = "C:\Program Files\Surfshark\Surfshark.exe"
                $Path2 = "C:\Program Files (x86)\Surfshark\Surfshark.exe"

                if (Test-Path $Path1) {
                    Start-Service -Name "Surfshark Service" -ErrorAction SilentlyContinue
                    Start-Process -FilePath $Path1
                    $this.Menu()
                } elseif (Test-Path $Path2) {
                    Start-Service -Name "Surfshark Service" -ErrorAction SilentlyContinue
                    Start-Process -FilePath $Path2
                    $this.Menu()
                } else {
                    Print "找不到啟動程序: $Path1 或 $Path2" 'Red'
                    Print "下載連結: https://surfshark.com/zh-tw/download" 'Green'
                    $this.WaitBack()
                }
            }
            (index) { # Surfshark 終止
                $this.StopProcess(
                    @("Surfshark", "Surfshark.Service")
                )
                # 關閉服務
                # Stop-Service -Name "Surfshark Service" -Force -ErrorAction SilentlyContinue
                Get-Service | Where-Object { $_.Name -eq "Surfshark Service" } | ForEach-Object { Stop-Service -Name $_.Name -Force }
                $this.Menu()
            }
            (index) { # 網路重置
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
                # 清除 ARP 緩存
                netsh interface ip delete arpcache
                # 清除 NetBIOS 快取
                nbtstat -R
                # 禁用並重新啟用網絡接口
                Get-NetAdapter | Disable-NetAdapter -Confirm:$false
                Get-NetAdapter | Enable-NetAdapter -Confirm:$false
                # 更新 IP 配置
                ipconfig /renew
                $this.Menu()
            }
            (index) { # 網路優化

                Print " ====================================== "
                Print "      這個優化不見得適用於所有人" "Cyan"
                Print " ====================================== "

                $this.DoubleConfirm({
                    Print "`n請稍後...`n"
                    Start-Sleep -Seconds 1
                })

                # TCP 接收側縮放 (RSS) (disabled|enabled|default)
                netsh int tcp set global rss=enabled
                # 接收窗口自動調整級別(disabled|highlyrestricted|restricted|normal|experimental)
                netsh int tcp set global autotuninglevel=normal
                # TCP ECN 擁塞控制能力(disabled|enabled|default)
                netsh int tcp set global ecncapability=enabled
                # TCP 時間戳(disabled|enabled|default)
                netsh int tcp set global timestamps=enabled
                # TCP 初始時的超時 重傳時間 (300~3000)
                netsh int tcp set global initialrto=1000
                # 接收段合併狀態 (disabled|enabled|default)
                netsh int tcp set global rsc=enabled
                # SACK 用於改進丟包恢復和擁塞控制 (disabled|enabled|default)
                netsh int tcp set global nonsackrttresiliency=enabled
                # 客戶端允許的最大 SYN 重傳次數 (2~8)
                netsh int tcp set global maxsynretransmissions=2
                # TCP 快速啟用 (disabled|enabled|default)
                netsh int tcp set global fastopen=enabled
                # TCP 快速回退,如果遠程端點不支持 TCP 快速打開或發生任何錯誤，將回退到正常的握手過程 (disabled|enabled|default)
                netsh int tcp set global fastopenfallback=enabled
                # 擁塞控制算法 (disabled|enabled|default)
                netsh int tcp set global hystart=enabled
                # 擁塞控制算法 (disabled|enabled|default)
                netsh int tcp set global prr=enabled
                # 啟用數據中心擁塞控制算法 (DCA)
                netsh int tcp set global dca=enabled
                # TCP 發送方的流量控制機制 (off|initialwindow|slowstart|always|default)
                netsh int tcp set global pacingprofile=always

                # netsh int tcp set supplemental template= (automatic|datacenter|internet|compat|custom)
                # TCP 超時最小重傳時間 (20~300)
                netsh int tcp set supplemental template=datacenter minrto=200
                # TCP 在連接剛建立時允許發送的數據包數量 (2~64)
                netsh int tcp set supplemental template=datacenter icw=64
                # 擁塞控制算法 (none|ctcp|dctcp|cubic|bbr2|default)
                netsh int tcp set supplemental template=datacenter congestionprovider=bbr2
                # 擁塞窗口重啟 (disabled|enabled|default)
                netsh int tcp set supplemental template=datacenter enablecwndrestart=enabled
                # TCP延遲應答的超時 (10~600)
                netsh int tcp set supplemental template=datacenter delayedacktimeout=100
                # TCP延遲應答頻率 (1~255)
                netsh int tcp set supplemental template=datacenter delayedackfrequency=30
                # TCP 啟發式優化
                netsh int tcp set heuristics forcews=disabled

                $this.RegistItem(@(
                    # 啟用黑洞偵測，以防止封包在網路中丟失
                    @("HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters", "EnablePMTUBHDetect", "DWORD", 1)
                    # 提高 IP 封包緩衝區容量，以增強封包處理能力
                    @("HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters", "ForwardBufferMemory", "DWORD", 1048576)
                    # 增加封包處理能力，降低丟包率
                    @("HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters", "NumForwardPackets", "DWORD", 256)
                    # 設置 TCP 超時值以更快釋放資源，但可能增加套接字重用問題
                    @("HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters", "TcpTimedWaitDelay", "DWORD", 60)
                    # 縮短 NetBT 廣播查詢超時以加快名稱解析速度，但可能增加網絡流量
                    @("HKLM:\SYSTEM\CurrentControlSet\Services\NetBT\Parameters", "BcastQueryTimeout", "DWORD", 500)
                    # 縮短 NetBT 名稱伺服器查詢超時以加快名稱解析速度，但可能增加網絡流量
                    @("HKLM:\SYSTEM\CurrentControlSet\Services\NetBT\Parameters", "NameSrvQueryTimeout", "DWORD", 1000)
                    # 增加 NetBT 會話保持時間以提高連接穩定性，但可能增加網絡流量
                    @("HKLM:\SYSTEM\CurrentControlSet\Services\NetBT\Parameters", "SessionKeepAlive", "DWORD", 1800000)
                    # 設置 NetBT 名稱表大小，選擇中型（2）或大型（3）
                    @("HKLM:\SYSTEM\CurrentControlSet\Services\NetBT\Parameters", "NameTableSize", "DWORD", 2)
                    # 減少名稱註冊的初始超時以加快名稱註冊速度，但可能增加網絡負荷
                    @("HKLM:\SYSTEM\CurrentControlSet\Services\NetBT\Parameters", "InitialRefreshT.O.", "DWORD", 480000)
                    # 設置 LMHOSTS 和 DNS 名稱查詢超時值
                    @("HKLM:\SYSTEM\CurrentControlSet\Services\NetBT\Parameters", "LmhostsTimeout", "DWORD", 3000)
                    # 增加 NetBT 數據報緩衝區容量以提升傳送性能，但可能增加內存消耗
                    @("HKLM:\SYSTEM\CurrentControlSet\Services\NetBT\Parameters", "MaxDgramBuffering", "DWORD", 0x40000)
                    # 縮短 WINS 重新嘗試超時以加快 WINS 查詢，但可能增加網絡負荷
                    @("HKLM:\SYSTEM\CurrentControlSet\Services\NetBT\Parameters", "WinsDownTimeout", "DWORD", 10000)
                    # 設定 DNS 快取中記錄的最大存活時間
                    @("HKLM:\SYSTEM\CurrentControlSet\Services\Dnscache\Parameters", "MaxCacheTtl", "DWORD", 86400)
                    # 設定 TCP 窗口大小以改善 TCP 連接的流量控制
                    @("HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters", "TcpWindowSize", "DWORD", 64000)
                    # 禁用 Nagle 算法以減少延遲（預設為 1，啟用）
                    @("HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters", "TcpNoDelay", "DWORD", 1)
                ), $false)

                $interfaces = Get-ChildItem -Path "HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces"
                foreach ($interface in $interfaces) {
                    $interfacePath = $interface.PSPath
                    # 嘗試獲取 IPAddress 屬性
                    $IPAddress = Get-ItemProperty -Path $interfacePath -Name DhcpIPAddress -ErrorAction SilentlyContinue
                    # 存在 IPAddress 且不為 0.0.0.0
                    if ($IPAddress -and $IPAddress.DhcpIPAddress -ne "0.0.0.0") {
                        $this.RegistItem(@(
                            # 調整 MTU 值以優化網路性能，特別是避免封包碎片化
                            @($interfacePath, "MTU", "DWORD", 1500)
                            # 設置 TCP 立即確認以降低延遲（預設為 1）
                            @($interfacePath, "TcpAckFrequency", "DWORD", 1)
                        ), $false)
                    }
                }

                Print "`n===== 重新啟動後應用 ====="
                $this.WaitBack()
            }
            (index) { # 自動配置 DNS
                $this.NetworkState()

                $dnsServers = @{
                    Global = @(
                        @{name="IBM"; dns="9.9.9.9"; doh="https://dns.quad9.net/dns-query"},
                        @{name="IBM"; dns="9.9.9.10"; doh="https://dns.quad9.net/dns-query"},
                        @{name="Google"; dns="8.8.8.8"; doh="https://dns.google/dns-query"},
                        @{name="Google"; dns="8.8.4.4"; doh="https://dns.google/dns-query"},
                        @{name="AdGuard"; dns="94.140.14.14"; doh="https://dns.adguard.com/dns-query"},
                        @{name="AdGuard"; dns="94.140.15.15"; doh="https://dns.adguard.com/dns-query"},
                        @{name="Control D"; dns="76.76.2.0"; doh="https://dns.google/dns-query"},
                        @{name="Control D"; dns="76.76.10.0"; doh="https://dns.google/dns-query"},
                        @{name="Alternate"; dns="76.76.19.19"; doh="https://dns.google/dns-query"},
                        @{name="Alternate"; dns="76.223.122.150"; doh="https://dns.google/dns-query"},
                        @{name="Cloudflare"; dns="1.1.1.1"; doh="https://cloudflare-dns.com/dns-query"},
                        @{name="Cloudflare"; dns="1.0.0.1"; doh="https://cloudflare-dns.com/dns-query"},
                        @{name="Cloudflare 病毒攔截"; dns="1.1.1.2"; doh="https://dns.google/dns-query"},
                        @{name="Cloudflare 病毒攔截"; dns="1.0.0.2"; doh="https://dns.google/dns-query"},
                        @{name="CleanBrowsing 病毒攔截"; dns="185.228.168.9"; doh="https://doh.cleanbrowsing.org/doh/security-filter"},
                        @{name="CleanBrowsing 病毒攔截"; dns="185.228.169.9"; doh="https://doh.cleanbrowsing.org/doh/security-filter"}
                    )
                    Europe = @(
                        @{name="Level3"; dns="209.244.0.3"; doh="https://dns.google/dns-query"},
                        @{name="Level3"; dns="209.244.0.4"; doh="https://dns.google/dns-query"},
                        @{name="Open"; dns="208.67.222.222"; doh="https://doh.opendns.com/dns-query"},
                        @{name="Open"; dns="208.67.220.220"; doh="https://doh.opendns.com/dns-query"},
                        @{name="德國 Watch"; dns="84.200.69.80"; doh="https://dns.google/dns-query"},
                        @{name="德國 Watch"; dns="84.200.70.40"; doh="https://dns.google/dns-query"}
                        @{name="Comodo Secure"; dns="8.26.56.26"; doh="https://dns.google/dns-query"},
                        @{name="Comodo Secure"; dns="8.20.247.20"; doh="https://dns.google/dns-query"}
                    )
                    Asia = @(
                        @{name="Ali"; dns="223.5.5.5"; doh="https://dns.alidns.com/dns-query"},
                        @{name="Ali"; dns="223.6.6.6"; doh="https://dns.alidns.com/dns-query"},
                        @{name="中華電信"; dns="168.95.1.1"; doh="https://dns.google/dns-query"},
                        @{name="中華電信"; dns="168.95.192.1"; doh="https://dns.google/dns-query"},
                        @{name="臺灣網路資訊中心"; dns="101.101.101.101"; doh="https://dns.google/dns-query"},
                        @{name="臺灣網路資訊中心"; dns="101.102.103.104"; doh="https://dns.google/dns-query"}
                    )
                }

                Print " ================================================== "
                Print "     自動開始配置時 建議不要有消耗網路流量的操作" "Cyan"
                Print "   根據環境不同 可能出現延遲顯示都是 0 這是正常的" "Cyan"
                Print " ================================================== "

                $this.DoubleConfirm({
                    Print "`n這個操作需要一些時間 請稍後...`n"
                    Start-Sleep -Seconds 1
                })

                $locationInfo = Invoke-RestMethod -Uri "https://ipinfo.io/json"
                $area = $locationInfo.timezone.Split("/")[0]
                $testServers = $dnsServers.Global + $dnsServers[$area]

                Print "===== 開始測試延遲 ======`n"
                $pingResults = @{} # 存儲每個 DNS 伺服器的平均延遲
                $testServers | ForEach-Object {
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
                        $pingResults[@($_.name, $_.dns, $_.doh)] = $averageTime
                        Print "$($_.name) | $($_.dns) | $([math]::Round($averageTime, 1)) ms" "Yellow"
                    }
                }

                # 按平均延遲排序，選出最短的兩個 DNS 伺服器
                $sortedResults = $pingResults.GetEnumerator() | Sort-Object Value

                # 取出慣用和其他的結果
                $idiomaticResults = $sortedResults[0].Key
                $otherResults = $sortedResults[1].Key

                # 獲取 dns, doh 項
                $idiomaticDNS = $idiomaticResults[1]
                $idiomaticdoh = $idiomaticResults[2]
                $otherDNS = $otherResults[1]
                $otherdoh = $otherResults[2]

                # 重置網路
                ipconfig /release
                Clear-DnsClientCache
                netsh interface ip delete arpcache
                netsh winsock reset
                netsh int ip reset
                nbtstat -R
                ipconfig /renew

                $interfaceName = (Get-NetAdapter | Where-Object { $_.Status -eq "Up" }).Name
                Set-DnsClientServerAddress -InterfaceAlias $interfaceName -ServerAddresses ($idiomaticDNS, $otherDNS)

                Try {
                    Set-DnsClientDohServerAddress -ServerAddress $idiomaticDNS -DohTemplate $idiomaticdoh -AllowFallbackToUdp $true -AutoUpgrade $true -ErrorAction Stop
                    Set-DnsClientDohServerAddress -ServerAddress $otherDNS -DohTemplate $otherdoh -AllowFallbackToUdp $true -AutoUpgrade $true -ErrorAction Stop
                } Catch {
                    Add-DnsClientDohServerAddress -ServerAddress $idiomaticDNS -DohTemplate $idiomaticdoh -AllowFallbackToUdp $true -AutoUpgrade $true -ErrorAction SilentlyContinue
                    Add-DnsClientDohServerAddress -ServerAddress $otherDNS -DohTemplate $otherdoh -AllowFallbackToUdp $true -AutoUpgrade $true -ErrorAction SilentlyContinue
                }

                Print "`n===== 配置完成 ======`n"

                Print "慣用配置: $($idiomaticResults[0]) | $idiomaticDNS" "Green"
                Print "其他配置: $($otherResults[0]) | $otherDNS" "Green"

                $this.WaitBack()
            }
            (index) { # 取得網址 IP
                $this.NetworkState()
                Print "===== 輸入要取得的網域 (輸入 0 直接退出返回) =====`n"
                Print "!! 只能取得網域的 IP 不是完整網址的" 'Magenta'

                while ($true) {
                    $url = Input "輸入網址" 'Yellow'

                    if ($url -eq "0") {
                        $this.Menu()
                    }

                    try {
                        $uri = [System.Uri]::new($url) # 解析 URL 獲取域名
                        $hostname = $uri.Host

                        # 解析域名地址
                        $dnsResult = Resolve-DnsName -Name $hostname -ErrorAction Stop
                        # 解析數據取得 IP
                        $ipAddresses = $dnsResult | Where-Object { $_.QueryType -eq 'A' } | Select-Object -ExpandProperty IPAddress

                        # 如果獲取到 IP 地址，進行 Test-Connection
                        if ($ipAddresses) {
                            $IPFormt = $ipAddresses | ConvertTo-Json -Compress
                            Print "轉換連結: $($ipAddresses[0])$($uri.LocalPath)"
                            Print "所有 IP 地址: $IPFormt" 'Green'
                        } else {
                            Print "無法獲取 IP 地址" 'Red'
                        }
                    } catch {
                        Print "解析錯誤: 確認輸入的 URL" 'Red'
                    }
                }
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
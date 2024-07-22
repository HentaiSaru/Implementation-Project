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
    
    # 打印文本
    Write-Host $text
}

class Main {

    [void]CMD([string]$command, [bool]$pause) {
        Start-Process cmd.exe -ArgumentList "/c $command" -NoNewWindow -Wait
        if ($pause) {
            pause
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

        $InitIndex = 0
        $index = { # 根據調用次數累加索引值
            param (
                [string]$param = ""
            )

            if ($param -eq "") {
                $global:InitIndex++
                return "[[31m$global:InitIndex[37m]"
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
        Print "   Windows 相關優化 :" 'Cyan'
        $P_
        Print "   $(& $index) Windows 一鍵優化設置    $(& $index) Windows 優化錯誤恢復    $(& $index) 關閉UAC安全通知" 'White'
        $P_
        Print "   $(& $index) Visual C++ (x64)安裝    $(& $index) .NET安裝`n" 'White'
        $P_
        Print "   瀏覽器設置 :" 'Cyan'
        $P_
        Print "   $(& $index) Google 變更緩存位置    $(& $index) Google 一鍵優化設置    $(& $index) Google 修復受機構管理 (重置優化設置)" 'White'
        $P_
        Print "   $(& $index) Edge 變更緩存位置    $(& $index) Edge 一鍵優化設置    $(& $index) Edge 修復受組織管理 (重置優化設置)`n" 'White'
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
        $choice = Read-Host "[37m輸入功能 [代號]/(Enter) "
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
                $this.Menu()
            }
            "MSI" { # 查看完整系統資訊
                MSInfo32
                $this.Menu()
            }
            "NV" { # 查看顯卡驅動版本
                $this.CMD("nvidia-smi", $true)
                $this.Menu()
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
                $this.Menu()
            }
            "IP" { # 查看 IP 和網卡資訊
                $this.CMD("ipconfig /all", $true)
                $this.Menu()
            }
            "RS" {
                $this.CMD("net share", $true)
                $this.Menu()
            }
            "MC" {
                $this.CMD("getmac /fo table /v", $true)
                $this.Menu()
            }
            "SV" {
                $this.CMD("net start", $true)
                $this.Menu()
            }
            "MRT" {
                mrt
                $this.Menu()
            }
            "WF" {
                $this.CMD("netsh wlan show profiles", $true)
                $this.Menu()
            }
            "DV" {
                msdt.exe -id DeviceDiagnostic
                $this.Menu()
            }
            "SR" {
                Print "準備修復 請稍後...`n"

                $this.CMD("Dism /Online /Cleanup-Image /ScanHealth", $false)
                $this.CMD("Dism /Online /Cleanup-Image /CheckHealth", $false)
                $this.CMD("DISM /Online /Cleanup-image /RestoreHealth", $false)
                $this.CMD("sfc /scannow", $false)
                $this.Menu()
            }
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
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

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

function Delete {
    param (
        [Object]$RemoveObject
    )

    if ($RemoveObject -is [string]) {
        if (Test-Path $RemoveObject) {
            try {
                Remove-Item -Path $RemoveObject -Recurse -Force -ErrorAction SilentlyContinue
                Print "清理成功: $RemoveObject" 'Green'
            } catch {
                Print "清理失敗: $_" 'Red'
            }
        }
    } elseif ($RemoveObject -is [Object]) {
        $RemoveObject | ForEach-Object {
            if (Test-Path $_) {
                try {
                    Remove-Item -Path $_ -Recurse -Force -ErrorAction SilentlyContinue
                    Print "清理成功: $_" 'Green'
                } catch {
                    Print "清理失敗: $_" 'Red'
                }
                
            }
        }
    }
}

Print "========================================================================================================================" 'Red'
Print "                                                    系統清理程式 v2" 'Magenta'
Print "========================================================================================================================" 'White'
Print ""
Print "                                              - Versions 1.0.0 2024/10/10 -" 'Green'
Print ""
Print "                                               清理時建議關閉所有應用程式" 'Yellow'
Print ""
Print "                                        此程式只會清除(緩存/暫存)檔案不會影響系統" 'Yellow'
Print ""
Print "-----------------------------------------------------------------------------------------------------------------------" 'White'
Print "                                                 按任意鍵開始清理系統"
Print "-----------------------------------------------------------------------------------------------------------------------" 'Red'
Input "輸入任意鍵..."

# 取得路徑
$Temp = $env:Temp
$C = $env:systemdrive
$Windows = $env:windir
$Roaming = $env:AppData
$User = $env:userprofile
$Local = $env:LocalAppData
$Program = $env:ProgramData
$LocalLow = "$(split-path $Roaming)\LocalLow"

# ===== 重置網路 =====
ipconfig /release # 釋放 IP
Clear-DnsClientCache # 清除 DNS 緩存
netsh int ip reset # 重置 IP 設定
netsh int tcp reset # 重置 TCP/IP 堆疊
netsh winsock reset # 重置 Winsock
certutil -URLCache * delete # 清除憑證 URL 緩存
netsh interface ip delete arpcache # 清除 ARP 緩存
nbtstat -R # 清除 NetBIOS 快取
ipconfig /renew # 更新 IP 配置

# ===== 重置更新緩存 =====
Stop-Service -Name bits, wuauserv, cryptSvc, msiserver -Force

Delete @(
    "$Windows\System32\catroot2.old"
    "$Windows\SoftwareDistribution.old"
)

Start-Service -Name bits, wuauserv, cryptSvc, msiserver

# ===== 清除系統基本緩存 =====
Delete @(
    # 舊的系統文件
    "$Windows.old"

    # 刪除錯誤報告 和 系統日誌
    "$Windows\System32\winevt\Logs\"
    "$Program\Microsoft\Windows\WER\"
    "$Windows\PCHealth\ERRORREP\QSIGNOFF\"
    "$Program\Microsoft\Diagnosis\ETLLogs\AutoLogger\"

    # ASP.NET 應用程序的臨時編譯文件
    "$Windows\Microsoft.NET\Framework\v1.1.4322\Temporary ASP.NET Files\"
    "$Windows\Microsoft.NET\Framework\v2.0.50727\Temporary ASP.NET Files\"
    "$Windows\Microsoft.NET\Framework\v4.0.30319\Temporary ASP.NET Files\"

    # 舊版瀏覽器緩存
    "$Local\Microsoft\Windows\WebCache\"
    "$Local\Microsoft\Windows\INetCache\"
    "$Roaming\Opera Software\Opera Stable\Cache\"
    "$Roaming\Mozilla\Firefox\Profiles\*\cache2\"
    "$Local\Microsoft\Windows\Explorer\thumbcache*"
    "$Roaming\Google\Chrome\User Data\Default\Cache\"

    # 緩存數據
    "$Temp\"
    "$C\*.tmp"
    "$C\*._mp"
    "$C\*.log"
    "$C\*.gid"
    "$C\*.chk"
    "$C\*.dlf"
    "$C\recycled\"
    "$Windows\Temp\"
    "$LocalLow\Temp\"
    "$Windows\KB*.log"
    "$Windows\*.bak"
    "$Windows\HELP\"
    "$Windows\prefetch\"
    "$User\recent\"
    "$User\cookies\"
    "$Windows\SystemTemp"
    "$User\Local Settings\Temp\"
    "$Local\Microsoft\Windows\Caches\"
    "$Windows\SoftwareDistribution\Download\"
    "$User\Local Settings\Temporary Internet Files\"

    "$User\RecycleBin\"
    "$Program\Package Cache\"
    "$Windows\ServiceProfiles\NetworkService\AppData\Local\Microsoft\Windows\DeliveryOptimization"

    "$User\Local"
    "$User\Intel"
    "$User\source"
    "$C\Program Files\Temp"

    "$C\AMD\"
    "$C\INTEL\"
    "$C\NVIDIA\"
    "$C\OneDriveTemp"
    "$Windows\logs\*.log"
    "$Windows\Panther\*.log"
    "$Windows\Logs\MoSetup\*.log"
    "$Windows\Logs\CBS\CbsPersist*.log"

    "$User\.cache"
    "$User\.Origin"
    "$Local\pip\cache"
    "$User\.QtWebEngineProcess"
    "$Local\Microsoft\Windows\INetCache\*.log"
)

# ===== 清除防火牆紀錄 =====
Delete @(
    "$Program\Microsoft\Windows Defender\Support\"
    "$Program\Microsoft\Windows Defender\Scans\MetaStore\"
    "$Program\Microsoft\Windows Defender\Scans\History\CacheManager\"
    "$Program\Microsoft\Windows Defender\Scans\History\Service\*.log"
    "$Program\Microsoft\Windows Defender\Scans\History\Results\Quick\"
    "$Program\Microsoft\Windows Defender\Scans\History\Results\Resource\"
    "$Program\Microsoft\Windows Defender\Scans\History\ReportLatency\Latency\"
    "$Program\Microsoft\Windows Defender\Network Inspection System\Support\*.log"
)

# ===== 第三方軟體緩存 =====
Delete @(
    "$Local\Surfshark\Updates"
    "$Roaming\nikke_launcher\tbs_cache"
    "$Roaming\Telegram Desktop\tdata\user_data"
    "$Program\IObit\Driver Booster\Download"
    "$LocalLow\NVIDIA\PerDriverVersion\DXCache"
    "$Roaming\IObit\Software Updater\Log\*.dbg"
    "$Roaming\IObit\Software Updater\AutoLog\*.dbg"

    "$Local\Google\Chrome\User Data\Default\IndexedDB"
    "$Local\Google\Chrome\User Data\extensions_crx_cache"
    "$Local\Google\Chrome\User Data\Default\Service Worker"

    "$Local\Microsoft\Edge\User Data\Profile*\IndexedDB"
    "$Local\Microsoft\Edge\User Data\extensions_crx_cache"
    "$Local\Microsoft\Edge\User Data\Profile*\Service Worker"

    "$Roaming\Code\logs"
    "$Roaming\Code\Crashpad"
    "$Roaming\Code\CachedData"
    "$Roaming\Code\User\History"
    "$Roaming\Code\CachedExtensions"
    "$Roaming\Code\CachedExtensionVSIXs"
    "$Roaming\Code\User\workspaceStorage"
    "$Roaming\Code\Service Worker\ScriptCache"
    "$Roaming\Code\Service Worker\CacheStorage"
    "$Roaming\Code\User\globalStorage\redhat.java"
    "$Local\Microsoft\vscode-cpptools"

    "$Local\LINE\bin\old"
)

# ===== 掃描清理緩存類型文件 =====
$findFolders = @($Roaming, $Local, $LocalLow)
$cacheFolders = @('Cache', 'Code Cache', 'GPUCache', 'DawnCache', 'INetCache', 'ShaderCache', 'GrShaderCache')

foreach ($find in $findFolders) {
    foreach ($cache in $cacheFolders) {
        $found = Get-ChildItem -Path $find -Filter $cache -Recurse -ErrorAction SilentlyContinue
        if ($found) { Delete $found }
    }
}

# ===== 調用系統清理 並檢查錯誤 =====
Start-Process cleanmgr.exe -ArgumentList "/sagerun:99"

Print "`n安全移除系統內隱藏檔案(這需要花一段時間)`n" 'Yellow'

# 清理不再需要的系統組件和臨時文件
& Dism.exe /online /Cleanup-Image /StartComponentCleanup

# 在組件清理的基礎上進行的擴展操作
& Dism.exe /online /Cleanup-Image /StartComponentCleanup /ResetBase

Print "`n檢查系統有無損壞(這需要花一段時間)`n" 'Green'
& Dism.exe /Online /Cleanup-Image /ScanHealth
& Dism.exe /Online /Cleanup-Image /CheckHealth
& Dism.exe /Online /Cleanup-image /RestoreHealth
& sfc /scannow

# ===== 結束選擇 =====
Print "  ✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬" 'Cyan'
Print ""
Print "           【 操作選擇 】"
Print ""
Print "    《1.電腦關機》   《2.電腦重啟》" 'Yellow'
Print ""
Print "    《3.清理還原》   《4.離開程式》" 'Yellow'
Print ""
Print "  ✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬" 'Cyan'
Print ""
$choice = Input "選擇功能 [代號]"

switch ($choice) {
    1 { Stop-Computer -Force }
    2 { Restart-Computer -Force }
    3 { control sysdm.cpl,0,4 }
    4 { exit }
}
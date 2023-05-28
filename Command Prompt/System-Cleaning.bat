@echo off
chcp 65001 >nul 2>&1
color C
%1 %2
ver|find "5.">nul&&goto :Admin
mshta vbscript:createobject("shell.application").shellexecute("%~s0","goto :Admin","","runas",1)(window.close)&goto :eof
:Admin

cls
title 系統清理優化

:: - Versions 1.0.0 -
::
:: (說明) win10 沿用 win11 , 有些指令不適用 win11 , 但可正常運行
:: 
:: [+] - 基本系統清理
:: [+] - Line 緩存清理
:: [+] - Google 緩存清理
:: [+] - Discord 緩存清理
:: [+] - 網路設置優化
:: [+] - 系統微優化
:: [+] - 系統修復

@echo off
@ ECHO.
@ ECHO.~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 系統緩存清理程序 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@ ECHO.
@ ECHO                                          清理中出現錯誤和畫面閃爍純屬正常現象                                 
@ ECHO.
@ ECHO                                        清理完畢後可選擇重新啟動電腦(或是直接離開)
@ ECHO.
@ ECHO -----------------------------------------------------------------------------------------------------------------------
@ ECHO                                                按任意鍵開始清理系統
@ ECHO -----------------------------------------------------------------------------------------------------------------------
@ ECHO.
@ ECHO.

:: 等待任意鍵
pause

@echo 開始清理請稍.....
timeout /t 03 >nul

:: ========== 網路重置 ==========
:: 釋放IP位置
ipconfig /release
:: 清空Dns緩存
ipconfig /flushdns
:: 重新請求IP位置
ipconfig /renew

:: ========== 網路優化 ==========
:: 禁用自動調整 TCP 接收窗口的功能
netsh int tcp set global autotuninglevel=disabled
:: 將 TCP 擁塞控制算法設置為 CTCP
netsh int tcp set global congestionprovider=ctcp
:: 啟用 TCP 解除安裝引擎
netsh int tcp set global chimney=enabled
:: 禁用 TCP 接收側縮放 (RSS)
netsh int tcp set global rss=disabled
:: 禁用 TCP 啟發式優化
netsh int tcp set heuristics=disabled
:: 啟用數據中心擁塞控制算法 (DCA)
netsh int tcp set global dca=enabled
netsh int tcp set supplemental template=internet
:: 啟用 TCP 時間戳
netsh int tcp set global timestamps=enabled
:: 禁用擁塞控制 ECN
netsh int tcp set global ecncapability=disabled
:: 禁用 TCP ECN
netsh int tcp set global ecn=disable
:: 啟用 TCP 快速打開
netsh int tcp set global fastopen=enabled
:: 刪除系統的 ARP 緩存
netsh interface ip delete arpcache
:: 刪除系統中的證書緩存
certutil -URLCache * delete
:: 啟用網路層源站驗證
netsh int ip set global source=validate-icmpv4
:: 啟用網路層源站路由
netsh int ip set global source=enable-ipv4-source-routing
:: 啟用網路層轉發
netsh int ip set global forwarding=enabled
:: 禁用 TCP/IP v6 協議
netsh int ipv6 uninstall
:: ========== 清理優化 ==========
:: 刪除錯誤報告
DEL /F /S /Q "C:\WINDOWS\PCHealth\ERRORREP\QSIGNOFF\*.*"
DEL /F /S /Q "C:\WINDOWS\system32\LogFiles\HTTPERR\*.*"
:: 刪除操作緩存
DEL /F /S /Q "C:\WINDOWS\Microsoft.NET\Framework\v1.1.4322\Temporary ASP.NET Files\*.*"
DEL /F /S /Q "C:\WINDOWS\Microsoft.NET\Framework\v2.0.50727\Temporary ASP.NET Files\*.*"
DEL /F /S /Q "C:\WINDOWS\Microsoft.NET\Framework\v4.0.30319\Temporary ASP.NET Files\*.*"
DEL /F /S /Q "C:\WINDOWS\temp\*.*"
:: 刪除臨時文件
DEL /F /S /Q /A:S "C:\WINDOWS\IIS Temporary Compressed Files\*.*"
DEL %windir%\KB*.log /F /q
echo Y | RD %windir%\$hf_mig$ /S
:: 刪除舊版系統文件
RD /S /Q C:\Windows.old
:: 舊版刪除各瀏覽器緩存
del /f /s /q "%LocalAppData%\Microsoft\Windows\WebCache\*.*"
del /f /s /q "%LocalAppData%\Microsoft\Windows\INetCache\*.*"
del /f /s /q "%AppData%\Opera Software\Opera Stable\Cache\*.*"
del /f /s /q "%AppData%\Mozilla\Firefox\Profiles\*\cache2\*.*"
del /f /s /q "%AppData%\Google\Chrome\User Data\Default\Cache\*.*"
del /f /s /q "%LocalAppData%\Microsoft\Windows\Explorer\thumbcache*"

del /f /s /q "%Temp%"
del /f /s /q "%windir%\*.bak"
del /f /s /q "%windir%\temp\*.*"
del /f /s /q "%systemdrive%\*.tmp"
del /f /s /q "%systemdrive%\*._mp"
del /f /s /q "%systemdrive%\*.log"
del /f /s /q "%systemdrive%\*.gid"
del /f /s /q "%systemdrive%\*.chk"
del /f /s /q "%systemdrive%\*.dlf"
del /f /s /q "C:\WINDOWS\HELP\*.*"
del /f /s /q "%systemroot%\Temp\*.*"
del /f /s /q "%windir%\prefetch\*.*"
del /f /s /q "%userprofile%\recent\*.*"
del /f /s /q "%userprofile%\cookies\*.*"
del /f /s /q "%systemdrive%\recycled\*.*"
del /f /s /q "%HomePath%\AppData\LocalLow\Temp\*.*"
del /f /s /q "%userprofile%\Local Settings\Temp\*.*"
del /f /s /q "%windir%\SoftwareDistribution\Download\*.*"
del /f /s /q "%LOCALAPPDATA%\Microsoft\Windows\Caches\*.*"
del /f /s /q "%programdata%\Microsoft\Windows\WER\Temp\*.*"
del /f /s /q "%userprofile%\Local Settings\Temporary Internet Files\*.*"
del /f /s /q "%AllUsersProfile%\「開始」功能表\程式集\Windows Messenger.lnk"

RD /s /q %localappdata%\Temp
RD /s /q %userprofile%\RecycleBin
RD /s /q C:\Windows\ServiceProfiles\NetworkService\AppData\Local\Microsoft\Windows\DeliveryOptimization

RD /s /q %userprofile%\Local
RD /s /q %userprofile%\Intel
RD /s /q %userprofile%\source
RD /s /q %systemdrive%\Program Files\Temp

del /s /f /q %windir%\logs\*.log
del /s /f /q %SYSTEMDRIVE%\AMD\*.*
del /s /f /q %windir%\Panther\*.log
del /s /f /q %SYSTEMDRIVE%\INTEL\*.*
del /s /f /q %SYSTEMDRIVE%\NVIDIA\*.*
del /s /f /q %SYSTEMDRIVE%\OneDriveTemp
del /s /f /q %windir%\Logs\MoSetup\*.log
del /s /f /q %windir%\Logs\CBS\CbsPersist*.log
del /s /f /q %localappdata%\Microsoft\Windows\WebCache\*.log

rd /s /f /q %LocalAppData%\pip\cache
rd /s /q C:\Users\%username%\.cache
rd /s /q C:\Users\%username%\.Origin
rd /s /q C:\Users\%username%\.QtWebEngineProcess
rd /s /q %localappdata%\Microsoft\Windows\INetCache\*.log

:: 額外特別項目清除
del /q /s /f "%APPDATA%\IObit\IObit Uninstaller\UMlog\*.dbg"
:: Dx緩存清除
rd /s /q "%USERPROFILE%\AppData\Local\NVIDIA\DXCache"

color 3
cls
:: ========== 清除更新緩存 ==========
net stop bits
net stop wuauserv
net stop cryptSvc
net stop msiserver
ren "C:\Windows\System32\catroot2 catroot2.old"
ren "C:\Windows\SoftwareDistribution SoftwareDistribution.old"

del /s /f /q "C:\Windows\SoftwareDistribution\*.*"

net start bits
net start wuauserv
net start cryptSvc
net start msiserver

:: ========== 清除內建防火牆紀錄 ==========
del "%ProgramData%\Microsoft\Windows Defender\Support" /F /Q /S
del "%ProgramData%\Microsoft\Windows Defender\Scans\MetaStore" /F /Q /S
del "%ProgramData%\Microsoft\Windows Defender\Scans\History\CacheManager" /F /Q /S
del "%ProgramData%\Microsoft\Windows Defender\Scans\History\Service\*.log" /F /Q /S
del "%ProgramData%\Microsoft\Windows Defender\Scans\History\Results\Quick" /F /Q /S
del "%ProgramData%\Microsoft\Windows Defender\Scans\History\Results\Resource" /F /Q /S
del "%ProgramData%\Microsoft\Windows Defender\Scans\History\ReportLatency\Latency" /F /Q /S
del "%ProgramData%\Microsoft\Windows Defender\Network Inspection System\Support\*.log" /F /Q /S


:: ========== Google清理 ==========
color A
cls
@echo Google Chrom清理(將會被關閉)
timeout /t 03 >nul

:: 關閉
wmic process where name="chrome.exe" delete

set ChromeCache="%ChromeDataDir%\Cache"
set ChromeDataDir="C:\Users\%USERNAME%\Local Settings\Application Data\Google\Chrome\User Data\Default"

rd /s /q "%LocalAppData%\Google\Chrome\User Data\Default\Cache"
del /f /s /q "%LocalAppData%\Google\Chrome\User Data\Default\*tmp"
del /f /s /q "%LocalAppData%\Google\Chrome\User Data\Default\History*"

rd /s /q "%USERPROFILE%\AppData\Local\Google\Chrome\User Data\Default\Cache"
rd /s /q "%USERPROFILE%\AppData\Local\Google\Chrome\User Data\Default\IndexedDB"
rd /s /q "%USERPROFILE%\AppData\Local\Google\Chrome\User Data\Default\Service Worker"

del /q /s /f "%ChromeCache%\*.*"
del /q /s /f "%ChromeDataDir%\*Cookies*.*"

:: ========== VScode清理 ==========
@echo VScode清理

del /f /s /q "%userprofile%\AppData\Roaming\Code\logs\*.*"
del /f /s /q "%userprofile%\AppData\Roaming\Code\Cache\*.*"
del /f /s /q "%userprofile%\AppData\Roaming\Code\Crashpad\*.*"
del /f /s /q "%userprofile%\AppData\Roaming\Code\Code Cache\*.*"
del /f /s /q "%userprofile%\AppData\Roaming\Code\CachedData\*.*"
del /f /s /q "%userprofile%\AppData\Roaming\Code\User\History\*.*"
del /f /s /q "%userprofile%\AppData\Roaming\Code\CachedExtensions\*.*"
del /f /s /q "%userprofile%\AppData\Roaming\Code\CachedExtensionVSIXs\*.*"
del /f /s /q "%userprofile%\AppData\Roaming\Code\User\workspaceStorage\*.*"
del /f /s /q "%userprofile%\AppData\Local\Microsoft\vscode-cpptools\ipch\*.*"
del /f /s /q "%userprofile%\AppData\Roaming\Code\Service Worker\ScriptCache\*.*"
del /f /s /q "%userprofile%\AppData\Roaming\Code\Service Worker\CacheStorage\*.*"

:: ========== discord清理 ==========
@echo discord清理(DC將會被關)

timeout /t 03 >nul

:: 關閉
wmic process where name="Discord.exe" delete

del /f /s /q "%AppData%\Discord\Cache\*.*"
del /f /s /q "%APPDATA%\Discord\GPUCache\*.*"
del /f /s /q "%APPDATA%\Discord\Code Cache\*.*"
del /f /s /q "%APPDATA%\Discord\DawnCache\*.*"

:: ========== Line清理 ==========
@echo 清理Line緩存(Line將會被關閉)

timeout /t 03 >nul

:: 關閉
wmic process where name="Line.exe" delete

del /f /s /q "%USERPROFILE%\AppData\Local\LINE\Cache\*.*"

:: ========== 優化操作 ==========
color B
cls
@echo 開始進行電腦優化

:: 終極效能(創建)
powercfg -duplicatescheme 95533644-e700-4a79-a56c-a89e8cb109d9
:: 終極效能(設置)
powercfg.exe /setactive 95533644-e700-4a79-a56c-a89e8cb109d9

:: 禁用休眠
powercfg.exe /hibernate off

:: 禁用硬碟節能
for /f "tokens=*" %%i in ('reg query "HKLM\SYSTEM\CurrentControlSet\Enum" /s /f "StorPort"^| findstr "StorPort"') do reg add "%%i" /v "EnableIdlePowerManagement" /t REG_DWORD /d "0" /f >nul 2>&1
    for %%i in (EnableHIPM EnableDIPM EnableHDDParking) do for /f %%a in ('reg query "HKLM\SYSTEM\CurrentControlSet\Services" /s /f "%%i" ^| findstr "HKEY"') do reg add "%%a" /v "%%i" /t REG_DWORD /d "0" /f >nul 2>&1
    for /f %%i in ('call "resources\smartctl.exe" --scan') do (
        call "resources\smartctl.exe" -s apm,off %%i
        call "resources\smartctl.exe" -s aam,off %%i
    ) >nul 2>&1
    reg add "HKLM\SYSTEM\CurrentControlSet\Control\Storage" /v "StorageD3InModernStandby" /t REG_DWORD /d "0" /f >nul 2>&1
    reg add "HKLM\SYSTEM\CurrentControlSet\Services\stornvme\Parameters\Device" /v "IdlePowerMode" /t REG_DWORD /d "0" /f >nul 2>&1

POWERSHELL "$devices = Get-WmiObject Win32_PnPEntity; $powerMgmt = Get-WmiObject MSPower_DeviceEnable -Namespace root\wmi; foreach ($p in $powerMgmt){$IN = $p.InstanceName.ToUpper(); foreach ($h in $devices){$PNPDI = $h.PNPDeviceID; if ($IN -like \"*$PNPDI*\"){$p.enable = $False; $p.psbase.put()}}}"

:: 碎片整理工具
%windir%\system32\defrag.exe %systemdrive% -b

:: 停止搜尋服務
net stop "Windows Search
:: 搜尋服務禁止啟用
sc config "Windows Search" start=disabled
:: 停止網路共享服務
net stop "WMPNetworkSvc"
:: 網路共享服務禁止啟用
sc config "WMPNetworkSvc" start=disabled

:: 關閉虛擬內存(分頁文件)
reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management" /v PagingFiles /t REG_MULTI_SZ /d "" /f
:: 關閉桌面管理器動畫
reg add "HKEY_CURRENT_USER\Software\Policies\Microsoft\Windows\DWM" /v "DisallowAnimations" /d 1 /t REG_dword /f
:: Windows Explorer 動畫關閉
reg add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer" /v "TurnOffSPIAnimations" /d 1 /t REG_dword /f
:: 視窗最大最小化動畫關閉
reg add "HKEY_CURRENT_USER\Control Panel\Desktop\WindowMetrics" /v "MinAnimate" /d 0 /t REG_SZ /f
:: 關閉自動更新
reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Update" /v "UpdateMode" /d "0" /t REG_DWORD /f
:: 啟用分離桌面
reg add "HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer" /v "DesktopProcess" /d "1" /t REG_DWORD /f

:: 重啟防火牆
Netsh advfirewall set currentprofile state on
Netsh advfirewall set domainprofile state on
netsh advfirewall set privateprofile state on
netsh advfirewall set allprofiles state on

color D
cls
@echo 接下來需要安全移除系統內隱藏檔案 所以需要一段掃描時間
timeout /t 03 >nul

:: 清理不再需要的系統組件和臨時文件
Dism.exe /online /Cleanup-Image /StartComponentCleanup
:: 在組件清理的基礎上進行的擴展操作
Dism.exe /online /Cleanup-Image /StartComponentCleanup /ResetBase

@echo 檢查系統修復檔有無損(這需要花一段時間確保系統無損壞)
Dism /Online /Cleanup-Image /ScanHealth
Dism /Online /Cleanup-Image /CheckHealth
DISM /Online /Cleanup-image /RestoreHealth

:: 刪除創建的多於文件
rd /s /q C:\Program
rd /s /q Settings
rd /s /q Files

cls
@echo 檢查系統有無損壞
sfc /scannow

:: 最後詢問是否重啟
color C
CLS
MODE con: COLS=40 LINES=15
ECHO.
ECHO.
ECHO    **********************************
ECHO.
ECHO        是否重新啟動(請按上方數字)
ECHO.
ECHO               1. 重啟
ECHO.
ECHO               2. 直接離開
ECHO.
ECHO    **********************************
ECHO.
ECHO.
Choice /C 12 /N /M 選擇（1、2）：
If ErrorLevel 1 If Not ErrorLevel 2 Goto Restart1
If ErrorLevel 2 If Not ErrorLevel 3 Goto Restart2

:Restart2
exit

:Restart1
shutdown /r /t 0

pause
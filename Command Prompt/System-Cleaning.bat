:: - Versions 1.0.9 -
:: 
:: [+] - 基本系統清理
:: [+] - Line 緩存清理
:: [+] - Google 緩存清理
:: [+] - Discord 緩存清理
:: [+] - 網路設置優化
:: [+] - 系統微優化
:: [+] - 系統修復

@echo off
chcp 65001 >nul 2>&1
color C
%1 %2
ver|find "5.">nul&&goto :Admin
mshta vbscript:createobject("shell.application").shellexecute("%~s0","goto :Admin","","runas",1)(window.close)&goto :eof
:Admin

cls
title 系統清理優化

@ ECHO.
@ ECHO.~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 系統緩存清理程序 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@ ECHO.
@ ECHO                                             - Versions 1.0.9 2023/06/01 -
@ ECHO.
@ ECHO                                        此程式只會清除(緩存/暫存)檔案不會影響系統                                 
@ ECHO.
@ ECHO                                      清理完畢後可選擇(重啟電腦/關機/直接離開程式等)
@ ECHO.
@ ECHO -----------------------------------------------------------------------------------------------------------------------
@ ECHO                                                按任意鍵開始清理系統
@ ECHO -----------------------------------------------------------------------------------------------------------------------
@ ECHO.

:: 等待任意鍵
pause

@echo 開始清理請稍.....
timeout /t 02 >nul

:: ========== 網路重置 ==========
:: 釋放IP位置
ipconfig /release
:: 清空Dns緩存
ipconfig /flushdns
:: 重新請求IP位置
ipconfig /renew

:: ========== 網路優化 ==========

:: TCP 接收側縮放 (RSS) (disabled|enabled|default)
netsh int tcp set global rss=enabled
:: 接收窗口自動調整級別(disabled|highlyrestricted|restricted|normal|experimental)
netsh int tcp set global autotuninglevel=normal
:: TCP ECN 擁塞控制能力(disabled|enabled|default)
netsh int tcp set global ecncapability=enabled
:: TCP 時間戳(disabled|enabled|default)
netsh int tcp set global timestamps=enabled
:: TCP 初始時的超時 重傳時間 (300~3000)
netsh int tcp set global initialrto=1000
:: 接收段合併狀態 (disabled|enabled|default)
netsh int tcp set global rsc=enabled
:: SACK 用於改進丟包恢復和擁塞控制 (disabled|enabled|default)
netsh int tcp set global nonsackrttresiliency=enabled
:: 客戶端允許的最大 SYN 重傳次數 (2~8)
netsh int tcp set global maxsynretransmissions=2
:: TCP 快速啟用 (disabled|enabled|default)
netsh int tcp set global fastopen=enabled
:: TCP 快速回退,如果遠程端點不支持 TCP 快速打開或發生任何錯誤，將回退到正常的握手過程 (disabled|enabled|default)
netsh int tcp set global fastopenfallback=enabled
:: 擁塞控制算法 (disabled|enabled|default)
netsh int tcp set global hystart=enabled
:: 擁塞控制算法 (disabled|enabled|default)
netsh int tcp set global prr=enabled
:: 啟用數據中心擁塞控制算法 (DCA)
netsh int tcp set global dca=enabled
:: TCP 發送方的流量控制機制 (off|initialwindow|slowstart|always|default)
netsh int tcp set global pacingprofile=always

::--------------------------------------------------------------------------------------::

:: netsh int tcp set supplemental template= (automatic|datacenter|internet|compat|custom)
:: TCP 超時最小重傳時間 (20~300)
netsh int tcp set supplemental template=datacenter minrto=200
:: CP 在連接剛建立時允許發送的數據包數量 (2~64)
netsh int tcp set supplemental template=datacenter icw=64
:: 擁塞控制算法 (none|ctcp|dctcp|cubic|bbr2|default)
netsh int tcp set supplemental template=datacenter congestionprovider=bbr2
:: 擁塞窗口重啟 (disabled|enabled|default)
netsh int tcp set supplemental template=datacenter enablecwndrestart=enabled
:: TCP延遲應答的超時 (10~600)
netsh int tcp set supplemental template=datacenter delayedacktimeout=100
:: TCP延遲應答頻率 (1~255)
netsh int tcp set supplemental template=datacenter delayedackfrequency=30

::--------------------------------------------------------------------------------------::

:: TCP 啟發式優化
netsh int tcp set heuristics forcews=disabled
:: 刪除系統中的證書緩存
certutil -URLCache * delete
:: 刪除系統的 ARP 緩存
netsh int ip delete arpcache

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
rd /s /q "C:\ProgramData\IObit\Driver Booster\Download"
rd /s /q "%LocalAppData%\Surfshark\Updates"

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
timeout /t 02 >nul

:: 關閉
wmic process where name="chrome.exe" delete

set ChromeCache="%ChromeDataDir%\Cache"
set ChromeDataDir="C:\Users\%USERNAME%\Local Settings\Application Data\Google\Chrome\User Data\Default"

rd /s /q "%LocalAppData%\Google\Chrome\User Data\Default\Cache"
del /f /s /q "%LocalAppData%\Google\Chrome\User Data\Default\*tmp"
del /f /s /q "%LocalAppData%\Google\Chrome\User Data\Default\History*"

rd /s /q "%LocalAppData%\Google\Chrome\User Data\Default\Cache"
rd /s /q "%LocalAppData%\Google\Chrome\User Data\Default\IndexedDB"
rd /s /q "%LocalAppData%\Google\Chrome\User Data\Default\Service Worker"

del /q /s /f "%ChromeCache%\*.*"
del /q /s /f "%ChromeDataDir%\*Cookies*.*"

:: ========== Edge清理 ==========
@echo edge清理(將會被關閉) 因為清除所有緩存 , 第一次重開會比較卡
timeout /t 2 >nul

wmic process where name="msedge.exe" delete

for /d %%E in ("%LocalAppData%\Microsoft\Edge\User Data\Profile*") do (
    rd /s /q "%%E\Cache"
    rd /s /q "%%E\GPUCache"
    rd /s /q "%%E\IndexedDB"
    rd /s /q "%%E\Code Cache"
    rd /s /q "%%E\Service Worker"
)

:: ========== VScode清理 ==========
@echo VScode清理

rd /s /q "%appdata%\Code\logs"
rd /s /q "%appdata%\Code\Cache"
rd /s /q "%appdata%\Code\Crashpad"
rd /s /q "%appdata%\Code\Code Cache"
rd /s /q "%appdata%\Code\CachedData"
rd /s /q "%appdata%\Code\User\History"
rd /s /q "%appdata%\Code\CachedExtensions"
rd /s /q "%appdata%\Code\CachedExtensionVSIXs"
rd /s /q "%appdata%\Code\User\workspaceStorage"
rd /s /q "%LocalAppData%\Microsoft\vscode-cpptools"
rd /s /q "%appdata%\Code\Service Worker\ScriptCache"
rd /s /q "%appdata%\Code\Service Worker\CacheStorage"
rd /s /q "%appdata%\Code\User\globalStorage\redhat.java"

:: ========== discord清理 ==========
@echo discord清理(DC將會被關)

timeout /t 02 >nul

:: 關閉
wmic process where name="Discord.exe" delete

del /f /s /q "%AppData%\Discord\Cache\*.*"
del /f /s /q "%APPDATA%\Discord\GPUCache\*.*"
del /f /s /q "%APPDATA%\Discord\Code Cache\*.*"
del /f /s /q "%APPDATA%\Discord\DawnCache\*.*"

:: ========== Line清理 ==========
@echo 清理Line緩存(Line將會被關閉)

timeout /t 02 >nul

:: 關閉
wmic process where name="Line.exe" delete

del /f /s /q "%LocalAppData%\LINE\Cache\*.*"
rd /s /q  "%LocalAppData%\LINE\bin\old"

:: ========== 優化操作 ==========
color B
cls
@echo 開始進行電腦優化

:: 終極效能 (測試)
powercfg -duplicatescheme 95533644-e700-4a79-a56c-a89e8cb109d9
powercfg.exe /setactive 95533644-e700-4a79-a56c-a89e8cb109d9

powercfg -duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61
powercfg.exe /setactive e9a42b02-d5df-448d-aa00-03f14749eb61

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

:: 清理虛擬內存後 , 再次創建設置
wmic pagefileset delete
wmic pagefileset create name="C:\pagefile.sys"
wmic pagefileset where name="C:\pagefile.sys" set InitialSize=8192, MaximumSize=16,384

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

:: 內建清理
cleanmgr /sagerun:99

color D
cls
@echo 接下來需要安全移除系統內隱藏檔案 所以需要一段掃描時間
timeout /t 02 >nul

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
ECHO    ✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬
ECHO.
ECHO             【 操作選擇 】
ECHO.
ECHO      《1.電腦關機》   《2.電腦重啟》
ECHO.
ECHO      《3.清理還原》   《4.離開程式》
ECHO.            
ECHO    ✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬✬
ECHO.

Choice /C 1234 /N /M "選擇 (數字) :"

if %errorlevel% == 1 (
    shutdown /s /t 0
    exit
) else if %errorlevel% == 2 (
    shutdown /r /t 0
    exit
) else if %errorlevel% == 3 (
    control sysdm.cpl,,4
    exit
) else if %errorlevel% == 4 (
    exit
)

pause
:: - Versions 1.0.4 -
:: - LastEditTime 2023/06/02 00:00 -
@echo off
chcp 65001 >nul 2>&1
%1 %2
ver|find "5.">nul&&goto :Admin
mshta vbscript:createobject("shell.application").shellexecute("%~s0","goto :Admin","","runas",1)(window.close)&goto :eof
:Admin

:menu
color BC

:: 檢查防火牆狀態
for /f "tokens=2 delims=: " %%i in ('netsh advfirewall show allprofiles state ^| find "State"') do set "firewall_status=%%i"
if "%firewall_status%"=="ON" (
    set "display=啟用"
) else (
    set "display=禁用"
)

cls

@ ECHO [1m
@ ECHO [94m======================================================================================================================
@ ECHO                                       - 工具箱 Versions 1.0.4 2023/06/02 -
@ ECHO ======================================================================================================================[91m
@ ECHO    Windows系統開關機 :    [1] 睡眠    [2] 重啟    [3] 關機
@ ECHO [92m-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -[91m
@ ECHO    Windows防火牆開關 :    [4] 開啟防火牆    [5] 關閉防火牆    [30m@防火牆當前狀態 : [95m[%display%][91m
@ ECHO [92m-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -[91m
@ ECHO    Surfshark服務操作 :    [6] 開啟服務 (Surfshark運行)    [7] 關閉服務 (Surfshark終止)
@ ECHO [92m-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -[91m
@ ECHO    瀏覽器操作 :            
@ ECHO.
@ ECHO    [8] Edge 啟用右上AI圖示    [9] Edge 關閉右上AI圖示    [10] Edge 一鍵設置優化    [11] Edge 修復受組織管理 (重置功能)
@ ECHO.
@ ECHO    [12] Edge 變更緩存位置     [13] Google 變更緩存位置    [14] Google 修復受機構管理 (重置功能)
@ ECHO [92m-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -[91m
@ ECHO    重置功能 :    [15] 網路重置    [16] Google重置    [17] Adobe結束背景    [18] AnLink結束背景    [19] R:/ 重置    
@ ECHO [92m-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -[91m
@ ECHO    授權功能 :    [20] RAR授權    [21] Windows 啟用授權    [22] Office 啟用授權
@ ECHO [97m----------------------------------------------------------------------------------------------------------------------
@ ECHO                                           - 系統指令操作 (不分大小寫) -
@ ECHO ----------------------------------------------------------------------------------------------------------------------[91m
@ ECHO    [CT] 控制台    [GP] 本機群組原則    [RD] 登入編輯程式    [UG] 使用者群組    [DX] DX診斷工具    [MF] 系統開機設置
@ ECHO.
@ ECHO    [WS] 電腦啟用狀態    [SI] 查詢系統資訊    [MSI] 查看完整系統資訊    [NV] 查詢顯卡驅動版本    [HW] 查詢電腦機器碼
@ ECHO.
@ ECHO    [IP] 查看電腦IP位置    [RS] 查看遠端分享    [MC] MAC地址查詢    [SV] 查看運行中的服務    [MRT] 惡意軟體移除工具    
@ ECHO.
@ ECHO    [WF] 搜尋電腦內已連接過的wifi    [DV] 修復驅動安裝問題    [SR] 系統修復            
@ ECHO.
@ ECHO [94m~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@ ECHO                                       [0] 離開程式             [H] 工具說明
@ ECHO ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[91m
@ ECHO.

:: ========================================================================================================================

set /p choice="選擇功能 - 輸入按下(Enter) : "

:: 選擇後清除
cls

:: ========================================================================================================================

if %choice% equ 0 (
    exit

) else if /I "%choice%"=="h" (
    call :Help&goto menu

) else if %choice% equ 1 (
    call :Sleep&goto menu

) else if %choice% equ 2 (
    call :Reboot&goto menu

) else if %choice% equ 3 (
    call :Shutdown&goto menu

) else if %choice% equ 4 (
    call :DE&goto menu

) else if %choice% equ 5 (
    call :DD&goto menu

) else if %choice% equ 6 (
    call :SE&goto menu

) else if %choice% equ 7 (
    call :SD&goto menu

) else if %choice% equ 8 (
    call :EdgeAIE&goto menu

) else if %choice% equ 9 (
    call :EdgeAID&goto menu

) else if %choice% equ 10 (
    call :EdgeOp&goto menu

) else if %choice% equ 11 (
    call :EdgeR&goto menu

) else if %choice% equ 12 (
    call :EdgeCC&goto menu

) else if %choice% equ 13 (
    call :GoogleCC&goto menu

) else if %choice% equ 14 (
    call :GoogleR&goto menu

) else if %choice% equ 15 (
    call :NR&goto menu

) else if %choice% equ 16 (
    call :GR&goto menu

) else if %choice% equ 17 (
    call :ADE&goto menu

) else if %choice% equ 18 (
    call :ALE&goto menu

) else if %choice% equ 19 (
    call :Rdisk&goto menu

) else if %choice% equ 20 (
    call :Authorization&goto menu

) else if %choice% equ 21 (
    call :windows&goto menu

) else if %choice% equ 22 (
    call :office&goto menu

) else if /I "%choice%"=="ct" (
    Control
    goto menu

) else if /I "%choice%"=="gp" (
    gpedit.msc
    goto menu

) else if /I "%choice%"=="rd" (
    regedit
    goto menu

) else if /I "%choice%"=="ug" (
    lusrmgr.msc
    goto menu

) else if /I "%choice%"=="dx" (
    dxdiag
    goto menu

) else if /I "%choice%"=="mf" (
    msconfig
    goto menu

) else if /I "%choice%"=="ws" (
    slmgr.vbs -xpr
    goto menu

) else if /I "%choice%"=="si" (
    ECHO 請稍後...
    systeminfo
    pause
    goto menu

) else if /I "%choice%"=="msi" (
    MSInfo32
    goto menu

) else if /I "%choice%"=="nv" (
    nvidia-smi
    pause
    goto menu

) else if /I "%choice%"=="hw" (
    call :Hwid&goto menu

) else if /I "%choice%"=="ip" (
    ipconfig /all
    pause
    goto menu

) else if /I "%choice%"=="rs" (
    net share
    pause
    goto menu

) else if /I "%choice%"=="mc" (
    getmac /fo table /v
    pause
    goto menu

) else if /I "%choice%"=="sv" (
    net start
    pause
    goto menu

) else if /I "%choice%"=="mrt" (
    mrt
    goto menu

) else if /I "%choice%"=="wf" (
    netsh wlan show profiles
    pause
    goto menu

) else if /I "%choice%"=="dv" (
    msdt.exe -id DeviceDiagnostic
    goto menu

) else if /I "%choice%"=="sr" (
    call :SystemRepair&goto menu

) else (
    echo 無效的選項
    timeout /t 2 >nul
    goto menu
)

:: ========================================================================================================================

:: ~~~~~ 電腦睡眠 ~~~~~
:Sleep

start rundll32.exe powrprof.dll,SetSuspendState 0,1,0 >nul

exit

:: ~~~~~ 電腦重啟 ~~~~~
:Reboot

shutdown /r /t 0 >nul

exit

:: ~~~~~ 電腦關機 ~~~~~
:Shutdown

shutdown /s /t 0 >nul

exit

:: ========================================================================================================================

:: ~~~~~ 啟用防火牆 ~~~~~
:DE

ECHO.
ECHO 防火牆 啟用中...
ECHO.

netsh advfirewall set allprofiles state on >nul

timeout /t 1 >nul

exit /b

:: ~~~~~ 禁用防火牆 ~~~~~
:DD

ECHO.
ECHO 防火牆 關閉中...
ECHO.

netsh advfirewall set allprofiles state off >nul

timeout /t 1 >nul

exit /b

:: ========================================================================================================================

:: ~~~~~ 啟動Surfshark ~~~~~
:SE

ECHO.
ECHO Surfshark 啟動中...
ECHO.

sc config "Surfshark Service" start= demand >nul
net start "Surfshark WireGuard" >nul
net start "Surfshark Service" >nul
start C:\"Program Files (x86)"\Surfshark\Surfshark.exe >nul

timeout /t 2 >nul

exit /b

:: ~~~~~ 關閉Surfshark ~~~~~
:SD

ECHO.
ECHO Surfshark 關閉中...
ECHO.

wmic process where name="Surfshark.exe" delete >nul
sc config "Surfshark Service" start= demand >nul
net stop "Surfshark WireGuard" >nul
net stop "Surfshark Service" >nul

timeout /t 2 >nul

exit /b

:: ========================================================================================================================

:: ~~~~~ 啟用edge AI圖示 ~~~~~
:EdgeAIE

reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Edge" /v "HubsSidebarEnabled" /t REG_DWORD /d 1 /f

ECHO.
ECHO 請自行重啟瀏覽器...
ECHO.

pause

exit /b

:: ~~~~~ 關閉edge AI圖示 ~~~~~
:EdgeAID

reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Edge" /v "HubsSidebarEnabled" /t REG_DWORD /d 0 /f

ECHO.
ECHO 請自行重啟瀏覽器...
ECHO.

pause

exit /b

:: ~~~~~ edge 一鍵功能優化 ~~~~~
:EdgeOp

reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Edge" /v "DiskCacheSize" /t REG_SZ /d "5000000000" /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Edge" /v "AccessibilityImageLabelsEnabled" /t REG_DWORD /d 1 /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Edge" /v "AllowDeletingBrowserHistory" /t REG_DWORD /d 1 /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Edge" /v "AlternateErrorPagesEnabled" /t REG_DWORD /d 1 /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Edge" /v "ApplicationGuardFavoritesSyncEnabled" /t REG_DWORD /d 1 /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Edge" /v "ApplicationGuardUploadBlockingEnabled" /t REG_DWORD /d 0 /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Edge" /v "AudioProcessHighPriorityEnabled" /t REG_DWORD /d 1 /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Edge" /v "AudioSandboxEnabled" /t REG_DWORD /d 1 /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Edge" /v "AutofillAddressEnabled" /t REG_DWORD /d 1 /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Edge" /v "AutofillCreditCardEnabled" /t REG_DWORD /d 1 /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Edge" /v "BackgroundModeEnabled" /t REG_DWORD /d 0 /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Edge" /v "BingAdsSuppression" /t REG_DWORD /d 1 /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Edge" /v "BuiltInDnsClientEnabled" /t REG_DWORD /d 1 /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Edge" /v "ConfigureDoNotTrack" /t REG_DWORD /d 1 /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Edge" /v "ConfigureOnlineTextToSpeech" /t REG_DWORD /d 1 /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Edge" /v "DeleteDataOnMigration" /t REG_DWORD /d 1 /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Edge" /v "EdgeEnhanceImagesEnabled" /t REG_DWORD /d 1 /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Edge" /v "EdgeWorkspacesEnabled" /t REG_DWORD /d 1 /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Edge" /v "EfficiencyModeEnabled" /t REG_DWORD /d 1 /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Edge" /v "FamilySafetySettingsEnabled" /t REG_DWORD /d 0 /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Edge" /v "HardwareAccelerationModeEnabled" /t REG_DWORD /d 1 /f

reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Edge" /v "ImmersiveReaderGrammarToolsEnabled" /t REG_DWORD /d 1 /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Edge" /v "ImmersiveReaderPictureDictionaryEnabled" /t REG_DWORD /d 1 /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Edge" /v "ImportAutofillFormData" /t REG_DWORD /d 1 /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Edge" /v "ImportBrowserSettings" /t REG_DWORD /d 1 /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Edge" /v "ImportCookies" /t REG_DWORD /d 1 /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Edge" /v "ImportExtensions" /t REG_DWORD /d 1 /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Edge" /v "ImportFavorites" /t REG_DWORD /d 1 /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Edge" /v "ImportHistory" /t REG_DWORD /d 1 /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Edge" /v "ImportHomepage" /t REG_DWORD /d 1 /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Edge" /v "ImportOpenTabs" /t REG_DWORD /d 1 /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Edge" /v "ImportPaymentInfo" /t REG_DWORD /d 1 /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Edge" /v "ImportSavedPasswords" /t REG_DWORD /d 1 /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Edge" /v "ImportSearchEngine" /t REG_DWORD /d 1 /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Edge" /v "ImportShortcuts" /t REG_DWORD /d 1 /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Edge" /v "ImportStartupPageSettings" /t REG_DWORD /d 1 /f

reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Edge" /v "InsecurePrivateNetworkRequestsAllowed" /t REG_DWORD /d 1 /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Edge" /v "NewTabPagePrerenderEnabled" /t REG_DWORD /d 1 /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Edge" /v "PasswordManagerRestrictLengthEnabled" /t REG_DWORD /d 1 /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Edge" /v "PasswordMonitorAllowed" /t REG_DWORD /d 1 /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Edge" /v "PreventSmartScreenPromptOverride" /t REG_DWORD /d 1 /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Edge" /v "PreventSmartScreenPromptOverrideForFiles" /t REG_DWORD /d 1 /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Edge" /v "QuicAllowed" /t REG_DWORD /d 1 /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Edge" /v "ShowMicrosoftRewards" /t REG_DWORD /d 0 /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Edge" /v "ShowPDFDefaultRecommendationsEnabled" /t REG_DWORD /d 0 /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Edge" /v "ShowRecommendationsEnabled" /t REG_DWORD /d 0 /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Edge" /v "SleepingTabsEnabled" /t REG_DWORD /d 1 /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Edge" /v "SmartScreenEnabled" /t REG_DWORD /d 0 /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Edge" /v "TaskManagerEndProcessEnabled" /t REG_DWORD /d 1 /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Edge" /v "WindowOcclusionEnabled" /t REG_DWORD /d 1 /f

ECHO.
ECHO 優化完成
ECHO.
ECHO 請自行重啟瀏覽器...
ECHO.

pause
exit /b

:: ~~~~~ 修復 edge 瀏覽器受管理 ~~~~~
:EdgeR

reg delete "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Edge" /f
reg delete "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\MicrosoftEdge" /f
reg delete "HKEY_CURRENT_USER\Software\Policies\Microsoft\Edge" /f
reg delete "HKEY_CURRENT_USER\Software\Policies\Microsoft\MicrosoftEdge" /f

ECHO.
ECHO 請自行重啟瀏覽器...
ECHO.

pause

exit /b

:: ~~~~~ edge 變更緩存位置 ~~~~~
:EdgeCC
setlocal

set "folderPath="
set "vbsScript=%temp%\folderSelection.vbs"

ECHO.
ECHO 這將會改變Edge的緩存位置
ECHO.
ECHO 請選擇要設置的路徑位置...
ECHO.
timeout /t 1 >nul

:: 選擇窗口(VBScript)
>"%vbsScript%" echo set shellApp = CreateObject("Shell.Application") : set folder = shellApp.BrowseForFolder(0, "Select path", 0, 64) : if not folder is nothing then WScript.Echo folder.Self.Path

for /f "delims=" %%I in ('cscript //nologo "%vbsScript%"') do set "folderPath=%%I"
del "%vbsScript%"

if defined folderPath (
    reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Edge" /v "DiskCacheDir" /t REG_SZ /d "%folderPath%EdgeCache" /f
    echo.
    echo 修改成功！緩存目錄已設置為："%folderPath%EdgeCache"
) else (
    echo 未選擇任何路徑，修改取消。
)

endlocal
timeout /t 2 >nul
exit /b

:: ~~~~~ google 變更緩存位置 ~~~~~
:GoogleCC
setlocal

set "folderPath="
set "vbsScript=%temp%\folderSelection.vbs"

ECHO.
ECHO 這將會改變Google的緩存位置
ECHO.
ECHO 請選擇要設置的路徑位置...
ECHO.
timeout /t 1 >nul

:: 選擇窗口(VBScript)
>"%vbsScript%" echo set shellApp = CreateObject("Shell.Application") : set folder = shellApp.BrowseForFolder(0, "Select path", 0, 64) : if not folder is nothing then WScript.Echo folder.Self.Path

for /f "delims=" %%I in ('cscript //nologo "%vbsScript%"') do set "folderPath=%%I"
del "%vbsScript%"

if defined folderPath (
    reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Google\Chrome" /v "DiskCacheDir" /t REG_SZ /d "%folderPath%GoogleCache" /f
    reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Google\Chrome" /v "DiskCacheSize" /t REG_SZ /d "5000000000" /f
    echo.
    echo 修改成功！緩存目錄已設置為："%folderPath%GoogleCache"
) else (
    echo 未選擇任何路徑，修改取消。
)

endlocal
timeout /t 2 >nul
exit /b

:: ~~~~~ 修復 Google 瀏覽器受管理 ~~~~~
:GoogleR

reg delete "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Google\Chrome" /f

ECHO.
ECHO 請自行重啟瀏覽器...
ECHO.

pause

exit /b

:: ========================================================================================================================

:: ~~~~~ 網路重置 ~~~~~
:NR

ECHO.
ECHO 網路重置中...
ECHO.

ipconfig /release >nul
ipconfig /flushdns >nul
netsh int ip reset >nul
netsh int tcp reset >nul
netsh winsock reset >nul
netsh advfirewall reset >nul
ipconfig /renew >nul

timeout /t 2 >nul

exit /b

:: ~~~~~ 網路重置 ~~~~~
:GR

ECHO.
ECHO Google重置中...
ECHO.

wmic process where name="chrome.exe" delete >nul

timeout /t 2 >nul

exit /b

:: ~~~~~ Adobe結束背景 ~~~~~
:ADE

ECHO.
ECHO Adobe結束背景...
ECHO.

wmic process where name="AdobeIPCBroker.exe" delete >nul
wmic process where name="CCLibrary.exe" delete >nul
wmic process where name="node.exe" delete >nul
wmic process where name="OfficeClickToRun.exe" delete >nul

timeout /t 2 >nul

exit /b

:: ~~~~~ AnLink結束背景 ~~~~~
:ALE

ECHO.
ECHO AnLink結束背景...
ECHO.

:loop

tasklist /fi "imagename eq ald.exe" | find /i "ald.exe" > nul
if %errorlevel% equ 0 (
    wmic process where name="ald.exe" delete >nul
    goto loop
)

tasklist /fi "imagename eq AnLink.exe" | find /i "AnLink.exe" > nul
if %errorlevel% equ 0 (
    wmic process where name="AnLink.exe" delete >nul
    goto loop
)

tasklist /fi "imagename eq dllhost.exe" | find /i "dllhost.exe" > nul
if %errorlevel% equ 0 (
    wmic process where name="dllhost.exe" delete >nul
    goto loop
)

tasklist /fi "imagename eq ApplicationFrameHost.exe" | find /i "ApplicationFrameHost.exe" > nul
if %errorlevel% equ 0 (
    wmic process where name="ApplicationFrameHost.exe" delete >nul
    goto loop
)

timeout /t 2 >nul

exit /b

:: ~~~~~ R盤重置 ~~~~~
:Rdisk

ECHO.
ECHO 開始重置...
ECHO.

RD /s /q R:\

timeout /t 1 >nul

exit /b

:: ~~~~~ RAR授權 ~~~~~
:Authorization

ECHO.
ECHO 授權中請稍後...
ECHO.

if not exist "C:\Program Files\WinRAR\Rarreg.key" (
    certutil -urlcache -split -f https://raw.githubusercontent.com/TenshinoOtoKafu/Implementation-Project/Main/Command%20Prompt/Rar/Rarreg.key Rarreg.key >nul
    move Rarreg.key "C:\Program Files\WinRAR" >nul
    ECHO 授權完成...
) else (
    ECHO 已存在授權...
)

timeout /t 2 >nul

exit /b

:: ~~~~~ windows啟用 ~~~~~
:windows

ECHO.
ECHO 獲取授權程式最新版本
ECHO.
ECHO 下載中請稍後...
ECHO.

:: 確保最新版本
certutil -urlcache -split -f https://raw.githubusercontent.com/massgravel/Microsoft-Activation-Scripts/master/MAS/All-In-One-Version/MAS_AIO.cmd MAS_AIO.cmd >nul
move MAS_AIO.cmd "%Temp%" >nul

ECHO 下載完成...
ECHO.
ECHO 啟動程式...

cd %Temp%
start MAS_AIO.cmd

timeout /t 2 >nul

exit /b

:: ~~~~~ office啟用 ~~~~~
:office

ECHO.
ECHO 獲取授權程式最新版本
ECHO.
ECHO 下載中請稍後...
ECHO.

certutil -urlcache -split -f https://raw.githubusercontent.com/abbodi1406/KMS_VL_ALL_AIO/master/KMS_VL_ALL_AIO.cmd KMS_VL_ALL_AIO.cmd >nul
move KMS_VL_ALL_AIO.cmd "%Temp%" >nul

ECHO 下載完成...
ECHO.
ECHO 啟動程式...

cd %Temp%
start KMS_VL_ALL_AIO.cmd

timeout /t 2 >nul

exit /b

:: ************************************************************************************************************************

:: ~~~~~ 查看機器碼 ~~~~~
:Hwid

Color 06

echo [92m===============================[93m
echo [91m        作業系統
echo [92m===============================[93m
wmic Os get caption

echo [95m===============================[93m
echo [91m      主機板資訊
echo [95m===============================[93m
wmic baseboard get product,manufacturer,serialnumber

echo [94m===============================[93m
echo [91m       CPU資訊
echo [94m===============================[93m
wmic cpu get name,processorid,serialnumber

echo [97m===============================[93m
echo [91m       硬碟資訊
echo [97m===============================[93m
wmic diskdrive get model,serialnumber,size

echo [95m===============================[93m
echo [91m       RAM資訊
echo [95m===============================[93m
wmic memorychip get PartNumber, SerialNumber,speed

echo [92m===============================[93m
echo [91m       GPU資訊
echo [92m===============================[93m
wmic Path win32_videocontroller get name,Description,PNPDeviceID

echo [96m===============================[93m
echo [91m       BIOS資訊
echo [96m===============================[93m
wmic bios get serialnumber,Manufacturer,Name

echo [92m===============================[93m
echo [91m       BIOS資訊 UUID
echo [92m===============================[93m
wmic csproduct get uuid

echo [97m===============================[93m
echo [91m       網路卡資訊
echo [97m===============================[93m 
wmic Nic get caption

getmac
ECHO 上面為MAC序號列

ECHO **********************************
ECHO       serialnumber為序號列
ECHO **********************************
ECHO.
pause

exit /b

:: ~~~~~ 系統修復 ~~~~~
:SystemRepair

color 02

ECHO.
ECHO 準備修復 請稍後...
ECHO.

Dism /Online /Cleanup-Image /ScanHealth
Dism /Online /Cleanup-Image /CheckHealth
DISM /Online /Cleanup-image /RestoreHealth
sfc /scannow

pause

exit /b

:: ========================================================================================================================

:: ~~~~~ 使用說明 ~~~~~
:Help

color 07

@ ECHO ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@ ECHO.
@ ECHO  - 使用說明:
@ ECHO.
@ ECHO 1. 請注意某些特別的設置(優化之類的) , 這是以本人的電腦製作的 , 不一定適用於所有人
@ ECHO.
@ ECHO 2. 需操作的程式 , 必須都安裝再預設的路徑上 , 才可成功運行
@ ECHO.
@ ECHO 3. 主要是自用的工具 , 除非有需要不然不會更新
@ ECHO.
@ ECHO 4. Window 和 Office 的啟用工具 , 是下載網路資源的 , 並非本人所寫 (有時候下載比較慢)
@ ECHO.
@ ECHO 5. 此程式是以個人使用為主去寫的 , 無考慮不同平台差異
@ ECHO.
@ ECHO ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
pause

exit /b
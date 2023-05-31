:: - Versions 1.0.0 -
:: 
:: [+] - 開關機操作
:: [+] - 防火牆開關
:: [+] - 自用工具組

@echo off
chcp 65001 >nul 2>&1
color BC
%1 %2
ver|find "5.">nul&&goto :Admin
mshta vbscript:createobject("shell.application").shellexecute("%~s0","goto :Admin","","runas",1)(window.close)&goto :eof
:Admin


:menu

:: 檢查防火牆狀態
for /f "tokens=2 delims=: " %%i in ('netsh advfirewall show allprofiles state ^| find "State"') do set "firewall_status=%%i"
if "%firewall_status%"=="ON" (
    set "display=啟用中"
) else (
    set "display=禁用中"
)

@ ECHO [1m
@ ECHO ======================================================================================================================
@ ECHO                                           - 自用工具組 Versions 1.0.0 -
@ ECHO ======================================================================================================================
@ ECHO.
@ ECHO -  Windows系統開關機 :    [1] 睡眠    [2] 重啟    [3] 關機
@ ECHO.
@ ECHO -  Windows防火牆開關 :    [4] 開啟防火牆    [5] 關閉防火牆    [30m@防火牆當前狀態 : [95m%display%[91m
@ ECHO.
@ ECHO -  Surfshark服務操作 :    [6] 開啟服務 (Surfshark運行)    [7] 關閉服務 (Surfshark終止)
@ ECHO.
@ ECHO -  特殊功能 :    [8] 網路重置    [9] Google重置    [10] Adobe結束背景    [11] AnLink結束背景
@ ECHO.
@ ECHO ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@ ECHO                                                    [0] 離開程式
@ ECHO ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@ ECHO.

:: ========================================================================================================================

set /p choice="選擇功能 - 輸入按下(Enter) : "

:: 選擇後清除
cls

:: ========================================================================================================================

if %choice% equ 0 (
    exit

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
    call :NR&goto menu

) else if %choice% equ 9 (
    call :GR&goto menu

) else if %choice% equ 10 (
    call :ADE&goto menu

) else if %choice% equ 11 (
    call :ALE&goto menu

)

:: ========================================================================================================================

:: ~~~~~ 電腦睡眠 ~~~~~
:Sleep

start rundll32.exe powrprof.dll,SetSuspendState 0,1,0

cls
exit

:: ~~~~~ 電腦重啟 ~~~~~
:Reboot

shutdown /r /t 0

cls
exit

:: ~~~~~ 電腦關機 ~~~~~
:Shutdown

shutdown /s /t 0

cls
exit

:: ========================================================================================================================

:: ~~~~~ 啟用防火牆 ~~~~~
:DE

ECHO.
ECHO 防火牆 啟用中...
ECHO.

netsh advfirewall set allprofiles state on >nul

timeout /t 1 >nul

cls
exit /b

:: ~~~~~ 禁用防火牆 ~~~~~
:DD

ECHO.
ECHO 防火牆 關閉中...
ECHO.

netsh advfirewall set allprofiles state off >nul

timeout /t 1 >nul

cls
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

cls
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

cls
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

cls
exit /b

:: ~~~~~ 網路重置 ~~~~~
:GR

ECHO.
ECHO Google重置中...
ECHO.

wmic process where name="chrome.exe" delete >nul

timeout /t 2 >nul

cls
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

cls
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

cls
exit /b
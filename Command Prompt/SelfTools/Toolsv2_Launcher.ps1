Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force # 給予臨時執行權限

Add-Type -AssemblyName System.Windows.Forms
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# 字串操作物件
$String = @{
    ToMD5 = {
        param (
            [string]$string,
            [int]$byte = 32
        )

        $MD5 = [System.Security.Cryptography.MD5]::Create()
        $fileBytes = [System.Text.Encoding]::UTF8.GetBytes($string)
        $hashBytes = $MD5.ComputeHash($fileBytes)
        $hashString = [BitConverter]::ToString($hashBytes) -replace '-'
        $lowerHash = $hashString.ToLower()

        return $lowerHash.Substring(0, [System.Math]::Min($byte, 32))
    };
    ToSHA = {
        param (
            [string]$string,
            [int]$byte = 64
        )

        $sha256 = [System.Security.Cryptography.SHA256]::Create()
        $fileBytes = [System.Text.Encoding]::UTF8.GetBytes($string)
        $hashBytes = $sha256.ComputeHash($fileBytes)
        $hashString = [BitConverter]::ToString($hashBytes) -replace '-'
        $lowerHash = $hashString.ToLower()

        return $lowerHash.Substring(0, [System.Math]::Min($byte, 64))
    }
}

function Print {
    param (
        [string]$text,
        [string]$foregroundColor = 'White',
        [string]$backgroundColor = 'Black'
    )
    $Host.UI.RawUI.ForegroundColor = [ConsoleColor]::$foregroundColor
    $Host.UI.RawUI.BackgroundColor = [ConsoleColor]::$backgroundColor
    Write-Host "[1m$text"
}

function CheckNetwork { # 檢查網路連接
    try {
        Test-Connection -ComputerName "www.google.com" -Count 1 -ErrorAction Stop
        return $true
    } catch {
        return $false
    }
}

function Request { # 請求數據
    param ([string]$url)
    try {
        $response = Invoke-WebRequest -Uri $url -ErrorAction Stop
        if ($response.StatusCode -eq 200) {
            return $response.Content
        } else {
            return "Request failed"
        }
    } catch {
        return "Update address to change"
    }
}

class ProcessingCore {
    [string]$path
    $aes = $null

    ProcessingCore([byte[]]$iv, [byte[]]$key, [string]$path) {
        $this.aes = [System.Security.Cryptography.Aes]::Create()
        $this.aes.IV = $iv
        $this.aes.Key = $key
        $this.path = $path
    }

    [string]Read() { # 讀取文件
        return Get-Content -Path $this.path -Raw
    }

    [void]OutputEncrypt([string]$content) { # 輸出加密文件
        Set-Content -Path $this.path -Value $this.Encrypt($content) -Encoding UTF8
    }

    [string]Encrypt([string]$plainText) { # AES 加密
        $encryptor = $this.aes.CreateEncryptor($this.aes.Key, $this.aes.IV)
        $plainTextBytes = [System.Text.Encoding]::UTF8.GetBytes($plainText)
        $encryptedBytes = $encryptor.TransformFinalBlock($plainTextBytes, 0, $plainTextBytes.Length)
        return [Convert]::ToBase64String($encryptedBytes)
    }

    [string]Decrypt([string]$cipherText) { # AES 解密
        $decryptor = $this.aes.CreateDecryptor($this.aes.Key, $this.aes.IV)
        $cipherTextBytes = [Convert]::FromBase64String($cipherText)
        $decryptedBytes = $decryptor.TransformFinalBlock($cipherTextBytes, 0, $cipherTextBytes.Length)
        return [System.Text.Encoding]::UTF8.GetString($decryptedBytes)
    }

    [string]GetDecrypt() { # 獲取解密字串
        return $this.Decrypt($this.Read())
    }

    [string]OutputAndGet([string]$content) { # 輸出並回傳加密結果
        $this.OutputEncrypt($content)
        if (Test-Path $this.path) {
            return $this.GetDecrypt()
        } else {
            return $null
        }
    }

    [void]InvokeCode([string]$code) { # 運行解密字串
        try {
            Invoke-Expression -Command $code
        } catch {
            Print "解碼運行錯誤" "Red"
            Read-Host "[1mEnter 退出程式..."
        }
    }
}

<# ============== #>

Print "======== 檢查更新中 ========" "Yellow"

# 取得使用者電腦資訊
$BiosInfo = Get-WmiObject -Class Win32_BIOS | Select-Object -Property SerialNumber
$BaseBoard = Get-WmiObject -Class Win32_BaseBoard | Select-Object -Property Product, SerialNumber
$UserInfo = Get-WmiObject -Class Win32_ComputerSystem | Select-Object -Property PrimaryOwnerName, Name

# 已使用者的電腦資訊計算 MD5 後, 分別取前半和後半作為 key,iv
$InfoHash = &($String.ToMD5) "$($UserInfo.PrimaryOwnerName)$($UserInfo.Name)$($BiosInfo.SerialNumber)$($BaseBoard.Product)$($BaseBoard.SerialNumber)"
$KeyHash = $InfoHash.Substring(0, 16)
$IvHash = $InfoHash.Substring(16, 16)

# 使用者資訊的哈希值, 合併成 保存目錄路徑
$LocalFile = "$env:Temp\$InfoHash"
$FileExists = {return Test-Path $LocalFile}
$DownloadURL = "https://raw.githubusercontent.com/Canaan-HS/Implementation-Project/Main/Command%20Prompt/SelfTools/Toolsv2.ps1"

# 處理核心 實例化
$Core = [ProcessingCore]::new(
    [System.Text.Encoding]::UTF8.GetBytes($IvHash), # 生成加密用 key, iv
    [System.Text.Encoding]::UTF8.GetBytes($KeyHash),
    $LocalFile
)

if (-not (CheckNetwork)) { # 沒有網路
    $Message = [System.Windows.Forms.MessageBox]::Show(
        "無法獲取更新, 是否嘗試啟動本地文件",
        "沒有網路",
        [System.Windows.Forms.MessageBoxButtons]::OKCancel,
        [System.Windows.Forms.MessageBoxIcon]::Information
    )
    if ($Message -eq "Cancel") {exit}

    if (& $FileExists) { # 有本地文件 => 解碼運行
        $Core.InvokeCode($Core.GetDecrypt())
    } else {
        $Message = [System.Windows.Forms.MessageBox]::Show(
            "本地無啟動文件",
            "找不到文件",
            [System.Windows.Forms.MessageBoxButtons]::OK,
            [System.Windows.Forms.MessageBoxIcon]::Error
        )
    }
} else { # 有網路
    $codeString = $null
    $remoteString = $null

    foreach ($_ in 1..5) {
        $remoteString = Request $DownloadURL
        if ($remoteString -eq "Request failed") {
            Print "請求失敗 重試 =>" "Green"
            continue
        } elseif ($remoteString -eq "Update address to change") {
            $Message = [System.Windows.Forms.MessageBox]::Show(
                "更新地址已變更嘗試已本地文件開啟",
                "地址已變更",
                [System.Windows.Forms.MessageBoxButtons]::OK,
                [System.Windows.Forms.MessageBoxIcon]::Warning
            )
            $remoteString = $null # 將狀態修改回去
            break
        } elseif ($null -ne $remoteString) { # 請求成功
            break
        }
    }

    $remoteStringValid = $null -ne $remoteString # 檢查遠端狀態

    if ((& $FileExists) -and $remoteStringValid) { # 有本地文件, 且有遠端數據
        $RemoteHash = &($String.ToSHA) $remoteString # 遠端哈希值
        $codeString = $Core.GetDecrypt() # 獲取本地代碼字串
        $LocalHash = &($String.ToSHA) $codeString # 本地哈希值

        Print "本地版本: $LocalHash" "Green"
        Print "雲端版本: $RemoteHash" "Green"

        if (-not($RemoteHash -eq $LocalHash)) { # 哈希值不同 (需要更新)
            $codeString = $Core.OutputAndGet($remoteString) # 輸出加密 並獲取結果
        }
    } elseif (-not((& $FileExists)) -and $remoteStringValid) { # 沒有本地文件, 但有遠端數據
        $codeString = $Core.OutputAndGet($remoteString) # 輸出加密 並獲取結果
    } elseif ((& $FileExists) -and -not $remoteStringValid) { # 只有本地文件
        $codeString = $Core.GetDecrypt()
    } else {
        $Message = [System.Windows.Forms.MessageBox]::Show(
            "本地無啟動文件",
            "找不到文件",
            [System.Windows.Forms.MessageBoxButtons]::OK,
            [System.Windows.Forms.MessageBoxIcon]::Error
        )
        exit
    }
    $Core.InvokeCode($codeString) # 運行代碼
}
# EasyWorship to ProPresenter Converter Installation Script
# Version: 1.0.0
# This script automates the installation of ewexport on Windows 11

param(
    [string]$InstallPath = "$env:LOCALAPPDATA\EWExport",
    [switch]$Silent = $false,
    [switch]$NoDesktopShortcut = $false
)

$ErrorActionPreference = "Stop"
$ProgressPreference = 'SilentlyContinue'

# Configuration
$GITHUB_REPO = "karllinder/ewexport"
$PYTHON_VERSION = "3.11.9"
$PYTHON_URL = "https://www.python.org/ftp/python/$PYTHON_VERSION/python-$PYTHON_VERSION-amd64.exe"
$APP_NAME = "EWExport"
$APP_DISPLAY_NAME = "EasyWorship to ProPresenter Converter"

# Colors for output
function Write-ColorOutput {
    param([string]$Message, [string]$Color = "White")
    Write-Host $Message -ForegroundColor $Color
}

function Write-Step {
    param([string]$Message)
    Write-ColorOutput "`n[*] $Message" "Cyan"
}

function Write-Success {
    param([string]$Message)
    Write-ColorOutput "[+] $Message" "Green"
}

function Write-Error {
    param([string]$Message)
    Write-ColorOutput "[!] $Message" "Red"
}

function Write-Info {
    param([string]$Message)
    Write-ColorOutput "[i] $Message" "Yellow"
}

# Banner
if (-not $Silent) {
    Write-ColorOutput @"

===========================================================
    EasyWorship to ProPresenter Converter Installer
===========================================================
"@ "Magenta"
}

# Check for admin rights (not required but recommended)
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Info "Running without administrator privileges. Some features may be limited."
}

# Function to check if Python is installed
function Test-PythonInstalled {
    try {
        $pythonVersion = python --version 2>&1
        if ($pythonVersion -match "Python (\d+)\.(\d+)") {
            $major = [int]$Matches[1]
            $minor = [int]$Matches[2]
            if ($major -eq 3 -and $minor -ge 11) {
                return $true
            }
        }
    } catch {
        return $false
    }
    return $false
}

# Function to get latest release from GitHub
function Get-LatestRelease {
    Write-Step "Checking for latest release..."
    try {
        $apiUrl = "https://api.github.com/repos/$GITHUB_REPO/releases/latest"
        $release = Invoke-RestMethod -Uri $apiUrl -Headers @{
            "User-Agent" = "PowerShell"
        }
        
        # Find the exe asset
        $exeAsset = $release.assets | Where-Object { $_.name -like "*.exe" } | Select-Object -First 1
        
        if ($exeAsset) {
            Write-Success "Found latest release: $($release.tag_name)"
            return @{
                Version = $release.tag_name
                DownloadUrl = $exeAsset.browser_download_url
                FileName = $exeAsset.name
            }
        } else {
            # Fallback to source code if no exe found
            Write-Info "No pre-built executable found. Will install from source."
            return @{
                Version = $release.tag_name
                SourceCode = $true
                DownloadUrl = $release.zipball_url
            }
        }
    } catch {
        Write-Error "Failed to get latest release: $_"
        throw
    }
}

# Function to install Python
function Install-Python {
    if (Test-PythonInstalled) {
        Write-Success "Python 3.11+ is already installed"
        return $true
    }

    Write-Step "Installing Python $PYTHON_VERSION..."
    
    $tempPath = "$env:TEMP\python_installer.exe"
    
    try {
        Write-Info "Downloading Python installer..."
        Invoke-WebRequest -Uri $PYTHON_URL -OutFile $tempPath
        
        Write-Info "Running Python installer (this may take a few minutes)..."
        $installArgs = @(
            "/quiet",
            "InstallAllUsers=0",
            "PrependPath=1",
            "Include_test=0",
            "Include_doc=0"
        )
        
        Start-Process -FilePath $tempPath -ArgumentList $installArgs -Wait -NoNewWindow
        
        # Refresh PATH
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")
        
        if (Test-PythonInstalled) {
            Write-Success "Python installed successfully"
            Remove-Item $tempPath -Force -ErrorAction SilentlyContinue
            return $true
        } else {
            throw "Python installation verification failed"
        }
    } catch {
        Write-Error "Failed to install Python: $_"
        return $false
    }
}

# Function to install the application
function Install-Application {
    param($ReleaseInfo)
    
    Write-Step "Installing $APP_DISPLAY_NAME..."
    
    # Create installation directory
    if (-not (Test-Path $InstallPath)) {
        New-Item -ItemType Directory -Path $InstallPath -Force | Out-Null
        Write-Success "Created installation directory: $InstallPath"
    }
    
    if ($ReleaseInfo.SourceCode) {
        # Install from source
        Write-Info "Installing from source code..."
        
        $tempZip = "$env:TEMP\ewexport_source.zip"
        $tempExtract = "$env:TEMP\ewexport_source"
        
        try {
            # Download source
            Invoke-WebRequest -Uri $ReleaseInfo.DownloadUrl -OutFile $tempZip
            
            # Extract
            Expand-Archive -Path $tempZip -DestinationPath $tempExtract -Force
            
            # Find the extracted folder (GitHub creates a subfolder)
            $sourceFolder = Get-ChildItem -Path $tempExtract -Directory | Select-Object -First 1
            
            # Copy source files to installation directory
            Copy-Item -Path "$($sourceFolder.FullName)\*" -Destination $InstallPath -Recurse -Force
            
            # Install Python dependencies
            Write-Info "Installing Python dependencies..."
            Push-Location $InstallPath
            python -m pip install --upgrade pip | Out-Null
            python -m pip install striprtf | Out-Null
            python -m pip install pyinstaller | Out-Null
            Pop-Location
            
            # Create batch file to run the application
            $batchContent = @"
@echo off
cd /d "$InstallPath"
python src\main.py %*
"@
            Set-Content -Path "$InstallPath\$APP_NAME.bat" -Value $batchContent
            
            Write-Success "Application installed from source"
            
            # Cleanup
            Remove-Item $tempZip -Force -ErrorAction SilentlyContinue
            Remove-Item $tempExtract -Recurse -Force -ErrorAction SilentlyContinue
            
        } catch {
            Write-Error "Failed to install from source: $_"
            throw
        }
        
    } else {
        # Install pre-built executable
        Write-Info "Downloading pre-built executable..."
        
        $exePath = Join-Path $InstallPath $ReleaseInfo.FileName
        
        try {
            Invoke-WebRequest -Uri $ReleaseInfo.DownloadUrl -OutFile $exePath
            Write-Success "Application downloaded successfully"
        } catch {
            Write-Error "Failed to download application: $_"
            throw
        }
    }
    
    # Save version information
    $versionFile = Join-Path $InstallPath "version.txt"
    Set-Content -Path $versionFile -Value $ReleaseInfo.Version
}

# Function to create desktop shortcut
function New-DesktopShortcut {
    if ($NoDesktopShortcut) {
        Write-Info "Skipping desktop shortcut creation (--NoDesktopShortcut specified)"
        return
    }
    
    Write-Step "Creating desktop shortcut..."
    
    $desktopPath = [Environment]::GetFolderPath("Desktop")
    $shortcutPath = Join-Path $desktopPath "$APP_DISPLAY_NAME.lnk"
    
    # Determine target based on installation type
    $exePath = Get-ChildItem -Path $InstallPath -Filter "*.exe" | Select-Object -First 1
    if ($exePath) {
        $targetPath = $exePath.FullName
    } else {
        $targetPath = Join-Path $InstallPath "$APP_NAME.bat"
    }
    
    if (-not (Test-Path $targetPath)) {
        Write-Error "Could not find application executable"
        return
    }
    
    try {
        $WshShell = New-Object -ComObject WScript.Shell
        $Shortcut = $WshShell.CreateShortcut($shortcutPath)
        $Shortcut.TargetPath = $targetPath
        $Shortcut.WorkingDirectory = $InstallPath
        $Shortcut.Description = $APP_DISPLAY_NAME
        $Shortcut.Save()
        
        Write-Success "Desktop shortcut created"
    } catch {
        Write-Error "Failed to create desktop shortcut: $_"
    }
}

# Function to add to PATH
function Add-ToPath {
    if (-not $isAdmin) {
        Write-Info "Cannot add to system PATH without admin rights. Add manually if needed."
        return
    }
    
    Write-Step "Adding to PATH..."
    
    try {
        $currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
        if ($currentPath -notlike "*$InstallPath*") {
            [Environment]::SetEnvironmentVariable("Path", "$currentPath;$InstallPath", "User")
            $env:Path = "$env:Path;$InstallPath"
            Write-Success "Added to PATH"
        } else {
            Write-Info "Already in PATH"
        }
    } catch {
        Write-Error "Failed to add to PATH: $_"
    }
}

# Main installation process
try {
    # Step 1: Check/Install Python
    if ($ReleaseInfo.SourceCode) {
        if (-not (Install-Python)) {
            throw "Python installation is required for source installation"
        }
    }
    
    # Step 2: Get latest release
    $releaseInfo = Get-LatestRelease
    
    # Step 3: Install application
    Install-Application -ReleaseInfo $releaseInfo
    
    # Step 4: Create desktop shortcut
    New-DesktopShortcut
    
    # Step 5: Add to PATH
    Add-ToPath
    
    # Success message
    Write-ColorOutput @"

===========================================================
    Installation Complete!
===========================================================

$APP_DISPLAY_NAME has been successfully installed.

Installation location: $InstallPath
Version: $($releaseInfo.Version)

You can now:
1. Use the desktop shortcut to launch the application
2. Run '$APP_NAME' from the command line (if added to PATH)

For documentation and support, visit:
https://github.com/$GITHUB_REPO

"@ "Green"
    
} catch {
    Write-ColorOutput @"

===========================================================
    Installation Failed
===========================================================

An error occurred during installation:
$_

Please report this issue at:
https://github.com/$GITHUB_REPO/issues

"@ "Red"
    
    exit 1
}
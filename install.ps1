# EasyWorship to ProPresenter Converter - Simple Installer
# Version: 2.0.0
# Downloads and installs the ewexport.exe standalone executable

param(
    [string]$InstallPath = "$env:LOCALAPPDATA\EWExport",
    [switch]$NoDesktopShortcut = $false,
    [switch]$Silent = $false
)

$ErrorActionPreference = "Stop"
$ProgressPreference = 'SilentlyContinue'

# Configuration
$GITHUB_REPO = "karllinder/ewexport"
$APP_NAME = "ewexport"
$APP_DISPLAY_NAME = "EasyWorship to ProPresenter Converter"

# Colors for output
function Write-ColorOutput {
    param([string]$Message, [string]$Color = "White")
    if (-not $Silent) {
        Write-Host $Message -ForegroundColor $Color
    }
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
    Simplified Standalone Version
===========================================================
"@ "Magenta"
}

# Function to get latest release from GitHub
function Get-LatestRelease {
    Write-Step "Checking for latest release..."
    try {
        $apiUrl = "https://api.github.com/repos/$GITHUB_REPO/releases/latest"
        $release = Invoke-RestMethod -Uri $apiUrl -Headers @{
            "User-Agent" = "PowerShell-Installer"
        }
        
        # Find the exe asset
        $exeAsset = $release.assets | Where-Object { $_.name -eq "ewexport.exe" } | Select-Object -First 1
        
        if ($exeAsset) {
            Write-Success "Found latest release: $($release.tag_name)"
            return @{
                Version = $release.tag_name
                DownloadUrl = $exeAsset.browser_download_url
                FileName = $exeAsset.name
                Size = [math]::Round($exeAsset.size / 1MB, 2)
            }
        } else {
            throw "No executable found in the latest release"
        }
    } catch {
        Write-Error "Failed to get latest release: $_"
        throw
    }
}

# Function to download the executable
function Install-Application {
    param($ReleaseInfo)
    
    Write-Step "Installing $APP_DISPLAY_NAME..."
    Write-Info "Version: $($ReleaseInfo.Version)"
    Write-Info "Size: $($ReleaseInfo.Size) MB"
    
    # Create installation directory
    if (-not (Test-Path $InstallPath)) {
        New-Item -ItemType Directory -Path $InstallPath -Force | Out-Null
        Write-Success "Created installation directory: $InstallPath"
    }
    
    $exePath = Join-Path $InstallPath $ReleaseInfo.FileName
    
    # Check if already installed
    $shouldDownload = $true
    if (Test-Path $exePath) {
        Write-Info "Existing installation found"
        if (-not $Silent) {
            $response = Read-Host "Overwrite existing installation? (Y/N)"
            $shouldDownload = $response -eq 'Y' -or $response -eq 'y'
        }
    }
    
    if ($shouldDownload) {
        Write-Info "Downloading executable..."
        try {
            # Download with progress
            $webClient = New-Object System.Net.WebClient
            $webClient.DownloadFile($ReleaseInfo.DownloadUrl, $exePath)
            Write-Success "Downloaded successfully to: $exePath"
        } catch {
            Write-Error "Failed to download: $_"
            throw
        }
    } else {
        Write-Info "Installation skipped"
    }
    
    # Save version information
    $versionFile = Join-Path $InstallPath "version.txt"
    Set-Content -Path $versionFile -Value $ReleaseInfo.Version
    
    return $exePath
}

# Function to create desktop shortcut
function New-DesktopShortcut {
    param([string]$ExePath)
    
    if ($NoDesktopShortcut) {
        Write-Info "Skipping desktop shortcut creation"
        return
    }
    
    Write-Step "Creating desktop shortcut..."
    
    $desktopPath = [Environment]::GetFolderPath("Desktop")
    $shortcutPath = Join-Path $desktopPath "$APP_DISPLAY_NAME.lnk"
    
    try {
        $WshShell = New-Object -ComObject WScript.Shell
        $Shortcut = $WshShell.CreateShortcut($shortcutPath)
        $Shortcut.TargetPath = $ExePath
        $Shortcut.WorkingDirectory = $InstallPath
        $Shortcut.Description = $APP_DISPLAY_NAME
        $Shortcut.Save()
        
        Write-Success "Desktop shortcut created"
    } catch {
        Write-Error "Failed to create desktop shortcut: $_"
    }
}

# Function to create Start Menu shortcut
function New-StartMenuShortcut {
    param([string]$ExePath)
    
    Write-Step "Creating Start Menu shortcut..."
    
    $startMenuPath = [Environment]::GetFolderPath("Programs")
    $shortcutPath = Join-Path $startMenuPath "$APP_DISPLAY_NAME.lnk"
    
    try {
        $WshShell = New-Object -ComObject WScript.Shell
        $Shortcut = $WshShell.CreateShortcut($shortcutPath)
        $Shortcut.TargetPath = $ExePath
        $Shortcut.WorkingDirectory = $InstallPath
        $Shortcut.Description = $APP_DISPLAY_NAME
        $Shortcut.Save()
        
        Write-Success "Start Menu shortcut created"
    } catch {
        Write-Info "Could not create Start Menu shortcut: $_"
    }
}

# Main installation process
try {
    # Get latest release information
    $releaseInfo = Get-LatestRelease
    
    # Download and install the executable
    $installedExe = Install-Application -ReleaseInfo $releaseInfo
    
    # Create shortcuts
    New-DesktopShortcut -ExePath $installedExe
    New-StartMenuShortcut -ExePath $installedExe
    
    # Success message
    Write-ColorOutput @"

===========================================================
    Installation Complete!
===========================================================

$APP_DISPLAY_NAME has been successfully installed.

Installation location: $InstallPath
Version: $($releaseInfo.Version)
Executable: $installedExe

The application is completely standalone and includes
all required dependencies. No Python installation needed!

You can now:
1. Use the desktop shortcut to launch the application
2. Run the executable directly from: $installedExe
3. Find it in your Start Menu

For documentation and support, visit:
https://github.com/$GITHUB_REPO

"@ "Green"
    
    # Offer to run the application
    if (-not $Silent) {
        $runNow = Read-Host "Would you like to run the application now? (Y/N)"
        if ($runNow -eq 'Y' -or $runNow -eq 'y') {
            Write-Info "Starting $APP_DISPLAY_NAME..."
            Start-Process $installedExe
        }
    }
    
} catch {
    Write-ColorOutput @"

===========================================================
    Installation Failed
===========================================================

An error occurred during installation:
$_

Please try:
1. Download the executable manually from:
   https://github.com/$GITHUB_REPO/releases/latest
   
2. Save it to your preferred location

3. Run it directly - no installation required!

"@ "Red"
    
    exit 1
}
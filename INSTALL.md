# Installation Guide - EasyWorship to ProPresenter Converter

## Quick Installation (Recommended)

### Option 1: Direct Download (Simplest)

1. Visit the [Latest Release](https://github.com/karllinder/ewexport/releases/latest) page
2. Download `ewexport.exe` from the Assets section
3. Save it anywhere you like (e.g., Desktop or Documents)
4. Double-click to run - **that's it!**

The executable is completely standalone and includes everything needed. No Python or other dependencies required!

### Option 2: Automated Installation Script

For automated download and shortcut creation:

1. **Download the installer script**:
   ```powershell
   curl -L https://raw.githubusercontent.com/karllinder/ewexport/main/install.ps1 -o install.ps1
   ```

2. **Review the script** (optional but recommended for security):
   ```powershell
   notepad install.ps1
   ```

3. **Run the installer**:
   ```powershell
   powershell -ExecutionPolicy Bypass -File install.ps1
   ```

The installer will:
- Download the latest ewexport.exe from GitHub
- Create desktop and Start Menu shortcuts
- Save the executable to `%LOCALAPPDATA%\EWExport`
- Offer to run the application immediately

### Installation Options

The installation script supports several options:

```powershell
# Custom installation path
powershell -ExecutionPolicy Bypass -File install.ps1 -InstallPath "D:\Apps\EWExport"

# Silent installation (no prompts)
powershell -ExecutionPolicy Bypass -File install.ps1 -Silent

# Skip desktop shortcut creation
powershell -ExecutionPolicy Bypass -File install.ps1 -NoDesktopShortcut
```

## The Standalone Executable

The `ewexport.exe` is a completely self-contained application that:
- **Includes Python runtime** - No Python installation needed
- **Contains all dependencies** - striprtf, packaging, etc. all bundled
- **Creates its own configuration** - Automatically sets up folders on first run
- **Manages settings** - Stores preferences in `%APPDATA%\EWExport`
- **Is portable** - Can run from any location (USB drive, network share, etc.)

## Manual Installation from Source (For Developers)

### Prerequisites

- Windows 10/11
- Python 3.11 or higher
- Git (optional, for cloning repository)

### Steps

1. **Install Python** (if not already installed):
   - Download from [python.org](https://www.python.org/downloads/)
   - During installation, check "Add Python to PATH"

2. **Download or clone the repository**:
   ```bash
   git clone https://github.com/karllinder/ewexport.git
   cd ewexport
   ```
   
   Or download and extract the ZIP file from GitHub

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python src/main.py
   ```

## Building from Source

To create your own executable:

1. **Install PyInstaller**:
   ```bash
   pip install pyinstaller
   ```

2. **Build the executable**:
   ```bash
   pyinstaller --onefile --windowed --name ewexport src/main.py
   ```

3. The executable will be created in the `dist` folder

## System Requirements

- **Operating System**: Windows 10 or Windows 11
- **Memory**: 512 MB RAM minimum
- **Disk Space**: 50 MB for executable + space for exported files
- **Database**: EasyWorship 6.1 or higher database files
- **No Python Required**: The executable includes everything needed

## Troubleshooting

### PowerShell Execution Policy Error

If you get an execution policy error, you have two options:

1. **Run with bypass** (recommended):
   ```powershell
   powershell -ExecutionPolicy Bypass -File install.ps1
   ```

2. **Change execution policy** (requires admin):
   ```powershell
   Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

### Download Failed

If the installer can't download the executable:
1. Check your internet connection
2. Try downloading manually from [GitHub Releases](https://github.com/karllinder/ewexport/releases/latest)
3. Your firewall or antivirus might be blocking the download

### Missing Dependencies

If you get import errors when running from source:
```bash
pip install --upgrade striprtf packaging
```

### Antivirus Warnings

Some antivirus software may flag the executable. This is a false positive common with PyInstaller executables. You can:
1. Add an exception for ewexport.exe
2. Check the file on [VirusTotal](https://www.virustotal.com) for peace of mind
3. Build your own executable from source if preferred

## Updating

### Automatic Update Check

The application automatically checks for updates on startup (can be disabled in settings). When an update is available:

1. Click "Download Update" in the notification
2. Download the new version from the GitHub releases page
3. Replace your existing executable with the new one

### Manual Update Check

Go to **Help → Check for Updates** in the application menu

## Uninstallation

### For Executable Version

Simply delete:
1. The ewexport.exe file
2. The desktop shortcut (if created)
3. The settings folder: `%APPDATA%\EWExport`

### For Source Installation

1. Delete the ewexport folder
2. Remove the desktop shortcut (if created)
3. Delete the settings folder: `%APPDATA%\EWExport`

## Configuration Files

Application settings and logs are stored in:
- Windows: `%APPDATA%\EWExport\`
- Contains: `settings.ini`, `section_mappings.json`, and log files

## Need Help?

- Check the [README](README.md) for usage instructions
- View [CLAUDE.md](CLAUDE.md) for technical documentation
- Report issues on [GitHub Issues](https://github.com/karllinder/ewexport/issues)
- Check [Releases](https://github.com/karllinder/ewexport/releases) for version history

## License

This software is provided under the license specified in the repository. See LICENSE file for details.
@echo off
REM Build script for creating ewexport.exe on Windows
REM This is a simple wrapper around build.py

echo ========================================
echo EWExport Windows Build Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Check if PyInstaller is installed
pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo PyInstaller not found. Installing...
    pip install pyinstaller
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install PyInstaller
        pause
        exit /b 1
    )
)

REM Run the build script
echo Starting build process...
python build.py

REM Check if build was successful
if %errorlevel% equ 0 (
    echo.
    echo Build completed successfully!
    echo Executable is in: dist\ewexport.exe
    echo.
    echo Press any key to open the dist folder...
    pause >nul
    explorer dist
) else (
    echo.
    echo Build failed! Check the error messages above.
    pause
)
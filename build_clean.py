"""
Clean build script optimized to reduce antivirus false positives
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def clean_environment():
    """Clean build environment thoroughly"""
    print("Cleaning build environment...")
    
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"  Removing {dir_name}...")
            try:
                shutil.rmtree(dir_name)
            except PermissionError as e:
                print(f"  Warning: Could not clean {dir_name}: {e}")
    
    # Clean spec files
    for spec_file in ['ewexport.spec', 'ewexport_clean.spec']:
        if os.path.exists(spec_file) and spec_file != 'ewexport_clean.spec':
            os.remove(spec_file)
            print(f"  Removed {spec_file}")

def build_with_spec():
    """Build using the clean spec file"""
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    spec_file = 'ewexport_clean.spec'
    if not Path(spec_file).exists():
        print(f"ERROR: {spec_file} not found!")
        return False
    
    print(f"Building with clean spec file: {spec_file}")
    
    try:
        # Use the spec file directly
        result = subprocess.run([
            'pyinstaller', 
            '--clean',
            '--noconfirm', 
            spec_file
        ], check=True, capture_output=True, text=True)
        
        print("Build completed successfully!")
        
        # Check if exe was created
        exe_path = Path('dist/ewexport.exe')
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"Executable created: {exe_path}")
            print(f"Size: {size_mb:.2f} MB")
            
            # Calculate file hash for verification
            import hashlib
            with open(exe_path, 'rb') as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()
            print(f"SHA256: {file_hash}")
            
            return True
        else:
            print("ERROR: Executable not found after build!")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
        return False
    except FileNotFoundError:
        print("ERROR: PyInstaller not found. Install it with: pip install pyinstaller")
        return False

def verify_clean_build():
    """Verify the build is clean"""
    exe_path = Path('dist/ewexport.exe')
    if not exe_path.exists():
        return False
    
    print("\nBuild verification:")
    print(f"File size: {exe_path.stat().st_size / (1024 * 1024):.2f} MB")
    
    # Check if UPX was used (should be avoided)
    try:
        result = subprocess.run(['strings', str(exe_path)], 
                              capture_output=True, text=True, timeout=10)
        if 'UPX' in result.stdout:
            print("WARNING: UPX compression detected (may trigger antivirus)")
        else:
            print("Good: No UPX compression detected")
    except:
        print("Could not verify UPX usage")
    
    return True

def main():
    print("=" * 60)
    print("EWExport Clean Build Script")
    print("Optimized to reduce antivirus false positives")
    print("=" * 60)
    
    # Clean environment first
    clean_environment()
    
    # Build with clean spec
    if build_with_spec():
        if verify_clean_build():
            print("\n" + "=" * 60)
            print("CLEAN BUILD SUCCESSFUL!")
            print("\nAntivirus optimization features:")
            print("[+] Windows version information added")
            print("[+] UPX compression disabled")
            print("[+] Unnecessary modules excluded")
            print("[+] Clean build environment")
            print("[+] No admin privileges requested")
            print("\nNext steps:")
            print("1. Test the executable on your system")
            print("2. Submit to VirusTotal for reputation building")
            print("3. Report false positives to Microsoft")
            print("=" * 60)
        else:
            print("Build verification failed")
    else:
        print("Build failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
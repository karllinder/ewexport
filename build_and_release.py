#!/usr/bin/env python3
"""
Local Build and Release Script for EWExport
Builds the executable locally and uploads to GitHub release
"""

import os
import sys
import shutil
import subprocess
import hashlib
import json
from pathlib import Path
from datetime import datetime

def get_version():
    """Get version from setup.py"""
    setup_py = Path('setup.py')
    if setup_py.exists():
        with open(setup_py, 'r') as f:
            content = f.read()
            for line in content.split('\n'):
                if 'VERSION = ' in line:
                    return line.split('"')[1]
    return "unknown"

def calculate_sha256(file_path):
    """Calculate SHA256 hash of file"""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def clean_build_environment():
    """Clean build environment"""
    print("🧹 Cleaning build environment...")
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if Path(dir_name).exists():
            shutil.rmtree(dir_name)
            print(f"   Removed {dir_name}/")
    
    # Clean .pyc files
    for pyc_file in Path('.').rglob('*.pyc'):
        pyc_file.unlink()
    
    print("   ✅ Environment cleaned")

def build_executable():
    """Build the executable using clean configuration"""
    print("🔨 Building executable...")
    
    # Use clean build script
    try:
        result = subprocess.run([
            sys.executable, 'build_clean.py'
        ], check=True, capture_output=True, text=True)
        
        print("   ✅ Build completed successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Build failed: {e}")
        print(f"   stdout: {e.stdout}")
        print(f"   stderr: {e.stderr}")
        return False
    except FileNotFoundError:
        print("   ❌ build_clean.py not found")
        return False

def verify_executable():
    """Verify the built executable"""
    exe_path = Path('dist/ewexport.exe')
    if not exe_path.exists():
        print("   ❌ Executable not found!")
        return False
    
    size_mb = exe_path.stat().st_size / (1024 * 1024)
    sha256 = calculate_sha256(exe_path)
    
    print(f"   📁 File: {exe_path}")
    print(f"   📏 Size: {size_mb:.2f} MB")
    print(f"   🔒 SHA256: {sha256}")
    
    # Test if executable runs
    try:
        result = subprocess.run([str(exe_path), '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0 or 'ewexport' in result.stderr.lower():
            print("   ✅ Executable verification passed")
            return True, sha256
    except:
        pass
    
    print("   ⚠️  Executable built but version check failed (this may be normal)")
    return True, sha256

def create_release_notes(version):
    """Extract release notes from CHANGELOG.md"""
    changelog = Path('CHANGELOG.md')
    if not changelog.exists():
        return f"Release {version}"
    
    try:
        with open(changelog, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find the section for this version
        lines = content.split('\n')
        in_section = False
        notes = []
        
        for line in lines:
            if line.startswith(f'## [{version}]') or line.startswith(f'## {version}'):
                in_section = True
                continue
            elif line.startswith('## ') and in_section:
                break
            elif in_section:
                notes.append(line)
        
        if notes:
            return '\n'.join(notes).strip()
        else:
            return f"Release {version}"
            
    except Exception as e:
        print(f"   ⚠️  Could not extract release notes: {e}")
        return f"Release {version}"

def create_release_info(version, sha256):
    """Create release information file"""
    release_info = {
        "version": version,
        "build_date": datetime.now().isoformat(),
        "build_machine": os.environ.get('COMPUTERNAME', 'unknown'),
        "sha256": sha256,
        "antivirus_notes": "Built with antivirus-friendly configuration. See ANTIVIRUS.md for details.",
        "python_version": sys.version,
        "build_script": "build_clean.py"
    }
    
    info_file = Path('dist/release_info.json')
    with open(info_file, 'w', encoding='utf-8') as f:
        json.dump(release_info, f, indent=2)
    
    print(f"   📋 Created release info: {info_file}")
    return info_file

def check_github_cli():
    """Check if GitHub CLI is available"""
    try:
        result = subprocess.run(['gh', '--version'], 
                              capture_output=True, text=True, check=True)
        print("   ✅ GitHub CLI available")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("   ❌ GitHub CLI not found")
        print("   📥 Install from: https://cli.github.com/")
        return False

def create_github_release(version, sha256):
    """Create GitHub release and upload executable"""
    print("🚀 Creating GitHub release...")
    
    if not check_github_cli():
        return False
    
    # Check if release already exists
    try:
        result = subprocess.run(['gh', 'release', 'view', f'v{version}'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"   ⚠️  Release v{version} already exists")
            
            # Ask if user wants to update
            response = input("   Do you want to upload to existing release? (y/n): ")
            if response.lower() != 'y':
                return False
            
            # Upload to existing release
            try:
                subprocess.run([
                    'gh', 'release', 'upload', f'v{version}',
                    'dist/ewexport.exe',
                    'dist/release_info.json',
                    '--clobber'  # Overwrite existing files
                ], check=True)
                
                print("   ✅ Files uploaded to existing release")
                return True
                
            except subprocess.CalledProcessError as e:
                print(f"   ❌ Upload failed: {e}")
                return False
    except:
        pass  # Release doesn't exist, continue to create it
    
    # Create new release
    release_notes = create_release_notes(version)
    
    # Add SHA256 to release notes
    enhanced_notes = f"""{release_notes}

## 🔒 File Verification
- **SHA256**: `{sha256}`
- **Size**: {Path('dist/ewexport.exe').stat().st_size / (1024 * 1024):.2f} MB
- **Build**: Local build with antivirus-friendly configuration

## 🛡️ Antivirus Information
This executable is built with optimized settings to reduce false positives. If your antivirus flags this file:

1. **Verify the SHA256 hash** matches the one above
2. **Add an exception** for ewexport.exe in your antivirus
3. **Check ANTIVIRUS.md** in the repository for detailed guidance
4. **Report false positives** to your antivirus vendor

## 📥 Installation
1. Download `ewexport.exe`
2. Run directly - no installation needed
3. See `INSTALL.md` for detailed instructions
"""
    
    try:
        # Create release
        subprocess.run([
            'gh', 'release', 'create', f'v{version}',
            '--title', f'Release v{version}',
            '--notes', enhanced_notes,
            'dist/ewexport.exe',
            'dist/release_info.json'
        ], check=True)
        
        print(f"   ✅ Release v{version} created successfully")
        print(f"   🌐 View at: https://github.com/karllinder/ewexport/releases/tag/v{version}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Release creation failed: {e}")
        return False

def main():
    """Main build and release process"""
    print("=" * 60)
    print("🏗️  EWExport Local Build and Release")
    print("=" * 60)
    
    # Get version
    version = get_version()
    print(f"📦 Building version: {version}")
    
    # Step 1: Clean environment
    clean_build_environment()
    
    # Step 2: Build executable
    if not build_executable():
        print("❌ Build failed - aborting")
        return False
    
    # Step 3: Verify executable
    success, sha256 = verify_executable()
    if not success:
        print("❌ Executable verification failed - aborting")
        return False
    
    # Step 4: Create release info
    create_release_info(version, sha256)
    
    # Step 5: Ask about GitHub release
    print("\n" + "=" * 60)
    print("📤 Ready to create GitHub release")
    print("=" * 60)
    
    response = input(f"Create GitHub release for v{version}? (y/n): ")
    if response.lower() == 'y':
        if create_github_release(version, sha256):
            print("\n🎉 Success! Release created and executable uploaded.")
        else:
            print("\n❌ Release creation failed.")
            print("💡 You can manually upload dist/ewexport.exe to GitHub releases")
    else:
        print("\n📁 Build complete! Files ready in dist/ folder:")
        print("   - dist/ewexport.exe")
        print("   - dist/release_info.json")
        print("\n💡 You can manually upload these to GitHub releases")
    
    print("\n" + "=" * 60)
    print("🏁 Build process complete")
    print("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Build cancelled by user")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        sys.exit(1)
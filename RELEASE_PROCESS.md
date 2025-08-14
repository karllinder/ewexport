# Manual Release Process

This document outlines the manual release process for EWExport to avoid antivirus false positives from GitHub Actions builds.

## Why Manual Releases?

GitHub Actions builds executables on virtual machines that may trigger antivirus false positives. Building locally with known, trusted development environments significantly reduces these issues.

## Prerequisites

### Required Software
- **Python 3.11+** with PyInstaller
- **GitHub CLI** (`gh`) - [Download here](https://cli.github.com/)
- **Git** with push access to the repository

### Setup GitHub CLI
```powershell
# Install GitHub CLI (if not already installed)
winget install GitHub.cli

# Authenticate
gh auth login
```

## Release Process

### Option 1: Full Build and Release (Recommended)

Use the comprehensive build and release script:

```powershell
# 1. Update version in setup.py and CHANGELOG.md
# 2. Commit changes and push to main
# 3. Run the build and release script
python build_and_release.py
```

This script will:
- ✅ Clean build environment
- ✅ Build executable with antivirus-friendly settings
- ✅ Verify build integrity
- ✅ Calculate SHA256 hash
- ✅ Create GitHub release
- ✅ Upload executable automatically
- ✅ Add security information to release notes

### Option 2: Separate Build and Upload

If you prefer more control over the process:

#### Step 1: Build Executable
```powershell
# Clean build with antivirus mitigation
python build_clean.py
```

#### Step 2: Create Release Tag
```powershell
# Update version first, then commit
git add -A
git commit -m "chore: bump version to X.X.X"
git push

# Create and push tag
git tag vX.X.X -m "Release vX.X.X"
git push origin vX.X.X
```

The GitHub Actions workflow will create a **draft release** automatically.

#### Step 3: Upload Executable
```powershell
# Upload to existing release
python upload_release.py
```

#### Step 4: Publish Release
1. Go to GitHub releases page
2. Edit the draft release
3. Verify SHA256 hash in release notes
4. Publish the release

### Option 3: Manual Upload via Web Interface

If scripts don't work:

1. **Build locally**: `python build_clean.py`
2. **Create tag**: Push version tag to trigger draft release
3. **Manual upload**: 
   - Go to GitHub releases
   - Edit the draft release
   - Drag and drop `dist/ewexport.exe`
   - Add SHA256 hash to release notes
   - Publish release

## Build Verification

### Calculate SHA256 Hash
```powershell
# PowerShell
Get-FileHash dist/ewexport.exe -Algorithm SHA256

# Python
python -c "import hashlib; print(hashlib.sha256(open('dist/ewexport.exe', 'rb').read()).hexdigest())"
```

### Test Executable
```powershell
# Quick test
dist/ewexport.exe --version

# Full test
dist/ewexport.exe
```

## Antivirus Best Practices

### Before Building
- ✅ Ensure clean development environment
- ✅ Update antivirus definitions
- ✅ Temporarily disable real-time scanning during build (optional)
- ✅ Use the clean build configuration (`build_clean.py`)

### After Building
- ✅ Calculate and verify SHA256 hash
- ✅ Test on your own machine first
- ✅ Submit to VirusTotal for analysis
- ✅ Include hash in release notes

### If Antivirus Flags the Executable
1. **Don't panic** - this is common with PyInstaller
2. **Verify hash** matches what you built
3. **Check VirusTotal** analysis
4. **Report false positive** to antivirus vendor
5. **Document** in GitHub issue if widespread

## Troubleshooting

### GitHub CLI Issues
```powershell
# Check authentication
gh auth status

# Re-login if needed
gh auth login --web

# Test access
gh repo view karllinder/ewexport
```

### Build Issues
```powershell
# Clean everything
rmdir /s build dist __pycache__
python build_clean.py
```

### Permission Issues
- Run as administrator if needed
- Check file permissions in dist/ folder
- Ensure no antivirus quarantine

## File Locations

After successful build:
```
dist/
├── ewexport.exe          # Main executable
└── release_info.json     # Build information (if using build_and_release.py)
```

## Release Checklist

### Pre-Release
- [ ] Update version in `setup.py`
- [ ] Update `CHANGELOG.md` with new features/fixes
- [ ] Commit and push changes
- [ ] Pull latest main branch

### Build
- [ ] Clean build environment
- [ ] Run `python build_clean.py`
- [ ] Verify executable works
- [ ] Calculate SHA256 hash

### Release
- [ ] Create version tag
- [ ] Run release script OR upload manually
- [ ] Verify release on GitHub
- [ ] Test download works
- [ ] Update any documentation if needed

### Post-Release
- [ ] Announce in appropriate channels
- [ ] Monitor for antivirus false positives
- [ ] Update installation documentation
- [ ] Close related GitHub issues

## Security Considerations

### Code Signing (Future)
Consider getting a code signing certificate for better antivirus compatibility:
- **Authenticode certificate** for Windows executables
- **Extended Validation (EV)** certificate for best compatibility
- **Cost**: $200-500/year depending on provider

### Build Environment Security
- Keep development machine secure
- Use reputable antivirus with exceptions for development folders
- Regularly update Python and dependencies
- Monitor for compromised dependencies

## Emergency Procedures

### If Release is Flagged as Malware
1. **Immediately** create GitHub issue documenting the problem
2. **Contact** the antivirus vendor to report false positive
3. **Provide** SHA256 hash and VirusTotal analysis
4. **Consider** emergency patch release if widespread
5. **Document** solution for future reference

### If Upload Fails
1. Check GitHub CLI authentication
2. Verify repository permissions
3. Try uploading via web interface
4. Check file size limits (GitHub has 2GB limit)
5. Contact GitHub support if persistent issues

## Support

For questions about the release process:
- **GitHub Issues**: https://github.com/karllinder/ewexport/issues
- **Label**: Use "release" label for release-related issues
- **Priority**: Tag urgent issues appropriately

Remember: Manual releases take more time but provide better quality control and reduced antivirus false positives.
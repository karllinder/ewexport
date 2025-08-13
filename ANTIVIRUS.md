# Antivirus and Security Information

## Why Antivirus Software Flags EWExport

EWExport is built using PyInstaller, which bundles Python applications into standalone executables. Unfortunately, this technique is also used by malware, causing antivirus software to flag legitimate applications as false positives.

**Important**: EWExport is completely safe and open source. All code is publicly available on GitHub for review.

## What We've Done to Reduce False Positives

### Build Optimizations
- ✅ **Disabled UPX Compression**: UPX-compressed files are often flagged
- ✅ **Added Windows Metadata**: Proper version information and file descriptions
- ✅ **Excluded Unnecessary Modules**: Smaller, cleaner executable
- ✅ **Clean Build Process**: No admin privileges requested
- ✅ **Open Source Transparency**: All code is publicly auditable

### Security Best Practices
- ✅ **No Network Activity**: Except for update checks (GitHub API only)
- ✅ **No Admin Rights**: Runs with normal user privileges
- ✅ **Local File Access Only**: Only accesses databases you select
- ✅ **No Data Collection**: No telemetry or tracking

## If Your Antivirus Flags EWExport

### Option 1: Add Exception (Recommended)
1. Add `ewexport.exe` to your antivirus exception list
2. This is safe - the file is digitally verifiable via SHA256 hash

### Option 2: Verify File Integrity
Check the file hash matches our official releases:
```powershell
# PowerShell command to verify SHA256 hash
Get-FileHash ewexport.exe -Algorithm SHA256
```

Compare against the hash shown in GitHub releases.

### Option 3: Check VirusTotal
1. Go to [VirusTotal.com](https://www.virustotal.com)
2. Upload or drag `ewexport.exe` 
3. View the analysis results
4. Most legitimate antivirus engines should show clean results

### Option 4: Build from Source
If you're still concerned, build your own executable:
```bash
git clone https://github.com/karllinder/ewexport.git
cd ewexport
pip install -r requirements.txt
python build_clean.py
```

## Reporting False Positives

Help improve detection by reporting false positives:

### Microsoft Defender
1. Visit [Microsoft Security Intelligence](https://www.microsoft.com/en-us/wdsi/filesubmission)
2. Submit `ewexport.exe` as a false positive
3. Provide details: "Open source worship song converter tool"

### Other Antivirus Vendors
Most vendors have false positive reporting systems:
- **Norton**: [Submit Sample](https://submit.norton.com)
- **McAfee**: [Submit File](https://www.mcafee.com/consumer/en-us/support/contact-us.html)
- **Avast**: [Submit File](https://www.avast.com/false-positive-file-form.php)

## VirusTotal Submission

We submit each release to VirusTotal to build reputation:

### Latest Release Analysis
- Visit: `https://www.virustotal.com/gui/search/[SHA256_HASH]`
- Replace `[SHA256_HASH]` with the hash from our GitHub release

### How to Submit
1. Go to [VirusTotal.com](https://www.virustotal.com)
2. Click "Choose file" or drag `ewexport.exe`
3. Wait for analysis
4. Share results with your IT department if needed

## For IT Administrators

### Whitelisting Information
- **File Name**: `ewexport.exe`
- **Publisher**: EWExport Open Source Project
- **Description**: EasyWorship to ProPresenter Converter
- **Source**: https://github.com/karllinder/ewexport
- **License**: MIT (Open Source)

### Security Assessment
- **Code Audit**: All source code publicly available on GitHub
- **No Outbound Traffic**: Except optional update checks (GitHub API)
- **File System Access**: Read-only database access, write to user-selected export folder
- **Registry Access**: None
- **Administrative Privileges**: Not required or requested
- **Digital Signature**: Currently unsigned (open source project)

### Enterprise Deployment
For enterprise environments:
1. Review source code on GitHub
2. Build internally using provided build scripts
3. Test in isolated environment
4. Deploy through standard software distribution

## Why This Happens

### PyInstaller Detection
- PyInstaller bundles Python runtime with your application
- This creates large executable files with embedded interpreters
- Technique is also used by malware for obfuscation
- Antivirus heuristics flag this pattern

### Machine Learning False Positives
- Modern antivirus uses ML models trained on malware samples
- These models sometimes flag legitimate software
- Especially common with newer, unsigned executables
- Reputation-based systems need time to learn

## Our Commitment to Security

### Transparency
- 100% open source - inspect all code on GitHub
- Detailed build process documentation
- Public issue tracking and resolution
- Community-driven development

### Best Practices
- Minimal system access requirements
- Clear data handling policies
- Regular security updates
- Responsive to security reports

## Contact

If you have security concerns:
- **GitHub Issues**: https://github.com/karllinder/ewexport/issues
- **Security Label**: Use "security" label for issues
- **Email**: Create GitHub issue for fastest response

## Alternative Solutions

If antivirus issues persist:
1. **Run from Source**: Use Python directly (`python src/main.py`)
2. **Portable Mode**: Run from USB/network drive
3. **Virtual Machine**: Test in isolated environment
4. **Docker**: Container-based execution (advanced)

Remember: EWExport only processes local database files and creates ProPresenter exports. It doesn't perform any suspicious activities that would warrant security concerns.
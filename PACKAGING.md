# Package Distribution Guide

This guide provides detailed information about the packaging process, version control strategy, and distribution channel options for the `kill-port` project.

## 1. Packaging Process

### 1.1 Environment Configuration

Before starting the packaging process, ensure your system meets the following requirements:

- **Python**：Version 3.7 or higher
- **pip**：Latest version
- **Operating System**：
  - Windows：Windows 10 or higher
  - macOS：macOS 10.14 or higher
  - Linux：Supports common distributions (Ubuntu, Debian, CentOS, etc.)

### 1.2 Dependency Installation

1. Clone the repository：
   ```bash
   git clone https://github.com/cyamoyed/kill-port.git
   cd kill-port
   ```

2. Install basic dependencies：
   ```bash
   pip install -r requirements.txt
   ```

3. Or use the packaging script to automatically install dependencies：
   ```bash
   python package.py --install-deps
   ```

### 1.3 Packaging Commands

#### Windows Platform

```bash
# Generate EXE executable file
python package.py --platform windows

# Or use PyInstaller directly
pyinstaller --name kill-port --windowed --onefile main.py
```

The generated executable file is located at `dist/kill-port.exe`.

#### macOS Platform

```bash
# Generate executable file
python package.py --platform macos

# Or use PyInstaller directly
pyinstaller --name kill-port --windowed --onefile main.py

# Create DMG file (needs to be executed on macOS)
# Using create-dmg tool
create-dmg --volname "kill-port" --window-pos 200 120 --window-size 600 300 \
          --app-drop-link 450 100 --icon "kill-port.app" 150 100 dist/kill-port.app
```

The generated executable file is located at `dist/kill-port`, and the DMG file needs to be created separately.

#### Linux Platform

```bash
# Generate executable file
python package.py --platform linux

# Or use PyInstaller directly
pyinstaller --name kill-port --windowed --onefile main.py

# Create AppImage file (needs to be executed on Linux)
# Using AppImageTool
appimagetool dist/kill-port kill-port.AppImage
```

The generated executable file is located at `dist/kill-port`, and the AppImage file needs to be created separately.

### 1.4 Clean Build Files

```bash
python package.py --clean

# Or clean manually
rm -rf build dist kill-port.spec
```

## 2. Version Control Strategy

### 2.1 Version Number Naming Rules

This project uses Semantic Versioning, with version numbers in the format：`X.Y.Z`

- **X** (Major version)：Increment when making incompatible API changes
- **Y** (Minor version)：Increment when adding backward-compatible new features
- **Z** (Patch version)：Increment when making backward-compatible bug fixes

### 2.2 Changelog Format

The changelog should include the following content：

```markdown
# Version (Release Date)

## Feature Changes
- New feature 1
- New feature 2

## Bug Fixes
- Fix bug 1
- Fix bug 2

## Other Changes
- Change 1
- Change 2
```

### 2.3 Release Process

1. Update code and perform tests
2. Update version numbers (in `setup.py` and related files)
3. Write changelog
4. Commit code and create tag
   ```bash
   git tag -a vX.Y.Z -m "Version X.Y.Z release"
   git push origin vX.Y.Z
   ```
5. Execute packaging process to generate executable files for each platform
6. Create a new release on GitHub Releases page and upload the packaged files

## 3. Multi-platform Distribution Channel Options

### 3.1 GitHub Releases

- **Main distribution channel**：All release files should be uploaded to GitHub Releases
- **File naming convention**：
  - Windows：`kill-port-vX.Y.Z-windows.exe`
  - macOS：`kill-port-vX.Y.Z-macos.dmg`
  - Linux：`kill-port-vX.Y.Z-linux.AppImage`
- **Release notes**：Should include version changes, installation instructions, and known issues

### 3.2 Software Repositories

#### Windows
- ** Chocolatey**：Consider publishing the software to Chocolatey package manager
- ** winget**：Consider publishing the software to Windows Package Manager

#### macOS
- ** Homebrew**：Consider creating a Homebrew formula

#### Linux
- ** DEB package**：Create DEB packages for Debian/Ubuntu systems
- ** RPM package**：Create RPM packages for Red Hat/CentOS systems
- ** AUR**：Create AUR packages for Arch Linux

### 3.3 Official Website Download

If the project has an official website, download links can be provided on the website, pointing to the GitHub Releases page or directly hosting installation files.

## 4. Package Verification and Signing Guide

### 4.1 Code Signing

To ensure the security and integrity of distributed packages, it is recommended to sign executable files：

#### Windows
- Sign EXE files using Microsoft code signing certificate
- Command example：
  ```bash
  signtool sign /f certificate.pfx /p password /t http://timestamp.digicert.com kill-port.exe
  ```

#### macOS
- Sign applications using Apple Developer certificate
- Command example：
  ```bash
  codesign --deep --force --verbose --sign "Developer ID Application: Your Name" kill-port.app
  ```

#### Linux
- Can sign AppImage files using GPG
- Command example：
  ```bash
  gpg --detach-sign --armor kill-port.AppImage
  ```

### 4.2 Hash Verification

Generate hash values for each released file to allow users to verify file integrity：

```bash
# Generate SHA256 hash
sha256sum kill-port.exe > kill-port.exe.sha256

# Generate MD5 hash
md5sum kill-port.exe > kill-port.exe.md5
```

Provide these hash values in the release notes, and users can verify them with the following commands：

```bash
# Verify SHA256 hash
sha256sum -c kill-port.exe.sha256

# Verify MD5 hash
md5sum -c kill-port.exe.md5
```

### 4.3 Security Recommendations

- Regularly update dependencies to avoid using versions with security vulnerabilities
- Validate all user input to prevent command injection attacks
- Ensure the packaging process is performed in a secure environment
- Regularly scan code for security vulnerabilities

## 5. Automated Building

To simplify the release process, it is recommended to set up automated builds：

### 5.1 GitHub Actions

Create a `.github/workflows/build.yml` file to configure CI/CD workflow：

```yaml
name: Build and Release

on:
  push:
    tags:
      - v*.*.*

jobs:
  build:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [windows-latest, ubuntu-latest, macos-latest]

    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Build
      run: |
        python package.py
    - name: Upload artifact
      uses: actions/upload-artifact@v2
      with:
        name: kill-port-${{ matrix.os }}
        path: dist/

  release:
    needs: build
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Download artifacts
      uses: actions/download-artifact@v2
      with:
        path: artifacts
    - name: Create Release
      uses: softprops/action-gh-release@v1
      with:
        files: artifacts/**/*
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### 5.2 Continuous Integration and Continuous Deployment

- **Continuous Integration**：Run tests on each code commit to ensure code quality
- **Continuous Deployment**：Automatically build and release when code is pushed to main branch or tags are created

## 6. Troubleshooting

### 6.1 Packaging Failure

- **Dependency issues**：Ensure all dependencies are correctly installed
- **Permission issues**：Ensure sufficient permissions to perform packaging operations
- **Environment issues**：Ensure packaging is executed in the correct environment, e.g., packaging macOS version on macOS

### 6.2 Signing Failure

- **Certificate issues**：Ensure certificates are valid and not expired
- **Permission issues**：Ensure sufficient permissions to use certificates
- **Network issues**：Ensure access to timestamp servers

### 6.3 Distribution Issues

- **File size**：Optimize packaging configuration to reduce executable file size
- **Compatibility**：Ensure testing on target platforms
- **Download speed**：Consider using CDN to accelerate downloads

## 7. Best Practices

- **Keep packaging process simple**：Use scripts to automate the packaging process
- **Test packaging results**：Test packaged executables on target platforms
- **Document processes**：Ensure all team members understand the packaging and distribution process
- **Regular updates**：Promptly update dependencies and fix security vulnerabilities
- **User feedback**：Collect user feedback to continuously improve packaging and distribution processes

## 8. Conclusion

By following this guide, you can ensure the packaging and distribution process of the `kill-port` project is safe, reliable, and efficient. Regularly update and optimize the packaging process to adapt to changing requirements and technical environments.
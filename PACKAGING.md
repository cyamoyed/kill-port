# 包分发指南

本指南详细介绍了 `kill-port` 项目的打包流程、版本控制策略和分发渠道方案。

## 1. 打包流程

### 1.1 环境配置

在开始打包之前，确保您的系统满足以下要求：

- **Python**：版本 3.7 或更高
- **pip**：最新版本
- **操作系统**：
  - Windows：Windows 10 或更高版本
  - macOS：macOS 10.14 或更高版本
  - Linux：支持常见的发行版（Ubuntu、Debian、CentOS 等）

### 1.2 依赖安装

1. 克隆仓库：
   ```bash
   git clone https://github.com/cyamoyed/kill-port.git
   cd kill-port
   ```

2. 安装基础依赖：
   ```bash
   pip install -r requirements.txt
   ```

3. 或者使用打包脚本自动安装依赖：
   ```bash
   python package.py --install-deps
   ```

### 1.3 打包命令

#### Windows 平台

```bash
# 生成 EXE 可执行文件
python package.py --platform windows

# 或者使用 PyInstaller 直接打包
pyinstaller --name kill-port --windowed --onefile main.py
```

生成的可执行文件位于 `dist/kill-port.exe`。

#### macOS 平台

```bash
# 生成可执行文件
python package.py --platform macos

# 或者使用 PyInstaller 直接打包
pyinstaller --name kill-port --windowed --onefile main.py

# 创建 DMG 文件（需要在 macOS 上执行）
# 使用 create-dmg 工具
create-dmg --volname "kill-port" --window-pos 200 120 --window-size 600 300 \
          --app-drop-link 450 100 --icon "kill-port.app" 150 100 dist/kill-port.app
```

生成的可执行文件位于 `dist/kill-port`，DMG 文件需要额外创建。

#### Linux 平台

```bash
# 生成可执行文件
python package.py --platform linux

# 或者使用 PyInstaller 直接打包
pyinstaller --name kill-port --windowed --onefile main.py

# 创建 AppImage 文件（需要在 Linux 上执行）
# 使用 AppImageTool
appimagetool dist/kill-port kill-port.AppImage
```

生成的可执行文件位于 `dist/kill-port`，AppImage 文件需要额外创建。

### 1.4 清理构建文件

```bash
python package.py --clean

# 或者手动清理
rm -rf build dist kill-port.spec
```

## 2. 版本控制策略

### 2.1 版本号命名规则

本项目使用语义化版本控制（Semantic Versioning），版本号格式为：`X.Y.Z`

- **X**（主版本号）：当进行不兼容的 API 更改时递增
- **Y**（次版本号）：当添加向后兼容的新功能时递增
- **Z**（补丁版本号）：当进行向后兼容的 bug 修复时递增

### 2.2 更新日志格式

更新日志应包含以下内容：

```markdown
# 版本号 (发布日期)

## 功能变更
- 新功能 1
- 新功能 2

## Bug 修复
- 修复 bug 1
- 修复 bug 2

## 其他变更
- 变更 1
- 变更 2
```

### 2.3 发布流程

1. 更新代码并进行测试
2. 更新版本号（在 `setup.py` 和相关文件中）
3. 编写更新日志
4. 提交代码并创建标签
   ```bash
   git tag -a vX.Y.Z -m "版本 X.Y.Z 发布"
   git push origin vX.Y.Z
   ```
5. 执行打包流程，生成各平台的可执行文件
6. 在 GitHub Releases 页面创建新的发布，上传打包好的文件

## 3. 多平台分发渠道方案

### 3.1 GitHub Releases

- **主要分发渠道**：所有版本的发布文件都应上传到 GitHub Releases
- **文件命名规范**：
  - Windows：`kill-port-vX.Y.Z-windows.exe`
  - macOS：`kill-port-vX.Y.Z-macos.dmg`
  - Linux：`kill-port-vX.Y.Z-linux.AppImage`
- **发布说明**：应包含版本变更内容、安装说明和已知问题

### 3.2 软件仓库

#### Windows
- ** Chocolatey**：可以考虑将软件发布到 Chocolatey 包管理器
- ** winget**：可以考虑将软件发布到 Windows 包管理器

#### macOS
- ** Homebrew**：可以考虑创建 Homebrew 公式

#### Linux
- ** DEB 包**：为 Debian/Ubuntu 系统创建 DEB 包
- ** RPM 包**：为 Red Hat/CentOS 系统创建 RPM 包
- ** AUR**：为 Arch Linux 创建 AUR 包

### 3.3 官网下载

如果项目有官方网站，可以在网站上提供下载链接，指向 GitHub Releases 页面或直接托管安装文件。

## 4. 包验证和签名指南

### 4.1 代码签名

为了确保分发包的安全性和完整性，建议对可执行文件进行代码签名：

#### Windows
- 使用 Microsoft 代码签名证书对 EXE 文件进行签名
- 命令示例：
  ```bash
  signtool sign /f certificate.pfx /p password /t http://timestamp.digicert.com kill-port.exe
  ```

#### macOS
- 使用 Apple Developer 证书对应用进行签名
- 命令示例：
  ```bash
  codesign --deep --force --verbose --sign "Developer ID Application: Your Name" kill-port.app
  ```

#### Linux
- 可以使用 GPG 对 AppImage 文件进行签名
- 命令示例：
  ```bash
  gpg --detach-sign --armor kill-port.AppImage
  ```

### 4.2 哈希验证

为每个发布的文件生成哈希值，以便用户验证文件的完整性：

```bash
# 生成 SHA256 哈希值
sha256sum kill-port.exe > kill-port.exe.sha256

# 生成 MD5 哈希值
md5sum kill-port.exe > kill-port.exe.md5
```

在发布说明中提供这些哈希值，用户可以通过以下命令验证：

```bash
# 验证 SHA256 哈希值
sha256sum -c kill-port.exe.sha256

# 验证 MD5 哈希值
md5sum -c kill-port.exe.md5
```

### 4.3 安全建议

- 定期更新依赖，避免使用有安全漏洞的版本
- 对所有用户输入进行验证，防止命令注入攻击
- 确保打包过程在安全的环境中进行
- 定期扫描代码中的安全漏洞

## 5. 自动化构建

为了简化发布流程，建议设置自动化构建：

### 5.1 GitHub Actions

创建 `.github/workflows/build.yml` 文件，配置 CI/CD 流程：

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

### 5.2 持续集成和持续部署

- **持续集成**：每次代码提交时运行测试，确保代码质量
- **持续部署**：当代码推送到主分支或创建标签时，自动构建和发布

## 6. 故障排除

### 6.1 打包失败

- **依赖问题**：确保所有依赖都已正确安装
- **权限问题**：确保有足够的权限执行打包操作
- **环境问题**：确保在正确的环境中执行打包，例如在 macOS 上打包 macOS 版本

### 6.2 签名失败

- **证书问题**：确保证书有效且未过期
- **权限问题**：确保有足够的权限使用证书
- **网络问题**：确保可以访问时间戳服务器

### 6.3 分发问题

- **文件大小**：优化打包配置，减小可执行文件大小
- **兼容性**：确保在目标平台上进行测试
- **下载速度**：考虑使用 CDN 加速下载

## 7. 最佳实践

- **保持打包过程简单**：使用脚本自动化打包流程
- **测试打包结果**：在目标平台上测试打包后的可执行文件
- **文档化流程**：确保所有团队成员都了解打包和分发流程
- **定期更新**：及时更新依赖和修复安全漏洞
- **用户反馈**：收集用户反馈，不断改进打包和分发流程

## 8. 结论

通过遵循本指南，您可以确保 `kill-port` 项目的打包和分发过程安全、可靠、高效。定期更新和优化打包流程，以适应不断变化的需求和技术环境。
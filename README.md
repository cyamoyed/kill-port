# 端口进程关闭助手 (kill-port)

一个跨平台的端口进程关闭助手工具，用于快速查找并终止占用指定端口的进程。支持 Windows、macOS 和 Linux 平台，提供 GUI 和命令行两种操作模式。

## 功能特性

- 🎯 **跨平台支持**：兼容 Windows、macOS 和 Linux 操作系统
- 🖥️ **双界面模式**：提供图形用户界面（GUI）和命令行界面（CLI）
- ⚡ **操作快速**：一键终止占用指定端口的进程
- 📋 **详细反馈**：显示操作结果和进程 PID
- 🔒 **权限提示**：当需要管理员/root 权限时提供清晰提示
- 🛠️ **自动化打包**：支持为各平台生成可执行文件

## 支持的平台

- **Windows**：生成 EXE 可执行文件
- **macOS**：生成 DMG 安装包
- **Linux**：生成 AppImage 或 DEB 包

## 安装指南

### 方法 1：使用预编译的可执行文件

1. 前往 [GitHub Releases](https://github.com/cyamoyed/kill-port/releases) 页面下载对应平台的可执行文件
2. 对于 Windows，下载 `kill-port.exe` 文件
3. 对于 macOS，下载 `kill-port.dmg` 文件并安装
4. 对于 Linux，下载 `kill-port.AppImage` 文件并赋予执行权限

### 方法 2：从源代码安装

1. 克隆仓库：
   ```bash
   git clone https://github.com/cyamoyed/kill-port.git
   cd kill-port
   ```

2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

3. 安装包：
   ```bash
   pip install .
   ```

## 使用指南

### GUI 模式

1. **Windows**：双击 `kill-port.exe` 文件
2. **macOS**：打开 `kill-port.app` 应用
3. **Linux**：运行 `kill-port` 可执行文件

在弹出的窗口中：
- 在输入框中输入要关闭的端口号
- 点击 "终止进程" 按钮
- 查看操作结果和进程 PID

### 命令行模式

```bash
# 基本使用
kill-port <端口>

# 显示版本信息
kill-port --version

# 安静模式，只输出错误信息
kill-port --quiet <端口>

# 显示帮助信息
kill-port --help
```

#### 示例

```bash
# 终止占用 8080 端口的进程
kill-port 8080

# 显示版本信息
kill-port --version

# 安静模式终止占用 3000 端口的进程
kill-port --quiet 3000
```

## 常见问题 (FAQ)

### Q: 当提示 "需要管理员权限" 时应该怎么做？
A: 在 Windows 上，右键点击可执行文件并选择 "以管理员身份运行"；在 macOS/Linux 上，使用 `sudo` 命令运行。

### Q: 执行后提示 "端口未被占用"，但我确定有进程在使用该端口？
A: 可能是由于权限不足无法查看所有进程，请尝试以管理员/root 身份运行。

### Q: 为什么在 macOS 上打包后需要创建 DMG 文件？
A: DMG 是 macOS 上常见的应用分发格式，需要在 macOS 系统上使用专门的工具创建。

### Q: 为什么在 Linux 上打包后需要创建 AppImage 文件？
A: AppImage 是一种跨 Linux 发行版的应用打包格式，可以在不同的 Linux 系统上直接运行。

## 故障排除

1. **无法找到端口占用信息**：
   - 检查是否有足够的权限
   - 确认端口号是否正确
   - 尝试使用 `netstat`（Windows）或 `lsof`（macOS/Linux）手动检查端口占用情况

2. **打包失败**：
   - 确保所有依赖已安装
   - 检查 PyInstaller 是否已正确安装
   - 尝试清理构建文件并重新打包

3. **GUI 界面无法启动**：
   - 检查 PyQt5 是否已正确安装
   - 尝试使用命令行模式作为替代

## 开发指南

### 项目结构

```
kill-port/
├── main.py          # 主入口文件
├── gui.py           # PyQt5 GUI 实现
├── cli.py           # 命令行界面实现
├── setup.py         # 包配置文件
├── pyinstaller.spec # PyInstaller 配置文件
├── package.py       # 打包脚本
├── test_cross_platform.py # 跨平台测试
├── README.md        # 项目文档
└── requirements.txt # 依赖文件
```

### 打包流程

1. 安装依赖：
   ```bash
   python package.py --install-deps
   ```

2. 打包当前平台：
   ```bash
   python package.py
   ```

3. 清理构建文件：
   ```bash
   python package.py --clean
   ```

### 测试

运行跨平台兼容性测试：
```bash
python test_cross_platform.py
```

## 版本控制策略

- 版本号格式：`X.Y.Z`
  - X：主版本号，重大功能变更
  - Y：次版本号，新增功能
  - Z：补丁版本号，bug 修复

- 变更日志格式：
  - 版本号
  - 发布日期
  - 功能变更列表
  - Bug 修复列表

## 贡献指南

欢迎提交 Issues 和 Pull Requests！请确保：

1. 代码遵循项目风格
2. 添加适当的测试
3. 更新文档
4. 提供清晰的提交信息

## 许可证

本项目使用 MIT 许可证，详情请参阅 [LICENSE](LICENSE) 文件。

## 联系方式

- 作者：cyam
- 邮箱：980713832@qq.com
- 项目地址：https://github.com/cyamoyed/kill-port
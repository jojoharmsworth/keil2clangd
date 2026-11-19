**[English](README.md) | 简体中文**

<h1 align="center" style="margin: 30px 0 30px; font-weight: bold;">Keil2Json</h1>

<p align="center">
  <a href="https://github.com/jojoharmsworth/keil2clangd/releases"><img src="https://img.shields.io/badge/release-download-blue.svg"></a>
  <a href="https://github.com/jojoharmsworth/keil2clangd/actions"><img src="https://img.shields.io/badge/build-GitHub%20Actions-brightgreen.svg"></a>
  <img src="https://img.shields.io/badge/platform-Windows%20%7C%20Linux-lightgrey.svg">
  <img src="https://img.shields.io/badge/project-Keil%20%7C%20IAR%20%7C%20Makefile-orange.svg">
</p>

Keil2Json 可以从 Keil MDK、IAR EWARM 和 Makefile 工程生成 `compile_commands.json`，用于 clangd、VS Code C/C++ 等工具的代码跳转、补全和诊断。

## 功能特性

- 支持 Keil MDK 工程：解析 `.uvprojx`。
- 支持 IAR EWARM 工程：解析 `.ewp`。
- 支持 Makefile 工程：执行 `make clean`、`make -n` 和 `make` 捕获编译命令。
- 自动补充 CMSIS 和 C 库 include 路径。
- 提供持久化配置向导，用于保存 Keil、IAR、CMSIS、ARMCC、ARMCLANG 和 IAR C include 配置。
- 支持 Keil 多 Target 工程选择。
- 当同一目录存在 Keil、IAR、Makefile 多种工程时，可交互选择或通过参数指定分支。
- 支持调用 Keil UV4 执行 build、rebuild、clean、flash、download 和 debug。
- 提供 Python 完整功能版和 C++ 小体积快速启动版。

## 支持的工程

| 工程类型 | 文件 | 行为 |
| --- | --- | --- |
| Keil MDK | `.uvprojx` | 解析源文件、include、宏定义、选中的 Target，以及 ARMCC/ARMCLANG include。 |
| IAR EWARM | `.ewp` | 解析源文件、include、宏定义、CMSIS include 和 IAR C 库 include。 |
| Makefile | `Makefile` 或 `makefile` | 执行 Make，并从 `make -n` 输出中提取编译命令。 |

## 快速开始

在工程目录运行：

```powershell
Keil2Json.exe
Keil2JsonCpp.exe
```

指定工程目录或工程文件：

```powershell
Keil2Json.exe -p D:\Project\Demo
Keil2JsonCpp.exe -p D:\Project\Demo
```

生成绝对路径：

```powershell
Keil2Json.exe -p D:\Project\Demo --absolute
Keil2JsonCpp.exe -p D:\Project\Demo --absolute
```

## 首次配置

首次使用建议运行配置向导：

```powershell
Keil2Json.exe --setup
Keil2JsonCpp.exe --setup
```

配置向导会扫描 Windows 注册表中的 Keil 和 IAR 安装路径，并引导选择或手动输入 CMSIS 和 C 库 include 路径。

配置会长期保存：

| 平台 | 路径 |
| --- | --- |
| Windows | `%APPDATA%\KeilFormat\config.json` |
| Linux | `~/.config/KeilFormat/config.json` |

查看当前配置：

```powershell
Keil2Json.exe --show-config
Keil2JsonCpp.exe --show-config
```

## CMSIS 和工具链 include

Keil 会优先读取 `TOOLS.INI` 中的 `RTEPATH`。例如：

```ini
RTEPATH="D:\keil\Keil_v5\Arm\Packs"
```

对应 CMSIS 包路径会按下面的形式推导：

```text
D:\keil\Keil_v5\Arm\Packs\ARM\CMSIS
```

同时兼容 Keil 4 风格路径：

```text
D:\keil\Keil_v4\ARM\CMSIS\Include
```

Keil 工具链 include 会根据工程编译器自动补充：

- ARMCC：`ARMCC\include`
- ARMCLANG：`ARMCLANG\include`

IAR 常见路径：

```text
<IAR>\arm\CMSIS
<IAR>\arm\inc\c
```

如果没有扫描到 Keil 或 IAR，配置向导会提示手动输入 CMSIS 和 C 库 include 路径。

## 命令行参数

| 参数 | 说明 |
| --- | --- |
| `<path>` | 位置参数形式的工程目录或文件；也可使用 `-p`。 |
| `-p, --path <path>` | 工程目录或工程文件。默认当前目录。 |
| `-o, --output-dir <dir>` | 指定输出目录，自动创建缺失目录；相对路径以当前工作目录为基准。 |
| `-a, --absolute` | 在 `compile_commands.json` 中写入绝对路径。 |
| `--project-type <type>` | 指定 `keil`、`iar`、`makefile` 或 `make` 分支。 |
| `-s, --setup` | 运行持久化配置向导。 |
| `--show-config` | 打印已保存配置。 |
| `-n, --dry-run` | Makefile 工程只执行 `make clean` 和 `make -n`。 |
| `--keil_build` | 调用 Keil UV4 操作，不生成 `compile_commands.json`。 |
| `--keil_action <action>` | `build`、`rebuild`、`clean`、`flash`、`download` 或 `debug`。 |
| `-t, --target <name>` | Keil Target 名称，用于 JSON 生成或 UV4 操作。 |
| `--list-targets` | 列出 Keil Target 后退出。 |
| `--keil_uv4 <path>` | 手动指定 `UV4.exe` 路径。 |
| `--keil_jobs <n>` | Keil 窗口隐藏时使用的 UV4 `-j` 参数。debug 不使用 `-j`。 |
| `--keil_log <path>` | 指定 Keil UV4 日志输出路径。 |
| `--keil_window` | 显示 Keil 窗口。debug 总是显示窗口。 |
| `-h, --help` | 显示帮助信息。 |

## 工程分支选择

如果同一目录存在多种工程类型，工具会提示选择分支：

- Keil：解析 `.uvprojx` 并生成 JSON。
- IAR：解析 `.ewp` 并生成 JSON。
- Makefile：执行 Make 并根据捕获的编译命令生成 JSON。

使用 `--project-type` 可以跳过交互：

```powershell
Keil2Json.exe -p . --project-type keil
Keil2Json.exe -p . --project-type iar
Keil2Json.exe -p . --project-type makefile
```

如果存在多个 Keil 或 IAR 工程文件，工具会继续提示选择具体工程。Makefile 按目录处理：即使同一目录同时存在 `Makefile` 和 `makefile`，也不会展示 Makefile 文件选择，而是按该目录默认 Make 行为执行。

## Keil Target 选择

如果 Keil 工程只有一个 Target，会自动使用该 Target。如果存在多个 Target，工具会提示选择。

也可以直接指定：

```powershell
Keil2Json.exe -p . --project-type keil --target "Target 1"
Keil2JsonCpp.exe -p . --project-type keil --target "Target 1"
```

## Keil UV4 操作

列出 Target：

```powershell
Keil2Json.exe -p . --list-targets
Keil2JsonCpp.exe -p . --list-targets
```

构建指定 Target：

```powershell
Keil2Json.exe -p . --keil_build --keil_action build -t "Target 1"
Keil2JsonCpp.exe -p . --keil_build --keil_action build -t "Target 1"
```

其他操作：

```powershell
Keil2Json.exe -p . --keil_build --keil_action clean
Keil2Json.exe -p . --keil_build --keil_action rebuild
Keil2Json.exe -p . --keil_build --keil_action flash
Keil2Json.exe -p . --keil_build --keil_action debug
```

Keil 窗口行为：

- 默认情况下，非 debug 操作会传入 `-j`，Keil 窗口隐藏。
- 使用 `--keil_window` 时不传 `-j`，Keil 窗口显示。
- `debug` 总是显示 Keil 窗口，并且永远不传 `-j`。
- `--keil_jobs` 用于设置隐藏窗口时的 `-j` 数值。

Keil 日志行为：

- `build` 默认写入 `build_log`。
- `clean`、`rebuild`、`flash`、`debug` 默认写入 `Prg_Output`。
- 可通过 `--keil_log <path>` 指定日志路径。
- Python 版和 C++ 版都会在 UV4 运行期间实时输出 Keil 构建日志。

## 输出路径规则

生成文件名固定为 `compile_commands.json`。

| 输入方式 | 未指定 `-o` 时的输出目录 |
| --- | --- |
| Keil / IAR 工程目录 | `-p` 指定的目录，省略时为当前工作目录。 |
| `.uvprojx` / `.ewp` 工程文件 | 指定工程文件所在目录。 |
| Makefile 工程 | 检测到的 Makefile 工程目录。 |

使用 `-o` 或 `--output-dir` 覆盖默认输出目录。不存在的目录会自动创建；相对输出路径以运行命令时的当前工作目录为基准，与 `-p` 无关。

```powershell
Keil2Json.exe -p "D:\Project\Demo" -o "D:\Project\Demo\.vscode"
Keil2JsonCpp.exe -p "D:\Project\Demo" --output-dir "D:\Project\Demo\.vscode"
python Keil2Json.py -p ./project -o ./build/clangd
```

输出目录只影响 JSON 文件的保存位置。Keil 工程中的源文件和 include 相对路径以 `.uvprojx` 所在目录解析，即使工程文件位于子目录也能正确处理。`--absolute` 控制数据库内的路径格式，不控制输出位置。

## VS Code clangd 配置

如果输出到工作区的 `.vscode` 目录，在 `.vscode/settings.json` 中配置：

```json
{
    "clangd.arguments": [
        "--background-index",
        "--compile-commands-dir=${workspaceFolder}/.vscode"
    ]
}
```

确保该目录内存在 `compile_commands.json`。如果输出到其他目录，修改 `--compile-commands-dir` 指向实际目录（不是 JSON 文件）；也可以使用绝对路径。重新生成后执行 **clangd: Restart language server**。已有 `clangd.arguments` 时，将该选项合并到现有数组中。

## 从 Release 使用

从 [GitHub Releases](https://github.com/jojoharmsworth/keil2clangd/releases) 下载对应平台可执行文件后运行：

```powershell
Keil2Json.exe -p .
Keil2JsonCpp.exe -p .
```

如果运行到旧版本，检查 `PATH`：

```powershell
where Keil2Json.exe
where Keil2JsonCpp.exe
```

## 从源码构建

直接运行 Python 版：

```powershell
python Keil2Json.py -p .
```

打包 Python exe：

```powershell
python -m PyInstaller --clean --noconfirm --onefile --console --name Keil2Json --distpath dist Keil2Json.py
```

构建 C++ exe：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\cpp\build.ps1
```

C++ 产物路径：

```text
dist-cpp\Keil2JsonCpp.exe
```

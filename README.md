**English | [简体中文](README_zh.md)**

<h1 align="center" style="margin: 30px 0 30px; font-weight: bold;">Keil2Json</h1>

<p align="center">
  <a href="https://github.com/jojoharmsworth/keil2clangd/releases"><img src="https://img.shields.io/badge/release-download-blue.svg"></a>
  <a href="https://github.com/jojoharmsworth/keil2clangd/actions"><img src="https://img.shields.io/badge/build-GitHub%20Actions-brightgreen.svg"></a>
  <img src="https://img.shields.io/badge/platform-Windows%20%7C%20Linux-lightgrey.svg">
  <img src="https://img.shields.io/badge/project-Keil%20%7C%20IAR%20%7C%20Makefile-orange.svg">
</p>

Keil2Json generates `compile_commands.json` for embedded projects that use Keil MDK, IAR EWARM, or Makefile-based builds. The generated compilation database can be used by clangd, VS Code C/C++, and other language servers for code navigation, completion, and diagnostics.

## Features

- Parse Keil MDK `.uvprojx` projects.
- Parse IAR EWARM `.ewp` projects.
- Capture Makefile compile commands through `make clean`, `make -n`, and `make`.
- Inject CMSIS and C library include paths automatically.
- Save Keil, IAR, CMSIS, ARMCC, ARMCLANG, and IAR C include configuration persistently.
- Select Keil targets for multi-target `.uvprojx` projects.
- Select a project branch when Keil, IAR, and Makefile projects exist in the same directory.
- Run Keil UV4 build, rebuild, clean, flash, download, and debug actions.
- Provide a Python executable for compatibility and a C++ executable for smaller size and faster startup.

## Supported Projects

| Project type | File | Behavior |
| --- | --- | --- |
| Keil MDK | `.uvprojx` | Parses sources, include paths, defines, selected target, and ARMCC/ARMCLANG include paths. |
| IAR EWARM | `.ewp` | Parses sources, include paths, defines, CMSIS include, and IAR C library include. |
| Makefile | `Makefile` or `makefile` | Runs Make and extracts compiler commands from `make -n`. |

## Quick Start

Run in a project directory:

```powershell
Keil2Json.exe
Keil2JsonCpp.exe
```

Specify a project directory or project file:

```powershell
Keil2Json.exe -p D:\Project\Demo
Keil2JsonCpp.exe -p D:\Project\Demo
```

Generate absolute paths:

```powershell
Keil2Json.exe -p D:\Project\Demo --absolute
Keil2JsonCpp.exe -p D:\Project\Demo --absolute
```

## First-Time Setup

Run the setup wizard before first use:

```powershell
Keil2Json.exe --setup
Keil2JsonCpp.exe --setup
```

The wizard scans the Windows registry for Keil and IAR installations, then asks you to select or manually enter CMSIS and C library include paths.

Configuration is stored permanently:

| Platform | Path |
| --- | --- |
| Windows | `%APPDATA%\KeilFormat\config.json` |
| Linux | `~/.config/KeilFormat/config.json` |

Show the current configuration:

```powershell
Keil2Json.exe --show-config
Keil2JsonCpp.exe --show-config
```

## CMSIS and Toolchain Includes

For Keil, the tool reads `TOOLS.INI` and uses `RTEPATH` when available. For example:

```ini
RTEPATH="D:\keil\Keil_v5\Arm\Packs"
```

The corresponding CMSIS package root is resolved as:

```text
D:\keil\Keil_v5\Arm\Packs\ARM\CMSIS
```

Legacy Keil 4 style CMSIS paths are also supported:

```text
D:\keil\Keil_v4\ARM\CMSIS\Include
```

Keil compiler include paths are injected according to the selected project compiler:

- ARMCC: `ARMCC\include`
- ARMCLANG: `ARMCLANG\include`

For IAR, common include paths are:

```text
<IAR>\arm\CMSIS
<IAR>\arm\inc\c
```

If no Keil or IAR installation is detected, the setup wizard asks for manual CMSIS and C library include paths.

## CLI Options

| Option | Description |
| --- | --- |
| `<path>` | Positional project directory or file; alternatively use `-p`. |
| `-p, --path <path>` | Project directory or project file. Defaults to the current directory. |
| `-o, --output-dir <dir>` | Output directory; created automatically. Relative paths are resolved from the current working directory. |
| `-a, --absolute` | Write absolute paths in `compile_commands.json`. |
| `--project-type <type>` | Select `keil`, `iar`, `makefile`, or `make`. |
| `-s, --setup` | Run the persistent setup wizard. |
| `--show-config` | Print the saved configuration. |
| `-n, --dry-run` | For Makefile projects, run `make clean` and `make -n` only. |
| `--keil_build` | Run a Keil UV4 action instead of generating `compile_commands.json`. |
| `--keil_action <action>` | `build`, `rebuild`, `clean`, `flash`, `download`, or `debug`. |
| `-t, --target <name>` | Keil target name for JSON generation or Keil UV4 actions. |
| `--list-targets` | List Keil targets and exit. |
| `--keil_uv4 <path>` | Override the `UV4.exe` path. |
| `--keil_jobs <n>` | Keil UV4 `-j` value when the Keil window is hidden. Debug never uses `-j`. |
| `--keil_log <path>` | Keil UV4 output log path. |
| `--keil_window` | Show the Keil window. Debug always shows the window. |
| `-h, --help` | Show help. |

## Project Selection

If a directory contains more than one project type, the tool asks which branch to use:

- Keil: parse `.uvprojx` and generate JSON.
- IAR: parse `.ewp` and generate JSON.
- Makefile: run Make and generate JSON from captured compile commands.

Use `--project-type` to skip the prompt:

```powershell
Keil2Json.exe -p . --project-type keil
Keil2Json.exe -p . --project-type iar
Keil2Json.exe -p . --project-type makefile
```

If multiple Keil or IAR project files exist, the tool asks you to select one. Makefile projects are directory-based: if both `Makefile` and `makefile` exist in the same directory, the tool does not ask which file to use; it runs the default Make behavior in that directory.

## Keil Target Selection

If a Keil project has one target, that target is used automatically. If it has multiple targets, the tool asks you to select one.

You can also specify it directly:

```powershell
Keil2Json.exe -p . --project-type keil --target "Target 1"
Keil2JsonCpp.exe -p . --project-type keil --target "Target 1"
```

## Keil UV4 Actions

List targets:

```powershell
Keil2Json.exe -p . --list-targets
Keil2JsonCpp.exe -p . --list-targets
```

Build a target:

```powershell
Keil2Json.exe -p . --keil_build --keil_action build -t "Target 1"
Keil2JsonCpp.exe -p . --keil_build --keil_action build -t "Target 1"
```

Other actions:

```powershell
Keil2Json.exe -p . --keil_build --keil_action clean
Keil2Json.exe -p . --keil_build --keil_action rebuild
Keil2Json.exe -p . --keil_build --keil_action flash
Keil2Json.exe -p . --keil_build --keil_action debug
```

Keil window behavior:

- Non-debug actions pass `-j` by default, so the Keil window is hidden.
- `--keil_window` disables `-j` and shows the Keil window.
- `debug` always shows the Keil window and never passes `-j`.
- `--keil_jobs` controls the `-j` value when the window is hidden.

Keil log behavior:

- `build` writes to `build_log` by default.
- `clean`, `rebuild`, `flash`, and `debug` write to `Prg_Output` by default.
- Use `--keil_log <path>` to override the log path.
- Both Python and C++ versions stream Keil build logs while UV4 is running.

## Output Path Rules

The generated file is always named `compile_commands.json`.

| Input | Output directory when `-o` is omitted |
| --- | --- |
| Keil / IAR project directory | The directory supplied with `-p`, or the current working directory when omitted. |
| `.uvprojx` / `.ewp` project file | The directory containing the supplied project file. |
| Makefile project | The detected Makefile project directory. |

Use `-o` or `--output-dir` to override the output directory. Missing directories are created automatically. Relative output paths are resolved from the current working directory, independently of `-p`.

```powershell
Keil2Json.exe -p "D:\Project\Demo" -o "D:\Project\Demo\.vscode"
Keil2JsonCpp.exe -p "D:\Project\Demo" --output-dir "D:\Project\Demo\.vscode"
python Keil2Json.py -p ./project -o ./build/clangd
```

The output directory only changes where the JSON file is saved. Relative source and include paths in Keil projects are resolved from the directory containing the `.uvprojx`, including projects stored in subdirectories. `--absolute` controls path formatting inside the database, not its output location.

## Automatic MCU Core Detection

For Keil projects, the generator reads `Cpu` / `CPUTYPE` from the selected Target and adds `--target=arm-none-eabi`, `-mcpu=<core>`, and `-mthumb` to the compilation database. Supported cores: Cortex-M0, M0+, M1, M3, M4, M7, M23, M33, M35P, M52, M55, and M85. No chip-name mapping is needed.

For example, the HC32L021 Cortex-M0+ becomes `-mcpu=cortex-m0plus`. Regenerate the database and restart clangd after switching targets or MCUs. Remove any CPU flags previously added manually in `.clangd` to avoid conflicting settings after a switch.

Automatic detection currently applies only to Keil Cortex-M projects. Missing or unsupported CPU information produces a warning; the generator does not guess the core or infer FPU, floating-point ABI, or TrustZone settings.

## VS Code clangd Configuration

When writing to the workspace's `.vscode` directory, configure `.vscode/settings.json`:

```json
{
    "clangd.arguments": [
        "--background-index",
        "--compile-commands-dir=${workspaceFolder}/.vscode"
    ]
}
```

Ensure this directory contains `compile_commands.json`. For other output locations, point `--compile-commands-dir` to the actual directory (not the JSON file); an absolute path also works. Run **clangd: Restart language server** after regenerating the database. If `clangd.arguments` already exists, merge the option into its existing array.

## Install from Release

Download the executable for your platform from [GitHub Releases](https://github.com/jojoharmsworth/keil2clangd/releases).

Recommended Windows usage:

```powershell
Keil2Json.exe -p .
Keil2JsonCpp.exe -p .
```

If an old executable is still being used, check `PATH`:

```powershell
where Keil2Json.exe
where Keil2JsonCpp.exe
```

## Build from Source

Run the Python version directly:

```powershell
python Keil2Json.py -p .
```

Build the Python executable:

```powershell
python -m PyInstaller --clean --noconfirm --onefile --console --name Keil2Json --distpath dist Keil2Json.py
```

Build the C++ executable:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\cpp\build.ps1
```

The C++ executable is generated at:

```text
dist-cpp\Keil2JsonCpp.exe
```

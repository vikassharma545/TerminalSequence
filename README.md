# TerminalSequence

A Python script to arrange Python terminal windows in a 5×6 grid on a selected monitor, accessible via a right-click context menu in Windows.

## Prerequisites

- **Git**: Ensure Git is installed (`git --version`).
- **Python**: Ensure Python is installed and added to PATH (`python --version`).
- **PowerShell**: Available by default on Windows.

## Installation

Run the following PowerShell command in **Admin Mode** to clone the repository and set up the context menu:

```powershell
$repoPath = "C:\Program Files\TerminalPosition"; if (Test-Path $repoPath) { Remove-Item -Recurse -Force $repoPath }; git clone https://github.com/vikassharma545/TerminalSequence.git $repoPath; cd $repoPath; Start-Process cmd.exe -ArgumentList "/c setup_context_menu.bat" -Verb RunAs
```

### What It Does

- Clones the repository to `C:\Program Files\TerminalPosition`.
- Installs dependencies (`psutil`, `screeninfo`, `pygetwindow`, `pywin32`).
- Adds a **"Terminal Sequence"** option to the right-click context menu.
- Prompts for UAC approval (click "Yes").

## Usage

1. Right-click on the desktop or in File Explorer.
2. Select **Terminal Sequence**.
3. Approve the UAC prompt.
4. Choose a monitor if multiple are detected.
5. The script arranges open Python terminal windows in a 5×6 grid on the selected monitor.

## Files

| File | Description |
|------|-------------|
| `window_sequence.py` | Main script to detect and arrange Python terminal windows. |
| `setup_context_menu.bat` | Installs dependencies and configures the right-click context menu. |
| `requirements.txt` | Python dependency list. |

## License

MIT

import ctypes
ctypes.windll.kernel32.SetConsoleTitleW("Set Position")

import re
import psutil
import screeninfo
import win32process
import tkinter as tk
from time import sleep
import pygetwindow as gw
from screeninfo import get_monitors

def get_clicked_monitor():
    main_root = tk.Tk()
    main_root.withdraw()
    monitors = screeninfo.get_monitors()
    
    if len(monitors) == 1:
        return monitors[0]

    def close_all_popups(popups, main_root, monitor_num, clicked_monitor):
        clicked_monitor[0] = monitor_num  # Store the clicked monitor number
        for popup in popups:
            if popup.winfo_exists():
                popup.destroy()  # Close each popup
        main_root.destroy()  # Exit the mainloop

    popups = []
    clicked_monitor = [None]  # Mutable list to track the clicked monitor

    for i, monitor in enumerate(monitors, start=1):
        popup = tk.Toplevel(main_root)
        popup.attributes("-topmost", True)  # Keep popup on top
        popup.overrideredirect(True)  # Remove window borders
        
        button = tk.Button(popup, text=f"Monitor {i}", font=("Arial", 20), bg="white", fg="black", relief="solid", bd=2, padx=20, pady=20,
                            command=lambda num=i: close_all_popups(popups, main_root, num, clicked_monitor))
        
        button.pack(padx=2, pady=2)
        x = monitor.x + monitor.width // 2
        y = monitor.y + monitor.height // 2
        popup.geometry(f"+{x}+{y}")        
        popups.append(popup)

    main_root.mainloop()  # Start the event loop
    return monitors[clicked_monitor[0]-1]  # Return the clicked monitor number

all_windows = gw.getAllWindows()

python_windows = []
for window in all_windows:
    pid = win32process.GetWindowThreadProcessId(window._hWnd)[1]
    proc = psutil.Process(pid)
    if ('python.exe' in proc.name() or 'py.exe' in proc.name()) and ('Set Position' not in window.title):
        print(window.title)
        python_windows.append(window)

if len(python_windows) > 0:

    python_windows = sorted(python_windows, key=lambda x: int(re.search(r'\[(\d+)\]', x[1]).group(1)) if '[' in x[1] else float('-inf'))
    monitor = get_clicked_monitor()
    
    row, col = 5, 6
    width = abs(int(monitor.width/col)) + 20
    height = abs(int(monitor.height/row)) - 7

    x, y = monitor.x, monitor.y

    fill_row = 1
    for window in python_windows:
        try:
            hwnd = window
            hwnd.restore()
            hwnd.moveTo(x, y)
            hwnd.resizeTo(width, height)
            if fill_row == row:
                fill_row = 1
                x+=width - 14
                y = monitor.y
            else:
                fill_row += 1
                y+=height - 7
        except IndexError:
            pass
        except Exception as e:
            print(e)
        sleep(0.1)
else:
    print("No terminal Found !!!")
    sleep(2)

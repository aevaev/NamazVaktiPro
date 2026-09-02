import os
import sys

from src.app import App

# Bismillahirrahmanirrahim
# OOP,src layout customtkinter denemesi

def otomatk_baslat_ayarla():
    if os.name != "nt":return

    try:
        import winreg

        exe = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "NamazVaktiPro.exe")
            )

        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_SET_VALUE,
        ) as key:
            winreg.SetValueEx(
                key,
                "NamazVaktiPro",
                0,
                winreg.REG_SZ,
                f'"{exe}"',
            )

    except Exception as e:
        print(e)
        
if __name__ == "__main__":
    otomatk_baslat_ayarla()
    app = App()
    app.mainloop()

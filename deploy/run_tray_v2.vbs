Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "D:\TNT_AI\venture_foundry\media"
WshShell.Run "cmd /c D:\TNT_AI\venv\Scripts\pythonw.exe app\tray.py", 0, False

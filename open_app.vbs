Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
strDir = fso.GetParentFolderName(WScript.ScriptFullName)
WshShell.Run """" & strDir & "\open_app.bat""", 0, False
Set WshShell = Nothing
Set fso = Nothing

pyinstaller -F -i PTB.ico main.py -w

python PGBase64.py

pause

pyinstaller -F -i PTB.ico PTB-BlueprintReader-setup.py -w

dist\PTB-BlueprintReader-setup.exe

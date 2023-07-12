python store_img_to_py.py
pyinstaller -F -i ICO.ico main.py -w
echo "Generate exe success!"
pause

python PGBase64.py
pyinstaller -F -i ICO.ico PTB-BlueprintReader-setup.py -w
dist\PTB-BlueprintReader-setup.exe
echo "Generate setup exe success!"

pause
```

echo "Start generate exe..."
cd objs
python obj2base64.py
cd ..
cd images
python store_img_to_py.py
cd ..
pyinstaller -F --version-file main.txt -i ICO.ico main.py -w
echo "Generate exe success!"
pause

python Data\PGBase64.py
pause
pyinstaller -F --version-file setup.txt -i ICO.ico PTB-BlueprintReader-setup.py -w
dist\PTB-BlueprintReader-setup.exe
echo "Generate setup exe success!"

pause

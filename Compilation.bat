@echo off
REM -----------------------------------------------------
REM Creation du repertoire de build
REM -----------------------------------------------------
if not exist build mkdir build 
echo Verification/creation du repertoire 'build'.

REM -----------------------------------------------------
REM Changement vers le repertoire de build
REM -----------------------------------------------------
cd build
echo Change vers le repertoire build.

REM -----------------------------------------------------
REM Configuration avec CMake pour Visual Studio 2022 (version 17) pour une architecture x64
REM -----------------------------------------------------
cmake -G "Visual Studio 17 2022" -A x64 ..
echo Configuration CMake terminee.

REM -----------------------------------------------------
REM Construction du projet avec msbuild en mode Release
REM -----------------------------------------------------
msbuild CNN_Project.sln /p:Configuration=Release
echo Compilation avec msbuild terminee.

REM -----------------------------------------------------
REM Deplacement de l'exe à la racine du build
REM -----------------------------------------------------
move "Release\CNN_Project.exe" .
echo Deplacement de l'exe fini.

REM -----------------------------------------------------
REM Changement vers le repertoire python et construction du script python
REM -----------------------------------------------------
cd ../python
echo Change vers le repertoire python.
python setup.py build
echo Compilation Python terminee.

REM -----------------------------------------------------
REM Copie de l'executable CNN_Project.exe vers le dossier specifie
REM -----------------------------------------------------
echo Copie de CNN_Project.exe vers ..\out\build\x64-Release\App.
copy ..\build\Release\CNN_Project.exe ..\App\CNN_Project.exe
echo Copie terminee.

REM -----------------------------------------------------
REM Changement vers le repertoire de l'application
REM -----------------------------------------------------
cd ../App

REM Fin du script
echo Tâches completees.
pause

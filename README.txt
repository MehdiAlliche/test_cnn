Compilation simplifiée : Lancer le fichier Compilation.bat --> Fonctionne complètement, mais le code python et c++ ne sont pas encore suffisamment mature pour fonctionner en standalone ensemble.
Pour tester le code il est nécessaire d'uilisé l'exe du code c++ et le script python directement (Voir Partie 2 - c)

Environnement de développement : Visual Studio 2022 v17 en configuration x64-Release et avec Spyder Version 5

1  :  Explication de l'arborescence : 
	- include     : header du script c++
	- src         : fichier CNN_Project.cpp
	- python      : module_TI.py le script python et setup.py pour la génération de l'exe python, ainsi qu'un fichier indiquant les bibliothèques nécessaires à la compilation du script python
	- CMakeFiles  : Fichier créer par CMake 
	- build       : Sortie de la compilation de l'executable c++
	- App         : Sortie de la compilation de l'éxécutable python
	- Compilation.bat : Script de commande permettant de compiler la totaliter le script python et le script c++
	- requirements.txt : Montrant les dépendances utiles pour le script python et le bon fonctionnement de tensorflow sur cette version
	- CMakeLists.txt : Fichier CMake contenant les paramètres de compilation du script c++

2  :  Instruction de compilation et de lancement :
	2  -  a   : Le projet est composé de deux parties distinctes et liées : 
			- Le script python qui est dans le dossier python 
			- Le script c++ et son header, séparer dans le sous dossier src, et include

        2  -  b   : La compilation de l'exécutable c++ peut se faire de 2 façon différentes :
			- Soit directement avec l'application visual studio 2022 --> Build en mode x64-release, la compilation se fait dans le dossier out/build
			- Soit en ligne de commande [cd out/build  ; cmake -G "Visual Studio 17 2022" -A x64 ..  ; msbuild CNN_Project.sln /p:Configuration=Release ]
	
	2  -  c   : Il est alors possible d'utilisé l'exécutable c++ obtenue pour faire de la reconnaissance d'image, pour se faire : 
			- Se placer dans le répertoire de l'application soit : build
			- ouvrir un terminal 
			- lancer la ligne de commande suivante : .\CNN_Project.exe "MODEL_TYPE" "PATH\TO\IMAGE\"
				==> MODEL_TYPE peut prendre plusieurs valeurs  : [VGG16, VGG19, ResNet101, EfficientNetB7, DenseNet201, RegNetY320, Xception] Si une autre valeur est renseigner le script va s'arrêter et retourner une erreur 
				==> PATH\TO\IMAGE\ peut prendre 3 formes 
					- Le chemin d'une image
					- Le chemin de plusieurs images sous la forme "PATH1" "PATH2" "PATH3"
					- Le chemin d'un répertoire contenant plusieurs images aux formats JPG, JPEG, ou PNG (les autres formats ne sont pas pris en compte)


3  :  !! Attention : La partie compilation en exécutable et interfacage avec l'application c++ ne fonctionne pas !!
La compilation de l'éxécutable python se fait avec le script "setup.py" dans le dossier python avec la commande suivante (nécessite la librairie cx_freeze téléchargeable avec pip install cx_freeze) "python setup.py build"
Le dossier App est alors créer et contient toutes les dépendances pour utiliser l'application python en ligne de commande
Cependant, le script ne fonctionne pas correctement avec l'application. 






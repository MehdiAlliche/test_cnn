// Contient toutes les includes nécessaires
#include "CNN_Project.h"    

int
main(int argc, char* argv[])
{
    // Mis à 1 du paramètre TF_CPP_MIN_LOG_LEVEL pour éviter l'affichage d'information non essentiel par la bibliotèque tensorflow
    putenv("TF_CPP_MIN_LOG_LEVEL=1");
    // Noms pour le module Python
    PyObject* pName, * pModule, * pFunc, * pFunc_model, * pModel;
    // Arguments pour la fonction Python
    PyObject* pArgs, * pArgs_model;
    // Résultats de la prédiction
    PyObject* pValue = new PyObject;
    // Nom de la fonction de prédiction
    const char* func = "main";
    // Nom de la fonction de chargement du modèle
    const char* func_model = "model_choice";
    // Nom du fichier Python
    const char* python_file = "python.module_TI";

    int i;

    if (argc < 2) {
        fprintf(stderr, "Utilisation : Pas assez d'argument (2 requis) [args]\n");
        return 1;
    }

    Py_Initialize();
    // Vérification des erreurs de pName 
    pName = PyUnicode_DecodeFSDefault(python_file);

    // Chargement du fichier Python
    pModule = PyImport_Import(pName);

    Py_DECREF(pName);

    if (pModule != NULL) {

        // Initialiser les arguments pour la fonction de prédiction
        pArgs = PyTuple_New(argc - 1);
        // Initialiser les arguments pour charger le modèle  
        pArgs_model = PyTuple_New(1);
        // Récupérer le nom de la fonction à utiliser 
        pFunc_model = PyObject_GetAttrString(pModule, func_model);

        if (pFunc_model && PyCallable_Check(pFunc_model)) {
            // Préparer les arguments pour le choix du modèle
            PyTuple_SetItem(pArgs_model, 0, PyUnicode_DecodeFSDefault(argv[1]));
            // Obtenir le modèle dans un PyObject
            pModel = PyObject_CallObject(pFunc_model, pArgs_model);
            // libération de la mémoire
            Py_DECREF(pFunc_model);

            // Affichage d'une erreur en cas de model vide et arret du programme
            if (!pModel) {
                PyErr_Print();
                fprintf(stderr, "Impossible de charger le modèle\n");
                // libération de la mémoire
                Py_DECREF(pModel);
                Py_DECREF(pArgs);
                return 1;
            }
            // Ajouter le modèle dans les arguments pour la prédiction
            PyTuple_SetItem(pArgs, 0, pModel);
        }
        // Affichage d'une erreur si impossible de charger la fonction et arret
        else {
            if (PyErr_Occurred()) {
                PyErr_Print();
            }
            fprintf(stderr, "Erreur lors du chargement du modèle\n");
            return 1;
        }
        // obtenir le nom de la fonction de prédiction
        pFunc = PyObject_GetAttrString(pModule, func);
        if (pFunc && PyCallable_Check(pFunc)) {

            for (i = 0; i < argc - 2; ++i) {
                // Obtenir les arguments pour pFunc
                pValue = PyUnicode_DecodeFSDefault(argv[i + 2]);
                if (!pValue) {
                    fprintf(stderr, "Impossible de convertir l'argument\n");
                    Py_DECREF(pArgs);
                    Py_DECREF(pModule);
                    return 1;
                }
                // Rangement des valeurs dans un tuple 
                PyTuple_SetItem(pArgs, i + 1, pValue);
            }

            // Lancer pfunc avec les arguments 
            pValue = PyObject_CallObject(pFunc, pArgs);
            // Liberation de la mémoire
            Py_DECREF(pArgs);

            if (pValue != NULL) {
                // Récupération des sorties de la fonction de prédiction 1 = Resultats, 2 inférence time moyen sur l'échantillon d'image
                PyObject* pRes = PyTuple_GetItem(pValue, 0);
                PyObject* pInferenceTime = PyTuple_GetItem(pValue, 1);

                if (PyList_Check(pRes)) {
                    for (Py_ssize_t i = 0; i < PyList_Size(pRes); ++i) {
                        // Récupération des résultats pour chaque images
                        PyObject* pList = PyList_GetItem(pRes, i);

                        if (PyList_Check(pList)) {
                            // Afficher les éléments du tuple
                            PyObject_Print(PyList_GetItem(pList, 0), stdout, Py_PRINT_RAW);
                            if (PyFloat_AsDouble(PyTuple_GetItem(PyList_GetItem(pList, 0), 2)) < 0.5) {
                                printf("\n Attention : Précision faible : %f \n", PyFloat_AsDouble(PyTuple_GetItem(PyList_GetItem(pList, 0), 2)));
                            }
                            else {
                                printf("\n Haute précision : %f \n", PyFloat_AsDouble(PyTuple_GetItem(PyList_GetItem(pList, 0), 2)));
                            }
                            printf("\n");
                            // Liberartion de la mémoire 
                            Py_DECREF(pList);
                        }
                        // Affichage d'une erreur si les résultats ne sont pas de la forme attendu
                        else {
                            printf("Erreur : les résultats Python ne sont pas une liste \n");
                        }
                    }
                    // Affichage du temps d'inférence moyen
                    printf("Temps d'inférence : %f \n", PyFloat_AsDouble(pInferenceTime));
                    // Liberartion de la mémoire 
                    Py_DECREF(pValue);
                    Py_DECREF(pRes);
                    Py_DECREF(pInferenceTime);
                }
                // Affichage d'une erreur si les résultats ne sont pas de la forme attendu
                else
                    fprintf(stderr, "Les résultats de prédiction ne sont pas une liste \n");
                return 1;
            }
            else {
                // Affichage d'une erreur si la sortie de la fonction de prédiction est vide
                PyErr_Print();
                fprintf(stderr, "pValue est null");
                // Liberartion de la mémoire 
                Py_DECREF(pFunc);
                Py_DECREF(pModule);
                return 1;
            }
        }
        else {
            // Affichage d'une erreur si impossible de trouver la fonction d'identification (main)
            if (PyErr_Occurred())
                PyErr_Print();
            fprintf(stderr, "Impossible de trouver la fonction \"%s\"\n", func);
            return 1;
        }
        // Liberartion de la mémoire 
        Py_XDECREF(pFunc);
        Py_DECREF(pModule);
    }
    else {
        // Affichage d'une erreur en cas d'échec du chargement du script python
        PyErr_Print();
        fprintf(stderr, "Échec du chargement de \"%s\"\n", python_file);
        return 1;
    }
    // Finalisation de python
    if (Py_FinalizeEx() < 0) {
        return 120;
    }
    return 0;
}

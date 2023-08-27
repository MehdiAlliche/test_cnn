# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 18:21:22 2023

@author: Mehdi
"""
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import time
import os
import numpy as np
import sys

def model_choice(model_type):
    """
    Charge et retourne un modèle spécifié. Pour l'instant, seulement quelques modèles 
    proposés par Keras sont inclus. La liste complète des modèles est disponible sur:
    https://keras.io/api/applications/ 
    """
    # Toutes les vérification se font tout en minuscule pour éviter les erreurs de majuscules 
    if model_type.lower() =="VGG16".lower():
        print("Model load : "+model_type)
        model = tf.keras.applications.VGG16()
    elif model_type.lower() =="VGG19".lower():
        print("Model load : "+model_type)
        model = tf.keras.applications.VGG19()
    elif model_type.lower() =="ResNet101".lower():
        print("Model load : "+model_type)
        model = tf.keras.applications.ResNet101()
    elif model_type.lower() =="EfficientNetB7".lower():
        print("Model load : "+model_type)
        model = tf.keras.applications.EfficientNetB7()
    elif model_type.lower() =="DenseNet201".lower():
        print("Model load : "+model_type)
        model = tf.keras.applications.DenseNet201()
    elif model_type.lower() =="RegNetY320".lower():
        print("Model load : "+model_type)
        model = tf.keras.applications.RegNetY320()
    elif model_type.lower() =="Xception".lower():
        print("Model load : "+model_type)
        model = tf.keras.applications.Xception()
    
    model.compile()
    return model


def preprocess_img(img_path,model):
    """
    Charge une image, la pré-traite et la met au format attendu par le modèle.
    """
    img = image.load_img(img_path, target_size=model.input_shape[1:4])
    x = image.img_to_array(img) 
    x = np.expand_dims(x, axis=0) 
    model_type = model.get_config()['name'];
    # Toutes les vérification se font tout en minuscule pour éviter les erreurs de majuscules 
    if model_type.lower() =="VGG16".lower():       
        print("Preprocess model :  : "+model_type)
        x = tf.keras.applications.vgg16.preprocess_input(x)
    elif model_type.lower() =="VGG19".lower():
        print("Preprocess model :  : "+model_type)
        x = tf.keras.applications.vgg19.preprocess_input(x)
    elif model_type.lower() =="ResNet101".lower():
        print("Preprocess model :  : "+model_type)
        x = tf.keras.applications.resnet.preprocess_input(x)
    elif model_type.lower() =="EfficientNetB7".lower():
        print("Preprocess model :  : "+model_type)
        x = tf.keras.applications.efficientnet.preprocess_input(x)
    elif model_type.lower() =="DenseNet201".lower():
        print("Preprocess model :  : "+model_type)
        x= tf.keras.applications.densenet.preprocess_input(x)
    elif model_type.lower() =="RegNetY320".lower():
        print("Preprocess model :  : "+model_type)
        x= tf.keras.applications.regnet.preprocess_input(x)
    elif model_type.lower() =="Xception".lower():
        print("Preprocess model :  : "+model_type)
        x = tf.keras.applications.xception.preprocess_input(x)
    
    return x
    
    
def decode_predictions(x, model):
    """
    Décode les prédictions en fonction du modèle utilisé.
    """
     # Récupération du nom du modèle
    model_type = model.get_config()['name'];
    # Toutes les vérification se font tout en minuscule pour éviter les erreurs de majuscules 
    if model_type.lower() =="VGG16".lower():
        predict_model = tf.keras.applications.vgg16.decode_predictions(x,top=1)[0]
    elif model_type.lower() =="VGG19".lower():
        predict_model = tf.keras.applications.vgg19.decode_predictions(x,top=1)[0]
    elif model_type.lower() =="ResNet101".lower():
        predict_model = tf.keras.applications.resnet.decode_predictions(x,top=1)[0]
    elif model_type.lower() =="EfficientNetB7".lower():
        predict_model = tf.keras.applications.efficientnet.decode_predictions(x,top=1)[0]
    elif model_type.lower() =="DenseNet201".lower():
        predict_model = tf.keras.applications.densenet.decode_predictions(x,top=1)[0]
    elif model_type.lower() =="RegNetY320".lower():
        predict_model = tf.keras.applications.regnet.decode_predictions(x,top=1)[0]
    elif model_type.lower() =="Xception".lower():
        predict_model = tf.keras.applications.xception.decode_predictions(x,top=1)[0]
        
    return predict_model
    
    
def gen_model_cpp(model_type):
    """
    Sauvegarde le modèle pour une utilisation ultérieure.
    """
    model = model_choice(model_type)
    model.compile()
    # Sauvegarde du model avec le nom correspondant
    model.save(model_type+"_model",save_format="tf")

def main(model,*args):
    """
    Fonction principale qui accepte un modèle et une liste de chemins d'images ou 
    un répertoire contenant des images (formats supportés: JPG, PNG, JPEG).
    """
    # Vérification du bon nombre d'arguments
    if len(args) < 1 :  
        print("Il faut au moins 2 arguments!")
        sys.exit(1)
    elif len(args) == 1:  
        args = args[0]

    # préparation de la sortie de prediction
    results= [];
    inference_time=[];
    
    # Préparation de la liste des images à traiter
    list_img = [];
    if isinstance(args,str):
        if os.path.isdir(args):
            for fichier_name in os.listdir(args):
                if fichier_name.endswith(".jpg") or fichier_name.endswith(".png") or fichier_name.endswith(".jpeg"):
                    img_path = os.path.join(args, fichier_name).replace(" \ ", " / ")
                    list_img.append(img_path)   
        else:
            list_img = [args];
    else:
        list_img =  args;
    
    # Traitement des images et prédictions
    for i in range(len(list_img)):
        x = preprocess_img(list_img[i-1],model)
        if len(list_img)>10:
            if len(tf.config.list_physical_devices('GPU'))>0:
                print("GPU predict :")
                start_time = time.time()
                preds = model.predict(x);
                end_time = time.time()
                results.append(decode_predictions(preds,model));
                inference_time.append(end_time - start_time) 
            else:
                print("Impossible d'utiliser le GPU") 
        else:
            if len(tf.config.list_physical_devices('CPU'))>0:
                device = tf.device('CPU:0')
                with device:
                    print("CPU predict :")
                    start_time = time.time()
                    preds = model.predict(x);
                    end_time = time.time()
                    results.append(decode_predictions(preds,model));
                    inference_time.append(end_time - start_time) 
            else:
                print("Impossible d'utiliser le CPU")
                
    tf.keras.backend.clear_session()
    
    # Remplacement de la premieère données correspondant a un index, par le chemin de l'image utilisé pour la prédiction
    for index,sous_res in enumerate(results):
        if sous_res:
            sous_res[0]=list_img[index-1],sous_res[0][1],sous_res[0][2]

    return results, np.mean(inference_time)

if __name__ == "__main__":
    main()
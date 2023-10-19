import numpy as np
import cv2
import json
import joblib
import pywt
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

face_casade = cv2.CascadeClassifier("../opencv/lbpcascade_animeface.xml")
eye_casade = cv2.CascadeClassifier("../opencv/anime-eyes-cascade.xml")
def get_cropped_image_if_2_eyes(image_path:str):
    """
    this function about how to detect mata dari
    karakter anime
    Args:
        image_path (str): link testing gambar

    Returns: 
    """
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_casade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        eyes = eye_casade.detectMultiScale(roi_gray)
        if len(eyes) >= 2:
            return roi_color.astype(np.uint8)


def w2d(img, mode='haar', level=1):
    imArray = img
    #Datatype conversions
    #convert to grayscale
    imArray = cv2.cvtColor( imArray,cv2.COLOR_RGB2GRAY )
    #convert to float
    imArray =  np.float32(imArray)   
    imArray /= 255;
    # compute coefficients 
    coeffs=pywt.wavedec2(imArray, mode, level=level)

    #Process Coefficients
    coeffs_H=list(coeffs)  
    coeffs_H[0] *= 0;  

    # reconstruction
    imArray_H=pywt.waverec2(coeffs_H, mode);
    imArray_H *= 255;
    imArray_H =  np.uint8(imArray_H)

    return imArray_H

def image_to_array(img_file:str,resize:bool=True):
    img = cv2.imread(img_file)
    scalled_raw_img = cv2.resize(img,(32,32))
    img_hair = w2d(img,"db1",5)
    scalled_img_har = cv2.resize(img_hair,(32,32))
    combined_img = np.vstack((scalled_raw_img.reshape(32*32*3,1),
                              scalled_img_har.reshape(32*32,1)))
    if resize:
        return combined_img.reshape(combined_img.shape[1],
                                   combined_img.shape[0])\
                                    .astype(float)
    else:
        return combined_img
    
def result_waifu_generate(arr: np.ndarray,
                          saving_model_file: str,
                          label_json_file: str):
    # Load the saved model
    model = joblib.load(saving_model_file)

    # Predict using the loaded model
    predictions = make_pipeline(StandardScaler(),model.predict(arr))

    # Load label mapping from the JSON file
    with open(label_json_file, 'r') as json_file:
        label_mapping = json.load(json_file)

    # Map predictions to labels
    labels =[key for key,value in label_mapping.items() if value in predictions]
    
    return labels
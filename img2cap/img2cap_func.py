from django.conf import settings
from django.core.files.storage import FileSystemStorage

import matplotlib.pyplot as plt
import numpy as np
import os
import pickle
import cv2 # opencv-python

from PIL import Image # pillow
from konlpy.tag import Okt

import tensorflow.keras.applications.inception_v3
import tensorflow.keras.preprocessing.image
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras import models


#

# 이미지 인코딩
def encodeImage(img):
    base_url = settings.MEDIA_ROOT_URL + settings.MEDIA_URL
    encode_model = models.load_model(base_url+'models/encode_model.h5')
    img = img.resize((299, 299), Image.ANTIALIAS)
    x = tensorflow.keras.preprocessing.image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = tensorflow.keras.applications.inception_v3.preprocess_input(x)
    x = encode_model.predict(x)
    x = np.reshape(x, 2048)

    return x


#############################[ 영어 캡션 ]#####################################

# 영어 캡션 생성
def generateCaption(photo):

    base_url = settings.MEDIA_ROOT_URL + settings.MEDIA_URL

    caption_model = models.load_model(base_url+'models/caption_model_django.h5')

    with open(base_url + 'pickles/idxtoword.pkl', 'rb') as f:
        idxtoword = pickle.load(f)

    with open(base_url + 'pickles/wordtoidx.pkl', 'rb') as f:
        wordtoidx = pickle.load(f)

    with open(base_url + 'pickles/embedding_matrix.pkl', 'rb') as f:
        embedding_matrix= pickle.load(f)

    in_text = 'STARTSEQ'
    for i in range(49):
        sequence = [wordtoidx[w] for w in in_text.split() if w in wordtoidx]
        sequence = pad_sequences([sequence], maxlen=49)
        yhat = caption_model.predict([photo,sequence], verbose=0)
        yhat = np.argmax(yhat)
        word = idxtoword[yhat]
        in_text += ' ' + word
        if word == 'STOPSEQ':
            break
    final = in_text.split()
    final = final[1:-1]
    final = ' '.join(final)

    return final


# 영어 캡션 리턴
def printCaption(path):
    img = tensorflow.keras.preprocessing.image.load_img(path, target_size=(299, 299))
    image = encodeImage(img).reshape((1,2048))

    return generateCaption(image)


# 동영상 캡션 리턴
def printVidCaption(path):

    base_url = settings.MEDIA_ROOT_URL + settings.MEDIA_URL
    fs = FileSystemStorage()
    vidcap = cv2.VideoCapture(path)
    captions_list = []

    while vidcap.isOpened():
        success, image = vidcap.read()
        if success is True:
            if int((vidcap.get(1))%30==0):
                impath = base_url + "frame.jpg"
                cv2.imwrite(impath, image)
                cap = printCaption(impath)
                captions_list.append(cap)
                fs.delete(impath)
        else:
            break

    vidcap.release()

    return captions_list


#############################[ 한국어 캡션 ]#####################################

# 한국어 캡션 생성
def generateKorCaption(photo):

    base_url = settings.MEDIA_ROOT_URL + settings.MEDIA_URL

    caption_model = models.load_model(base_url+'models/caption-model_ko.h5')
    with open(base_url + 'pickles/idxtoword_ko.pkl', 'rb') as f:
        idxtoword = pickle.load(f)
    with open(base_url + 'pickles/wordtoidx_ko.pkl', 'rb') as f:
        wordtoidx = pickle.load(f)
    with open(base_url + 'pickles/embedding_matrix_ko.pkl', 'rb') as f:
        embedding_matrix= pickle.load(f)
    max_length = 144
    in_text = 'startseq'
    for i in range(max_length):
        sequence = [wordtoidx[w] for w in in_text.split() if w in wordtoidx]
        sequence = pad_sequences([sequence], maxlen=max_length)
        yhat = caption_model.predict([photo,sequence], verbose=0)
        yhat = np.argmax(yhat)
        word = idxtoword[yhat]
        in_text += ' ' + word
        if word == 'endseq':
            break
    final = in_text.split()
    final = final[1:-1]
    final = ' '.join(final)

    return final


# 한국어 캡션 리턴
def printKorCaption(path):
    img = tensorflow.keras.preprocessing.image.load_img(path, target_size=(299, 299))
    image = encodeImage(img).reshape((1,2048))

    return generateKorCaption(image)


# 해시태그 생성, 리턴
def find_nouns(sentence):
    okt = Okt()
    hashtags = okt.nouns(sentence)
    hashtags = '#'+'#'.join(hashtags)

    return hashtags

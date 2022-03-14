#!/usr/bin/env python
# coding: utf-8
import pywebio
import pickle
import numpy as np
import texthero as hero
import pandas as pd
import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text as text
from joblib import dump,load
from pywebio.platform.flask import webio_view
from pywebio import STATIC_PATH
from flask import Flask, send_from_directory
from pywebio.input import *
from pywebio.output import *
import argparse
from pywebio import start_server

import pickle
ntc_model=pickle.load(open('ntc_model','rb'))#ml model
ss=load('std_scaler.bin')#standardscaler model

app=Flask(__name__)
bert_preprocess = hub.load("https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3") 
bert_encoder = hub.load("https://tfhub.dev/tensorflow/bert_en_uncased_L-12_H-768_A-12/4")

le_name_mapping={0: 'BUSINESS', 1: 'EDUCATION', 2: 'ENTERTAINMENT', 3: 'FOOD & DRINK', 4: 'POLITICS', 5: 'SPORTS', 6: 'TECH', 7: 'WELLNESS'}

def predict():
    text= input("Enter The Data", type=TEXT)
    #text = textarea('Text Area', rows=3, placeholder='Some text')
    text=str(text)
    d_ = pd.DataFrame([text], columns = ['txt'])
    text=hero.clean(d_['txt'])#d_['txt'].pipe(hero.clean, custom_pipeline)
    bp_=bert_preprocess(text)
    vectors_=bert_encoder(bp_)['pooled_output']
    vec=ss.transform(vectors_)
    prediction=ntc_model.predict(vec)
    put_text('prediction = %r' % le_name_mapping[prediction[0]])
import os
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    
'''if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8080)
    args = parser.parse_args()
    start_server(predict, port=args.port)'''
#if __name__ == '__main__':
#   app.run(debug=True)
#app.add_url_rule('/ntc','webio_view',webio_view(predict),methods=['GET','POST','OPTIONS'])
#app.run(host='localhost',port=88)




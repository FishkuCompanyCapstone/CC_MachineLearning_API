import os 
import numpy as np
import requests
from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import load_img, img_to_array

app = Flask(__name__)
model = load_model('fish_classification.h5')
model_kembung=load_model('kembung_eye_freshness.h5')
model_bandeng=load_model('bandeng_eye_freshness.h5')
model_kuniran=load_model('kuniran_eye_freshness.h5')
model_mujair=load_model('mujair_eye_freshness.h5')
model_nila=load_model('nila_eye_freshness.h5')

@app.route('/classify', methods=['POST'])
def classify_fish():
    if 'photo_url' not in request.files:
        return jsonify({'error': 'No image uploaded.'}), 400
    url = request.files.get('photo_url')
    if not url:
        return
    tmp_file = f'img/{url.filename}'
    url.save(tmp_file)
    img = load_img(tmp_file, target_size=(150, 150))
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    images = np.vstack([img_array])
    prediction = model.predict(images, batch_size=32)
    if(prediction == [[1,0,0,0,0]]).all():
        fish= "bandeng"
    elif(prediction == [[0,1,0,0,0]]).all():
        fish= "kembung"
    elif(prediction == [[0,0,1,0,0]]).all():
        fish= "kuniran"
    elif(prediction == [[0,0,0,1,0]]).all():
        fish= "mujair"
    elif(prediction == [[0,0,0,0,1]]).all():
        fish= "nila"
    else :
        fish="not_classified"
    os.remove(tmp_file)
    return jsonify({
            'fish_name' : fish})
    
@app.route('/freshness', methods=['POST'])
def validate_image():
    if 'photo_url' not in request.files:
        return jsonify({'error': 'No image uploaded.'}), 400
    url = request.files.get('photo_url')
    fish= request.form.get('fish_name')
    if not url:
        return
    tmp_file = f'img/{url.filename}'
    url.save(tmp_file)
    img = load_img(tmp_file, target_size=(150, 150))
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    images = np.vstack([img_array])
    if(fish== "bandeng"):
        fresh_prediction= model_bandeng.predict(images,batch_size=32)
    elif(fish== "kembung"):
        fresh_prediction=model_kembung.predict(images,batch_size=32)
    elif(fish== "kuniran"):
        fresh_prediction=model_kuniran.predict(images,batch_size=32)
    elif(fish== "mujair"):
        fresh_prediction=model_mujair.predict(images,batch_size=32)
    elif(fish== "nila"):
        fresh_prediction=model_nila.predict(images,batch_size=32)
    os.remove(tmp_file)
    if(fresh_prediction==[1,0,0]).all():
        return jsonify({
            'prediction': "highly_fresh"})
    elif(fresh_prediction==[0,1,0]).all():
        return jsonify({
            'prediction': "fresh"})
    elif(fresh_prediction==[0,0,1]).all():
        return jsonify({
            'prediction': "not_fresh"})
    else :
        return jsonify({
            'prediction': "not_fish"})    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
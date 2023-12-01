import os 
from flask import Flask, request, jsonify, send_file
import requests
from google.cloud import storage
app = Flask(__name__)

@app.route('/upload-image', methods=['POST'])
def upload_image():
    file = request.files.get('image')
    if not file:
        return jsonify({'error': 'Image is required'}), 400,
    resize_image(file,'save_img.jpg')
    tmp_file = f'C:/Users/MSI GAMING/Documents/GitHub/CC_MachineLearning_API/img/{file.filename}'
    file.save(tmp_file)
    #url = gcs_upload_image(tmp_file)
    #os.remove(tmp_file)
    return jsonify({'url': "oke"})

def resize_image(url, output_file):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(output_file, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
    except:
        pass
    return


def gcs_upload_image(filename: str):
    storage_client: storage.Client = storage.Client()
    
    bucket: storage.Bucket = storage_client.bucket('fishku-bucket')
    blob: storage.Blob = bucket.blob(filename.split("/")[-1])
    blob.upload_from_filename(filename)
    blob.make_public()
    public_url: str = blob.public_url
    print(f"Image uploaded to {public_url}")
    os.remove(filename)
    return public_url

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
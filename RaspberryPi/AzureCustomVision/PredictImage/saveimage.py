import requests
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# URL of the image you want to download
image_url = "http://172.20.10.5/capture"

# Define the local file path where you want to save the image
local_file_path = "downloaded" + datetime.today().strftime('%Y%m%d%H%M%S') + ".jpg"

try:
    # Send an HTTP GET request to the image URL
    response = requests.get(image_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Open the local file for binary write
        with open(local_file_path, 'wb') as file:
            # Write the content of the response to the local file
            file.write(response.content)
        print(f"Image saved as {local_file_path}")
    else:
        print(f"Failed to download image. Status code: {response.status_code}")
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
    
endpoint = "https://hafidzganteng-prediction.cognitiveservices.azure.com/customvision/v3.0/Prediction/4dc628bf-eb73-418f-874f-2dab9acfd873/detect/iterations/Iteration2/image"
headers = {
    "Prediction-Key": "ebd3bbd9553340939db2f70491da2cbb",
    "Content-Type": "application/octet-stream",
}

image_data = open(local_file_path, "rb").read()

response = requests.post(endpoint, headers=headers, data=image_data)

if response.status_code == 200:
    predictions = response.json()
    
    image = Image.open(local_file_path)
    draw = ImageDraw.Draw(image)
    # Process and extract prediction results from 'predictions' JSON
    for prediction in predictions['predictions']:
        tag = prediction['tagName']
        probability = prediction['probability']
        bbox = prediction['boundingBox']
        
        if prediction['probability'] > 0.4:
        # Convert normalized bounding box coordinates to pixel coordinates
            x, y, w, h = map(float, [bbox['left'], bbox['top'], bbox['width'], bbox['height']])
            x, y, w, h = int(x * image.width), int(y * image.height), int(w * image.width), int(h * image.height)

            # Draw bounding box and label
            draw.rectangle([x, y, x + w, y + h], outline=(255, 0, 0), width=2)
            font = ImageFont.load_default()
            draw.text((x, y - 12), f"{tag}: {probability:.2f}", fill=(255, 0, 0), font=font)
            
        image.save(datetime.today().strftime('%Y%m%d%H%M%S') + ".jpg")
    
else:
    print("Prediction request failed with status code:", response.status_code)

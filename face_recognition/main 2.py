import os

input_dir = '/Users/sinchanagowda/Desktop/mini_project/frontend/face_recognition/data/raw'

for root, dirs, files in os.walk(input_dir):
    print(root)
    for filename in files:
        print(f"  {filename}")

import cv2
import face_recognition
import os

def preprocess_images(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for root, dirs, files in os.walk(input_dir):
        for filename in files:
            # Check if the file is a JPEG image
            if filename.lower().endswith(('.jpeg', '.jpg')):
                img_path = os.path.join(root, filename)
                print(f"Attempting to load image: {img_path}")
                img = cv2.imread(img_path)
                
                # Check if the image was read correctly
                if img is None:
                    print(f"Failed to load image {img_path}")
                    continue
                
                print(f"Processing image {img_path} with shape {img.shape} and dtype {img.dtype}")
                
                face_locations = face_recognition.face_locations(img)

                for i, (top, right, bottom, left) in enumerate(face_locations):
                    face_image = img[top:bottom, left:right]
                    face_filename = f"{os.path.splitext(filename)[0]}_face_{i}.jpg"
                    face_path = os.path.join(output_dir, face_filename)
                    cv2.imwrite(face_path, face_image)

# Specify the paths and call the function
input_dir = '/Users/sinchanagowda/Desktop/mini_project/frontend/face_recognition/data/raw'
output_dir = '/Users/sinchanagowda/Desktop/mini_project/frontend/face_recognition/data/processed'

preprocess_images(input_dir, output_dir)

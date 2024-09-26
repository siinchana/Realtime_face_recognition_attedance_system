import csv
import numpy as np

def load_encodings(csv_file_path):
    names = []
    encodings = []
    
    with open(csv_file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            name = row[0]
            encoding = np.array(row[1:], dtype=float)
            names.append(name)
            encodings.append(encoding)
    
    return names, encodings

import os
import bz2

# Paths to your compressed model files
compressed_shape_predictor_path = "/Users/sinchanagowda/Desktop/mini_project/frontend/face_recognition/models/shape_predictor_68_face_landmarks.dat.bz2"
compressed_face_recognition_model_path = "/Users/sinchanagowda/Desktop/mini_project/frontend/face_recognition/models/dlib_face_recognition_resnet_model_v1.dat.bz2"
# Paths to your extracted model files
shape_predictor_path = compressed_shape_predictor_path.replace('.bz2', '')
face_recognition_model_path = compressed_face_recognition_model_path.replace('.bz2', '')

# Function to extract .bz2 files
def extract_bz2(compressed_file, output_file):
    with bz2.BZ2File(compressed_file, 'rb') as file:
        with open(output_file, 'wb') as new_file:
            new_file.write(file.read())

# Extract the .dat files
if not os.path.exists(shape_predictor_path):
    extract_bz2(compressed_shape_predictor_path, shape_predictor_path)

if not os.path.exists(face_recognition_model_path):
    extract_bz2(compressed_face_recognition_model_path, face_recognition_model_path)

import os
import csv
import cv2
import dlib
import numpy as np

# Paths to your model files (already extracted)
shape_predictor_path = "/Users/sinchanagowda/Desktop/mini_project/frontend/face_recognition/models/shape_predictor_68_face_landmarks.dat"
face_recognition_model_path = "/Users/sinchanagowda/Desktop/mini_project/frontend/face_recognition/models/dlib_face_recognition_resnet_model_v1.dat"
known_faces_dir = "/Users/sinchanagowda/Desktop/mini_project/frontend/face_recognition/data/processed"  # Make sure this directory contains your known face images
csv_file_path = "/Users/sinchanagowda/Desktop/mini_project/frontend/face_recognition/models/encodings.csv"

# Load dlib models
detector = dlib.get_frontal_face_detector()
shape_predictor = dlib.shape_predictor(shape_predictor_path)
face_recognition_model = dlib.face_recognition_model_v1(face_recognition_model_path)

# List to hold names and encodings
known_names = []
known_encodings = []

# Process each image in the known faces directory
for filename in os.listdir(known_faces_dir):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        image_path = os.path.join(known_faces_dir, filename)
        image = cv2.imread(image_path)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Detect faces in the image
        faces = detector(rgb_image)
        
        # Debugging: Print number of faces detected
        print(f"Processing {filename}, Detected faces: {len(faces)}")
        
        # Assuming each image contains only one face
        for face in faces:
            shape = shape_predictor(rgb_image, face)
            encoding = face_recognition_model.compute_face_descriptor(rgb_image, shape)
            encoding = np.array(encoding)
            
            # Extract the name from the filename (without extension)
            name = os.path.splitext(filename)[0]
            
            known_names.append(name)
            known_encodings.append(encoding)
            break

# Debugging: Print number of encodings generated
print(f"Generated {len(known_encodings)} encodings.")

# Save encodings and names to a CSV file
with open(csv_file_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for name, encoding in zip(known_names, known_encodings):
        writer.writerow([name] + list(encoding))

print("Encodings saved to CSV file successfully.")


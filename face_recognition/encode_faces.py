import os
import face_recognition
import pandas as pd
from PIL import UnidentifiedImageError

def encode_faces(face_dir):
    encodings = []
    names = []

    for filename in os.listdir(face_dir):
        img_path = os.path.join(face_dir, filename)
        try:
            img = face_recognition.load_image_file(img_path)
            face_encodings = face_recognition.face_encodings(img)

            if face_encodings:
                encodings.append(face_encodings[0])
                name = filename.split('_face_')[0]  # Extract the person name
                names.append(name)
            else:
                print(f"No face encodings found for {img_path}")

        except UnidentifiedImageError:
            print(f"Skipping non-image file: {img_path}")

    # Convert encodings to list for CSV storage
    encodings_list = [encoding.tolist() for encoding in encodings]

    # Create a DataFrame
    df = pd.DataFrame({'name': names, 'encoding': encodings_list})
    return df

# Directory containing processed images
face_dir = '/Users/sinchanagowda/Desktop/face_recognition/data/processed'
df = encode_faces(face_dir)

# Save to CSV
csv_path = '/Users/sinchanagowda/Desktop/face_recognition/models/encodings.csv'
df.to_csv(csv_path, index=False)

print(f"Encodings saved to {csv_path}")

import pandas as pd
import ast

def load_encodings(csv_path):
    df = pd.read_csv(csv_path)
    df['encoding'] = df['encoding'].apply(ast.literal_eval)  # Convert string representation back to list
    return df

csv_path = '/Users/sinchanagowda/Desktop/mini_project/frontend/face_recognition/models/encodings.csv'
loaded_df = load_encodings(csv_path)

# Display the loaded DataFrame to verify contents
print(loaded_df.head())

# Check if the encodings are correct
for index, row in loaded_df.iterrows():
    print(f"Name: {row['name']}, Encoding Length: {len(row['encoding'])}")

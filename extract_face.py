import os
import cv2

# Chemins des dossiers
input_folder = "./Images_Peace"
output_folder = "./faces_peace"

# Crée le dossier de sortie s'il n'existe pas
os.makedirs(output_folder, exist_ok=True)

# Charger le modèle de détection de visage d'OpenCV (Haarcascade)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Parcourir toutes les images dans le dossier
for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):  # Vérifie les extensions valides
        image_path = os.path.join(input_folder, filename)
        image = cv2.imread(image_path)

        if image is None:
            print(f"Impossible de lire l'image : {filename}")
            continue

        # Convertir l'image en niveaux de gris
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Détection des visages
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for i, (x, y, w, h) in enumerate(faces):
            # Définir la taille 225x225 centrée sur le visage
            cx, cy = x + w // 2, y + h // 2
            half_size = 125 // 2

            # Calcul des coordonnées pour la découpe
            x1, y1 = max(cx - half_size, 0), max(cy - half_size, 0)
            x2, y2 = min(cx + half_size, image.shape[1]), min(cy + half_size, image.shape[0])

            # Extraire le visage
            face_crop = image[y1:y2, x1:x2]

            # Redimensionner exactement à 225x225 si les bords dépassent
            face_resized = cv2.resize(face_crop, (125, 125), interpolation=cv2.INTER_AREA)

            # Sauvegarder l'extraction
            output_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_face_{i}.jpg")
            cv2.imwrite(output_path, face_resized)
            print(f"Visage extrait et sauvegardé : {output_path}")

print("Traitement terminé !")
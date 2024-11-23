import os
import shutil
from sklearn.model_selection import train_test_split

# Dossier contenant les images classées par identités
input_folder = "chemin/vers/dataset_complet"
output_folder = "chemin/vers/dataset_organise"

# Crée les dossiers de sortie
os.makedirs(f"{output_folder}/train", exist_ok=True)
os.makedirs(f"{output_folder}/validation", exist_ok=True)
os.makedirs(f"{output_folder}/test", exist_ok=True)

# Parcours des dossiers (chaque dossier représente une classe/identité)
for class_name in os.listdir(input_folder):
    class_path = os.path.join(input_folder, class_name)
    if os.path.isdir(class_path):  # Vérifie qu'il s'agit d'un dossier
        images = [os.path.join(class_path, img) for img in os.listdir(class_path) if img.endswith(('png', 'jpg', 'jpeg'))]
        
        # Diviser les données
        train_imgs, temp_imgs = train_test_split(images, test_size=0.3, random_state=42)  # 70% train
        val_imgs, test_imgs = train_test_split(temp_imgs, test_size=0.5, random_state=42)  # 15% val, 15% test

        # Copier les fichiers dans les dossiers correspondants
        for img_path in train_imgs:
            shutil.copy(img_path, os.path.join(output_folder, "train", class_name))
        for img_path in val_imgs:
            shutil.copy(img_path, os.path.join(output_folder, "validation", class_name))
        for img_path in test_imgs:
            shutil.copy(img_path, os.path.join(output_folder, "test", class_name))

        print(f"Classe {class_name} : {len(train_imgs)} train, {len(val_imgs)} val, {len(test_imgs)} test.")

print("Séparation terminée !")

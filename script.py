import cv2
import os

def extract_frames(video_path, output_dir, frame_rate=1):
    """
    Extrait des frames d'une vidéo à un intervalle donné et les enregistre dans un répertoire.
    
    Args:
        video_path (str): Chemin vers le fichier vidéo.
        output_dir (str): Répertoire où les frames seront enregistrées.
        frame_rate (int): Nombre d'images à extraire par seconde.
    """
    # Ouvrir la vidéo
    video = cv2.VideoCapture(video_path)
    
    if not video.isOpened():
        print(f"Impossible d'ouvrir la vidéo : {video_path}")
        return

    # Obtenir le frame rate de la vidéo
    video_fps = int(video.get(cv2.CAP_PROP_FPS))
    frame_interval = int(video_fps / frame_rate)

    # Créer le dossier de sortie s'il n'existe pas
    os.makedirs(output_dir, exist_ok=True)
    
    frame_count = 607
    extracted_count = 607

    while True:
        ret, frame = video.read()
        if not ret:
            break

        # Extraire une frame tous les frame_interval
        if frame_count % frame_interval == 0:
            frame_name = f"frame_{extracted_count:04d}.jpg"
            frame_path = os.path.join(output_dir, frame_name)
            cv2.imwrite(frame_path, frame)
            print(f"Frame enregistrée : {frame_path}")
            extracted_count += 1

        frame_count += 1

    video.release()
    print(f"Extraction terminée. {extracted_count} frames extraites dans {output_dir}.")

# Exemple d'utilisation
video_file = "./Codes Drone5.mp4"  # Remplacez par le chemin de votre vidéo
output_folder = "output_frames"  # Répertoire où les images seront enregistrées
frames_per_second = 10  # Nombre d'images à extraire par seconde

extract_frames(video_file, output_folder, frames_per_second)

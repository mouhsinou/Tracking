from djitellopy import Tello
import cv2
import time

# Durée pendant laquelle la vidéo sera enregistrée (en secondes)
temps_de_vol = 60

# Initialiser et connecter le drone
drone = Tello()
drone.connect()

# Activer le flux vidéo
drone.streamon()

# Définir le codec et initialiser l'objet VideoWriter pour MP4
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('C://Users//EEIA//Desktop//DRONE_EEIA_2024//VID.mp4', fourcc, 20.0, (640, 480))

# Temps de début
temps_de_debut = time.time()

# Capture et enregistrement du flux vidéo
while True:
    
    if time.time() - temps_de_debut > temps_de_vol:
        break

    img = drone.get_frame_read().frame
    img_resized = cv2.resize(img, (640, 480))
    out.write(img_resized)

    cv2.imshow('Drone Video', img_resized)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Arrêter le flux vidéo et libérer les ressources
drone.streamoff()
out.release()
cv2.destroyAllWindows()

# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 08:27:19 2023

@author: HP
"""

from djitellopy import tello
import cv2
from ultralytics import YOLO
model = YOLO("best_2.pt")


drone = tello.Tello()
drone.connect()
print(drone.get_battery())
drone.streamon()
drone.takeoff()
drone.move_up(100)

limit1 = 32000
limit2 = 36000
limit = (limit1+limit2)/2
pErreurF = 0
pErreurA = 0
pErreurH = 0

def trakeFace(aire, pErreur):
    erreur = pErreur
    if aire == 0:
        devant =  0
    else:
        Kp = 0.001
        Kd = 0.001
        erreur = limit - aire
        
        devant = Kp*erreur + Kd*(erreur - pErreur) #+ Ki*sErreur
    return int(devant), erreur

def trakeAngle(centre, pErreur):
    erreur = pErreur
    if centre == 0:
        yaw =  0
    else:
        Kp = 0.25
        Kd = 0.1
        erreur = 320 - centre
        erreur = -erreur
        
        yaw = Kp*erreur + Kd*(erreur - pErreur) #+ Ki*sErreur
    return int(yaw), erreur



def trakeHauteur (centre, pErreur):
    erreur = pErreur
    if centre == 0:
        yaw =  0
    else:
        Kp = 0.3
        Kd = 0.1
        erreur = 320 - centre
        erreur = -erreur
        
        yaw = Kp*erreur + Kd*(erreur - pErreur) #+ Ki*sErreur
    return -int(yaw), erreur

    



def findFace(img):
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    results = model(img)
    bboxes = results[0].boxes
    coordList = []
    areaList = []
    boxes = results[0].boxes.xyxy.tolist()
    classes = results[0].boxes.cls.tolist()
    names = results[0].names
    confidences = results[0].boxes.conf.tolist()
    for box, cls, conf in zip(boxes, classes, confidences):
        x_min, y_min, x_max, y_max = box
        x , y = x_min, y_min
        w = x_max - x_min
        h = y_max - y_min
        cv2.rectangle(img,(int(x),int(y)),(int(x+w),int(y+h)),(255,0,0),2)
        cx = x + w//2
        cy = y + h//2
        cv2.circle(img, (int(cx), int(cy)), 5, (0,0,255), cv2.FILLED)
        coordList.append([cx, cy])
        areaList.append(w*h)
       
    if len(areaList) != 0:
        i = areaList.index(max(areaList))
        return img, [coordList[i], areaList[i]]
    else:
        return img, [[0, 0], 0]


while True:
    if drone.get_battery() < 20:
        drone.land()
        break

    img = drone.get_frame_read().frame
    img = cv2.resize(img, (640, 640))
    img, info = findFace(img)
    print("Center",info[0],"Aire : ", info[1])
    
    # Commande pour aller de l'avant ou derriere
    sortie = trakeFace(info[1], pErreurF)
    devant = sortie[0]
    pErreurF = sortie[1]
    
    # Commande pour tourner le drone
    sortie = trakeAngle(info[0][0], pErreurA)
    yaw = sortie[0]
    pErreurA = sortie[1]
    
    # Commande pour monter ou descendre le drone
    sortie = trakeHauteur(info[0][1], pErreurH)
    monter = sortie[0]
    pErreurH = sortie[1]
    
    drone.send_rc_control(0, devant, monter, yaw)
    print(devant, yaw)
    cv2.imshow("Image Drone", img)
    cv2.waitKey(1)











#!/usr/bin/env python
# Generacion de MArcador OnLine
# Para este proyecto ,debe ser de 6x6
# http://chev.me/arucogen/


import cv2
import cv2.aruco as aruco
import numpy as np


# In[44]:


aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)
# DICT_6X6_250 is an example of predefined dictionary of markers with 6x6 bits and a total of 250 markers.


# Crea imagen de 700x700
img = np.full((700, 700), 255, np.uint8)

# Pega primer marcador (Imagen de 200x200)
img[100:300, 100:300] = aruco.drawMarker(aruco_dict, 2, 200)
# Pega segundo marcador (Imagen de 200x200)
img[100:300, 400:600] = aruco.drawMarker(aruco_dict, 76, 200)
# Pega tercer marcador (Imagen de 200x200)
img[400:600, 100:300] = aruco.drawMarker(aruco_dict, 42, 200)
# Pega cuarto marcador (Imagen de 200x200)
img[400:600, 400:600] = aruco.drawMarker(aruco_dict, 123, 200)

# Difuminado de imagen
img = cv2.GaussianBlur(img, (11, 11), 0)

# Localización de los marcadores
corners, ids, _ = aruco.detectMarkers(img, aruco_dict)

# Obtiene uan versión en escala de grises de los marcadores
img_color = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

#  Dibujar los marcadores
aruco.drawDetectedMarkers(img_color, corners, ids)

# Muestra Imagenes
cv2.imshow('Created AruCo markers', img)
cv2.imshow('Detected AruCo markers', img_color)
cv2.waitKey(0)
cv2.destroyAllWindows()

cap = cv2.VideoCapture(0)
while True:
	status_cap, frame = cap.read()
	if not status_cap:
		break

	# Difuminado de imagen
	frame = cv2.GaussianBlur(frame, (11, 11), 0)

	#gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# Localización de los marcadores
	corners, ids, _ = aruco.detectMarkers(frame, aruco_dict)

	#  Dibujar los marcadores
	aruco.drawDetectedMarkers(frame, corners, ids)


#	faces = detector.detectMultiScale(gray, 1.3, 5)

#	for x, y, w, h in faces:
#		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
#		text_size, _ = cv2.getTextSize('Face', cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
		#cv2.rectangle(frame, (x, y - text_size[1]), (x + text_size[0], y), (255, 255, 255), cv2.FILLED)
		#cv2.putText(frame, 'Face', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
	cv2.imshow("Ventana", frame)

	if cv2.waitKey(1) == 27: 
		break

cap.release()
cv2.destroyAllWindows()


# In[ ]:





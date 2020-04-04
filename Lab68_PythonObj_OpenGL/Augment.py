# Enlace proyecto original:
# https://github.com/hughesj919/PyAugmentedReality
# Ejecución
# python3 Augment.py camera_params.txt
# Modificar N para cambiar el modelo

import cv2
import numpy as np
import glob
import pyzbar.pyzbar as pyzbar
import time
import pygame

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys
import os.path
import getopt

#global N
N = 0  # 0 -Despliega CONEJO (ROJO PARA ACABARLA)
N = 1  # 1 - Despliega Balon de Futbol
N = 2  # 2 - Despliega Gato
N = 3  # 3 -Despliega Balon (con Textura!

#NombreModelo="Balon.obj"
#NombreModelo="soccerball.obj"
#NombreModelo="Ball.obj"
NombreModelo3="12221_Cat_v1_l3.obj"
global obj
obj = None

NombreModelo="bunny.small.obj"
global obj2
obj2 = None

NombreModelo2="soccerball.obj"
global obj3
obj3 = None

NombreModelo4="NBA_BASKETBALL.obj"
global obj4
obj4 = None

currFrame = None
cap = None
fovx = None
fovy = None
fy = None
fx = None
principalX = None
principalY = None
focalLength = None
dist_co = None
cameraMatrix = None
image_shape = None
out = None
spheres = False
output = False
width = None
height = None
#lightZeroPosition = [20.0, 20.0, 20.0, 1.0]
#lightZeroPosition = [0.0, 0.0, -20.0, 1.0]
#lightZeroColor = [2.5, 2.5, 2.5, 1]
#lightZeroColor = [1.0, 1.0, 1.0, 1]
near = 1
far = 500
dimensiones_tetera=0.75
hullTemporal = None

font = cv2.FONT_HERSHEY_SIMPLEX

def MTL(filename):
    contents = {}
    mtl = None
    for line in open(filename, "r"):
        if line.startswith('#'): continue
        values = line.split()
        if not values: continue
        if values[0] == 'newmtl':
            mtl = contents[values[1]] = {}
        elif mtl is None:
            raise ValueError ("mtl file doesn't start with newmtl stmt")
            #X=1
        elif values[0] == 'map_Kd':
            # load the texture referred to by this declaration
            #mtl[values[0]] = values[1]
            #mtl[values[0]] = map(float, values[1:])
            print ("Valor de values",len(values),values[1],values[1:])
            if len(values)==2:
            	ValerVerg=1
            	surf = pygame.image.load(values[1])
            	image = pygame.image.tostring(surf, 'RGBA', 1)
            	ix, iy = surf.get_rect().size
            	texid = glGenTextures(1)
            	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,
		            GL_LINEAR)
            	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER,
		            GL_LINEAR)
            	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_RGBA,
		            GL_UNSIGNED_BYTE, image)

            else:			
            	mtl[values[0]] = list(map(float, values[1:]))
            	
        elif values[0] == 'map_Ka':
            # load the texture referred to by this declaration
            #mtl[values[0]] = values[1]
            #mtl[values[0]] = map(float, values[1:])
 #           print ("Valor de values",values[1],values[1:])
            print ("Valor de values",values[0],len(values),values[1],values[1:])
            if len(values)==2: # Incluye una Textura!
            	ValerVerg=1
            	surf = pygame.image.load(values[1])
            	image = pygame.image.tostring(surf, 'RGBA', 1)
            	ix, iy = surf.get_rect().size
            	texid = glGenTextures(1)
            	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,
		            GL_LINEAR)
            	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER,
		            GL_LINEAR)
            	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_RGBA,
		            GL_UNSIGNED_BYTE, image)

            else:			
            	mtl[values[0]] = list(map(float, values[1:]))
            	
        else:
            #mtl[values[0]] = map(float, values[1:])
            mtl[values[0]] = list(map(float, values[1:]))
    return contents

class OBJ:
    def __init__(self, filename, swapyz=False):
        """Loads a Wavefront OBJ file. """
        self.vertices = []
        self.normals = []
        self.texcoords = []
        self.faces = []

        material = None
        for line in open(filename, "r"):
            if line.startswith('#'): continue
            values = line.split()
            if not values: continue
            if values[0] == 'v':
                #v = map(float, values[1:4])
                v = list(map(float, values[1:4]))                       
                if swapyz:
                    v = v[0], v[2], v[1]
                self.vertices.append(v)
            elif values[0] == 'vn':
#                v = map(float, values[1:4])
                v = list(map(float, values[1:4]))
                if swapyz:
                    v = v[0], v[2], v[1]
                self.normals.append(v)
            elif values[0] == 'vt':
                #self.texcoords.append(map(float, values[1:3]))
                self.texcoords.append(list(map(float, values[1:3])))
            elif values[0] in ('usemtl', 'usemat'):
                material = values[1]
            elif values[0] == 'mtllib':
                self.mtl = MTL(values[1])
            elif values[0] == 'f':
                face = []
                texcoords = []
                norms = []
                for v in values[1:]:
                    w = v.split('/')
                    face.append(int(w[0]))
                    if len(w) >= 2 and len(w[1]) > 0:
                        texcoords.append(int(w[1]))
                    else:
                        texcoords.append(0)
                    if len(w) >= 3 and len(w[2]) > 0:
                        norms.append(int(w[2]))
                    else:
                        norms.append(0)
                self.faces.append((face, norms, texcoords, material))

        self.gl_list = glGenLists(1)
        glNewList(self.gl_list, GL_COMPILE)
        glEnable(GL_TEXTURE_2D)
        glFrontFace(GL_CCW)
        for face in self.faces:
            vertices, normals, texture_coords, material = face

            mtl = self.mtl[material]
            if 'texture_Kd' in mtl:
                # use diffuse texmap
                glBindTexture(GL_TEXTURE_2D, mtl['texture_Kd'])
            else:
                # just use diffuse colour
                glColor(*mtl['Kd'])

            glBegin(GL_POLYGON)
            for i in range(len(vertices)):
                if normals[i] > 0:
                    glNormal3fv(self.normals[normals[i] - 1])
                if texture_coords[i] > 0:
                    glTexCoord2fv(self.texcoords[texture_coords[i] - 1])
                glVertex3fv(self.vertices[vertices[i] - 1])
            glEnd()
        glDisable(GL_TEXTURE_2D)
        glEndList()

def decode(im): 
    # Find barcodes and QR codes
    decodedObjects = pyzbar.decode(im)
    # Print results
    for obj in decodedObjects:
        print('Type : ', obj.type)
        print('Data : ', obj.data,'\n')     
    return decodedObjects


def loadParams(params):
    global fovx, fovy, aspectRatio, principalX, principalY, focalLength, dist_co, image_shape, cameraMatrix, fx, fy
    if os.path.exists(params) and os.path.isfile(params):
        f = open(params)
        fovx = float(f.readline())
        fovy = float(f.readline())
        focalLength = float(f.readline())
        fx = float(f.readline())
        fy = float(f.readline())
        cameraMatrix = np.zeros((3, 3), np.float32)
        cameraMatrix[0, 0] = fx
        cameraMatrix[1, 1] = fy
        cameraMatrix[0, 2] = float(f.readline())
        principalX = cameraMatrix[0, 2]
        cameraMatrix[1, 2] = float(f.readline())
        principalY = cameraMatrix[1, 2]
        cameraMatrix[2, 2] = 1.0
        print("Camera Matrix")
        print(cameraMatrix)

        dist_co = [float(f.readline()), float(f.readline()), float(f.readline()), float(f.readline())]
        dist_co = np.asarray(dist_co)
    else:
        print("No parameter file.")

#
# Initialize video capture
#
def initVideoCapture(fileName):
    global cap, out, image_shape
    
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    if output:
        out = cv2.VideoWriter('output.avi',fourcc, 30.0, (640, 480))

    if fileName is not None:
        cap = cv2.VideoCapture(fileName)
    else:
        cap = cv2.VideoCapture(0)
    if cap is None or not cap.isOpened():
        print("Error starting capture")
        return None
    else:
        image_shape = (int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
    return cap
#
# Start our video capture
#
def startVideoCapture():

    global cap
#    cap.set(3,640)
#    cap.set(4,480)
    cap = initVideoCapture()
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Our operations on the frame come here
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Display the resulting frame
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

def keyboard(key, x, y):
    if key.decode("utf-8") == 'q':
        global cap
        cap.release()
        cv2.destroyAllWindows()
        exit()
    if key.decode("utf-8") == ' ':
        global spheres
        spheres = not spheres

#
# function to draw Axis
#
def drawAxis(length):
    BanderaPrueba=1


#
# Get the object points
#
# El plano donde el objeto se despliega el objeto
def getObjPoints():
    objp = np.zeros((3 * 3, 3), np.float32)
    objp[:, :2] = np.mgrid[0:3, 0:3].T.reshape(-1, 2)    
#    print ("matrizOBJ:")    
#    print (objp)
    return objp





def getImagePoints_prueba1():
    objp = np.zeros((3 * 3, 2), np.float32)

    print ("Hull Temporal:") 
    #print (hullTemporal)

    n = len(hullTemporal)     
    # Draw the convext hull
    for j in range(0,n):
        #cv2.line(currFrame, hull[j], hull[ (j+1) % n], (255,0,0), 3)        
        #print ("Puntos",hullTemporal[j], hullTemporal[ (j+1) % n])
        print ("\tPuntos",hullTemporal[j].x,hullTemporal[j].y)


	
    objp[0] = [hullTemporal[0].x,hullTemporal[0].y]
    objp[1] = [hullTemporal[0].x+5,hullTemporal[0].y]
    objp[2] = [hullTemporal[2].x,hullTemporal[0].y]

    objp[3] = [hullTemporal[0].x,hullTemporal[0].y+5]
    objp[4] = [hullTemporal[0].x+5,hullTemporal[0].y+5]
    objp[5] = [hullTemporal[2].x,hullTemporal[0].y+5]

    objp[6] = [hullTemporal[0].x,hullTemporal[1].y]
    objp[7] = [hullTemporal[0].x+5,hullTemporal[1].y]
    objp[8] = [hullTemporal[2].x,hullTemporal[1].y]


    #print ("matrizOBJ:")    
    #print (objp)
    return objp



def getImagePoints_prueba2(hull):
    objp = np.zeros((3 * 3, 2), np.float32)

    print ("Hull Analizado:") 
    #print (hullTemporal)

    n = len(hull)     
    # Draw the convext hull
    for j in range(0,n):
        #cv2.line(currFrame, hull[j], hull[ (j+1) % n], (255,0,0), 3)        
        #print ("Puntos",hullTemporal[j], hullTemporal[ (j+1) % n])
        print ("\tPuntos",hull[j].x,hull[j].y)

    objp[0] = [hull[0].x,hull[0].y]
    objp[1] = [hull[0].x+5,hull[0].y]
    objp[2] = [hull[2].x,hull[0].y]

    objp[3] = [hull[0].x,hull[0].y+5]
    objp[4] = [hull[0].x+5,hull[0].y+5]
    objp[5] = [hull[2].x,hull[0].y+5]

    objp[6] = [hull[0].x,hull[1].y]
    objp[7] = [hull[0].x+5,hull[1].y]
    objp[8] = [hull[2].x,hull[1].y]


    #print ("matrizOBJ:")    
    #print (objp)
    return objp
#
# image points test
#
def getImagePoints2():
    four_corners_img = ((600.0, 400.0), (620.0, 400.0), (600.0, 420.0), (620.0, 420.0))
    four_corners_img = np.reshape(np.asarray(four_corners_img), (4,1,2))
    return four_corners_img

def imprime_esquinas_formato_comprensible(corners):
	for i in range (corners.shape[0]):
		print ("Esquina i",i,corners[i])
#    print ("Filas ",corners.shape[0])
#    print ("Columnas ",corners.shape[1])
#    print ("Componentes ",corners.shape[2])
	return None
                        

#
# OpenGL display loop
#
def Objeto1(hullTemporal):
	if hullTemporal is not None:

		objp = getObjPoints()
		#corners2 = getImagePoints()

		#corners2 = getImagePoints_fin(ret, corners)
		#print (corners2)
		#corners2 = getImagePoints_prueba1()
		corners2 = getImagePoints_prueba2(hullTemporal)

		#criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
		#gray = cv2.cvtColor(currFrame, cv2.COLOR_BGR2GRAY)
		#corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)

		#print("Esquinas 2",corners2)
		imprime_esquinas_formato_comprensible(corners2)
		#print("Esquinas 2",corners2.shape)
		#print("Obj",objp.shape)
		#print("Obj",objp)
		imprime_esquinas_formato_comprensible(objp)

		ret, rotv, tvecs = cv2.solvePnP(objp, corners2, cameraMatrix, dist_co, None, None, 0, cv2.SOLVEPNP_ITERATIVE)

		#projectedImgPts, _ = cv2.projectPoints(objp, rotv, tvecs, cameraMatrix, dist_co)
		#j = 0
		#for i in projectedImgPts:
		#    cv2.circle(currFrame, (i[0][0], i[0][1]), 2, (0, 255, 0), -1)
		#    j = j+1


		if ret is True:
			rotMat, jacobian = cv2.Rodrigues(rotv)

			matrix = np.identity(4)
			matrix[0:3, 0:3] = rotMat
			matrix[0:3, 3:4] = tvecs
			newMat = np.identity(4)
			newMat[1][1] = -1
			newMat[2][2] = -1
			matrix = np.dot(newMat, matrix)
			matrix = matrix.T
			glLoadMatrixf(matrix)
			drawAxis(4.0)

			glPushMatrix()			
			glScalef(0.10,0.10,0.10)
			glRotatef(90, 1, 0, 0)
			glRotatef(180, 0, 1, 0)
			#glTranslatef(0.5, 0.0, 0.0)
			#glTranslatef(dimensiones_tetera, dimensiones_tetera*1.25, dimensiones_tetera/2.0)8
			#glTranslatef(dimensiones_tetera, dimensiones_tetera*1.25, dimensiones_tetera)
			
			#color = [1.0,1.0,1.0,1.0]
			#glLightfv(GL_LIGHT0, GL_POSITION, lightZeroPosition)
			#glLightfv(GL_LIGHT0, GL_DIFFUSE, lightZeroColor)
			#glMaterialfv(GL_FRONT_AND_BACK,GL_DIFFUSE,color)
				#glutSolidCube(2.0)
			#glutSolidTeapot(dimensiones_tetera)
			#glScalef(0.05,0.05,0.05)
			glCallList(obj.gl_list)
			#drawAxis(10.0)
			glPopMatrix()
		else:
			print("No checkerboard found.")

def Objeto2(hullTemporal):
	if hullTemporal is not None:
		objp = getObjPoints()
		corners2 = getImagePoints_prueba2(hullTemporal)

		imprime_esquinas_formato_comprensible(corners2)
		imprime_esquinas_formato_comprensible(objp)

		ret, rotv, tvecs = cv2.solvePnP(objp, corners2, cameraMatrix, dist_co, None, None, 0, cv2.SOLVEPNP_ITERATIVE)

		if ret is True:
			rotMat, jacobian = cv2.Rodrigues(rotv)

			matrix = np.identity(4)
			matrix[0:3, 0:3] = rotMat
			matrix[0:3, 3:4] = tvecs
			newMat = np.identity(4)
			newMat[1][1] = -1
			newMat[2][2] = -1
			matrix = np.dot(newMat, matrix)
			matrix = matrix.T
			glLoadMatrixf(matrix)
			drawAxis(4.0)

			glPushMatrix()
			#glTranslatef(3.5, 2.5, -2.5)
			glTranslatef(dimensiones_tetera/2.0, dimensiones_tetera/2.0, dimensiones_tetera/2.0)
			glTranslatef(0.0,1.0,0.0)
			glRotatef(180, 1, 0, 0)
			glRotatef(90, 0, 1, 0)
			glRotatef(90, 0, 0, 90)
			#color = [1.0,1.0,1.0,1.0]
			#glLightfv(GL_LIGHT0, GL_POSITION, lightZeroPosition)
			#glLightfv(GL_LIGHT0, GL_DIFFUSE, lightZeroColor)
			#glMaterialfv(GL_FRONT_AND_BACK,GL_DIFFUSE,color)
				#glutSolidCube(2.0)
			#glutSolidTeapot(dimensiones_tetera)
			#glScalef(0.25,0.25,0.25)
			#glCallList(obj.gl_list)
			glScalef(0.20,0.20,0.2)
			glCallList(obj2.gl_list)
			#drawAxis(10.0)
			glPopMatrix()
		else:
			print("No checkerboard found.")

def Objeto3(hullTemporal):
	if hullTemporal is not None:

		objp = getObjPoints()
		corners2 = getImagePoints_prueba2(hullTemporal)
		imprime_esquinas_formato_comprensible(corners2)
		imprime_esquinas_formato_comprensible(objp)

		ret, rotv, tvecs = cv2.solvePnP(objp, corners2, cameraMatrix, dist_co, None, None, 0, cv2.SOLVEPNP_ITERATIVE)

		if ret is True:
			rotMat, jacobian = cv2.Rodrigues(rotv)

			matrix = np.identity(4)
			matrix[0:3, 0:3] = rotMat
			matrix[0:3, 3:4] = tvecs
			newMat = np.identity(4)
			newMat[1][1] = -1
			newMat[2][2] = -1
			matrix = np.dot(newMat, matrix)
			matrix = matrix.T
			glLoadMatrixf(matrix)
			drawAxis(4.0)

			glPushMatrix()
			glScalef(0.25,0.25,0.25)
			glScalef(0.20,0.20,0.20)
			glCallList(obj3.gl_list)
			#drawAxis(10.0)
			glPopMatrix()
		else:
			print("No checkerboard found.")


def Objeto4(hullTemporal):
	if hullTemporal is not None:

		objp = getObjPoints()
		corners2 = getImagePoints_prueba2(hullTemporal)

		imprime_esquinas_formato_comprensible(corners2)
		imprime_esquinas_formato_comprensible(objp)

		ret, rotv, tvecs = cv2.solvePnP(objp, corners2, cameraMatrix, dist_co, None, None, 0, cv2.SOLVEPNP_ITERATIVE)

		if ret is True:
			rotMat, jacobian = cv2.Rodrigues(rotv)

			matrix = np.identity(4)
			matrix[0:3, 0:3] = rotMat
			matrix[0:3, 3:4] = tvecs
			newMat = np.identity(4)
			newMat[1][1] = -1
			newMat[2][2] = -1
			matrix = np.dot(newMat, matrix)
			matrix = matrix.T
			glLoadMatrixf(matrix)
			drawAxis(4.0)

			glPushMatrix()
			glTranslatef(dimensiones_tetera/2.0, dimensiones_tetera/2.0, dimensiones_tetera/2.0)
			glTranslatef(0.8, 0.8, 0.0)
			glScalef(0.05,0.05,0.05)
			glCallList(obj4.gl_list)
			glPopMatrix()
		else:
			print("No checkerboard found.")



def display():
    global fovy, aspectRatio, dist_co, cameraMatrix, currFrame, output, spheres
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    #currFrame=cv2.imread("QRsNuevos.png")
    hullTemporal=None
    hullTemporal2=None
    hullTemporal3=None
    hullTemporal4=None
    hull=None

    if currFrame is not None:
        conteo_objetos=0;
        hullTemporal=None
        decodedObjects = decode(currFrame)
        for decodedObject in decodedObjects: 
            points = decodedObject.polygon
     
        	# If the points do not form a quad, find convex hull
            if len(points) > 4 : 
                hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
                hull = list(map(tuple, np.squeeze(hull)))
            else : 
                hull = points;
            
			# Formato Fila-Columna
            print (hull) 

            #if conteo_objetos==0 :
                #global hullTemporal
             #   punto=1
             #   hullTemporal=hull

            #if conteo_objetos==1 :
            #    #global hullTemporal
            #    punto=1
            #    hullTemporal2=hull           

            conteo_objetos=conteo_objetos+1
            # Number of points in the convex hull
            n = len(hull)     
            # Draw the convext hull
            for j in range(0,n):
                cv2.line(currFrame, hull[j], hull[ (j+1) % n], (0,255,0), 3)

            x = decodedObject.rect.left
            y = decodedObject.rect.top

            #print(x, y)

            #print('Type : ', decodedObject.type)
            #print('Data : ', decodedObject.data,'\n')
			

            barCode = str(decodedObject.data)
            barCode=barCode.replace('http://','')[2:-1]	
            if barCode=='programacion': # CONEJO
                hullTemporal=hull
                print ("Conejo")

            if barCode=='matematicas':
                hullTemporal2=hull
                print ("EEE SUUUUSOSTO")

            if barCode=='fisica':
                hullTemporal3=hull
                print ("EEE SUUUUSOSTO")

            if barCode=='logica':
                hullTemporal4=hull
                print ("EEE SUUUUSOSTO")


            print('Data :-', barCode,'-')
            cv2.putText(currFrame, barCode, (x, y), font, 1, (0,0,0), 2, cv2.LINE_AA)


        #currFrame = cv2.undistort(currFrame, cameraMatrix, dist_co)
        flippedImage = cv2.flip(currFrame, 0)

        # draw the flipped image, set depth coord to 1.0 (having issue when set exactly to 1.0)
        glDisable(GL_DEPTH_TEST)
        # Para algunos funciona con .data y para otros con flippedImage
        #glDrawPixels(flippedImage.shape[1], flippedImage.shape[0], GL_BGR, GL_UNSIGNED_BYTE, flippedImage.data)
        glDrawPixels(flippedImage.shape[1], flippedImage.shape[0], GL_BGR, GL_UNSIGNED_BYTE, flippedImage)
        glEnable(GL_DEPTH_TEST)

        #setup our viewport
        glViewport(0, 0, width, height)

		# Esta de mas en el código original
        #currFrame = cv2.flip(currFrame, 0)
        glDisable(GL_DEPTH_TEST)
        glDrawPixels(currFrame.shape[1], currFrame.shape[0], GL_BGR, GL_UNSIGNED_BYTE, currFrame.data)
        glEnable(GL_DEPTH_TEST)


        #setup our project matrix
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        #set our projection matrix to perspective based on camera params

        # http://kgeorge.github.io/2014/03/08/calculating-opengl-perspective-matrix-from-opencv-intrinsic-matrix/
        print("Principal x: "+ str(principalX))
        print("Principal y: "+ str(principalY))
        print("fx:"+str(fx))
        print("fy:"+str(fy))
        print("height:"+str(height))
        print("width:"+str(width))

        glFrustum(-principalX / fx, (width - principalX) / fy, (principalY - height) / fy, principalY / fy, near, far)

        #setup our model view matrix
        glMatrixMode(GL_MODELVIEW)

        #glLightfv(GL_LIGHT0, GL_POSITION, lightZeroPosition)
        #glLightfv(GL_LIGHT0, GL_DIFFUSE, lightZeroColor)
        #glMaterialfv(GL_FRONT_AND_BACK,GL_DIFFUSE,color)

        glLoadIdentity()

        if N == 0:
	#		print "You typed zero.\n"
			#global obj
			#obj = OBJ(NombreModelo, swapyz=True)
        	Objeto1(hullTemporal) # Conejo (ROJO)
        elif N== 1:
	#		print "n is a perfect square\n"
			#global obj2
			#obj2 = OBJ(NombreModelo2, swapyz=True)
        	Objeto2(hullTemporal2) # Balon Soccer (ROJO??!!)        
        elif N == 2:
	#		print "n is an even number\n"
			#global obj3
			#obj3 = OBJ(NombreModelo3, swapyz=True)
        	Objeto3(hullTemporal3) # Gato 
        elif  N== 3:
	#		print "n is a prime number\n"
			#global obj4
			#obj4 = OBJ(NombreModelo4, swapyz=True)
        	Objeto4(hullTemporal4) # Balon Basket

#        glColor3f(1.0,1.0,1.0);
#        Objeto1(hullTemporal) # Conejo (ROJO)

#        glColor3f(1.0,1.0,1.0);
#        Objeto2(hullTemporal2) # Balon Soccer (ROJO??!!)        

#        glColor3f(1.0,1.0,1.0);
#        Objeto3(hullTemporal3) # Gato 

#        glColor3f(1.0,1.0,1.0);
#        Objeto4(hullTemporal4) # Balon Basket



    glutSwapBuffers()
    glutPostRedisplay()

#
# OpenGl reshape
#
def reshape(w, h):
    glViewport(0, 0, w, h)

#
# OpenGL Idle Loop
#
def idle():
    global currFrame
    ret, frame = cap.read()
    if ret is True:
        currFrame = frame
#
# Main Camera Calibration and OpenGL loop
#
def main():
    global width, height
    

    args, params = getopt.getopt(sys.argv[1:], '', ['video_name='])
    args = dict(args)
    video_name = args.get('--video_name')

    loadParams(params[0])
    initVideoCapture(video_name)
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    print(image_shape)
    width = image_shape[1]
    height = image_shape[0]
    glutInitWindowSize(image_shape[1], image_shape[0])

    glutCreateWindow("OpenGL / OpenCV Example")

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_CULL_FACE)

    #we cull the front faces because my depth values are reversed from typical 0 to 1
    glCullFace(GL_FRONT)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_DEPTH_TEST)

    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    glutReshapeFunc(reshape)
    glutIdleFunc(idle)

    glLightfv(GL_LIGHT0, GL_POSITION,  (0, 0, 100, 0.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)           # most obj files expect to be smooth-shaded

    if N == 0:
#		print "You typed zero.\n"
    	global obj
    	obj = OBJ(NombreModelo, swapyz=True)
    elif N== 1:
#		print "n is a perfect square\n"
    	global obj2
    	obj2 = OBJ(NombreModelo2, swapyz=True)
    elif N == 2:
#		print "n is an even number\n"
    	global obj3
    	obj3 = OBJ(NombreModelo3, swapyz=True)
    elif  N== 3:
#		print "n is a prime number\n"
    	global obj4
    	obj4 = OBJ(NombreModelo4, swapyz=True)

#    global obj
#    obj = OBJ(NombreModelo, swapyz=True)

#    global obj2
#    obj2 = OBJ(NombreModelo2, swapyz=True)

#    global obj3
#    obj3 = OBJ(NombreModelo3, swapyz=True)

#    global obj4
#    obj4 = OBJ(NombreModelo4, swapyz=True)

    glutMainLoop()


if __name__ == '__main__':
    main()


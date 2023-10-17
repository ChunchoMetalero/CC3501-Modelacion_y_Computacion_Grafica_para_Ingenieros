### Juan Ignacio Valdivia ###
### 21.087.645-6 ###
### Juan.valdivia.g@ug.uchile.cl ###

# coding=utf-8

import pyglet
import numpy as np
from OpenGL.GL import *
from math import sin, cos
from grafica import basic_shapes as bs
from grafica import easy_shaders as es
from grafica import transformations as tr
from grafica import scene_graph as sg
from grafica.assets_path import getAssetPath
import grafica.lighting_shaders as ls

# Controlador que permite comunicarse con la ventana de pyglet
class Controller(pyglet.window.Window):

    def __init__(self, width, height, title="Tarea 2 - Juan Ignacio Valdivia"):
        super().__init__(width, height, title)
        self.total_time = 0.0
        self.fillPolygon = True
        self.showAxis = True
        self.pipeline = None
        self.repeats = 0
        self.Camera_Position = np.array([6,6,7])
        self.Camera_OBJ = np.array([0,0,3])
        self.Position_X = 0
        self.Position_Y = 0
        self.Position_Z = 0
        self.Cam_Position_X = 0
        self.Cam_Position_Y = 0
        self.Cam_Position_Z = 0
        self.speedX = 0
        self.speedY = 0
        self.speedZ = 0
        self.Cam_speedX = 0
        self.Cam_speedY = 0
        self.Cam_speedZ = 0
        self.camera_rotation_speedx = 0.0
        self.camera_rotation_anglex = 0.0
        self.camera_rotation_speedy = 0.0
        self.camera_rotation_angley = 0.0
        self.camera_rotation_speedz = 0.0
        self.camera_rotation_anglez = 0.0

# Se asigna el ancho y alto de la ventana y se crea.
WIDTH, HEIGHT = 1280, 720
controller = Controller(width=WIDTH, height=HEIGHT)

# Se asigna el color de fondo de la ventana
glClearColor(78/255, 92/255, 205/255, 1.0)

# Como trabajamos en 3D, necesitamos chequear cuáles objetos están en frente, y cuáles detrás.
glEnable(GL_DEPTH_TEST)

# Se configura el pipeline
mvpPipeline = es.SimpleModelViewProjectionShaderProgram()
textureGouraudPipeline = ls.SimpleGouraudShaderProgram()
controller.pipeline = mvpPipeline
lightingPipeline = textureGouraudPipeline

# El controlador puede recibir inputs del usuario. Estas funciones define cómo manejarlos.
@controller.event
def on_key_press(symbol, modifiers):
    # Controles Mariposa
    if symbol == pyglet.window.key.E:
        controller.fillPolygon = not controller.fillPolygon

    elif symbol == pyglet.window.key.LSHIFT:
        controller.showAxis = not controller.showAxis
    
    elif symbol == pyglet.window.key.A:
        controller.speedX -= 3

    elif symbol == pyglet.window.key.D:
        controller.speedX += 3

    elif symbol == pyglet.window.key.W:
        controller.speedY -= 3

    elif symbol == pyglet.window.key.S:
        controller.speedY += 3

    elif symbol == pyglet.window.key.LCTRL:
        controller.speedZ -= 3

    elif symbol == pyglet.window.key.SPACE:
        controller.speedZ += 3  

    # Controles Camara
    elif symbol == pyglet.window.key.L:
        controller.Cam_speedX -= 3

    elif symbol == pyglet.window.key.J:
        controller.Cam_speedX += 3

    elif symbol == pyglet.window.key.O:
        controller.Cam_speedY -= 3

    elif symbol == pyglet.window.key.U:
        controller.Cam_speedY += 3

    elif symbol == pyglet.window.key.K:
        controller.Cam_speedZ -= 3

    elif symbol == pyglet.window.key.I:
        controller.Cam_speedZ += 3          

    elif symbol == pyglet.window.key.LEFT:
        controller.camera_rotation_speedz += 1.0

    elif symbol == pyglet.window.key.RIGHT:
        controller.camera_rotation_speedz -= 1.0

    elif symbol == pyglet.window.key.UP:
        controller.camera_rotation_speedy += 1

    elif symbol == pyglet.window.key.DOWN:
        controller.camera_rotation_speedy -= 1

    elif symbol == pyglet.window.key.UP:
        controller.camera_rotation_speedy += 1

    elif symbol == pyglet.window.key.DOWN:
        controller.camera_rotation_speedy -= 1 

    elif symbol == pyglet.window.key.M:
        controller.camera_rotation_speedx += 1

    elif symbol == pyglet.window.key.N:
        controller.camera_rotation_speedx -= 1  
    
    elif symbol == pyglet.window.key.ESCAPE:
        controller.close()
    else:
        print('Unknown key')

@controller.event
def on_key_release(symbol, modifiers):
    # Mariposa
    if symbol == pyglet.window.key.A:
        controller.speedX = 0

    elif symbol == pyglet.window.key.D:
        controller.speedX = 0

    elif symbol == pyglet.window.key.W:
        controller.speedY = 0

    elif symbol == pyglet.window.key.S:
        controller.speedY = 0

    elif symbol == pyglet.window.key.LCTRL:
        controller.speedZ = 0

    elif symbol == pyglet.window.key.SPACE:
        controller.speedZ = 0 

    # Camara
    elif symbol == pyglet.window.key.LEFT:
        controller.camera_rotation_speedz = 0

    elif symbol == pyglet.window.key.RIGHT:
        controller.camera_rotation_speedz = 0

    elif symbol == pyglet.window.key.UP:
        controller.camera_rotation_speedy = 0

    elif symbol == pyglet.window.key.DOWN:
        controller.camera_rotation_speedy = 0    

    elif symbol == pyglet.window.key.M:
        controller.camera_rotation_speedx = 0

    elif symbol == pyglet.window.key.N:
        controller.camera_rotation_speedx = 0

    elif symbol == pyglet.window.key.J:
        controller.Cam_speedX = 0

    elif symbol == pyglet.window.key.L:
        controller.Cam_speedX = 0

    elif symbol == pyglet.window.key.U:
        controller.Cam_speedY = 0

    elif symbol == pyglet.window.key.O:
        controller.Cam_speedY = 0

    elif symbol == pyglet.window.key.I:
        controller.Cam_speedZ = 0

    elif symbol == pyglet.window.key.K:
        controller.Cam_speedZ = 0  

def readFaceVertex(faceDescription):

    aux = faceDescription.split('/')

    assert len(aux[0]), "Vertex index has not been defined."

    faceVertex = [int(aux[0]), None, None]

    assert len(aux) == 3, "Only faces where its vertices require 3 indices are defined."

    if len(aux[1]) != 0:
        faceVertex[1] = int(aux[1])

    if len(aux[2]) != 0:
        faceVertex[2] = int(aux[2])

    return faceVertex

def readOBJ(filename, color):

    vertices = []
    normals = []
    textCoords= []
    faces = []

    with open(filename, 'r') as file:
        for line in file.readlines():
            aux = line.strip().split(' ')
            
            if aux[0] == 'v':
                vertices += [[float(coord) for coord in aux[1:]]]

            elif aux[0] == 'vn':
                normals += [[float(coord) for coord in aux[1:]]]

            elif aux[0] == 'vt':
                assert len(aux[1:]) == 2, "Texture coordinates with different than 2 dimensions are not supported"
                textCoords += [[float(coord) for coord in aux[1:]]]

            elif aux[0] == 'f':
                N = len(aux)                
                faces += [[readFaceVertex(faceVertex) for faceVertex in aux[1:4]]]
                for i in range(3, N-1):
                    faces += [[readFaceVertex(faceVertex) for faceVertex in [aux[i], aux[i+1], aux[1]]]]

        vertexData = []
        indices = []
        index = 0

        # Per previous construction, each face is a triangle
        for face in faces:

            # Checking each of the triangle vertices
            for i in range(0,3):
                vertex = vertices[face[i][0]-1]
                normal = normals[face[i][2]-1]

                vertexData += [
                    vertex[0], vertex[1], vertex[2],
                    color[0], color[1], color[2],
                    normal[0], normal[1], normal[2]
                ]

            # Connecting the 3 vertices to create a triangle
            indices += [index, index + 1, index + 2]
            index += 3        

        return bs.Shape(vertexData, indices)

def createGPUShape(pipeline, shape):
        gpuShape = es.GPUShape().initBuffers()
        pipeline.setupVAO(gpuShape)
        gpuShape.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)
        return gpuShape

# Funcion para crear nuestra Mariposa
def CreateButterfly(pipeline,r,g,b):

    # Creating shapes on GPU memory
    Cilindro = bs.createColorCylinderTarea2(r,g,b)
    gpuCilindro = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuCilindro)
    gpuCilindro.fillBuffers(Cilindro.vertices,Cilindro.indices, GL_STATIC_DRAW)

    Esfera_Amarilla = bs.createColorSphereTarea2(r,g,b)
    gpuEsfera_Amarilla = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuEsfera_Amarilla)
    gpuEsfera_Amarilla.fillBuffers(Esfera_Amarilla.vertices,Esfera_Amarilla.indices, GL_STATIC_DRAW)

    Esfera_Celeste = bs.createColorSphereTarea2(64/255,191/255,236/255)
    gpuEsfera_Celeste = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuEsfera_Celeste)
    gpuEsfera_Celeste.fillBuffers(Esfera_Celeste.vertices,Esfera_Celeste.indices, GL_STATIC_DRAW)

    Cubo = bs.createColorCube(r,g,b)
    gpuCubo = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuCubo)
    gpuCubo.fillBuffers(Cubo.vertices, Cubo.indices, GL_STATIC_DRAW)


    # Creando el cuerpo
    Cuerpo1 = sg.SceneGraphNode("Cuerpo1")
    Cuerpo1.childs += [gpuCilindro]

    Cuerpo2 = sg.SceneGraphNode("Cuerpo2")
    Cuerpo2.childs += [gpuEsfera_Amarilla]

    CuerpoSup = sg.SceneGraphNode("CuerpoSup")
    CuerpoSup.transform = tr.translate(0,1,0)
    CuerpoSup.childs += [Cuerpo2]

    CuerpoInf = sg.SceneGraphNode("CuerpoInf")
    CuerpoInf.transform = tr.translate(0,-1,0)
    CuerpoInf.childs += [Cuerpo2]

    Cuerpo = sg.SceneGraphNode("Cuerpo")
    Cuerpo.transform = tr.matmul([
    
    tr.scale(0.15,0.15,0.5),
    tr.rotationX(np.pi/2)
    ])
    Cuerpo.childs += [Cuerpo1]
    Cuerpo.childs += [CuerpoSup]
    Cuerpo.childs += [CuerpoInf]

    # Creando las alas
    Ala = sg.SceneGraphNode("Ala")
    Ala.childs += [gpuEsfera_Celeste]
    
    #Ala Superior Derecha
    AlaDerechaSupRot = sg.SceneGraphNode("AlaDerechaSupRot")
    AlaDerechaSupRot.transform = tr.matmul([
        tr.rotationY(np.pi/4),
        tr.scale(0.5,0.02,0.9),
    ])
    AlaDerechaSupRot.childs += [Ala]

    AlaDerechaSup = sg.SceneGraphNode("AlaDerechaSup")
    AlaDerechaSup.transform = tr.translate(0.87,0,0.5)
    AlaDerechaSup.childs= [AlaDerechaSupRot]

    # Ala Inferior Derecha
    AlaDerechaInfRot = sg.SceneGraphNode("AlaDerechaInfRot")
    AlaDerechaInfRot.transform = tr.matmul([
        tr.rotationY(np.pi/4),
        tr.scale(-0.5,0.02,0.9),
        ])
    AlaDerechaInfRot.childs += [Ala]

    AlaDerechaInf = sg.SceneGraphNode("AlaDerechaInf")
    AlaDerechaInf.transform = tr.matmul([
        tr.translate(0.72,0,-0.45),
        tr.scale(-0.8,1,1)
    ])
    AlaDerechaInf.childs= [AlaDerechaInfRot]

    # Ala Derecha
    AlaDerecha = sg.SceneGraphNode("AlaDerecha")
    AlaDerecha.childs += [AlaDerechaSup]
    AlaDerecha.childs += [AlaDerechaInf]

    # Ala Izquierda
    AlaIzquierda = sg.SceneGraphNode("AlaIzquierda")
    AlaIzquierda.transform = tr.scale(-1,1,1)
    AlaIzquierda.childs += [AlaDerecha]

    # Alas completas
    Alas = sg.SceneGraphNode("Alas")
    Alas.transform = tr.rotationZ(0)
    Alas.childs += [AlaDerecha]
    Alas.childs += [AlaIzquierda]

    # Mariposa Completa
    Mariposa = sg.SceneGraphNode("Mariposa")
    Mariposa.childs += [Cuerpo]
    Mariposa.childs += [Alas]
    
    return Mariposa

# Funcion para crear el piso
def CreateSuelo(pipeline):
    # Creating shapes on GPU memory
    Cubo_Verde = bs.createColorCube(35/255,155/255,86/255)
    gpuCubo_Verde = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuCubo_Verde)
    gpuCubo_Verde.fillBuffers(Cubo_Verde.vertices,Cubo_Verde.indices, GL_STATIC_DRAW)

    # Suelo
    suelo = sg.SceneGraphNode("suelo")
    suelo.transform = tr.matmul([
        tr.scale(100,100,0.01),
        tr.translate(0,0,-0.5)
    ])
    suelo.childs = [gpuCubo_Verde]

    suelofinal = sg.SceneGraphNode("suelofinal")
    suelofinal.childs += [suelo]

    return suelofinal

# Funcion utilizada para hacer un arbol
def CreateBosque(pipeline):
    # Creating shapes on GPU memory
    Cilindro_Cafe = bs.createColorCylinderTarea2(120/255,66/255,18/255)
    gpuCilindro_Cafe = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuCilindro_Cafe)
    gpuCilindro_Cafe.fillBuffers(Cilindro_Cafe.vertices,Cilindro_Cafe.indices, GL_STATIC_DRAW)

    Cono_Verde = bs.createColorConeTarea2(35/255,155/255,86/255)
    gpuCono_Verde = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuCono_Verde)
    gpuCono_Verde.fillBuffers(Cono_Verde.vertices,Cono_Verde.indices, GL_STATIC_DRAW)

    # Arboles

    # Tronco
    Tronco = sg.SceneGraphNode("Tronco")
    Tronco.transform = tr.matmul([
        tr.translate(0,0,3.5),
        tr.scale(0.5,0.5,3.5),
        tr.rotationX(np.pi/2),
    ])
    Tronco.childs += [gpuCilindro_Cafe]

    # Copa
    Copa = sg.SceneGraphNode("Copa")
    Copa.transform = tr.matmul([
        tr.translate(0,0,10),
        tr.scale(1.5,1.5,3.5),
        tr.rotationX(np.pi/2),
    ])
    Copa.childs += [gpuCono_Verde]

    # Arbol Completo
    Arbol = sg.SceneGraphNode("Arbol")
    Arbol.childs += [Copa]
    Arbol.childs += [Tronco]
                     
    # Bosque
    Bosque2 = sg.SceneGraphNode("Bosque2")
    Bosque2.childs += [Arbol]

    return Bosque2


# Creating shapes on GPU memory
cpuAxis = bs.createAxis(7)
gpuAxis = es.GPUShape().initBuffers()
mvpPipeline.setupVAO(gpuAxis)
gpuAxis.fillBuffers(cpuAxis.vertices, cpuAxis.indices, GL_STATIC_DRAW)

SueloNode = CreateSuelo(mvpPipeline)
MariposaNode = CreateButterfly(mvpPipeline,24/255,24/255,24/255)
BosqueNode = CreateBosque(mvpPipeline)

# La mariposa tiene acceso al internet :D
Porsche = readOBJ(getAssetPath('Porsche_911_GT2.obj'), (1, 1, 1))
gpuPorsche = createGPUShape(textureGouraudPipeline, Porsche)

Carretera = readOBJ(getAssetPath('road.obj'),(51/255,53/255,72/255))
gpuCarretera = createGPUShape(textureGouraudPipeline, Carretera)

# Funcion utilizada para crear el conjunto de arboles
def Arboles(BosqueNode):
    Bosque_Completo = sg.SceneGraphNode("Bosque_Node")

    for i in range(0, 10):
        for j in range(1, 10):
            # Calcular los desplazamientos en las coordenadas x e y
            x_offset = 2 + j * 5
            y_offset = 2 + i * 5

            # Crear el nodo de los árboles
            ArbolesNode = sg.SceneGraphNode("ArbolesAux" + str(i))
            ArbolesNode.transform = tr.translate(x_offset, y_offset, 0)
            ArbolesNode.childs = [BosqueNode]

            Arboles1 = sg.SceneGraphNode("Arboles1Aux" + str(i))
            Arboles1.transform = tr.translate(-1*x_offset, y_offset, 0)
            Arboles1.childs = [BosqueNode]

            Arboles2 = sg.SceneGraphNode("Arboles2Aux" + str(i))
            Arboles2.transform = tr.translate(x_offset,-1* y_offset, 0)
            Arboles2.childs = [BosqueNode]

            Arboles3 = sg.SceneGraphNode("Arboles3Aux" + str(i))
            Arboles3.transform = tr.translate(-1*x_offset,-1* y_offset, 0)
            Arboles3.childs = [BosqueNode]

            Bosque_Completo.childs += [ArbolesNode]
            Bosque_Completo.childs += [Arboles1]
            Bosque_Completo.childs += [Arboles2]
            Bosque_Completo.childs += [Arboles3]

    return Bosque_Completo

        
Bosque_Completo = Arboles(BosqueNode)
            

# Esta función se ejecuta aproximadamente 60 veces por segundo, dt es el tiempo entre la última
# ejecución y ahora
def update(dt, window):
    window.total_time += dt
    controller.Position_X += controller.speedX * dt
    controller.Position_Y += controller.speedY * dt
    controller.Position_Z += controller.speedZ * dt 
    controller.Cam_Position_X += controller.Cam_speedX * dt
    controller.Cam_Position_Y += controller.Cam_speedY * dt
    controller.Cam_Position_Z += controller.Cam_speedZ * dt 
    controller.camera_rotation_anglez += controller.camera_rotation_speedz * dt 
    controller.camera_rotation_angley += controller.camera_rotation_speedy * dt
    controller.camera_rotation_anglex += controller.camera_rotation_speedx * dt
    
# Cada vez que se llama update(), se llama esta función también
@controller.event
def on_draw():
    glUseProgram(mvpPipeline.shaderProgram)
    controller.clear()

    # Si el controller está en modo fillPolygon, dibuja polígonos. Si no, líneas.
    if controller.fillPolygon:
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    else:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)


    # Using the same view and projection matrices in the whole application
    projection = tr.perspective(45, float(WIDTH)/float(HEIGHT), 0.1, 100)
    glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "projection"), 1, GL_TRUE,
                       projection)
    
    # Configuracion de la camara
    view = tr.lookAt(
            controller.Camera_Position+np.array([controller.Cam_Position_X,controller.Cam_Position_Y,controller.Cam_Position_Z]),
            controller.Camera_OBJ+np.array([controller.Cam_Position_X,controller.Cam_Position_Y,controller.Cam_Position_Z]),
            np.array([0,0,1])
        )
    
    view = tr.matmul([
        view,
        tr.rotationX(controller.camera_rotation_anglez),
        tr.rotationY(controller.camera_rotation_angley),
        tr.rotationZ(controller.camera_rotation_anglex),
        
    ])
    
    
    glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "view"), 1, GL_TRUE, view)

    if controller.showAxis:
        glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "model"), 1, GL_TRUE,
                           tr.identity())
        mvpPipeline.drawCall(gpuAxis, GL_LINES)

    # Moviendo la mariposa 
    MariposaNode.transform = tr.translate(controller.Position_X,controller.Position_Y,controller.Position_Z+4)
    # Haciendo que la mariposa aletee
    Aleteo = sg.findNode(MariposaNode, "AlaDerecha")
    Aleteo.transform = tr.rotationZ(-1*abs(np.cos(controller.total_time*5)))

    # Dibujando la Mariposa
    sg.drawSceneGraphNode(MariposaNode, mvpPipeline,"model")

    # Dibujando el bosque
    sg.drawSceneGraphNode(Bosque_Completo, mvpPipeline,"model")
    
    # Dibujando Suelo
    sg.drawSceneGraphNode(SueloNode, mvpPipeline,"model")
    
    # Pipeline Con Iluminacion
    glUseProgram(textureGouraudPipeline.shaderProgram)

    rotation_theta = controller.total_time
    axis = np.array([1,-1,1])
    #axis = np.array([0,0,1])
    axis = axis / np.linalg.norm(axis)
    model = tr.rotationA(rotation_theta, axis)
    model = tr.identity()

    # White light in all components: ambient, diffuse and specular.
    glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "La"), 1.0, 1.0, 1.0)
    glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ld"), 1.0, 1.0, 1.0)
    glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ls"), 1.0, 1.0, 1.0)

    # Object is barely visible at only ambient. Diffuse behavior is slightly red. Sparkles are white
    glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ka"), 0.2, 0.2, 0.2)
    glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Kd"), 0.9, 0.9, 0.9)
    glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ks"), 1.0, 1.0, 1.0)

    # TO DO: Explore different parameter combinations to understand their effect!

    glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "lightPosition"), -3, 0, 3)
    glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "viewPosition"), 5, 7, 7)
    glUniform1ui(glGetUniformLocation(lightingPipeline.shaderProgram, "shininess"), 100)
    
    glUniform1f(glGetUniformLocation(lightingPipeline.shaderProgram, "constantAttenuation"), 0.0001)
    glUniform1f(glGetUniformLocation(lightingPipeline.shaderProgram, "linearAttenuation"), 0.03)
    glUniform1f(glGetUniformLocation(lightingPipeline.shaderProgram, "quadraticAttenuation"), 0.01)

    glUniformMatrix4fv(glGetUniformLocation(lightingPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
    glUniformMatrix4fv(glGetUniformLocation(lightingPipeline.shaderProgram, "view"), 1, GL_TRUE, view)
    glUniformMatrix4fv(glGetUniformLocation(lightingPipeline.shaderProgram, "model"), 1, GL_TRUE,
            tr.matmul([
                tr.translate(0,30*sin(controller.total_time),0.6),
                tr.rotationX(np.pi/2),
                ])
        )

    # Dibujamos el Porsche
    lightingPipeline.drawCall(gpuPorsche)

    glUniformMatrix4fv(glGetUniformLocation(lightingPipeline.shaderProgram, "model"), 1, GL_TRUE, tr.matmul([
        tr.translate(0,0,-0.28),
        tr.scale(1,12,1),
        tr.rotationX(np.pi/2)
    ]))
    # Dibujamos la carretera
    lightingPipeline.drawCall(gpuCarretera)

# Try to call this function 60 times per second
pyglet.clock.schedule(update, controller)
# Se ejecuta la aplicación
pyglet.app.run()
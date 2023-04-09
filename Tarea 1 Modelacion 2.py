### Juan Ignacio Valdivia ###
### 21.087.645-6 ###
### Juan.valdivia.g@ug.uchile.cl ###

import os.path
import sys
import glfw
import numpy as np
import pyglet
from OpenGL.GL import *
from math import sin, cos

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import grafica.easy_shaders as es
import grafica.scene_graph as sg
import grafica.basic_shapes as bs
import grafica.transformations as tr

# Controlador que permite comunicarse con la ventana de pyglet

class Controller(pyglet.window.Window):

    def __init__(self, width, height, title="Mariposa.exe"):
        super().__init__(width, height, title)
        self.total_time = 0.0
        self.fillPolygon = True
        self.pipeline = None
        self.repeats = 0


# Se asigna el ancho y alto de la ventana y se crea.
WIDTH, HEIGHT = 1280, 720
controller = Controller(width=WIDTH, height=HEIGHT)
# Se asigna el color de fondo de la ventana
glClearColor(98/255, 238/255, 245/255, 1.0)

# Se configura el pipeline y se le dice a OpenGL que utilice ese shader
pipeline = es.SimpleTransformShaderProgram()
controller.pipeline = pipeline
glUseProgram(pipeline.shaderProgram)

# Función que crea un triángulo de un color especificado


def createColorTriangle(r, g, b):

    # Defining the location and colors of each vertex  of the shape
    vertices = [
        #   positions        colors
        -0.5, -0.5, 0.0,  r, g, b,
        0.5, -0.5, 0.0,  r, g, b,
        0.0,  0.5, 0.0,  r, g, b]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [0, 1, 2]

    return bs.Shape(vertices, indices)


# Función que crea un círculo de una resolución, radio y color especificado
def createColorCircle(N, R, r, g, b):

    # First vertex at the center
    vertices = [0, 0, 0, r, g, b]
    indices = []

    dtheta = 2 * np.pi / N

    for i in range(N):
        theta = i * dtheta

        vertices += [
            # vertex coordinates
            R * np.cos(theta), R * np.sin(theta), 0, r, g, b]

        # A triangle is created using the center, this and the next vertex
        indices += [0, i, i+1]

    # The final triangle connects back to the second vertex
    indices += [0, N, 1]

    return bs.Shape(vertices, indices)

# Función que crea un grafo de escena de un hombre de nieve


def createButterfly(pipeline):

    # Convenience function to ease initialization
    def createGPUShape(shape):
        gpuShape = es.GPUShape().initBuffers()
        pipeline.setupVAO(gpuShape)
        gpuShape.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)
        return gpuShape

    # basic GPUShapes
    gpuRedTriangle = createGPUShape(createColorTriangle(252/255, 97/255, 58/255))
    gpuYellowTriangle = createGPUShape(createColorTriangle(244/255, 208/255, 63/255))
    gpuBrownTriangle = createGPUShape(createColorTriangle(146/255,43/255,33/255))

    # nodos de hojas
    RedTriangleNode = sg.SceneGraphNode("RedTriangleNode")
    RedTriangleNode.childs = [gpuRedTriangle]

    YellowTriangleNode = sg.SceneGraphNode("YellowTriangleNode")
    YellowTriangleNode.childs = [gpuYellowTriangle]

    BrownTriangleNode = sg.SceneGraphNode("BrownTriangleNode")
    BrownTriangleNode.childs = [gpuBrownTriangle]

    # Body

    ButterflyBody = sg.SceneGraphNode("ButterflyBody")
    ButterflyBody.childs = [YellowTriangleNode]

    ButterflyBody1 = sg.SceneGraphNode("ButterflyBody1")
    ButterflyBody1.transform = tr.matmul([
        tr.rotationZ(20*np.pi/180),
        tr.translate(0,10,0),
        tr.scale(2,15,1)
    ])
    ButterflyBody1.childs = [ButterflyBody]

    ButterflyBody2 = sg.SceneGraphNode("ButterflyBody2")
    ButterflyBody2.transform = tr.matmul([
        tr.rotationZ(20*np.pi/180),
        tr.rotationX(np.pi),
        
        tr.translate(0,5,0),
        tr.scale(2,15,1)
    ])
    ButterflyBody2.childs = [ButterflyBody]

    Antenas = sg.SceneGraphNode("Antenas")
    Antenas.childs = [BrownTriangleNode]

    Antena1 = sg.SceneGraphNode("Antena1")
    Antena1.transform = tr.matmul([
        tr.translate(-5,16,0),
        tr.rotationZ(45*4*np.pi/180),
        tr.scale(12/16,30/9,1)

    ])
    Antena1.childs = [Antenas]

    Antena2 = sg.SceneGraphNode("Antena2")
    Antena2.transform = tr.matmul([
    tr.translate(-5.6,15,0),
    tr.rotationZ(210*np.pi/180),
    tr.scale(12/16,30/9,1)

    ])
    Antena2.childs = [Antenas]

    Antenitas = sg.SceneGraphNode("Antenitas")
    Antenitas.childs = [Antena1, Antena2]

    body = sg.SceneGraphNode("body")
    body.childs = [Antenitas, ButterflyBody1, ButterflyBody2]


    # Alas
    Alas = sg.SceneGraphNode("Alas")
    Alas.childs = [RedTriangleNode]

    Ala1 = sg.SceneGraphNode("Ala1")
    Ala1.transform = tr.matmul([
        tr.rotationZ(45*np.pi/180),
        tr.translate(-7.45,9.7,0),
        tr.scale(15,15,1)
    ])
    Ala1.childs = [Alas]

    Ala2 = sg.SceneGraphNode("Ala2")
    Ala2.transform = tr.matmul([
        tr.identity(),
        tr.translate(7.5,12.4,0),
        tr.rotationZ(-285*np.pi/180),
        tr.scale(22,-10,5),
        ])
    Ala2.childs = [Alas]

    Ala3 = sg.SceneGraphNode("Ala3")
    Ala3.transform = tr.matmul([
        tr.rotationZ(-5*np.pi/180),
        tr.translate(-1.71,-5.5,0),
        tr.scale(-10,14,1)
    ])
    Ala3.childs = [Alas]

    Ala4 = sg.SceneGraphNode("Ala4")
    Ala4.transform = tr.matmul([
        tr.translate(8.22,-0.65,0),
        tr.rotationZ(-65*np.pi/180),
        tr.scale(14,12,1)
    ])
    Ala4.childs = [Alas]
         

    wings = sg.SceneGraphNode("wings") 
    wings.transform = tr.scale(abs(cos(controller.total_time * 22)), 1, 0)
    wings.childs = [Ala1, Ala2, Ala3, Ala4]


    # Butterfly, the one and only
    Butterfly = sg.SceneGraphNode("Butterfly")
    Butterfly.childs = [body, wings]

    return Butterfly

def createscene(pipeline):
    # Convenience function to ease initialization
    def createGPUShape(shape):
        gpuShape = es.GPUShape().initBuffers()
        pipeline.setupVAO(gpuShape)
        gpuShape.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)
        return gpuShape
    
    # basic GPUShapes
    gpuGreenQuad = createGPUShape(bs.createColorQuad(46/255, 204/255, 113/255))
    gpuYellowCircle = createGPUShape(createColorCircle(100,1,235/255, 249/255, 15/255))
    gpuYellowCircle2 = createGPUShape(createColorCircle(8,1,235/255, 249/255, 15/255))
    gpuPurpleCircle = createGPUShape(createColorCircle(100,1,179/255, 91/255, 215/255))
    gpuGreenTriangle = createGPUShape(createColorTriangle(46/255, 204/255, 113/255))

    # nodos de hojas
    GreenQuadNode = sg.SceneGraphNode("GreenQuadNode")
    GreenQuadNode.childs = [gpuGreenQuad]

    YellowCircleNode = sg.SceneGraphNode("YellowCircleNode")
    YellowCircleNode.childs = [gpuYellowCircle]

    YellowCircle2Node = sg.SceneGraphNode("YellowCircle2Node")
    YellowCircle2Node.childs = [gpuYellowCircle2]

    PurpleCircleNode = sg.SceneGraphNode("PurpleCircleNode")
    PurpleCircleNode.childs = [gpuPurpleCircle]

    GreenTriangleNode = sg.SceneGraphNode("GreenTriangleNode")
    GreenTriangleNode.childs = [gpuGreenTriangle]

    # Escena

    # Pasto
    Pasto = sg.SceneGraphNode("Pasto")
    Pasto.transform = tr.matmul([
        tr.translate(0,-50,0),
        tr.scale(100,20,0)
    ])
    Pasto.childs = [GreenQuadNode]

    #Sol
    Sol = sg.SceneGraphNode("Sol")
    Sol.transform = tr.matmul([
    tr.scale(150/16,150/9,0),
    tr.translate(4,1.8,0)
    ])
    Sol.childs = [YellowCircleNode]

    # Flor

    # Tallo
    Tallo = sg.SceneGraphNode("Tallo")
    Tallo.transform = tr.matmul([
    tr.translate(-30,-32,0),
    tr.scale(3,30,0)
    ])
    Tallo.childs = [GreenQuadNode]

    # Hojas
    Hoja = sg.SceneGraphNode("Hoja")
    Hoja.childs = [GreenTriangleNode]

    Hoja1 = sg.SceneGraphNode("Hoja1")
    Hoja1.transform = tr.matmul([
        tr.translate(-2.83,-3,0),
        tr.rotationZ(-30*np.pi/180),
    ])
    Hoja1.childs = [Hoja]

    Hoja2 = sg.SceneGraphNode("Hoja2")
    Hoja2.transform = tr.matmul([
        tr.translate(-4.56,-3,0),
        tr.rotationZ(30*np.pi/180),
    ])
    Hoja2.childs = [Hoja]

    Hojas = sg.SceneGraphNode("Hojas")
    Hojas.transform = tr.scale(130/16,90/9,0)
    Hojas.childs = [Hoja1, Hoja2]

    # Centro
    Centro = sg.SceneGraphNode("Centro")
    Centro.transform = tr.matmul([
        tr.translate(-30,-6.5,0),
        tr.scale(100/16,100/9,1),
        tr.rotationZ(23*np.pi/180)
    ])
    Centro.childs = [YellowCircle2Node]

    #Petalos
    Petalos = sg.SceneGraphNode("Petalos")
    Petalos.childs = [PurpleCircleNode]

    Petalo1 = sg.SceneGraphNode("Petalo1")
    Petalo1.transform = tr.translate(-5.7,-2.5,1)
    Petalo1.childs = [Petalos]

    Petalo2 = sg.SceneGraphNode("Petalo2")
    Petalo2.transform = tr.translate(-5.1,-0.9,1)
    Petalo2.childs = [Petalos]

    Petalo3 = sg.SceneGraphNode("Petalo3")
    Petalo3.transform = tr.translate(-5.7,0.7,1)
    Petalo3.childs = [Petalos]

    Petalo4 = sg.SceneGraphNode("Petalo4")
    Petalo4.transform = tr.translate(-7.4,1.3,1)
    Petalo4.childs = [Petalos]

    Petalo5 = sg.SceneGraphNode("Petalo5")
    Petalo5.transform = tr.translate(-9.1,0.7,1)
    Petalo5.childs = [Petalos]

    Petalo6 = sg.SceneGraphNode("Petalo6")
    Petalo6.transform = tr.translate(-9.7,-0.9,1)
    Petalo6.childs = [Petalos]

    Petalo7 = sg.SceneGraphNode("Petalo7")
    Petalo7.transform = tr.translate(-9.1,-2.5,1)
    Petalo7.childs = [Petalos]

    Petalo8 = sg.SceneGraphNode("Petalo8")
    Petalo8.transform = tr.translate(-7.4,-3.2,1)
    Petalo8.childs = [Petalos]

    ConjuntoPetalos = sg.SceneGraphNode("ConjuntoPetalos")
    ConjuntoPetalos.transform = tr.scale(65/16,65/9,1)
    ConjuntoPetalos.childs = [Petalo1, Petalo2, Petalo3, Petalo4, Petalo5, Petalo6, Petalo7, Petalo8]

    Flor = sg.SceneGraphNode("Flor")
    Flor.transform = tr.scale(0.3,0.3,1)
    Flor.childs = [Tallo, Hojas, Centro, ConjuntoPetalos]

    # Dibujar la Flor varias veces
    for i in range(6):
        Flores = sg.SceneGraphNode("FloresAux" + str(i))
        Flores.childs = [Flor]
        sg.drawSceneGraphNode(Flores,pipeline,"transform",
                          np.matmul(tr.translate(i*0.27 - 0.5, -0.55, 0), tr.scale(0.02, 0.02, 1)))





    Escena = sg.SceneGraphNode("Escena")
    Escena.childs = [Pasto, Sol]

    

    return Escena


# Esta función se ejecuta aproximadamente 60 veces por segundo, dt es el tiempo entre la última
# ejecución y ahora


def update(dt, controller):
    controller.total_time += dt

# Cada vez que se llama update(), se llama esta función también


@controller.event
def on_draw():
    controller.clear()

    # Si el controller está en modo fillPolygon, dibuja polígonos. Si no, líneas.
    if controller.fillPolygon:
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    else:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    # Creating shapes on GPU memory
    Butterfly = createButterfly(pipeline)
    Escena = createscene(pipeline)
    # Drawing the Car
    sg.drawSceneGraphNode(Escena,pipeline,"transform",
                          np.matmul(tr.translate(0, 0, 0), tr.scale(0.02, 0.02, 1)))
    sg.drawSceneGraphNode(Butterfly, pipeline, "transform",
                          np.matmul(tr.translate(-0.5 * cos(controller.total_time), 0.5 * sin(controller.total_time), 0.0), tr.scale(0.02, 0.02, 1)))
                             

# Try to call this function 60 times per second
pyglet.clock.schedule(update, controller)
# Se ejecuta la aplicación
pyglet.app.run()

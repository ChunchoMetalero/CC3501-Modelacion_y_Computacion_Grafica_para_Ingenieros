Tarea 2 Mariposa 3D


Esta tarea dibuja una mariposa 3D capaz de aletear y de desplazarse a través del input del usuario controlado con WASD, LCTRL y SPACE.
Para la Cámara opte por una cámara libre en la escena controlada completamente por el input del usuario (los controles son algo toscos), pero son funcionales:
Los controles son IJKL, U, O, M, N y las flechas del teclado.


Cree un bosque para la mariposa, que si bien no es infinito es bastante extenso y la mariposa puede vivir cómoda en dicho bosque, la cantidad de árboles puede producir
pérdidas de rendimiento.


Para la Parte 5 descargué un modelo .obj de un Porsche y de una carretera.
Carretera: https://free3d.com/3d-model/road-47211.html
Porsche: https://free3d.com/3d-model/porsche-911-gt-43465.html


Respecto al formato .obj este almacena información sobre la geometría de objetos en 3D, lo que incluye sus vértices, normales, coordenadas de texturas y caras, que hacen que cada
El polígono se define como una lista de vértices y vértices de textura. Estos vértices se almacenan en sentido contrario a las agujas del reloj, lo que hace innecesaria la declaración explícita de caras normales. No tienen dimensiones, pero pueden tener comentarios.
Los vértices representan los puntos en el espacio 3D que definen la forma de un objeto.
Las normales son vectores que indican la orientación de la cara, se utilizan para calcular la iluminación.
Las coordenadas de textura se utilizan para poder poner una textura bidimensional es la superficie del objeto 3D.


El formato de archivo es abierto y ha sido adoptado por otros proveedores de aplicaciones de gráficos 3D, lo que lo hace muy compatible con distintos softwares.
Es capaz de almacenar objetos complejos, con distintas texturas. A menudo viene con más archivos, ya que por lo general solo almacena la geometría del objeto.


De forma adicional también importé una carretera a la que trate de colocarle una textura(me siento algo estafado, ya que no me funciono muy bien), además le otorgué movimiento al porsche a través de la carretera e introduje un pipeline con iluminación, para que así los cuerpos importados se vean mejor(a falta de texturas, al menos tenemos iluminación :D)

Tambián modifique archivos de la carpeta gráfica y agregue los assets correspondientes a la carpeta assets :D 
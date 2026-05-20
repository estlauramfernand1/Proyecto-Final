# =========================================================
# ENSAMBLE JERÁRQUICO DE BRAZO ROBÓTICO EN OPENGL
# ---------------------------------------------------------
# Autor: Juan José (el jura)
# Descripción: Top 10 codigos que no tienen chatgpt en ningun lado 2026 un solo link mega mediafire
# Programa para visualizar y controlar un brazo robótico
# ensamblado a partir de archivos STL utilizando:
#
# - OpenGL
# - GLUT
# - numpy-stl
#
# El sistema usa transformaciones jerárquicas:
# cada pieza hija depende de la transformación
# de la pieza padre.
#
# Controles:
#   Mouse Izquierdo  -> Rotar cámara
#   Mouse Derecho    -> Zoom
#
#   A / D -> Base
#   Q / E -> Pieza 3
#   R / F -> Pieza 4
#   T / G -> Pieza 5
#   Y / H -> Pieza 6
#   U / J -> Pieza 7
#   I / K -> Garras
#
#   0 -> Reiniciar articulaciones
# =========================================================

import numpy as np
from stl import mesh
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import tkinter as tk
from tkinter import ttk


root = tk.Tk()
root.title("Control de Vistas y Guía de Teclas")
root.geometry("350x300")
root.resizable(False, False)
vista_actual = "Frontal"

def cambiar_vista(nueva_vista):
    global vista_actual
    vista_actual = nueva_vista
    label_vista_activa.config(text=f"Vista actual: {vista_actual}")
    print(f"[VISTA] Cambiado a: {vista_actual}")

# Aquí pones la lógica que cambia la cámara o render según la vista_actual

# --- Panel 1: Botones para las Vistas ---
frame_vistas = ttk.LabelFrame(root, text=" Cambiar Vistas ", padding=10)
frame_vistas.pack(fill="x", padx=15, pady=10)

btn_frontal = ttk.Button(frame_vistas, text="Vista Frontal", command=lambda: cambiar_vista("Frontal"))
btn_frontal.pack(fill="x", pady=2)

btn_lateral = ttk.Button(frame_vistas, text="Vista Lateral", command=lambda: cambiar_vista("Lateral"))
btn_lateral.pack(fill="x", pady=2)

btn_superior = ttk.Button(frame_vistas, text="Vista Superior (Top)", command=lambda: cambiar_vista("Superior"))
btn_superior.pack(fill="x", pady=2)

# --- Panel 2: Texto de Guía (Teclas) ---
frame_guia = ttk.LabelFrame(root, text=" Guía de Teclas (Calibración) ", padding=10)
frame_guia.pack(fill="x", padx=15, pady=10)

texto_guia = (
    "• Tecla [ I ] : Aumentar ángulo Garra (Pieza 8)\n"
    "• Tecla [ K ] : Disminuir ángulo Garra (Pieza 8)\n"
    "• Tecla [ O ] : Aumentar ángulo Brazo (Pieza 9)\n"
    "• Tecla [ L ] : Disminuir ángulo Brazo (Pieza 9)"
)
label_teclas = ttk.Label(frame_guia, text=texto_guia, justify="left", font=("Arial", 9))
label_teclas.pack(anchor="w")

# Estado en la parte inferior
label_vista_activa = ttk.Label(root, text=f"Vista actual: {vista_actual}", font=("Arial", 10, "bold"))
label_vista_activa.pack(pady=5)


# =========================================================
# TU BUCLE PRINCIPAL (Donde lees el teclado)
# =========================================================
ang_pieza8 = 0  # Tu variable original

# Simulando tu bucle (puede ser un 'while True', el bucle de OpenCV, Pygame, etc.)
ejecutando = True
while ejecutando:
    
    # 1. ACTUALIZAR LA VENTANA DE TKINTER
    # Esto hace que la ventana responda a los clics de los botones sin trabar el programa
    try:
        root.update()
    except tk.TclError:
        # Por si el usuario cierra la ventana de Tkinter con la "X"
        break

    # 2. TU LÓGICA DE DETECCIÓN DE TECLADO
    # (Aquí uso un ejemplo conceptual, mantén cómo tú detectas la variable 'key')
    key = ""  # <--- Aquí va tu lectura real del teclado (ej. cv2.waitKey, pygame.event, etc.)

    # =========================================================
    # MODO CALIBRACIÓN DE GARRAS (Tu código original)
    # =========================================================
    if key == "i":
        ang_pieza8 += 5
        print(f"[CALIBRACIÓN] Ángulo actual de la garra (Pieza 8): {ang_pieza8}°")

    if key == "k":
        ang_pieza8 -= 5
        print(f"[CALIBRACIÓN] Ángulo actual de la garra (Pieza 8): {ang_pieza8}°")
        
    # Lógica de salida del bucle (ejemplo)
    if key == "escape":
        ejecutando = False

print("Programa finalizado.")

# =========================================================
# CONFIGURACIÓN DE CÁMARA
# =========================================================

cam_dist = 1000
cam_angX = 30
cam_angY = 45

mouse_prev = [0, 0]
boton_act = None


def actualizar_camara():
    """
    Calcula la posición orbital de la cámara
    usando coordenadas esféricas.
    """

    rad_x = math.radians(cam_angX)
    rad_y = math.radians(cam_angY)

    cx = cam_dist * math.cos(rad_x) * math.sin(rad_y)
    cy = cam_dist * math.sin(rad_x)
    cz = cam_dist * math.cos(rad_x) * math.cos(rad_y)

    gluLookAt(
        cx, cy, cz,      # posición cámara
        0, 150, 0,         # punto observado
        0, 1, 0          # vector UP
    )


def mouse_boton(boton, estado, x, y):
    """
    Detecta botones del mouse.
    """

    global boton_act, mouse_prev

    boton_act = boton if estado == GLUT_DOWN else None
    mouse_prev = [x, y]


def mouse_movimiento(x, y):
    """
    Control orbital:
    - Click izquierdo -> rotación
    - Click derecho -> zoom
    """

    global cam_angX, cam_angY
    global cam_dist
    global mouse_prev

    dx = x - mouse_prev[0]
    dy = y - mouse_prev[1]

    # ROTACIÓN
    if boton_act == GLUT_LEFT_BUTTON:

        cam_angY += dx * 0.5
        cam_angX -= dy * 0.5

        cam_angX = max(-89, min(89, cam_angX))

    # ZOOM
    elif boton_act == GLUT_RIGHT_BUTTON:

        cam_dist += dy * 5
        cam_dist = max(100, cam_dist)

    mouse_prev = [x, y]
    
    glutPostRedisplay()


# =========================================================
# CLASE PIEZA
# =========================================================

class Pieza:
    """
    Representa una pieza STL individual.
    """

    def __init__(self, ruta_stl, color=(0.8, 0.8, 0.8)):

        self.color = color

        # cargar STL
        self.datos_stl = mesh.Mesh.from_file(ruta_stl)

        # display list OpenGL
        self.lista_id = None

        # centro geométrico
        self.centro = np.array([0.0, 0.0, 0.0])

    def crear_lista_dibujo(self):
        
        """
        Centra automáticamente la pieza
        y crea una display list.
        """

        todos = self.datos_stl.vectors.reshape(-1, 3)

        # centro promedio
        self.centro = todos.mean(axis=0)

        self.lista_id = glGenLists(1)

        glNewList(self.lista_id, GL_COMPILE)

        glBegin(GL_TRIANGLES)

        for i, triangulo in enumerate(self.datos_stl.vectors):

            # normal de la cara
            glNormal3fv(self.datos_stl.normals[i])

            for vertice in triangulo:
                glVertex3fv(vertice - self.centro)

        glEnd()

        glEndList()

    def dibujar_local(self):
        """
        Dibuja la pieza STL.
        """

        glColor3f(*self.color)

        glCallList(self.lista_id)


# =========================================================
# RUTAS STL
# =========================================================

ruta = r"C:\Users\miche\Downloads\Brazo Robotico - EX.GR\Brazo Robotico Progra"

direcciones = [

    ("pieza1", ruta + r"\Brazo robotico - Pieza 1.STL", (1.0, 0.0, 0.0)),
    ("pieza2", ruta + r"\Brazo robotico - Pieza 2.STL", (0.0, 0.8, 0.6)),
    ("pieza3", ruta + r"\Brazo robotico - Pieza 3.STL", (1.0, 1.0, 1.0)),
    ("pieza4", ruta + r"\Brazo robotico - Pieza 4.STL", (1.0, 1.0, 0.0)),
    ("pieza5", ruta + r"\Brazo robotico - Pieza 5.STL", (1.0, 0.5, 0.0)),
    ("pieza6", ruta + r"\Brazo robotico - Pieza 6.STL", (0.8, 0.0, 0.8)),
    ("pieza7", ruta + r"\Brazo robotico - Pieza 7.STL", (0.0, 1.0, 1.0)),
    ("pieza8", ruta + r"\Brazo robotico - Pieza 8.STL", (1.0, 0.0, 0.5))
]

lista_piezas = {}


# =========================================================
# VARIABLES DE ARTICULACIÓN
# =========================================================

ang_base = 0

ang_pieza3 = 0
ang_pieza4 = 0
ang_pieza5 = 0
ang_pieza6 = 0
ang_pieza7 = 0
ang_pieza8 = 0


# =========================================================
# POSICIONES DE ARTICULACIÓN
# =========================================================

# pieza2
D_P1_X = 0
D_P1_Y = 0
D_P1_Z = 0

# pieza3
D_P2_X = -34
D_P2_Y = 22
D_P2_Z = -45

# pieza4
D_P3_X = -280
D_P3_Y = 0
D_P3_Z = 0

# pieza5
D_P4_X = 7
D_P4_Y = 10
D_P4_Z = 240

# pieza6
D_P5_X = 0
D_P5_Y = 0
D_P5_Z = 0

# pieza7
D_P6_X = 0
D_P6_Y = -40
D_P6_Z = 0

# garra izquierda
D_P7_X = 40
D_P7_Y = 0
D_P7_Z = 8

# garra derecha
D_P8_X = -38
D_P8_Y = 0
D_P8_Z = 5

# =========================================================
# INICIALIZACIÓN OPENGL
# =========================================================

def inicializar():

    # iluminación
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glShadeModel(GL_SMOOTH)

    # profundidad
    glEnable(GL_DEPTH_TEST)

    # normalización
    glEnable(GL_NORMALIZE)

    # posición luz
    # luz principal
    glLightfv(GL_LIGHT0, GL_POSITION, (500, 800, 500, 1))

    # luz difusa
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1))

    # luz ambiente
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.25, 0.25, 0.25, 1))

    # brillo especular
    glLightfv(GL_LIGHT0, GL_SPECULAR, (1, 1, 1, 1))

    glMaterialfv(GL_FRONT, GL_SPECULAR, (1,1,1,1))
    glMaterialf(GL_FRONT, GL_SHININESS, 50)
    glClearColor(0.15, 0.15, 0.18, 1)
    # cargar piezas
    for nombre, ruta_stl, color in direcciones:

        try:

            pieza = Pieza(ruta_stl, color)

            pieza.crear_lista_dibujo()

            lista_piezas[nombre] = pieza

            print(f"[OK] {nombre}")

        except Exception as e:

            print(f"[ERROR] {nombre}: {e}")

# =========================================================
# ENSAMBLE JERÁRQUICO
# =========================================================

def dibujar_ensamble():

    # =====================================================
    # PIEZA 1 - BASE
    # =====================================================

    glPushMatrix()

    lista_piezas["pieza1"].dibujar_local()

    # =====================================================
    # PIEZA 2
    # =====================================================

    glPushMatrix()

    glTranslatef(D_P1_X, D_P1_Y, D_P1_Z)

    glRotatef(ang_base, 0, 1, 0)

    # offset STL
    glTranslatef(-115.1, 171, 19.01)

    lista_piezas["pieza2"].dibujar_local()

    # =====================================================
    # PIEZA 3
    # =====================================================

    glPushMatrix()

    glTranslatef(D_P2_X, D_P2_Y, D_P2_Z)

    glRotatef(ang_pieza3, 0, 0, 1)

    # offset STL
    glTranslatef(-71.2, 0, -18)

    # orientación STL
    glRotatef(90, 1, 0, 0)
    glRotatef(180, 0, 1, 0)
    glRotatef(180, 0, 0, 1)

    lista_piezas["pieza3"].dibujar_local()

    # =====================================================
    # PIEZA 4
    # =====================================================

    glPushMatrix()

    glTranslatef(D_P3_X, D_P3_Y, D_P3_Z)

    glRotatef(ang_pieza4, 0, 1, 0)

    # orientación STL
    glRotatef(-90, 0, 0, 1)

    # offset STL
    glTranslatef(62, 37, 112)

    lista_piezas["pieza4"].dibujar_local()

    # =====================================================
    # PIEZA 5
    # =====================================================

    glPushMatrix()

    glTranslatef(D_P4_X, D_P4_Y, D_P4_Z)

    glRotatef(ang_pieza5, 0, 0, 1)

    lista_piezas["pieza5"].dibujar_local()

    # =====================================================
    # PIEZA 6
    # =====================================================

    glPushMatrix()

    glTranslatef(D_P5_X, D_P5_Y, D_P5_Z)

    glRotatef(ang_pieza6, 1, 0, 0)

    # offset STL
    glTranslatef(0, -80, 0)

    lista_piezas["pieza6"].dibujar_local()

    # =====================================================
    # PIEZA 7
    # =====================================================

    glPushMatrix()

    glTranslatef(D_P6_X, D_P6_Y, D_P6_Z)

    glRotatef(ang_pieza7, 0, 1, 0)

    glRotatef(90, 1, 0, 0)

    lista_piezas["pieza7"].dibujar_local()

    # =====================================================
    # GARRA IZQUIERDA
    # =====================================================

    glPushMatrix()

    glTranslatef(D_P7_X, D_P7_Y, D_P7_Z)

    glRotatef(ang_pieza8, 0, 1, 0)

    # offset STL
    glTranslatef(35, 1, 50)

    lista_piezas["pieza8"].dibujar_local()

    glPopMatrix()

    # =====================================================
    # GARRA DERECHA
    # =====================================================

    glPushMatrix()

    glTranslatef(D_P8_X, D_P8_Y, D_P8_Z)

    # espejo
    glScalef(-1, 1, 1)

    glRotatef(ang_pieza8, 0, 1, 0)

    # offset STL
    glTranslatef(35, 0, 53)

    lista_piezas["pieza8"].dibujar_local()

    glPopMatrix()  # pieza8

    # =====================================================
    # CIERRE DE MATRICES
    # =====================================================

    glPopMatrix()  # pieza7
    glPopMatrix()  # pieza6
    glPopMatrix()  # pieza5
    glPopMatrix()  # pieza4
    glPopMatrix()  # pieza3
    glPopMatrix()  # pieza2
    glPopMatrix()  # pieza1


# =========================================================
# DISPLAY
# =========================================================

def display():

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glLoadIdentity()

    actualizar_camara()

    dibujar_ensamble()

    glutSwapBuffers()


# =========================================================
# TECLADO
# =========================================================
# ── CONTROL DE CÁMARA ───────────────────────────────────

def vista_superior():
    global cam_angX, cam_angY
    cam_angX = 90
    cam_angY = 0
    glutPostRedisplay()

def vista_frontal():
    global cam_angX, cam_angY
    cam_angX = 0
    cam_angY = 0
    glutPostRedisplay()

def vista_lateral():
    global cam_angX, cam_angY
    cam_angX = 0
    cam_angY = 90
    glutPostRedisplay()

def vista_isometrica():
    global cam_angX, cam_angY
    cam_angX = 30
    cam_angY = 45
    glutPostRedisplay()
    
def teclado(key, x, y):

    global ang_base
    global ang_pieza3
    global ang_pieza4
    global ang_pieza5
    global ang_pieza6
    global ang_pieza7
    global ang_pieza8

    key = key.decode("utf-8").lower()

    # BASE
    if key == "a":
        ang_base = min(0, ang_base + 5)

    if key == "d":
        ang_base = max(-360, ang_base - 5)

    # PIEZA 3
    if key == "q":
        ang_pieza3 = min(30, ang_pieza3 + 5)

    if key == "e":
        ang_pieza3 = max(-180, ang_pieza3 - 5)

    # PIEZA 4
    if key == "r":
        ang_pieza4 += 5

    if key == "f":
        ang_pieza4 -= 5

    # PIEZA 5
    if key == "t":
        ang_pieza5 += 5

    if key == "g":
        ang_pieza5 -= 5

    # PIEZA 6
    if key == "y":
        ang_pieza6 += 5

    if key == "h":
        ang_pieza6 -= 5

    # PIEZA 7
    if key == "u":
        ang_pieza7 += 5

    if key == "j":
        ang_pieza7 -= 5

    # GARRAS
    if key == "i": #preparate bb 
        if ang_pieza8 < 65: #quiero que llegue hasta que se abran a 180 si?
            ang_pieza8 += 5
        else:
            print("Nao Nao Las garras no se abren mas no seas animal ")

    if key == "k":
        if ang_pieza8 > -40:
            ang_pieza8 -= 5
        else: 
            print("Nao Nao Las garras no se cierran masno seas animal ")

    # =========================================================
    # MODO CALIBRACIÓN DE GARRAS (Muestra el ángulo en consola)
    # =========================================================
    """ Esto ignorenlo bbs o ps si les sirve es lo que hic para saber el angulo de las garras para poder limitarlas y yap mis bbs
    if key == "i":
        ang_pieza8 += 5
        print(f"[CALIBRACIÓN] Ángulo actual de la garra (Pieza 8): {ang_pieza8}°")

    if key == "k":
        ang_pieza8 -= 5
        print(f"[CALIBRACIÓN] Ángulo actual de la garra (Pieza 8): {ang_pieza8}°")"""

    # RESETEAR
    if key == "0":

        ang_base = 0
        ang_pieza3 = 0
        ang_pieza4 = 0
        ang_pieza5 = 0
        ang_pieza6 = 0
        ang_pieza7 = 0
        ang_pieza8 = 0
        # ── VISTAS PREDETERMINADAS ─────────────────

    if key == "1":
        vista_superior()

    if key == "2":
        vista_frontal()

    if key == "3":
        vista_lateral()

    if key == "4":
        vista_isometrica()

    glutPostRedisplay()


# =========================================================
# RESHAPE
# =========================================================

def reshape(w, h):

    if h == 0:
        h = 1

    glViewport(0, 0, w, h)

    glMatrixMode(GL_PROJECTION)

    glLoadIdentity()

    gluPerspective(45, w / h, 0.1, 2000.0)

    glMatrixMode(GL_MODELVIEW)

# =========================================================
# MAIN
# =========================================================

def main():

    glutInit()

    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)

    glutInitWindowSize(800, 600)

    glutCreateWindow(b"Brazo Robotico OpenGL")

    inicializar()

    # callbacks GLUT
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(teclado)

    glutMouseFunc(mouse_boton)
    glutMotionFunc(mouse_movimiento)

    glutMainLoop()



##



# =========================================================
# EJECUCIÓN
# =========================================================

if __name__ == "__main__":
    main()
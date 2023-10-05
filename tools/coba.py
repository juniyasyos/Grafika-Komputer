# from OpenGL.GL import *
# from OpenGL.GLUT import *
# import sys

# # Variabel untuk menyimpan posisi segitiga
# triangle_position = [0.0, 0.0]
# rotation_angle = 0.0  # Sudut rotasi awal
# rotation_speed = 5  # Kecepatan rotasi

# def display():
#     global rotation_angle
#     glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
#     # Mengatur rotasi segitiga
#     glPushMatrix()
#     glTranslatef(triangle_position[0], triangle_position[1], 0.0)
#     glRotatef(rotation_angle, 0.0, 0.0, 1.0)  # Rotasi pada sumbu z
#     glColor3f(1.0, 0.0, 0.0)  # Warna segitiga: Merah
#     glBegin(GL_TRIANGLES)
#     glVertex2f(-0.1, -0.1)
#     glVertex2f(0.1, -0.1)
#     glVertex2f(0.0, 0.1)
#     glEnd()
#     glPopMatrix()
    
#     glutSwapBuffers()

# def init():
#     glClearColor(0.0, 0.0, 0.0, 1.0)  # Warna latar belakang (hitam)

# def keyboard(key, x, y):
#     global triangle_position
#     if key == b'w' or key == b'W':
#         # Pindahkan segitiga ke atas
#         triangle_position[1] += 0.1
#     elif key == b's' or key == b'S':
#         # Pindahkan segitiga ke bawah
#         triangle_position[1] -= 0.1
#     elif key == b'a' or key == b'A':
#         # Pindahkan segitiga ke kiri
#         triangle_position[0] -= 0.1
#     elif key == b'd' or key == b'D':
#         # Pindahkan segitiga ke kanan
#         triangle_position[0] += 0.1
#     glutPostRedisplay()

# def idle():
#     global rotation_angle
#     # Mengupdate sudut rotasi
#     rotation_angle += rotation_speed
#     if rotation_angle >= 360.0:
#         rotation_angle -= 360.0
#     glutPostRedisplay()

# glutInit(sys.argv)
# glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
# glutInitWindowSize(800, 600)
# glutCreateWindow("Contoh Mengubah Posisi dan Rotasi dengan glutPostRedisplay")

# glutDisplayFunc(display)
# glutKeyboardFunc(keyboard)
# glutIdleFunc(idle)
# init()

# glutMainLoop()


# from OpenGL.GL import *
# from OpenGL.GLUT import *
# import sys

# # Variabel untuk menyimpan posisi bola
# ball_position = [-0.9, 0.0]  # Posisi awal bola
# ball_speed = 0.005  # Kecepatan pergerakan bola

# def display():
#     glClear(GL_COLOR_BUFFER_BIT)
#     glColor3f(1.0, 0.0, 0.0)  # Warna bola: Merah
#     glPointSize(50.0)  # Ukuran bola
#     glBegin(GL_POINTS)
#     glVertex2f(ball_position[0], ball_position[1])
#     glEnd()
#     glutSwapBuffers()

# def update():
#     global ball_position
#     ball_position[0] += ball_speed
#     if ball_position[0] > 0.9:  # Batas kanan jendela
#         ball_position[0] = -0.9  # Mulai lagi dari kiri
#     glutPostRedisplay()

# def init():
#     glClearColor(0.0, 0.0, 0.0, 1.0)  # Warna latar belakang (hitam)

# def main():
#     glutInit(sys.argv)
#     glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
#     glutInitWindowSize(800, 600)
#     glutCreateWindow("Animasi Bola Sederhana")

#     glutDisplayFunc(display)
#     glutIdleFunc(update)
#     init()
    
#     glutMainLoop()

# if __name__ == "__main__":
#     main()


from OpenGL.GL import *
from OpenGL.GLUT import *
import sys

# Variabel untuk mengatur pergerakan, rotasi, dan skalasi
translation_x = 0.0
translation_y = 0.0
rotation_angle = 0.0
scaling_factor = 1.0

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    
    glPushMatrix()
    glTranslatef(translation_x, translation_y, 0.0)
    glRotatef(rotation_angle, 0.0, 0.0, 1.0)
    glScalef(scaling_factor, scaling_factor, 1.0)
    
    # Gambar objek (misalnya, segitiga)
    glColor3f(1.0, 0.0, 0.0)  # Warna objek: Merah
    glBegin(GL_TRIANGLES)
    glVertex2f(-0.1, -0.1)
    glVertex2f(0.1, -0.1)
    glVertex2f(0.0, 0.1)
    glEnd()
    
    glPopMatrix()
    glutSwapBuffers()

def animate_movement():
    global translation_x, translation_y
    translation_x += 0.001
    translation_y += 0.001
    glutPostRedisplay()

def animate_rotation():
    global rotation_angle
    rotation_angle += 0.5
    glutPostRedisplay()

def animate_scaling():
    global scaling_factor
    scaling_factor += 0.01
    glutPostRedisplay()

def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    
def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(800, 600)
    glutCreateWindow("Animasi Gerakan PyOpenGL")
    
    glutDisplayFunc(display)
    glutIdleFunc(animate_movement)  # Ganti menjadi animate_rotation atau animate_scaling untuk animasi yang berbeda
    init()
    
    glutMainLoop()

if __name__ == "__main__":
    main()

from OpenGL.GL import *
from OpenGL.GLUT import *

class OpenGLInitializer:
    def __init__(self, window_size=(800, 600), window_title="OpenGL Window"):
        self.window_size = window_size
        self.window_title = window_title
        self.fullscreen = False
        self.object_manager = ObjectManager()

    def initialize_window(self):
        glutInit()
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(*self.window_size)
        glutCreateWindow(self.window_title)
        glutDisplayFunc(self.display)
        glutKeyboardFunc(self.keyboard)

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            glutFullScreen()
        else:
            glutReshapeWindow(*self.window_size)
            glutPositionWindow(100, 100)

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.object_manager.draw_objects()
        glutSwapBuffers()

    def keyboard(self, key, x, y):
        if key == b'f':
            self.toggle_fullscreen()
            if self.fullscreen:
                print("Mode Layar Penuh Aktif")
            else:
                print("Mode Layar Penuh Nonaktif")
            glutPostRedisplay()

class ObjectManager:
    def __init__(self):
        self.objects = []

    def add_square(self, x, y, width, height, color=(1.0, 1.0, 1.0)):
        square = {
            "type": "square",
            "x": x,
            "y": y,
            "width": width,
            "height": height,
            "color": color
        }
        self.objects.append(square)

    def draw_objects(self):
        for obj in self.objects:
            if obj["type"] == "square":
                self.draw_square(obj)

    def draw_square(self, obj):
        x = obj["x"]
        y = obj["y"]
        width = obj["width"]
        height = obj["height"]
        color = obj["color"]

        glColor3f(*color)
        glBegin(GL_QUADS)
        glVertex2f(x, y)
        glVertex2f(x + width, y)
        glVertex2f(x + width, y + height)
        glVertex2f(x, y + height)
        glEnd()

if __name__ == "__main__":
    initializer = OpenGLInitializer()
    initializer.initialize_window()

    # Tambahkan objek persegi merah
    initializer.object_manager.add_square(0.0, 0.0, 0.5, 0.5, (1.0, 0.0, 0.0))

    glutMainLoop()

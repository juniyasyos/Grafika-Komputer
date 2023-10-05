from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

# Initialization and Window Configuration
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

class OpenGLInitializer:
    """
    Initializes and configures the OpenGL window.
    """
    def __init__(self, window_size=(1280, 720), window_title="OpenGL Window"):
        self.window_size = window_size
        self.window_title = window_title
        self.fullscreen = False
        self.object_manager = ObjectManager()

    def initialize_window(self):
        """
        Initialize the OpenGL window using the appropriate library (e.g., GLUT or GLFW).
        """
        glutInit()
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(*self.window_size)
        glutCreateWindow(self.window_title)
        glutDisplayFunc(self.display)

        # Fungsi keyboard untuk menangani tombol 'f' untuk fullscreen
        glutKeyboardFunc(self.keyboard)

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            glutFullScreen()
        else:
            glutReshapeWindow(*self.window_size)
            glutPositionWindow(100, 100)

    def set_view(self):
        glViewport(0, 0, *self.window_size)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, self.window_size[0], self.window_size[1], 0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.set_view()  # Set tampilan sebelum menggambar objek
        self.object_manager.draw_object()
        glutSwapBuffers()

    def set_window_properties(self, size, title):
        """
        Set window properties such as size and title.

        Args:
            size (tuple): The size of the window in (width, height) format.
            title (str): The title of the window.
        """
        self.window_size = size
        self.window_title = title
        glutReshapeWindow(*size)  # Set ulang ukuran jendela saat properti diubah

    def keyboard(self, key):
        if key == b'f':
            self.toggle_fullscreen()
            if self.fullscreen:
                print("Mode Layar Penuh Aktif")
            else:
                print("Mode Layar Penuh Nonaktif")
            glutPostRedisplay()


# Object Management
class ObjectManager:
    """
    Manages objects in the OpenGL scene.
    """
    def __init__(self):
        self.objects = []


    def set_object_color(self, obj, color):
        """
        Set the color of an object.

        Args:
            obj: The object to set the color for.
            color (tuple): The color in (R, G, B) format.
        """
        if obj in self.objects:
            obj["color"] = color

    def create_rectangle(self, x, y, width, height, color=(1.0, 1.0, 1.0)):
        """
        Create a rectangle object.

        Args:
            x (float): X-coordinate of the rectangle's origin.
            y (float): Y-coordinate of the rectangle's origin.
            width (float): Width of the rectangle.
            height (float): Height of the rectangle.
            color (tuple, optional): Color of the rectangle in RGB format. Default is white (1.0, 1.0, 1.0).
        """
        obj = {
            "type": "rectangle",
            "x": x,
            "y": y,
            "width": width,
            "height": height,
            "color": color
        }
        self.objects.append(obj)

    def create_circle(self, x, y, radius, color=(1.0, 1.0, 1.0)):
        """
        Create a circle object.

        Args:
            x (float): X-coordinate of the circle's center.
            y (float): Y-coordinate of the circle's center.
            radius (float): Radius of the circle.
            color (tuple, optional): Color of the circle in RGB format. Default is white (1.0, 1.0, 1.0).
        """
        obj = {
            "type": "circle",
            "x": x,
            "y": y,
            "radius": radius,
            "color": color
        }
        self.objects.append(obj)

    def create_triangle(self, x, y, side_length, color=(1.0, 1.0, 1.0)):
        """
        Create a triangle object.

        Args:
            x (float): X-coordinate of the triangle's origin.
            y (float): Y-coordinate of the triangle's origin.
            side_length (float): Length of each side of the equilateral triangle.
            color (tuple, optional): Color of the triangle in RGB format. Default is white (1.0, 1.0, 1.0).
        """
        obj = {
            "type": "triangle",
            "x": x,
            "y": y,
            "side_length": side_length,
            "color": color
        }
        self.objects.append(obj)

    def create_point(self, x, y, color=(1.0, 1.0, 1.0)):
        """
        Create a point object.

        Args:
            x (float): X-coordinate of the point.
            y (float): Y-coordinate of the point.
            color (tuple, optional): Color of the point in RGB format. Default is white (1.0, 1.0, 1.0).
        """
        obj = {
            "type": "point",
            "x": x,
            "y": y,
            "color": color
        }
        self.objects.append(obj)

    def create_polygon(self, vertices, color=(1.0, 1.0, 1.0)):
        """
        Create a polygon object.

        Args:
            vertices (list of tuple): List of vertex positions in the format [(x1, y1), (x2, y2), ...].
            color (tuple, optional): Color of the polygon in RGB format. Default is white (1.0, 1.0, 1.0).
        """
        obj = {
            "type": "polygon",
            "vertices": vertices,
            "color": color
        }
        self.objects.append(obj)

    def create_line(self, x1=0, y1=0, x2=0, y2=0, length_line=0, degree=0, color=(1.0, 1.0, 1.0)):
        """
        Create a line object.

        Args:
            x1 (float): X-coordinate of the starting point of the line.
            y1 (float): Y-coordinate of the starting point of the line.
            x2 (float): X-coordinate of the ending point of the line.
            y2 (float): Y-coordinate of the ending point of the line.
            length_line (float): Length of the line (optional).
            degree (float): Rotation angle in degrees (optional).
            color (tuple, optional): Color of the line in RGB format. Default is white (1.0, 1.0, 1.0).
        """
        obj = {
            "type": "line",
            "x1": x1,
            "y1": y1,
            "x2": x2,
            "y2": y2,
            "length_line": length_line,
            "degree": degree,
            "color": color
        }
        self.objects.append(obj)

    def draw_object(self):
        """
        Draw the specified objects on the screen.
        """
        for obj in self.objects:
            if obj["type"] == "rectangle":
                self.draw_rectangle(obj)
            elif obj["type"] == "circle":
                self.draw_circle(obj)
            elif obj["type"] == "triangle":
                self.draw_triangle(obj)
            elif obj["type"] == "point":
                self.draw_point(obj)
            elif obj["type"] == "line":
                self.draw_line(obj)
            elif obj["type"] == "polygon":
                self.draw_polygon(obj)

    def draw_rectangle(self, obj):
        """
        Draw a rectangle object.
        """
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

    def draw_circle(self, obj):
        """
        Draw a circle object.
        """
        x = obj["x"]
        y = obj["y"]
        radius = obj["radius"]
        color = obj["color"]

        glColor3f(*color)
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(x, y)
        for i in range(360):
            angle = i * 3.1415926 / 180
            glVertex2f(x + radius * math.cos(angle), y + radius * math.sin(angle))
        glEnd()

    def draw_triangle(self, obj):
        """
        Draw a triangle object.
        """
        x = obj["x"]
        y = obj["y"]
        side_length = obj["side_length"]
        color = obj["color"]

        glColor3f(*color)
        glBegin(GL_TRIANGLES)
        glVertex2f(x, y)
        glVertex2f(x + side_length, y)
        glVertex2f(x + side_length / 2, y + (side_length * math.sqrt(3)) / 2)
        glEnd()

    def draw_point(self, obj):
        """
        Draw a point object.
        """
        x = obj["x"]
        y = obj["y"]
        color = obj["color"]

        glColor3f(*color)
        glBegin(GL_POINTS)
        glVertex2f(x, y)
        glEnd()

    def draw_polygon(self, obj):
        """
        Draw a polygon object.
        """
        vertices = obj["vertices"]
        color = obj["color"]

        glColor3f(*color)
        glBegin(GL_POLYGON)
        for vertex in vertices:
            glVertex2f(*vertex)
        glEnd()

    def draw_line(self, obj):
        """
        Draw a line object.
        """
        if "x1" in obj and "y1" in obj and "x2" in obj and "y2" in obj:
            # Case 1: Using start and end points
            x1 = obj["x1"]
            y1 = obj["y1"]
            x2 = obj["x2"]
            y2 = obj["y2"]
        elif "x" in obj and "y" in obj and "length_line" in obj:
            # Case 2: Using position (x, y) and length (length_line)
            x1 = obj["x"]
            y1 = obj["y"]
            length_line = obj["length_line"]
            degree = obj.get("degree", 0.0)
            x2 = x1 + length_line * math.cos(degree * math.pi / 180.0)
            y2 = y1 + length_line * math.sin(degree * math.pi / 180.0)
        else:
            raise ValueError("Invalid line object. Please provide either start and end points or position and length.")

        color = obj["color"]

        glColor3f(*color)
        glBegin(GL_LINES)
        glVertex2f(x1, y1)
        glVertex2f(x2, y2)
        glEnd()


if __name__ == "__main__":
    initializer = OpenGLInitializer()
    initializer.initialize_window()

    initializer.object_manager.create_rectangle(-0.5,-0.6,1,1,(0,1,0))
    initializer.object_manager.create_rectangle(-0.8,-0.7,1,1,(1,0,0))
    # initializer.object_manager.create_circle(0,0,1,(0,0,1))
    # initializer.object_manager.create_line(0,0,1,1,color=(1,1,1))
    # initializer.object_manager.create_point(-0.5,-0.5)
    glutMainLoop()
    # initializer.object_manager.create_triangle(-1, -1, 0.7,(1.0, 0.0, 0.0))
    # glutMainLoop()

# # Transformation
# class TransformObject:
#     """
#     Perform transformations on objects in the OpenGL scene.
#     """

#     def transform_object(self, obj, position, rotation, scale):
#         """
#         Transform an object by setting its position, rotation, and scale.

#         Args:
#             obj: The object to be transformed.
#             position (tuple): The new position in (x, y, z) format.
#             rotation (tuple): The rotation angles in (x, y, z) format.
#             scale (tuple): The scaling factors in (x, y, z) format.
#         """
#         pass

#     def apply_global_transformation(self, obj):
#         """
#         Apply global transformations to an object.

#         Args:
#             obj: The object to apply global transformations to.
#         """
#         pass

# # User Interaction
# class UserInteraction:
#     """
#     Handles user interaction such as mouse and keyboard input.
#     """

#     def capture_user_input(self):
#         """
#         Capture user input events, such as mouse clicks and keyboard presses.
#         """
#         pass

#     def respond_to_user_input(self, obj):
#         """
#         Respond to user input by moving or modifying objects on the screen.

#         Args:
#             obj: The object to be modified based on user input.
#         """
#         pass

# # Display Management
# class DisplayManager:
#     """
#     Manages the display settings and camera projection.
#     """

#     def set_background_color(self, color):
#         """
#         Set the background color of the scene.

#         Args:
#             color (tuple): The background color in (R, G, B) format.
#         """
#         pass

#     def configure_view_and_projection(self):
#         """
#         Configure the view and projection settings for the camera.
#         """
#         pass

# # Animation
# class Animator:
#     """
#     Creates and manages animations in the OpenGL scene.
#     """

#     def animate_object(self, obj, frame_rate):
#         """
#         Animate an object by gradually changing its properties.

#         Args:
#             obj: The object to be animated.
#             frame_rate (int): The frame rate of the animation.
#         """
#         pass

#     def set_frame_rate(self, frame_rate):
#         """
#         Set the frame rate and timing for animations.

#         Args:
#             frame_rate (int): The desired frame rate for animations.
#         """
#         pass

# # File Management
# class FileHandler:
#     """
#     Handles saving/loading projects and importing 3D models or texture images.
#     """

#     def save_project(self, project, file_name):
#         """
#         Save the OpenGL project to an external file.

#         Args:
#             project: The OpenGL project to be saved.
#             file_name (str): The name of the file to save the project to.
#         """
#         pass

#     def load_project(self, file_name):
#         """
#         Load an OpenGL project from an external file.

#         Args:
#             file_name (str): The name of the file to load the project from.
#         """
#         pass

#     def import_3d_model(self, file_name):
#         """
#         Import a 3D model from an external file.

#         Args:
#             file_name (str): The name of the 3D model file to import.
#         """
#         pass

#     def import_texture_image(self, file_name):
#         """
#         Import a texture image from an external file.

#         Args:
#             file_name (str): The name of the texture image file to import.
#         """
#         pass

# # Memory Management
# class MemoryManager:
#     """
#     Manages GPU memory allocation and prevents memory leaks.
#     """

#     def allocate_gpu_memory(self, obj):
#         """
#         Allocate GPU memory for an object to prevent memory leaks.

#         Args:
#             obj: The object for which GPU memory should be allocated.
#         """
#         pass

from GL_tools.GL_tools import *

def main():
    """ Tugas membuat nama menggunakan PyOpenGL,GLU,GLUT dan GL """
    window = OpenGLInitializer(window_size=(1000,1000),window_title="Tugas Nama",kiri=0,kanan=1000,bawah=0,atas=1000)
    window.initialize_window()
    #  Huruf A sudut [a,b,c,d,e,f,g,h] and [a,b,c]
    window.object_manager.create_polygon([(100,700),(150,800),(200,800),(250,700)],color=colors['White'])
    window.object_manager.create_polygon([(140,700),(165,740),(185,740),(210,700)],color=colors['Black'])
    window.object_manager.create_triangle(166,755,18,colors['Black'])

    #  Huruf H
    window.object_manager.create_rectangle(260,700,30,100,color=colors['White'])
    window.object_manager.create_rectangle(260,740,80,25,color=colors['White'])
    window.object_manager.create_rectangle(340,700,30,100,color=colors['White'])

    # Huruf M
    window.object_manager.create_rectangle(390 ,700,30,100,color=colors['White'])
    window.object_manager.create_rectangle(490 ,700,30,100,color=colors['White'])
    window.object_manager.create_polygon([(400,800),(445,750),(465,750),(505,800),(495,800)],color=colors['Red'])

    # Huruf A sudut [a,b,c,d,e,f,g,h] and [a,b,c]
    window.object_manager.create_polygon([(525,700),(575,800),(635,800),(685,700)],color=colors['White'])
    window.object_manager.create_polygon([(565,700),(590,740),(620,740),(645,700)],color=colors['Black'])
    window.object_manager.create_triangle(595,755,18,colors['Black'])

    # Huruf D
    window.object_manager.create_circle(735,750,50)
    window.object_manager.create_rectangle(685,690,50,120,color=colors['Black'])
    window.object_manager.create_rectangle(700,700,40,100,color=colors['White'])
    window.object_manager.create_circle(730,750,15,color=colors['Black'])
    window.object_manager.create_rectangle(710,710,20,80,color=colors['White'])

    # Huruf I
    window.object_manager.create_rectangle(100,500,30,100)
    
    # Huruf L
    window.object_manager.create_rectangle(145,500,30,100)
    window.object_manager.create_rectangle(145,500,80,25)

    # Huruf Y
    window.object_manager.create_rectangle(270,500,25,70)
    window.object_manager.create_triangle(322.1,600,-80)
    window.object_manager.create_triangle(304,600,-40,color=colors['Black'])

    glutMainLoop()
main()
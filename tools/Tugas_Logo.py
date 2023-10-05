from GL_tools.GL_tools import *

def main():
    window = OpenGLInitializer(window_size=(800,800),window_title="Logo Xendit",kiri=0,kanan=9,atas=9,bawah=0)
    
    # Tameng 1
    window.object_manager.create_polygon([(2.5110828365283,1.6948025938735),(1.5996653302464,3.2438182723229),(1.959497413408,3.2544015688864),(2.7,2)])
    window.object_manager.create_polygon([(1.5996653302464,3.2438182723229),(2.5,4.8),(2.7,4.5),(1.959497413408,3.2544015688864)])
    window.object_manager.create_polygon([(2.5,4.8),(3.4,4.8),(3.2,4.5),(2.7,4.5),(2.7,4.5)])

    # X
    window.object_manager.create_polygon([(2.7,4.5),(2.9581243868851,4.0631863646461),(2.766121510799,3.7685755875341),(2.5,4.2)],color=colors['Red'])
    window.object_manager.create_polygon([(2.5098288347141,2.312488174728),(2.7,2),(3.9741603345122,4.1918285461149),(3.7875298444594,4.4982030235776)],color=colors['Red'])
    window.object_manager.create_polygon([(3.5437625328962,2.4330239999353),(3.7145537791955,2.7264346025521),(3.9685510172818,2.319163169069),(3.8,2)],color=colors['Red'])

    # Tameng 2
    window.object_manager.create_polygon([(3.0970777348824,1.6973078620303),(3.9641717545561,1.6929285993046),(3.8,2),(3.2634897184562,1.9863392019215)])
    window.object_manager.create_polygon([(3.8,2),(3.9641717545561,1.6929285993046),(4.8865764970506,3.2644342475013),(4.5241599157606,3.2591818332797)])
    window.object_manager.create_polygon([(4.8865764970506,3.2644342475013),(4.5241599157606,3.2591818332797),(3.7875298444594,4.4982030235776),(3.9751578728795,4.8072397296619)])
    window.transform.rotate(30)

    window.initialize_window()
    glutMainLoop()
main()


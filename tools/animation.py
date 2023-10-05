from GL_tools.GL_tools import *

window = OpenGLInitializer(window_size=(720,720),window_title=("Belajar"))
window.initialize_window()

window.object_manager.create_circle(0,0,150,name="head",color=colors['Green'],opsi=0.5)
window.object_manager.create_circle(-60,-70,20,name="mata1")
window.object_manager.create_circle(60,-70,20,name="mata2")

window.object_manager.create_rectangle(-150,10,300,300,name="body",color=colors['Green'])
window.object_manager.create_circle(-192,25,40,name="bahu1",color=colors['Green'])
window.object_manager.create_circle(192,25,40,name="bahu2",color=colors['Green'])

window.object_manager.create_rectangle(-231.5,15,79,170,name="lengan1",color=colors["Green"])
window.object_manager.create_rectangle(152.5,15,79,170,name="lengan2",color=colors["Green"])

window.object_manager.create_circle(-192,180,40,name="tangan1",color=colors['Green'])
window.object_manager.create_circle(192,180,40,name="tangan2",color=colors['Green'])

window.object_manager.create_rectangle(-121.5,250,79,170,name="kaki1",color=colors["Green"])
window.object_manager.create_rectangle(42.5,250,79,170,name="kaki2",color=colors["Green"])

window.object_manager.create_circle(-82,410,39,name="alas1",color=colors['Green'])
window.object_manager.create_circle(82,410,39,name="alas2",color=colors['Green'])

window.transform.translate(0,-200,name=["head","mata1","mata2","body","lengan1","lengan2","tangan1","tangan2","kaki1","kaki2","alas1","alas2","bahu1","bahu2"])
glutMainLoop()
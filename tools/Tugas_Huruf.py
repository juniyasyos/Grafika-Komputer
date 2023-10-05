# git_clone dulu kakak di 
# git clone https://github.com/juniyasyos/GL_tools.git


# Nama : Ahmad Ilyas
# NIM  : 222410103049


from GL_tools.GL_tools import *

window = OpenGLInitializer(window_size=(700,700),window_title="Tugas Inisial Nama : Ahmad Ilyas",kiri=0,kanan=928,atas=0,bawah=700)
window.object_manager.create_rectangle(0,0,928,700,color=colors['Black'])

window.object_manager.create_polygon([(912,18),(17,18),(17,687.8798624709378),(911.9829466302,687.8798624709378)])
window.object_manager.create_polygon([(880,50),(50,50),(48,656),(880,656)],color=colors['Black'])

# Huruf A
line_A = [
    (100,112),(133,112),(316,606),(374,606),(554.9994130789462,112),(404.0259465963241,112),
    (352,268),(210,268),(155,112),(208,112),(208,100),(100,100)]
window.object_manager.create_line(x1=100,y1=112,x2=100,y2=112,lines=line_A)
window.object_manager.create_line(x1=354,y1=112,x2=354,y2=112,lines=[(354,100),(588,100),(588,112)])
window.object_manager.create_line(x1=217,y1=284,x2=217,y2=284,lines=[(284,469.5),(346.5,284)])

# Huruf I
lines_i = [
    (610,589),(650,588),(650,112),(612,112),(612,100),(830,100),(830,100),(830,112),
    (790.1004978145886,112.365931379245),(790,590),(830,590),(829.9045624678631,601.7087838498422)
]
window.object_manager.create_line(x1=610,y1=602,lines=lines_i)
window.initialize_window()
glutMainLoop()

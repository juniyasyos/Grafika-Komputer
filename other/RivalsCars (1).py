from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# import cv2 as cv
# img = cv.imread("Image/eren1.jpg")

import random as rd, os, OpenGL.GLUT as glut, math
os.system('cls')
w, h = 600, 500

play = False
selesai = False
crash_Player = False

xy = 0
xc = 0
Cek_xy = 20
#Player
xPlayer = 0
yPlayer = 35
#Musuh
xMusuh = 0
yMusuh = 0
xRintangan = 50
#Pembatas
grid_y_player = [0,160, 0,115]
#RandomMusuh
yRPlayer = rd.randrange(50, 200)

jumlah_bintang = 1000
jedag, jedug = 1, 1

ScorePlayer = 0
kecepatan = 1

#Draw Text
def drawText(ch,xpos,ypos,r,b,g):
    color = (r, b, g)
    font_style = glut.GLUT_BITMAP_8_BY_13
    glColor3ub(color[0],color[1],color[2])
    line=0
    glRasterPos2f (xpos, ypos)
    for i in ch:
        if  i=='\n':
            line=line+1
            glRasterPos2f (xpos, ypos*line)
        else:
            glutBitmapCharacter(font_style, ord(i))  

def drawTextBold(ch,xpos,ypos):
    glPushMatrix()
    color = (255,255,255)
    font_style = glut.GLUT_BITMAP_HELVETICA_18
    glColor3ub(color[0],color[1],color[2])
    line=0
    glRasterPos2f (xpos, ypos)
    for i in ch:
        if  i=='\n':
            line=line+1
            glRasterPos2f (xpos, ypos*line)
        else:
            glutBitmapCharacter(font_style, ord(i))  
    glPopMatrix()  

def drawTextNum(skor,xpos,ypos,r,b,g):
    color = (r, b, g)
    font_style = glut.GLUT_BITMAP_8_BY_13
    glColor3ub(color[0],color[1],color[2])
    line=0
    glRasterPos2f (xpos, ypos)
    for i in str(skor):
        if  i=='\n':
            line=line+1
            glRasterPos2f (xpos, ypos*line)
        else:
            glutBitmapCharacter(font_style, ord(i))

#Menu/GameOver
def mainMenu():
    glBegin(GL_QUADS)
    glColor3ub(152, 251, 152) 
    glVertex2f(0, 0)
    glVertex2f(0, 500)
    glVertex2f(700, 500)
    glVertex2f(700, 0)
    glEnd()

    def jalan():
        glBegin(GL_QUADS)
        glColor3ub(160, 160, 160) 
        glVertex2f(0, 65)
        glVertex2f(0, 0)
        glVertex2f(700, 0)
        glVertex2f(700, 65)
        glEnd()

    def TextMenu():
        def Cars():
            x = 0
            glTranslated(x, 0, 0)
            x += 10
            #C
            glLineWidth(4)
            glBegin(GL_LINE_LOOP)
            glColor3ub(255, 255, 255) 
            glVertex2f(x+3, 350)
            glVertex2f(x+3, 420)
            glEnd()
            glLineWidth(4)
            glBegin(GL_LINE_LOOP)
            glColor3ub(255, 255, 255) 
            glVertex2f(x+3, 350)
            glVertex2f(x+55, 350)
            glEnd()
            glLineWidth(4)
            glBegin(GL_LINE_LOOP)
            glColor3ub(255, 255, 255) 
            glVertex2f(x+3, 420)
            glVertex2f(x+55, 420)
            glEnd()

            #A
            glLineWidth(4)
            glBegin(GL_LINE_LOOP)
            glColor3ub(255, 255, 255) 
            glVertex2f(x+60, 345)
            glVertex2f(x+90, 425)
            glEnd()
            glLineWidth(4)
            glBegin(GL_LINE_LOOP)
            glColor3ub(255, 255, 255) 
            glVertex2f(x+90, 425)
            glVertex2f(x+120, 345)            
            glEnd()
            glLineWidth(4)
            glBegin(GL_LINE_LOOP)
            glColor3ub(255, 255, 255) 
            glVertex2f(x+110, 375)
            glVertex2f(x+70, 375)
            glEnd()

            #R
            glLineWidth(4)
            glBegin(GL_LINE_LOOP)
            glColor3ub(255, 255, 255) 
            glVertex2f(x+135, 345)
            glVertex2f(x+135, 425)
            glEnd()
            glLineWidth(4)
            glBegin(GL_LINE_LOOP)
            glColor3ub(255, 255, 255) 
            glVertex2f(x+135, 425)
            glVertex2f(x+175, 425)
            glEnd()
            glLineWidth(4)
            glBegin(GL_LINE_LOOP)
            glColor3ub(255, 255, 255) 
            glVertex2f(x+175, 425)
            glVertex2f(x+175, 395)
            glEnd()
            glLineWidth(4)
            glBegin(GL_LINE_LOOP)
            glColor3ub(255, 255, 255) 
            glVertex2f(x+175, 395)
            glVertex2f(x+135, 395)
            glEnd()
            glLineWidth(4)
            glBegin(GL_LINE_LOOP)
            glColor3ub(255, 255, 255) 
            glVertex2f(x+135, 395)
            glVertex2f(x+175, 345)
            glEnd()

            #S
            glLineWidth(4)
            glBegin(GL_LINE_LOOP)
            glColor3ub(255, 255, 255) 
            glVertex2f(x+190, 350)
            glVertex2f(x+250, 350)
            glEnd()
            glLineWidth(4)
            glBegin(GL_LINE_LOOP)
            glColor3ub(255, 255, 255) 
            glVertex2f(x+250, 350)
            glVertex2f(x+250, 380)
            glEnd()
            glLineWidth(4)
            glBegin(GL_LINE_LOOP)
            glColor3ub(255, 255, 255) 
            glVertex2f(x+250, 380)
            glVertex2f(x+190, 380)
            glEnd()
            glLineWidth(4)
            glBegin(GL_LINE_LOOP)
            glColor3ub(255, 255, 255) 
            glVertex2f(x+190, 380)
            glVertex2f(x+190, 420)
            glEnd()
            glLineWidth(4)
            glBegin(GL_LINE_LOOP)
            glColor3ub(255, 255, 255) 
            glVertex2f(x+190, 420)
            glVertex2f(x+250, 420)
            glEnd()

            #L
            glLineWidth(4)
            glBegin(GL_LINE_LOOP)
            glColor3ub(255, 255, 255) 
            glVertex2f(x+295, 345)
            glVertex2f(x+295, 425)
            glEnd()
            glLineWidth(4)
            glBegin(GL_LINE_LOOP)
            glColor3ub(255, 255, 255) 
            glVertex2f(x+295, 346)
            glVertex2f(x+348, 346)
            glEnd()

            #E
            glLineWidth(4)
            glBegin(GL_LINE_LOOP)
            glColor3ub(255, 255, 255) 
            glVertex2f(x+360, 345)
            glVertex2f(x+360, 425)
            glEnd()
            glLineWidth(4)
            glBegin(GL_LINE_LOOP)
            glColor3ub(255, 255, 255) 
            glVertex2f(x+360, 346)
            glVertex2f(x+415, 346)
            glEnd()
            glLineWidth(4)
            glBegin(GL_LINE_LOOP)
            glColor3ub(255, 255, 255) 
            glVertex2f(x+360, 386)
            glVertex2f(x+415, 386)
            glEnd()
            glLineWidth(4)
            glBegin(GL_LINE_LOOP)
            glColor3ub(255, 255, 255)
            glVertex2f(x+360, 426)
            glVertex2f(x+415, 426)
            glEnd()

            #F
            glLineWidth(4)
            glBegin(GL_LINE_LOOP)
            glColor3ub(255, 255, 255) 
            glVertex2f(x+430, 345)
            glVertex2f(x+430, 425)
            glEnd()
            glLineWidth(4)
            glBegin(GL_LINE_LOOP)
            glColor3ub(255, 255, 255) 
            glVertex2f(x+430, 386)
            glVertex2f(x+485, 386)
            glEnd()
            glLineWidth(4)
            glBegin(GL_LINE_LOOP)
            glColor3ub(255, 255, 255) 
            glVertex2f(x+430, 426)
            glVertex2f(x+485, 426)
            glEnd()

            #T
            glLineWidth(4)
            glBegin(GL_LINE_LOOP)
            glColor3ub(255, 255, 255) 
            glVertex2f(x+520, 345)
            glVertex2f(x+520, 425)
            glEnd()
            glLineWidth(4)
            glBegin(GL_LINE_LOOP)
            glColor3ub(255, 255, 255) 
            glVertex2f(x+490, 426)
            glVertex2f(x+555, 426)
            glEnd()

            #block1
            glLineWidth(10)
            glBegin(GL_LINE_LOOP)
            glColor3ub(255, 255, 255) 
            glVertex2f(x+30, 290)
            glVertex2f(x+130, 290)
            glEnd()

            #block2
            glLineWidth(10)
            glBegin(GL_LINE_LOOP)
            glColor3ub(255, 255, 255) 
            glVertex2f(x+30, 270)
            glVertex2f(x+130, 270)
            glEnd()

            #block3
            glLineWidth(10)
            glBegin(GL_LINE_LOOP)
            glColor3ub(255, 255, 255) 
            glVertex2f(x+30, 250)
            glVertex2f(x+130, 250)
            glEnd()

            #B
            glLineWidth(4)
            glBegin(GL_LINE_LOOP)
            glColor3ub(255, 255, 255) 
            glVertex2f(x+160, 235)
            glVertex2f(x+160, 315)
            glEnd()
            glLineWidth(4)
            glBegin(GL_LINE_LOOP)
            glColor3ub(255, 255, 255) 
            glVertex2f(x+160, 234)
            glVertex2f(x+236, 234)
            glEnd()
            glLineWidth(4)
            glBegin(GL_LINE_LOOP)
            glColor3ub(255, 255, 255) 
            glVertex2f(x+160, 315)
            glVertex2f(x+220, 315)
            glEnd()
            glLineWidth(4)
            glBegin(GL_LINE_LOOP)
            glColor3ub(255, 255, 255) 
            glVertex2f(x+220, 315)
            glVertex2f(x+220, 280)
            glEnd()
            glLineWidth(4)
            glBegin(GL_LINE_LOOP)
            glColor3ub(255, 255, 255) 
            glVertex2f(x+160, 278)
            glVertex2f(x+235, 278)
            glEnd()
            glLineWidth(4)
            glBegin(GL_LINE_LOOP)
            glColor3ub(255, 255, 255) 
            glVertex2f(x+235, 277)
            glVertex2f(x+235, 235)
            glEnd()

            #L
            glLineWidth(4)
            glBegin(GL_LINE_LOOP)
            glColor3ub(255, 255, 255) 
            glVertex2f(x+255, 235)
            glVertex2f(x+255, 315)
            glEnd()
            glLineWidth(4)
            glBegin(GL_LINE_LOOP)
            glColor3ub(255, 255, 255) 
            glVertex2f(x+255, 236)
            glVertex2f(x+313, 236)
            glEnd()

            #O
            glLineWidth(4)
            glBegin(GL_LINE_LOOP)
            glColor3ub(255, 255, 255) 
            glVertex2f(x+325, 236)
            glVertex2f(x+325, 315)
            glEnd()
            glLineWidth(4)
            glBegin(GL_LINE_LOOP)
            glColor3ub(255, 255, 255) 
            glVertex2f(x+323, 235)
            glVertex2f(x+380, 235)
            glEnd()
            glLineWidth(4)
            glBegin(GL_LINE_LOOP)
            glColor3ub(255, 255, 255) 
            glVertex2f(x+323, 313)
            glVertex2f(x+380, 313)
            glEnd()
            glLineWidth(4)
            glBegin(GL_LINE_LOOP)
            glColor3ub(255, 255, 255) 
            glVertex2f(x+377, 236)
            glVertex2f(x+377, 315)
            glEnd()

            #C
            glLineWidth(4)
            glBegin(GL_LINE_LOOP)
            glColor3ub(255, 255, 255) 
            glVertex2f(x+400, 237)
            glVertex2f(x+400, 315)
            glEnd()
            glLineWidth(4)
            glBegin(GL_LINE_LOOP)
            glColor3ub(255, 255, 255) 
            glVertex2f(x+400, 235)
            glVertex2f(x+452, 235)
            glEnd()
            glLineWidth(4)
            glBegin(GL_LINE_LOOP)
            glColor3ub(255, 255, 255) 
            glVertex2f(x+400, 315)
            glVertex2f(x+452, 315)
            glEnd()

            #R
            glLineWidth(4)
            glBegin(GL_LINE_LOOP)
            glColor3ub(255, 255, 255) 
            glVertex2f(x+470, 230)
            glVertex2f(x+470, 320)
            glEnd()
            glLineWidth(4)
            glBegin(GL_LINE_LOOP)
            glColor3ub(255, 255, 255) 
            glVertex2f(x+470, 280)
            glVertex2f(x+520, 230)
            glEnd()
            glLineWidth(4)
            glBegin(GL_LINE_LOOP)
            glColor3ub(255, 255, 255) 
            glVertex2f(x+470, 280)
            glVertex2f(x+520, 310)
            glEnd()
            


        Cars()

    def start_game():
        glPushMatrix()
        glColor3b(36, 150, 127)
        glBegin(GL_QUADS)
        glVertex2f(200, 100)
        glVertex2f(400, 100)
        glVertex2f(400, 160)
        glVertex2f(200, 160)
        glEnd()
        glColor3ub(0,0,0)
        glLineWidth(3)
        glBegin(GL_LINE_LOOP)
        glVertex2f(200, 100)
        glVertex2f(400, 100)
        glVertex2f(400, 160)
        glVertex2f(200, 160)
        glEnd()
        glPopMatrix()
        drawTextBold("P L A Y G A M E",235,125)
    
    jalan(), TextMenu(), start_game()

def GameOver():
    glPushMatrix()
    glColor3ub(152, 251, 152)
    glBegin(GL_QUADS)
    glVertex2f(0, 0)
    glVertex2f(0, 500)
    glVertex2f(700, 500)
    glVertex2f(700, 0)
    glEnd()
    glPopMatrix()

    def Score_Player():
        drawText('SCORE : ',15,480,0,0,0)
        drawTextNum(ScorePlayer,15,460,0,0,0)

    def kelapKelip():
        glPointSize(8)
        glColor3f(1.0, 1.0, 1.0) #RGB
        glBegin(GL_POINTS)
        y = 1000
        for i in range(jumlah_bintang):
            x = rd.randrange(-1000,1000)
            glVertex2f(x,y)
            if y != 1000:
                x = x
            y -= 100
        glEnd()

    def Game():
        global jedag, jedug
        #G
        glLineWidth(10)     
        glBegin(GL_LINE_LOOP)
        glVertex2f(200,450)
        glVertex2f(100,450)
        glEnd()
        glLineWidth(10)     
        glBegin(GL_LINE_LOOP)
        glVertex2f(100,450)
        glVertex2f(100,350)
        glEnd()
        glLineWidth(10)     
        glBegin(GL_LINE_LOOP)
        glVertex2f(100,350)
        glVertex2f(200,350)
        glEnd()
        glLineWidth(10)     
        glBegin(GL_LINE_LOOP)
        glVertex2f(200,350)
        glVertex2f(200,400)
        glEnd()
        glLineWidth(10)     
        glBegin(GL_LINE_LOOP)
        glVertex2f(200,400)
        glVertex2f(150,400)
        glEnd()

        #A
        glLineWidth(10)     
        glBegin(GL_LINE_LOOP)
        glVertex2f(200,350)
        glVertex2f(250,450)
        glEnd()
        glLineWidth(10)     
        glBegin(GL_LINE_LOOP)
        glVertex2f(250,450)
        glVertex2f(300,350)
        glEnd()
        glLineWidth(10)     
        glBegin(GL_LINE_LOOP)
        glVertex2f(225,400)
        glVertex2f(275,400)
        glEnd()

        #M
        glLineWidth(10)     
        glBegin(GL_LINE_LOOP)
        glVertex2f(300,350)
        glVertex2f(300,450)
        glEnd()
        glLineWidth(10)     
        glBegin(GL_LINE_LOOP)
        glVertex2f(300,450)
        glVertex2f(350,400)
        glEnd()
        glLineWidth(10)     
        glBegin(GL_LINE_LOOP)
        glVertex2f(350,400)
        glVertex2f(400,450)
        glEnd()
        glLineWidth(10)     
        glBegin(GL_LINE_LOOP)
        glVertex2f(400,450)
        glVertex2f(400,350)
        glEnd()

        #E
        glLineWidth(10)     
        glBegin(GL_LINE_LOOP)
        glVertex2f(400,450)
        glVertex2f(500,450)
        glEnd()
        glLineWidth(10)     
        glBegin(GL_LINE_LOOP)
        glVertex2f(400,400)
        glVertex2f(500,400)
        glEnd()
        glLineWidth(10)     
        glBegin(GL_LINE_LOOP)
        glVertex2f(400,350)
        glVertex2f(500,350)
        glEnd()

    def Over():
        #O
        glLineWidth(10)     
        glBegin(GL_LINE_LOOP)
        glVertex2f(100,330)
        glVertex2f(200,330)
        glVertex2f(200,230)
        glVertex2f(100,230)
        glVertex2f(100,230)
        glEnd()

        #V
        glLineWidth(10)     
        glBegin(GL_LINE_LOOP)
        glVertex2f(200,330)
        glVertex2f(250,230)
        glEnd()
        glLineWidth(10)     
        glBegin(GL_LINE_LOOP)
        glVertex2f(250,230)
        glVertex2f(300,330)
        glEnd()

        #E
        glLineWidth(10)     
        glBegin(GL_LINE_LOOP)
        glVertex2f(300,330)
        glVertex2f(300,230)
        glEnd()
        glLineWidth(10)     
        glBegin(GL_LINE_LOOP)
        glVertex2f(300,330)
        glVertex2f(400,330)
        glEnd()
        glLineWidth(10)     
        glBegin(GL_LINE_LOOP)
        glVertex2f(300,280)
        glVertex2f(400,280)
        glEnd()
        glLineWidth(10)     
        glBegin(GL_LINE_LOOP)
        glVertex2f(300,230)
        glVertex2f(400,230)
        glEnd()

        #R
        glLineWidth(10)     
        glBegin(GL_LINE_LOOP)
        glVertex2f(400,330)
        glVertex2f(400,230)
        glEnd()
        glLineWidth(10)     
        glBegin(GL_LINE_LOOP)
        glVertex2f(400,330)
        glVertex2f(500,330)
        glEnd()
        glLineWidth(10)     
        glBegin(GL_LINE_LOOP)
        glVertex2f(500,330)
        glVertex2f(500,280)
        glEnd()
        glLineWidth(10)     
        glBegin(GL_LINE_LOOP)
        glVertex2f(500,280)
        glVertex2f(400,280)
        glEnd()
        glLineWidth(10)     
        glBegin(GL_LINE_LOOP)
        glVertex2f(400,280)
        glVertex2f(500,230)
        glEnd()

    def Ulang():
        # drawTextBold("E N T E R  U N T U K  M E N G U L A N G",130,125)
        drawTextBold("By Kelompok H Grafika Komputer",160,10)
    
    Score_Player(), kelapKelip(), Ulang(), Game(), Over()

#Asset Game
#MobilPlayer
def Player(cx, cy):
    global xPlayer, yPlayer, xMusuh, yMusuh, crash_Player, yRPlayer

    def circle1(cx,cy,r,num_segment): #BAN BELAKANG
        glBegin(GL_POLYGON)
        glColor3ub(96,96,96)
        for i in range(num_segment):
            theta= 2 *3.1415926*i/num_segment
            x = r * math.cos(theta)
            y = r * math.sin(theta)
            glVertex2f(x + cx, y + cy)
        glEnd()

    def circle2(cx,cy,r,num_segment): #BAN DEPAN
        glBegin(GL_POLYGON)
        glColor3ub(96,96,96)
        for i in range(num_segment):
            theta= 2 *3.1415926*i/num_segment
            x = r * math.cos(theta)
            y = r * math.sin(theta)
            glVertex2f(x + cx, y + cy)
        glEnd()

    def circle3(cx,cy,r,num_segment): #BAN DALEM BELAKANG
        glBegin(GL_POLYGON)
        glColor3ub(0,0,255)
        for i in range(num_segment):
            theta= 2 *3.1415926*i/num_segment
            x = r * math.cos(theta)
            y = r * math.sin(theta)
            glVertex2f(x + cx, y + cy)
        glEnd()

    def circle4(cx,cy,r,num_segment): #BAN DALEM DEPAN
        glBegin(GL_POLYGON)
        glColor3ub(0,0,255)
        for i in range(num_segment):
            theta= 2 *3.1415926*i/num_segment
            x = r * math.cos(theta)
            y = r * math.sin(theta)
            glVertex2f(x + cx, y + cy)
        glEnd()
    #bodyBelakang
    glColor3ub(255,0,0)
    glBegin(GL_POLYGON)
    glVertex2f(22+cx, 48+cy)#S
    glVertex2f(22+cx, 42+cy)#R
    glVertex2f(28+cx, 34+cy)#Q
    glVertex2f(40+cx, 28+cy)#P
    glVertex2f(45+cx, 28+cy)#O
    glVertex2f(65+cx, 28+cy)#G1
    glVertex2f(70+cx, 26+cy)#h1
    glVertex2f(98+cx, 26+cy)#a3
    glVertex2f(98+cx, 74+cy)#b3
    glVertex2f(69+cx, 74+cy)#e1
    glVertex2f(60+cx, 70+cy)#d1
    glVertex2f(45+cx, 60+cy)#c1
    glVertex2f(33+cx, 53+cy)#b1
    glVertex2f(26+cx, 53+cy)#w
    glVertex2f(25+cx, 53+cy)#v
    glVertex2f(24+cx, 52+cy)#u
    glVertex2f(24+cx, 48+cy)#t
    #bodyDepan
    glVertex2f(98+cx, 26+cy)#a3 
    glVertex2f(140+cx, 26+cy)#i1
    glVertex2f(161+cx, 26+cy)#m1
    glVertex2f(190+cx, 26+cy)#n1
    glVertex2f(194+cx, 27+cy)#z1
    glVertex2f(197+cx, 31+cy)#w1
    glVertex2f(193+cx, 30+cy)#v1
    glVertex2f(197+cx, 42+cy)#u1
    glVertex2f(196+cx, 44+cy)#t1
    glVertex2f(192+cx, 46+cy)#s1
    glVertex2f(193+cx, 49+cy)#r1
    glVertex2f(193+cx, 53+cy)#q1
    glVertex2f(186+cx, 56+cy)#p1
    glVertex2f(155+cx, 59+cy)#o1
    glVertex2f(146+cx, 63+cy)#k1
    glVertex2f(134+cx, 72+cy)#j1
    glVertex2f(129+cx, 74+cy)#f1
    glVertex2f(98+cx, 74+cy)#b3
    glEnd()
    #kacaDepan
    glColor3ub(255, 255, 255)
    glBegin(GL_POLYGON)
    glVertex2f(134+cx, 72+cy)#j1
    glVertex2f(129+cx, 72+cy)#a2 
    glVertex2f(148+cx, 56+cy)#b2
    glVertex2f(155+cx, 59+cy)#o1
    glVertex2f(146+cx, 63+cy)#k1
    glEnd()
    glColor3ub(0, 0, 0)
    glLineWidth(1)
    glBegin(GL_LINES)
    glVertex2f(134+cx, 72+cy)#j1
    glVertex2f(129+cx, 72+cy)#a2 
    glVertex2f(148+cx, 56+cy)#b2
    glVertex2f(129+cx, 72+cy)#a2 
    glVertex2f(148+cx, 56+cy)#b2
    glVertex2f(155+cx, 59+cy)#o1
    glVertex2f(146+cx, 63+cy)#k1
    glEnd()
    #kacaPintuDepan
    glColor3ub(255, 255, 255)
    glBegin(GL_POLYGON)
    glVertex2f(125+cx, 72+cy)#c2
    glVertex2f(136+cx, 63+cy)#d2 
    glVertex2f(143+cx, 55+cy)#e2
    glVertex2f(99+cx, 55+cy)#d3
    glVertex2f(98+cx, 72+cy)#j2
    glEnd()
    glColor3ub(0, 0, 0)
    glLineWidth(1)
    glBegin(GL_LINES)
    glVertex2f(125+cx, 72+cy)#c2
    glVertex2f(125+cx, 72+cy)#c2
    glVertex2f(136+cx, 63+cy)#d2 
    glVertex2f(136+cx, 63+cy)#d2 
    glVertex2f(143+cx, 55+cy)#e2
    glVertex2f(99+cx, 55+cy)#d3
    glVertex2f(98+cx, 72+cy)#j2
    glVertex2f(98+cx, 72+cy)#j2
    glEnd()
    #kacaPintuDBelakang
    glColor3ub(255, 255, 255)
    glBegin(GL_POLYGON)
    glVertex2f(70+cx, 72+cy)#r2
    glVertex2f(94+cx, 72+cy)#k2 
    glVertex2f(95+cx, 56+cy)#c3
    glVertex2f(50+cx, 56+cy)#p2
    glVertex2f(65+cx, 69+cy)#q2
    glEnd()
    glColor3ub(0, 0, 0)
    glLineWidth(1)
    glBegin(GL_LINES)
    glVertex2f(70+cx, 72+cy)#r2
    glVertex2f(94+cx, 72+cy)#k2 
    glVertex2f(94+cx, 72+cy)#k2 
    glVertex2f(95+cx, 56+cy)#c3
    glVertex2f(95+cx, 56+cy)#c3
    glVertex2f(50+cx, 56+cy)#p2
    glVertex2f(50+cx, 56+cy)#p2
    glVertex2f(65+cx, 69+cy)#q2
    glEnd()
    #PintuDepan
    glColor3ub(255, 255, 153)
    glBegin(GL_POLYGON)
    glVertex2f(99+cx, 55+cy)#d3
    glVertex2f(143+cx, 55+cy)#e2
    glVertex2f(143+cx, 33+cy)#f2
    glVertex2f(141+cx, 28+cy)#g2
    glVertex2f(98+cx, 28+cy)#h2
    glVertex2f(100+cx, 50+cy)#i2
    glEnd()
    glColor3ub(0, 0, 0)
    glLineWidth(1)
    glBegin(GL_LINES)
    glVertex2f(99+cx, 55+cy)#d3
    glVertex2f(100+cx, 50+cy)#i2
    glVertex2f(100+cx, 50+cy)#i2
    glVertex2f(98+cx, 28+cy)#h2

    glVertex2f(143+cx, 55+cy)#e2
    glVertex2f(143+cx, 33+cy)#f2
    glVertex2f(143+cx, 33+cy)#f2
    glVertex2f(141+cx, 28+cy)#g2
    glEnd()
    #PintuBelakang
    glColor3ub(255, 255, 153)
    glBegin(GL_POLYGON)
    glVertex2f(50+cx, 56+cy)#p2
    glVertex2f(95+cx, 56+cy)#c3
    glVertex2f(96+cx, 49+cy)#l2
    glVertex2f(94+cx, 29+cy)#m2
    glVertex2f(64+cx, 29+cy)#n2
    glVertex2f(50+cx, 50+cy)#o2
    glEnd()
    glColor3ub(0, 0, 0)
    glLineWidth(1)
    glBegin(GL_LINES)
    glVertex2f(95+cx, 56+cy)#c3
    glVertex2f(96+cx, 49+cy)#l2
    glVertex2f(96+cx, 49+cy)#l2
    glVertex2f(94+cx, 29+cy)#m2

    glVertex2f(50+cx, 56+cy)#p2
    glVertex2f(50+cx, 50+cy)#o2
    glVertex2f(50+cx, 50+cy)#o2
    glVertex2f(64+cx, 29+cy)#n2
    glEnd()

    #LampuDepan
    glColor3ub(255, 255, 255)
    glBegin(GL_POLYGON)
    glVertex2f(192+cx, 46+cy)#s1
    glVertex2f(193+cx, 49+cy)#r1
    glVertex2f(193+cx, 53+cy)#q1
    glVertex2f(182+cx, 53+cy)#s2
    glVertex2f(180+cx, 50+cy)#t2
    glVertex2f(183+cx, 46+cy)#u2
    glEnd()
    #LampuBelakang
    glColor3ub(255, 255, 255)
    glBegin(GL_POLYGON)
    glVertex2f(24+cx, 52+cy)#u
    glVertex2f(24+cx, 48+cy)#t
    glVertex2f(30+cx, 48+cy)#z2
    glVertex2f(32+cx, 50+cy)#w2
    glVertex2f(32+cx, 52+cy)#v2
    glEnd()

    #BodyKitBawah
    glColor3ub(2255,215,0)
    glBegin(GL_POLYGON)
    glVertex2f(40+cx, 28+cy)#P
    glVertex2f(45+cx, 28+cy)#O
    glVertex2f(65+cx, 28+cy)#G1
    glVertex2f(70+cx, 26+cy)#h1
    glVertex2f(98+cx, 26+cy)#a3
    glVertex2f(140+cx, 26+cy)#i1
    glVertex2f(161+cx, 26+cy)#m1
    glVertex2f(190+cx, 26+cy)#n1
    glVertex2f(194+cx, 27+cy)#z1
    glVertex2f(197+cx, 31+cy)#w1
    glVertex2f(193+cx, 30+cy)#v1
    glVertex2f(36+cx, 30+cy)#e3
    glEnd()

    circle1(55+cx,32+cy,12,360)
    circle3(55+cx,32+cy,7,360)
    circle2(150+cx,32+cy,12,360)
    circle4(150+cx,32+cy,7,360)
#Musuh/Rintangan
def Musuh(dx, dy):
    global xMusuh, yMusuh, yRPlayer, selesai, crash_Player, yPlayer, xPlayer
    glColor3ub(150, 75, 0) 
    glBegin(GL_POLYGON)
    glVertex2f(100+dx, 20+dy)#f3
    glVertex2f(50+dx, 20+dy)#g3
    glVertex2f(50+dx, 150+dy)#h1
    glVertex2f(100+dx, 150+dy)#i1
    glEnd()

def background():
    glPushMatrix()
    glColor3ub(152, 251, 152)
    glBegin(GL_QUADS)
    glVertex2f(0, 0)
    glVertex2f(0, 500)
    glVertex2f(700, 500)
    glVertex2f(700, 0)
    glEnd()
    glPopMatrix()
#Jalan
def jalan():
    glBegin(GL_QUADS) 
    glColor3ub(160,160,160)
    glVertex2f(0, 190)
    glVertex2f(0, 0)
    glVertex2f(1000, 0)
    glVertex2f(1000, 190)
    glEnd()

    def GarisTJalan(kck):
        glColor3ub(0,0,0)
        glLineWidth(30)
        glBegin(GL_LINES)
        glVertex2f(0, kck)
        glVertex2f(1000, kck)
        glEnd()

    def Tepi(tp):
        glColor3ub(0,0,0)
        glLineWidth(25)
        glBegin(GL_LINES)
        glVertex2f(0, tp)
        glVertex2f(1000, tp)
        glEnd()
    
    def GMidJalan(kx, ky):
        global xy, Cek_xy
        glPushMatrix()
        glTranslated(xy, 0, 0)
        glColor3ub(255, 255, 255)
        glLineWidth(15)
        glBegin(GL_LINES)
        glVertex2f(kx, ky)
        glVertex2f(kx + 70, ky)
        glEnd()
        glPopMatrix()

    def transMidJalan():
        def MidJalan1():
            GMidJalan(30, 100)
        def MidJalan2():
            GMidJalan(130, 100)
        def MidJalan3():
            GMidJalan(230, 100)
        def MidJalan4():
            GMidJalan(330, 100)
        def MidJalan5():
            GMidJalan(430, 100)
        def MidJalan6():
            GMidJalan(530, 100)
        def MidJalan7():
            GMidJalan(630, 100)
        def MidJalan8():
            GMidJalan(730, 100)
        def MidJalan9():
            GMidJalan(830, 100)
        def MidJalan10():
            GMidJalan(930, 100)
        def MidJalan11():
            GMidJalan(1030, 100)

        MidJalan1()
        MidJalan2()
        MidJalan3()
        MidJalan4()
        MidJalan5()
        MidJalan6()
        MidJalan7()
        MidJalan8()
        MidJalan9()
        MidJalan10()
        MidJalan11()

    def Pembatas(pbt):
        glColor3ub(0, 0, 0)
        glLineWidth(20)
        glBegin(GL_LINES)
        glVertex2f(0, pbt)
        glVertex2f(700, pbt)
        glEnd()

    Tepi(190), Pembatas(200), Pembatas(10), GarisTJalan(100), transMidJalan()
#Kota
def kota(zx, vy):
    global xy, Cek_xy
    glPushMatrix()
    xy -= 0.5
    if xy < -400:
        xy = Cek_xy
    glTranslated(xy, 0, 0)
    glBegin(GL_QUADS) 
    glColor3ub(128,128,128) #ABU TUA
    glVertex2f(zx + 0, 190)
    glVertex2f(zx + 0, vy+320)
    glVertex2f(zx + 100, vy+320)
    glVertex2f(zx + 100, 190)
    glEnd()
    glPopMatrix()

def transKota():
    def kota1():
        kota(0,0)
    def kota2():
        kota(115, -30)
    def kota3():
        kota(220, 45)
    def kota4():
        kota(340, -20)
    def kota5():
        kota(440, 25)
    def kota6():
        kota(570, -10)
    def kota7():
        kota(640, 10)
    def kota8():
        kota(770, 20)
    def kota9():
        kota(840, 30)
    def kota10():
        kota(940, -10)
    
    kota1(), kota2(),kota3(),kota4(),kota5(),kota6(),kota7(),kota8(),kota9(),kota10()
#Salju
def salju():
    glPointSize(9)
    glColor3f(135.0, 206.0, 250.0) #RGB
    glBegin(GL_POINTS)
    y = 1000
    for i in range(jumlah_bintang):
        x = rd.randrange(-1000,1000)
        glVertex2f(x,y)
        if y != 1000:
            x = x
        y -= 50
    glEnd()
#Score
def Score_Player():
    drawText('SCORE : ',15,480,0,0,0)
    drawTextNum(ScorePlayer,15,460,0,0,0) 
#Logika
def collisionMusuh():
    global yPlayer, yRPlayer, xMusuh, yMusuh, crash_Player, selesai
    
    #Collision Musuh
    xMusuh -= 2
    if xMusuh < -600:
        yRPlayer = rd.randrange(yMusuh -250, yMusuh +125)
        yMusuh = yRPlayer
        xMusuh = 500
        
    #Collision Musuh dengan Player
    if yPlayer in range(yRPlayer-50, yRPlayer+50) and xMusuh < -390:
        crash_Player = True

    #Collision Batas Musuh
    if not selesai:
        if yMusuh > 140:
            yMusuh = 140
        if yMusuh < 10:
            yMusuh = 10

def key_Mobil(key, x, y):
    global xPlayer, yPlayer, crash_Player, play
    if key == GLUT_KEY_UP:
        if crash_Player == False:
            if yPlayer+50 > grid_y_player[1]:
                yPlayer += 0
                crash_Player = True
            else:
                yPlayer += 15
        else:
            yPlayer += 0
    elif key == GLUT_KEY_DOWN:
        if crash_Player == False:
            if yPlayer-5 < grid_y_player[0]:
                yPlayer -= 0
                crash_Player = True
            else:
                yPlayer -= 15
        else:
            yPlayer -= 0
    elif key == GLUT_KEY_RIGHT:
        if xPlayer+50 > 600:
            xPlayer +=0
        else:
            xPlayer += 0
    elif key == GLUT_KEY_LEFT:
        if xPlayer-20 < 0:
            xPlayer -=0
        else:
            xPlayer -= 0

def inputMouse(button, state, x,y):
    global play, crash_Player

    if button == GLUT_LEFT_BUTTON:
        if (x >= 200 and x <= 400) and (y >= 340 and y <=420):
            play = True

#Play
def playG():
    background()
    transKota()
    salju()
    Score_Player()
    jalan()
    Player(xPlayer, yPlayer)
    Musuh(xMusuh, yMusuh)
    collisionMusuh()

def play_Game():
    global ScorePlayer, kecepatan, cek_Kecepatan
    if crash_Player == False:
        playG()
        ScorePlayer += kecepatan

    if crash_Player == True:
        GameOver()

def iterate():
    glViewport(0, 0, 600, 500) #utk mengatur area pandang
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 600, 0.0, 500, 0.0, 1.0) #utk mengatur berapa blok yang digunakan (skala) nilai x, y, z
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) 
    glLoadIdentity()
    iterate()
    if play == False:
        mainMenu()
    else:
        play_Game()
    glFlush()
    glutSwapBuffers()

def Main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize(w,h)
    glutInitWindowPosition(350, 100)
    wind = glutCreateWindow("CARS LEFT BLOCK")
    glutDisplayFunc(showScreen)
    glutSpecialFunc(key_Mobil)
    glutKeyboardFunc(key_Mobil)
    glutIdleFunc(showScreen)
    glutMouseFunc(inputMouse)
    glutMainLoop()
    # cv.imshow("Gambar Eren",img)
    # cv.waitKey(30)

Main()
import pygame
import sys

class Beranda:
    def __init__(self,screen) -> None:
        self.info = pygame.display.Info()
        self.rasio_button = 0.13
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.color_lvl = 'silver'
        self.height_lvl = 0
        self.width_lvl = 0
        self.path = "Beranda"
    
    def button(self,color,size,color_hover,text,pos_x,pos_y,text_color='black',text_color_hover="white",action=None,parameters=[]):
        font = pygame.font.Font(None,24)
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        if pos_x < mouse_pos[0] < pos_x + size[0] and pos_y < mouse_pos[1] < pos_y + size[1]:
            pygame.draw.rect(self.screen,color_hover,(pos_x,pos_y,size[0],size[1]),border_radius=10)
            if mouse_click[0] == 1 and action is not None:
                for i in range(len(action)):
                    if parameters == []:
                        action[i]()
                    else:
                        if parameters[i][0] == None:
                            action[i]()
                        else:
                            action[i](*parameters[i])
        else:
            pygame.draw.rect(self.screen,color,(pos_x,pos_y,size[0],size[1]),border_radius=10)
        
        text_hover = font.render(text,True,text_color_hover if pos_x < mouse_pos[0] < pos_x + size[0] and pos_y < mouse_pos[1] < pos_y + size[1] else text_color)
        text_rect = text_hover.get_rect(center=(pos_x + size[0] / 2, pos_y + size[1] / 2))
        self.screen.blit(text_hover,text_rect)
    

    def menu_lvl(self):
        pygame.draw.rect(self.screen, self.color_lvl, (self.width_lvl//6+400,self.height_lvl//6, self.width_lvl//1.5-400, self.height_lvl//1.5+100), border_radius=10)
        for i in range(5):
            self.button(color='cyan',color_hover='black',text=f"Stage {i+1}",size=(400,80),pos_y=(self.height_lvl//2-(250 - (i*90))),pos_x=self.width_lvl//2)
        self.button(color='cyan',color_hover='black',text=f"Back",size=(400,80),pos_y=(self.height_lvl//2)+260,pos_x=self.width_lvl//2,action=[self.set_path],parameters=[["Beranda"]])


    def rendering(self, color,height,width):
        self.height_lvl = height
        self.width_lvl = width

        if self.path == "Beranda":
            pygame.draw.rect(self.screen, color, (width//6,height//6, width//1.5, height//1.5), border_radius=10)
            self.button(color='white',color_hover='black',text="Battle",size=(400,80),pos_y=height//2-100,pos_x=width//2+30,action=[self.menu_lvl,self.set_path],parameters=[[None],["Beranda/Stage"]])
            self.button(color='white',color_hover='black',text="Inventory",size=(400,80),pos_y=height//2+20,pos_x=width//2+30)
            self.button(color='white',color_hover='black',text="Quit",size=(400,80),pos_y=height//2+140,pos_x=width//2+30,action=[pygame.quit,sys.exit])
        elif self.path == "Beranda/Stage":
            self.menu_lvl()
    

    def set_path(self,path):
        self.path = path

    
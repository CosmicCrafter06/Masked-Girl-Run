import pygame as pg

class Girl(pg.sprite.Sprite):
    def __init__(self):
        super(Girl,self).__init__()
        self.girl_run_list=[pg.image.load("assets\Char_Girl_runnig1.png").convert_alpha(),
                            pg.image.load("assets/Char_Girl_runnig2.png").convert_alpha()]
        self.girl_duck_list=[pg.image.load("assets\Char_Girl_ducking1.png").convert_alpha(),
                            pg.image.load("assets\Char_Girl_ducking2.png").convert_alpha()]

        self.image=self.girl_run_list[0]
        self.mask=pg.mask.from_surface(self.image)
        self.resetGirl()
        self.gravity=10
        self.jump_speed=250

    
    def update(self,dt):
        keys=pg.key.get_pressed()
        if keys[pg.K_DOWN]: self.duck=True
        else: self.duck=False

        if self.is_on_ground:
            if self.anim_counter==5:

                if self.duck: 
                    self.image=self.girl_duck_list[self.image_switch]
                    self.rect=pg.Rect(458, 265, 55,30)
                else: 
                    self.image=self.girl_run_list[self.image_switch]
                    self.rect=pg.Rect(467,250,43,51)
                self.mask=pg.mask.from_surface(self.image)
                
                if self.image_switch==0: self.image_switch=1
                else: self.image_switch=0

                self.anim_counter=0
            self.anim_counter+=1
        else:
            self.velocity_y+=self.gravity*dt
            self.rect.y+=self.velocity_y
            if self.rect.y>=250:
                self.is_on_ground=True
                self.rect.y=250

    def jumpGirl(self,dt):
        if self.is_on_ground:
            self.velocity_y=-self.jump_speed*dt
            self.is_on_ground=False

    
    def resetGirl(self):
        self.rect=pg.Rect(467,250,43,51)
        self.image_switch=1
        self.anim_counter=0
        self.duck=False
        self.is_on_ground=True
        self.velocity_y=0


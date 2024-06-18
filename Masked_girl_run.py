import pygame as pg
import sys,time
from girl import Girl
from trap import Trap
from hurdle import Hurdle
import random
pg.init()
pg.display.set_caption("Masked girl run")

class Game:
    def __init__(self):
        self.width=1000
        self.height=600
        self.win=pg.display.set_mode((self.width,self.height))
        self.clock=pg.time.Clock()

        self.ground1=pg.image.load("Assets\ground.png").convert_alpha()
        self.ground1_rect=self.ground1.get_rect(center=(500,300))

        self.ground2=pg.image.load("Assets\ground.png").convert_alpha()
        self.ground2_rect=self.ground2.get_rect()
        self.ground2_rect=self.ground2.get_rect(center=(1100,300))

        self.font=pg.font.Font("Assets/font.ttf",20)
        self.label_score=self.font.render("Score: 0",True,(255,255,255))
        self.label_score_rect=self.label_score.get_rect(center=(900,20))

        self.label_restart=self.font.render("Restart Game",True,(255,255,255))
        self.label_restart_rect=self.label_restart.get_rect(center=(500,300))

        self.girl=Girl()
        self.game_lost=False
        self.move_speed=250
        self.enemy_spawn_counter=0
        self.enemy_spawn_time=80
        self.score=0
        self.enemy_group=pg.sprite.Group()

        self.dead_sound=pg.mixer.Sound("Assets/sfx/dead.mp3")
        self.jump_sound=pg.mixer.Sound("Assets/sfx/jump.mp3")
        self.points_sound=pg.mixer.Sound("Assets/sfx/points.mp3")

        self.gameLoop()
    
    def checkCollisions(self):
        if pg.sprite.spritecollide(self.girl,self.enemy_group,False,pg.sprite.collide_mask):
            self.stopGame()
    
    def stopGame(self):
        self.game_lost=True
        self.dead_sound.play()

    def restart(self):
        self.game_lost=False
        self.score=0
        self.enemy_spawn_counter=0
        self.move_speed=250
        self.label_score=self.font.render("Score: 0",True,(255,255,255))
        self.girl.resetGirl()

        for enemy in self.enemy_group:
            enemy.deleteMyself()

    def gameLoop(self):
        last_time=time.time()
        while True:
            new_time=time.time()
            dt=new_time-last_time
            last_time=new_time

            for event in pg.event.get():
                if event.type==pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type==pg.KEYDOWN:
                    print(f"key {event.key} pressed")
                    if event.key==pg.K_UP:
                        print(f"key {event.key} pressed")
                        if not self.game_lost:
                            self.girl.jumpGirl(dt)
                            self.jump_sound.play()
                        else:
                            self.restart()

            
            self.win.fill((0, 0, 0))
            if not self.game_lost:
                self.ground1_rect.x-=int(self.move_speed*dt)
                self.ground2_rect.x-=int(self.move_speed*dt)

                if self.ground1_rect.right<0:
                    self.ground1_rect.x=600
                if self.ground2_rect.right<0:
                    self.ground2_rect.x=600

                self.score+=0.1
                self.label_score=self.font.render(f"Score: {int(self.score)}",True,(255, 255, 255))
                self.girl.update(dt)
                self.enemy_group.update(dt)

                if self.enemy_spawn_counter==self.enemy_spawn_time:
                    if random.randint(0,1)==0: self.enemy_group.add(Trap(self.enemy_group,self.move_speed))
                    else: self.enemy_group.add(Hurdle(self.enemy_group,self.move_speed))
                    self.enemy_spawn_counter=0
                self.enemy_spawn_counter+=1

                if int(self.score)%30==0:
                    self.move_speed+=5
                    for enemy in self.enemy_group:
                        enemy.setMoveSpeed(self.move_speed)

                if int(self.score+1)%100==0:
                    self.points_sound.play()

                self.win.blit(self.girl.image,self.girl.rect)
                for enemy in self.enemy_group:
                    self.win.blit(enemy.image,enemy.rect)
                
                self.checkCollisions()
            else:
                self.win.blit(self.label_restart,self.label_restart_rect)
            
            self.win.blit(self.ground1,self.ground1_rect)
            self.win.blit(self.ground2,self.ground2_rect)
            self.win.blit(self.label_score,self.label_score_rect)
            pg.display.update()
            self.clock.tick(60)



game=Game()

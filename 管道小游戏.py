# -*- coding: utf-8 -*-

import pygame
import sys
import random
from pygame.sprite import Sprite
from pygame.sprite import Group

class Setting():
    '''记录类中的各种基本信息'''
    def __init__(self):
        #屏幕信息
        self.screen_width = 800
        self.screen_height = 600
        
        #小鸟信息
        self.bird_up_speed = 10
        self.bird_down_speed = 5
        self.bird_dead = True
        self.bird_up = False
        self.bird_down = False
        
        #管道信息
        self.pipe_speed = 4
        self.pipes_allowed = 4
        self.pipes_between = 40
        self.pipes_distance = 200
        
        #地图信息
        self.bg_speed = 4
        
        #等级信息
        self.level = 1
        self.high_level = 1
        
        #记录刷新次数和帧数
        self.count = 0
        self.fps = 10
        
        #提高游戏难度
        self.pipe_speed_scale = 1
        self.pipes_between_scale = 1
        self.pipes_distance_scale = 1
        
    def init_setting(self):
        self.pipe_speed = 4
        self.pipes_allowed = 4
        self.pipes_between = 40
        self.pipes_distance = 200
        self.level = 1
        self.count = 0
        self.fps = 10
        
    def harder(self):
        self.count = 0
        self.fps += 1
        self.level += 1
        if self.pipe_speed < 10:
            self.pipe_speed += self.pipe_speed_scale
        if self.pipes_between > 35:
            self.pipes_between -= self.pipes_between_scale
        if self.pipes_distance > 80:
            self.pipes_distance -= self.pipes_distance_scale
        if self.pipes_allowed*(90+self.pipes_distance) <= 600:
            self.pipes_allowed += 1
    
class Bird(Sprite):
    '''小鸟'''
    def __init__(self,screen,setting):
        #初始化
        super(Bird,self).__init__()
        self.screen = screen
        self.setting = setting
        
        #加载小鸟图片及初始化其rect属性
        self.image = pygame.image.load("images/0.png")
        self.image_dead = pygame.image.load("images/dead1.png")
        self.rect = self.image.get_rect()
        self.rect.x = 40
        self.rect.y = 250
        
    def update_bird(self):
        #更新小鸟的信息
        if self.setting.bird_up:
            self.rect.y -= self.setting.bird_up_speed
        if self.setting.bird_down:
            self.rect.y += self.setting.bird_down_speed
            
    def draw_bird(self):
        #将小鸟绘制到屏幕上
        if self.setting.bird_dead:
            self.screen.blit(self.image_dead,self.rect)
        else:
            self.screen.blit(self.image,self.rect)

class Pipe(Sprite):
    '''管道'''
    def __init__(self,screen,setting):
        #初始化
        super(Pipe,self).__init__()
        self.screen = screen
        self.setting = setting
        
        #加载图片和初始化rect属性
        self.image_top = pygame.image.load("images/top1.png")
        self.image_bottom = pygame.image.load("images/bottom.png")
        self.top_rect = self.image_top.get_rect()
        self.bottom_rect = self.image_bottom.get_rect()
        self.top_rect.x = 200
        self.bottom_rect.x = 200
        self.top_rect.y = -280
        self.bottom_rect.y = 300
    
    def update_pipe(self):
        #更新管道信息
        self.top_rect.x -= self.setting.pipe_speed
        self.bottom_rect.x -= self.setting.pipe_speed
        self.top_rect.y = -280
        self.bottom_rect.y = 300
        temp = random.randint(-20,20)
        self.top_rect.y += temp
        self.bottom_rect.y += self.setting.pipes_between - temp
        
    def draw_pipe(self):
        #将管道绘制在屏幕上
        self.screen.blit(self.image_top,self.top_rect)
        self.screen.blit(self.image_bottom,self.bottom_rect)
        
class Bg():
    '''地图'''
    def __init__(self,screen,setting):
        #初始化
        self.screen = screen
        self.setting = setting
        
        #加载地图图片
        self.image1 = pygame.image.load("images/bg.png")
        self.image2 = pygame.image.load("images/bg.png")
        self.image1_x = 0
        self.image2_x = 800
        
    def update_bg(self):
        #使地图移动
        if self.image1_x == 0:
           self.image2_x = 800
        if self.image2_x == 0:
            self.image1_x = 800
        self.image1_x -= self.setting.bg_speed
        self.image2_x -= self.setting.bg_speed
        
    def draw_bg(self):
        #将背景绘制在屏幕上
        self.screen.blit(self.image1,(self.image1_x,0))
        self.screen.blit(self.image2,(self.image2_x,0))
        
class Button():
    '''开关按钮'''
    def __init__(self,screen,msg):
        #初始化
        self.screen = screen 
        self.screen_rect = self.screen.get_rect()
        self.msg = msg
        
        #设置按钮属性
        self.width,self.height = 200,50
        self.button_color = (0,255,0)
        self.text_color = (255,255,255)
        self.font = pygame.font.SysFont(None, 48)
        
        #创建按钮rect对象
        self.rect = pygame.Rect(0,0,self.width,self.height)
                
        #将按钮渲染为图像
        self.image = self.font.render(self.msg,True,self.text_color,self.button_color)
        self.image_rect = self.image.get_rect()
        
    def draw_button(self):
        #将按钮绘制在屏幕上
        self.image_rect.center = self.rect.center
        self.screen.fill(self.button_color,self.rect)
        self.screen.blit(self.image,self.image_rect)
        
class Level():
    '''记分牌'''
    def __init__(self,screen,setting):
        #初始化
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.setting = setting
        
        #设置字体属性
        self.text_color = (0,0,0)
        self.font = pygame.font.SysFont(None,48)
        
        #分别渲染等级和最高等级
        #self.pred_level()
        #self.pred_high_level()
        
    def draw_level(self):
        #渲染level图像和初始化其rect属性
        self.level_image = self.font.render("Level:"+str(self.setting.level),True,self.text_color)
        self.level_rect = self.level_image.get_rect()
        
        self.level_rect.x = 20
        self.level_rect.y = 20
        
        self.screen.blit(self.level_image,self.level_rect)
        
    def draw_high_level(self):
        #渲染high_level图像和初始化其rect属性
        self.high_level_image = self.font.render("High Level:"+str(self.setting.high_level),True,self.text_color)
        self.high_level_rect = self.high_level_image.get_rect()
        
        self.high_level_rect.x = 600
        self.high_level_rect.top = self.screen_rect.top + 20
        
        self.screen.blit(self.high_level_image,self.high_level_rect)
     
    '''
    def draw_level(self):
        #将等级情况绘制到屏幕上
        self.screen.blit(self.level_image,self.level_rect)
        self.screen.blit(self.high_level_image,self.high_level_rect)
    '''   
class Others():
    '''绘制其他信息的类'''
    def __init__(self,screen):
        #初始化
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        
        self.text_color = (255,0,0)
        
    def draw_over(self,msg):
        #绘制在屏幕中央的信息
        self.font = pygame.font.SysFont(None, 66)
        self.over_image = self.font.render(msg,True,self.text_color)
        self.over_rect = self.over_image.get_rect()
        
        self.over_rect.center = self.screen_rect.center
        
        self.screen.blit(self.over_image,self.over_rect)
        
    def draw_time(self,msg):
        #绘制在屏幕中上的信息
        self.font = pygame.font.SysFont(None, 48)
        self.time_image = self.font.render(msg,True,self.text_color)
        self.time_rect = self.time_image.get_rect()
        
        self.time_rect.centerx = self.screen_rect.centerx
        self.time_rect.top = self.screen_rect.top + 20
        
        self.screen.blit(self.time_image,self.time_rect)
        
def check_events(setting,other,play_button,pipes,next_button,over_button):
    '''响应事件'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                setting.bird_up = True
           
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y = pygame.mouse.get_pos()
            check_play_button(setting,play_button,pipes,mouse_x,mouse_y)
            check_over_button(setting,over_button,mouse_x,mouse_y)
            check_next_button(setting,next_button,mouse_x,mouse_y)
        else:
            setting.bird_up = False
            setting.bird_down = True
        '''   
        elif event.type == pygame.KEYUP:
           # setting.bird_down = True
            
            if event.key == pygame.K_UP:
                setting.bird_up = False
            if event.key == pygame.K_DOWN:
                setting.bird_down = False
             
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                setting.bird_up = True
            if event.key == pygame.K_DOWN:
                setting.bird_down = True
        '''
        
        
'''           
def buttons(screen,setting):
    if setting.bird_dead and setting.level == 1 :
        play_button = Button(screen,"Play")
        play_button.rect.center = play_button.screen_rect.center
        play_button.draw_button()
        #check_play_button(setting,play_button,mouse_x,mouse_y)
    if setting.count == 3600:
        over_button = Button(screen,"Over")
        over_button.rect.center = over_button.screen_rect.center
        over_button.draw_button()
        #check_over_button(setting,over_button,mouse_x,mouse_y)
        if setting.level > 1:
            next_button = Button(screen,"Next")
            next_button.rect.centerx = next_button.screen_rect.centerx
            next_button.rect.top = over_button.rect.bottom + 10
            next_button.draw_button()
            #check_next_button(setting,next_button,mouse_x,mouse_y)
 '''
       
def check_play_button(setting,play_button,pipes,mouse_x,mouse_y):
    '''检查游戏是否要开始'''
    button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
    
    if button_clicked:
        setting.bird_dead = False
        #将画面重置为开始画面
        x = 0
        for pipe in pipes:
            x = 200 - pipe.top_rect.x
            break
        
        for pipe in pipes:
            pipe.top_rect.x += x
            pipe.bottom_rect.x += x
        setting.init_setting() 
        
def check_next_button(setting,next_button,mouse_x,mouse_y):
    '''检查是否要开始下一关'''
    button_clicked = next_button.rect.collidepoint(mouse_x,mouse_y)
    
    if button_clicked and not setting.bird_dead:
        setting.harder()
        check_high_level(setting)
 
def check_over_button(setting,over_button,mose_x,mouse_y):
    button_clicked = over_button.rect.collidepoint(mose_x,mouse_y)
    
    if button_clicked:
        sys.exit()
        
def check_bird_dead(setting,bird,pipes):
    '''检查小鸟是否还存活'''
    if bird.rect.y < 0:
        setting.bird_dead = True
        return True
    if bird.rect.y > setting.screen_height:
        setting.bird_dead = True
        return True
    '''
    if pygame.sprite.spritecollide(bird,pipes,False):
        setting.bird_dead = True
    '''
    for pipe in pipes:
        if pipe.top_rect.colliderect(bird.rect) or pipe.bottom_rect.colliderect(bird.rect):
            setting.bird_dead = True
            return True
    return False
    
def create_pipes(screen,setting,pipes):
    '''创建管道组'''
    size = len(pipes)
    while size < setting.pipes_allowed:
        size += 1
        pipe = Pipe(screen,setting)
        x = size*200
        pipe.top_rect.x = x
        pipe.bottom_rect.x = x
        pipes.add(pipe)

def check_pipes_edges(pipes):
    '''检查是否有管道需要删除'''
    for pipe in pipes.copy():
        if pipe.top_rect.x <= -90:
            pipes.remove(pipe)
            break
        
def check_high_level(setting):
    '''检查是否需要更换最高分'''
    if setting.level > setting.high_level:
        setting.high_level = setting.level

def run_game():
    #初始化屏幕
    pygame.init()
    setting = Setting()
    screen = pygame.display.set_mode((setting.screen_width,setting.screen_height))
    pygame.display.set_caption("Bird") 

    #创建小鸟
    bird = Bird(screen,setting)
    #创建一个管道编组
    pipes = Group()
    create_pipes(screen,setting,pipes)
    #创建地图对象
    bg = Bg(screen,setting)
    #创建记分牌
    level = Level(screen,setting)
    #创建时钟对象
    clock = pygame.time.Clock()
    #创建显示其他信息的对象
    other = Others(screen)
    #创建play按钮
    play_button = Button(screen,"Play")
    #创建over按钮
    over_button = Button(screen,"Over")
    #创建next按钮
    next_button = Button(screen,"Next")
    
    while True:
        clock.tick(setting.fps)
        
        bg.draw_bg()
        bird.draw_bird()
        #pipes.draw()
        
        for pipe in pipes:
            pipe.draw_pipe()
        #level.draw_level()
        level.draw_level()
        level.draw_high_level()
       
       # buttons(screen,setting)
        is_dead = check_bird_dead(setting,bird,pipes)
        if setting.bird_dead and setting.level == 1 and not is_dead :
            play_button.rect.center = play_button.screen_rect.center 
            play_button.draw_button()
           
        if setting.count >= 60*setting.fps:
            next_button.rect.center = next_button.screen_rect.center
            next_button.draw_button()
            
            over_button.rect.centerx = over_button.screen_rect.centerx 
            over_button.rect.top = next_button.rect.bottom + 10
            over_button.draw_button()
            
        check_events(setting,other,play_button,pipes,next_button,over_button)
        
        
        if not setting.bird_dead and setting.count <= 60*setting.fps :
            for pipe in pipes:
                pipe.update_pipe()
            bg.update_bg()
            bird.update_bird() 
            if setting.count <= 60*setting.fps:
                time = 60 - setting.count//setting.fps
                other.draw_time("Time:"+str(time))
                
        setting.count += 1
        
        if is_dead and setting.bird_dead:
            other.draw_over("Game Over!")
            
            play_button.rect.centerx = play_button.screen_rect.centerx 
            play_button.rect.top = other.over_rect.bottom + 10
            play_button.draw_button()
            
            bird.rect.x = 40
            bird.rect.y = 250
           
            over_button.rect.centerx = over_button.screen_rect.centerx 
            over_button.rect.top = play_button.rect.bottom + 10
            over_button.draw_button()
            
        check_pipes_edges(pipes)
        create_pipes(screen,setting,pipes)
        
        pygame.display.flip()
                   
run_game()    
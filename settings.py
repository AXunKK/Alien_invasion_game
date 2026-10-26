import pygame

class Settings():
    """存储《外星人入侵》的所有设置的类"""
    def __init__(self):
        """初始化游戏的静态设置"""
        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0,)

        # 飞船的设置
        self.ship_limit = 3

        # 子弹设置
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 3

        # 外星人设置
        self.fleet_drop_speed = 10

        # 加快游戏节奏的速度
        self.speedup_scale = 1.1
        # 外星人分数的提高速度
        self.score_scale = 1.5

        self.initialize_dynamic_settings()
        self.laser_sound = pygame.mixer.Sound('sounds/laser.wav')
        self.explosion_sound = pygame.mixer.Sound('sounds/explosion.wav')
        self.hit_sound = pygame.mixer.Sound('sounds/hit.wav')
        
        # 调整音量 (0.0 到 1.0)
        self.laser_sound.set_volume(0.3)
        self.explosion_sound.set_volume(0.5)
        self.hit_sound.set_volume(0.8)

        # 外星人子弹设置
        self.alien_bullet_width = 5
        self.alien_bullet_height = 15
        self.alien_bullet_color = (255, 50, 50)  # 红色子弹，醒目
        self.alien_bullet_speed_factor = 1.5     # 外星子弹下落速度
        self.alien_fire_rate = 0.02

    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置"""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 0.3

        # fleet_direction为1表示向右移，为-1表示向左移
        self.fleet_direction = 1

        # 记分
        self.alien_points = 50

         # 外星人子弹设置
        self.alien_bullet_width = 5
        self.alien_bullet_height = 15
        self.alien_bullet_color = (255, 50, 50)  # 红色子弹，醒目
        self.alien_bullet_speed_factor = 1.5     # 外星子弹下落速度
        self.alien_fire_rate = 0.02              # 每帧每个外星人开火的概率

    def increase_speed(self):
        """提高速度设置和外星人分数"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
import pygame
from pygame.sprite import Sprite
import random  # 导入随机模块

class Alien(Sprite):
    """表示单个外星人的类"""
    def __init__(self, ai_settings, screen):
        """初始化外星人并设置其起始位置"""
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # 加载图像并缩放
        image_raw = pygame.image.load('images/alien.bmp')
        self.image = pygame.transform.scale(image_raw, (60, 60))
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # 随机生成X坐标，Y坐标在屏幕上方（负值，表示还没进入屏幕）
        self.rect.x = random.randint(-200, self.screen_rect.width - self.rect.width)
        self.rect.y = -self.rect.height - random.randint(0, 200) # 随机在屏幕上方不同高度准备

        # 每个外星人可以有略微不同的下落速度，增加随机性
        self.speed = self.ai_settings.alien_speed_factor * random.uniform(0.5, 1.0)
        
        # 存储准确位置（小数）
        self.y = float(self.rect.y)

    def update(self):
        """向下移动外星人"""
        self.y += self.speed
        self.rect.y = self.y
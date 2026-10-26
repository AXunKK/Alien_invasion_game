import pygame
import random

class Star():
    """表示单颗星星的类"""
    def __init__(self, screen_rect):
        self.screen_rect = screen_rect
        self.reset()

    def reset(self):
        """重置星星到屏幕最上方"""
        self.x = random.randint(0, self.screen_rect.width)
        # 初始 y 坐标在屏幕上方随机位置
        self.y = random.randint(-self.screen_rect.height, self.screen_rect.height)
        
        # 随机生成星星的大小
        self.radius = random.choice([1, 1, 1, 2, 2, 3]) 
        
        self.speed = self.radius * 0.15 + random.uniform(0.05, 0.2)
        
        # 星星的颜色，带点微弱的蓝/黄
        colors = [(255, 255, 255), (200, 200, 255), (255, 255, 200)]
        self.color = random.choice(colors)

    def update(self):
        """让星星向下移动"""
        self.y += self.speed
        # 如果星星移出了屏幕底部，让它重新回到顶部
        if self.y > self.screen_rect.height:
            self.x = random.randint(0, self.screen_rect.width)
            self.y = random.randint(-50, -10)

    def draw(self, screen):
        """绘制星星"""
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

class Starfield():
    """管理所有星星的类"""
    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        # 生成 200 颗星星
        self.stars = [Star(self.screen_rect) for _ in range(200)]

    def update(self):
        for star in self.stars:
            star.update()

    def draw(self):
        for star in self.stars:
            star.draw(self.screen)
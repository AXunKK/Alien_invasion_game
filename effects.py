import pygame
from pygame.sprite import Sprite

class Explosion(Sprite):
    """爆炸特效类"""
    def __init__(self, screen, center_x, center_y):
        super(Explosion, self).__init__()
        self.screen = screen
        self.center_x = center_x
        self.center_y = center_y
        
        # 改大初始半径和最大半径
        self.radius = 10 
        self.max_radius = 50 
        self.color = (255, 100, 0)  # 橘红色
        self.alive_time = 20  # 存活时间稍微变长

    def update(self):
        self.radius += 3
        self.alive_time -= 1
        
        if self.alive_time <= 0:
            self.kill()

    def draw(self):
        """画出实心渐隐圆圈"""
        alpha = max(0, self.alive_time / 20)
        color_with_alpha = (self.color[0], self.color[1], self.color[2], int(255 * alpha))
        
        # 半径不能小于0
        draw_radius = max(1, self.radius)
        
        surface = pygame.Surface((draw_radius * 2, draw_radius * 2), pygame.SRCALPHA)
        # 去掉了最后一个参数 2，让它变成实心圆
        pygame.draw.circle(surface, color_with_alpha, (draw_radius, draw_radius), draw_radius)
        self.screen.blit(surface, (self.center_x - draw_radius, self.center_y - draw_radius))
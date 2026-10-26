import pygame.font
from pygame.sprite import Group
# 不需要再导入 Ship 了，因为我们要自己画爱心

class Heart(pygame.sprite.Sprite):
    """用代码画一个爱心图标"""
    def __init__(self, x, y):
        super(Heart, self).__init__()
        # 创建一个带透明通道的表面
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        color = (255, 50, 50) # 鲜艳的红色
        
        # 用两个圆和一个多边形（倒三角）拼出一个爱心
        # 左边圆
        pygame.draw.circle(self.image, color, (8, 10), 8)
        # 右边圆
        pygame.draw.circle(self.image, color, (22, 10), 8)
        # 下方三角形
        pygame.draw.polygon(self.image, color, [(0, 10), (30, 10), (15, 28)])
        
        # 获取爱心的矩形并设置位置
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Scoreboard():
    """显示得分信息的类"""
    def __init__(self, ai_settings, screen, stats):
        """初始化显示得分涉及的属性"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        # 显示得分信息时使用的字体设置 (改成了白色，适应黑色星空背景)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # 准备初始得分图像
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """将得分转换为一幅渲染的图像"""
        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.ai_settings.bg_color)

        # 将得分放在屏幕右上角
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """将最高得分转换为渲染的图像"""
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.ai_settings.bg_color)

        # 将最高得分放在屏幕顶部中央
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """将等级转换为渲染的图像"""
        self.level_image = self.font.render(str(self.stats.level), True, self.text_color, self.ai_settings.bg_color)

        # 将等级放在得分下方
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """显示还余下多少生命值（爱心）"""
        self.ships = Group()
        for heart_number in range(self.stats.ships_left):
            # 创建爱心对象，设置间距
            heart = Heart(15 + heart_number * 40, 15)
            self.ships.add(heart)

    def show_score(self):
        """在屏幕上显示飞船、得分、等级和最高得分"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        # 绘制爱心
        self.ships.draw(self.screen)
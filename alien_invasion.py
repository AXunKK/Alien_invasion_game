import pygame
from pygame.sprite import Group
from starfield import Starfield
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
import game_functions as gf

def run_game():
    # 初始化pygame、设置和屏幕对象
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height)
    )
    pygame.display.set_caption("Alien Invasion")

    # 创建Play按钮
    play_button = Button(ai_settings, screen, "Play")

    # 创建存储游戏统计信息的实例，并创建记分牌
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # 创建一艘飞船、一个子弹编组和一个外星人编组
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()
    
    alien_bullets = Group() 

    explosions = Group() 
    starfield = Starfield(screen)

    # 开始游戏的主循环
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, alien_bullets)
        
        starfield.update()

        if stats.game_active:
            ship.update()
            
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, explosions)
            
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets)
            
            gf.update_alien_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets)
            
            explosions.update()
        
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets, play_button, explosions, starfield)

run_game()
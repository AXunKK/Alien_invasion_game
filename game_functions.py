import sys
import pygame
import random
from bullet import Bullet, AlienBullet
from alien import Alien
from time import sleep
from effects import Explosion

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """响应按键"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def check_keyup_events(event, ship):
    """响应松开"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, alien_bullets):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, alien_bullets, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, alien_bullets, mouse_x, mouse_y):
    """在玩家单击Play按钮时开始新游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        ai_settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active = True

        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        aliens.empty()
        bullets.empty()
        alien_bullets.empty() # 清空外星子弹
        ship.center_ship()

def fire_bullet(ai_settings, screen, ship, bullets):
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
        ai_settings.laser_sound.play()

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets, play_button, explosions, starfield):
    """更新屏幕上的图像，并切换到新屏幕"""
    screen.fill(ai_settings.bg_color)
    starfield.draw()

    # 绘制玩家子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    
    # 绘制外星子弹
    for alien_bullet in alien_bullets.sprites():
        alien_bullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen)

    for explosion in explosions.sprites():
        explosion.draw()

    sb.show_score()

    if not stats.game_active:
        play_button.draw_button()

    pygame.display.flip()

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, explosions):
    """更新子弹的位置，并删除已消失的子弹"""
    bullets.update()

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets, explosions)

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets, explosions):
    """响应子弹和外星人的碰撞"""
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for hit_aliens in collisions.values():
            for alien in hit_aliens:
                explosion = Explosion(screen, alien.rect.centerx, alien.rect.centery)
                explosions.add(explosion)
            
            ai_settings.explosion_sound.play()
            
            stats.score += ai_settings.alien_points * len(hit_aliens)
            sb.prep_score()
        check_high_score(stats, sb)

        new_level = stats.score // 500 + 1
        if new_level > stats.level:
            stats.level = new_level
            ai_settings.increase_speed()
            sb.prep_level()

def check_high_score(stats, sb):
    """检查是否诞生了新的最高得分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
        stats.save_high_score() 

def create_random_alien(ai_settings, screen, aliens):
    """随机生成一只外星人并加入编组"""
    new_alien = Alien(ai_settings, screen)
    aliens.add(new_alien)

def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets):
    """响应被外星人撞到或被外星子弹击中"""
    if stats.ships_left > 0:
        stats.ships_left -= 1
        sb.prep_ships()
        
        ai_settings.hit_sound.play()
        
        aliens.empty()
        bullets.empty()
        alien_bullets.empty() # 清空外星子弹
        ship.center_ship()
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets):
    """检查是否有外星人掉出了屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.copy():
        if alien.rect.top >= screen_rect.bottom:
            aliens.remove(alien) 

def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets):
    """更新外星人的位置，随机生成新外星人，处理碰撞和开火"""
    # 1. 让现有外星人向下移动
    aliens.update()

    # 2. 随机生成外星人
    if len(aliens) < 10 and random.random() < 0.015: 
        create_random_alien(ai_settings, screen, aliens)

    # 3. 【新增】：外星人随机开火逻辑
    # 如果屏幕上有外星人，且 5% 的概率触发开火
    if aliens and random.random() < 0.01: 
        # 随机挑选一个外星人开火
        alien = random.choice(aliens.sprites())
        new_bullet = AlienBullet(ai_settings, screen, alien)
        alien_bullets.add(new_bullet)

    # 4. 检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets)

    # 5. 检查是否有外星人掉出屏幕底端
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets)

def update_alien_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets):
    """更新外星人子弹的位置，并检查是否击中飞船"""
    # 移动子弹
    alien_bullets.update()

    # 删除飞出屏幕底部的子弹
    for alien_bullet in alien_bullets.copy():
        if alien_bullet.rect.top >= screen.get_rect().bottom:
            alien_bullets.remove(alien_bullet)

    # 检查子弹是否击中了飞船
    if pygame.sprite.spritecollideany(ship, alien_bullets):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets)
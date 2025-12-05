"""
👾 Space Invaders
Classic arcade shooter - destroy the alien invasion!

Controls:
- Left/Right arrows or A/D to move
- SPACE to shoot
- ESC to quit
- R to restart after game over
"""

import pygame
import random
import sys

pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
PURPLE = (150, 0, 255)

class Player:
    def __init__(self):
        self.width = 50
        self.height = 30
        self.x = WINDOW_WIDTH // 2 - self.width // 2
        self.y = WINDOW_HEIGHT - 60
        self.speed = 7
        self.color = GREEN
    
    def move(self, direction):
        self.x += direction * self.speed
        self.x = max(0, min(WINDOW_WIDTH - self.width, self.x))
    
    def draw(self, screen):
        # Draw spaceship shape
        points = [
            (self.x + self.width // 2, self.y),
            (self.x, self.y + self.height),
            (self.x + self.width, self.y + self.height)
        ]
        pygame.draw.polygon(screen, self.color, points)
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Bullet:
    def __init__(self, x, y, direction=-1, color=YELLOW):
        self.x = x
        self.y = y
        self.width = 4
        self.height = 15
        self.speed = 10
        self.direction = direction
        self.color = color
    
    def update(self):
        self.y += self.speed * self.direction
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Alien:
    def __init__(self, x, y, alien_type=0):
        self.width = 40
        self.height = 30
        self.x = x
        self.y = y
        self.alien_type = alien_type
        self.colors = [CYAN, PURPLE, RED]
        self.points = [10, 20, 30]
    
    def draw(self, screen):
        color = self.colors[self.alien_type % 3]
        # Draw alien body
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height), border_radius=5)
        # Draw eyes
        eye_y = self.y + 8
        pygame.draw.circle(screen, WHITE, (self.x + 12, eye_y), 5)
        pygame.draw.circle(screen, WHITE, (self.x + 28, eye_y), 5)
        pygame.draw.circle(screen, BLACK, (self.x + 12, eye_y), 2)
        pygame.draw.circle(screen, BLACK, (self.x + 28, eye_y), 2)
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def get_points(self):
        return self.points[self.alien_type % 3]

import asyncio

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("👾 Space Invaders")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        self.reset()
    
    def reset(self):
        self.player = Player()
        self.bullets = []
        self.alien_bullets = []
        self.aliens = []
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.victory = False
        self.alien_direction = 1
        self.alien_speed = 1
        self.shoot_cooldown = 0
        self.alien_shoot_timer = 0
        self.create_aliens()
    
    def create_aliens(self):
        self.aliens = []
        for row in range(5):
            for col in range(10):
                x = 50 + col * 60
                y = 50 + row * 45
                alien = Alien(x, y, row // 2)
                self.aliens.append(alien)
    
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key == pygame.K_r and (self.game_over or self.victory):
                    self.reset()
        
        if not self.game_over and not self.victory:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.player.move(-1)
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.player.move(1)
            if keys[pygame.K_SPACE] and self.shoot_cooldown <= 0:
                self.shoot()
                self.shoot_cooldown = 20
        
        return True
    
    def shoot(self):
        bullet_x = self.player.x + self.player.width // 2 - 2
        bullet_y = self.player.y
        self.bullets.append(Bullet(bullet_x, bullet_y))
    
    def alien_shoot(self):
        if self.aliens and random.random() < 0.02:
            alien = random.choice(self.aliens)
            bullet = Bullet(alien.x + alien.width // 2 - 2, alien.y + alien.height, 1, RED)
            self.alien_bullets.append(bullet)
    
    def update(self):
        if self.game_over or self.victory:
            return
        
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        
        # Update player bullets
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.y < 0:
                self.bullets.remove(bullet)
        
        # Update alien bullets
        for bullet in self.alien_bullets[:]:
            bullet.update()
            if bullet.y > WINDOW_HEIGHT:
                self.alien_bullets.remove(bullet)
        
        # Check bullet-alien collisions
        for bullet in self.bullets[:]:
            for alien in self.aliens[:]:
                if bullet.get_rect().colliderect(alien.get_rect()):
                    self.score += alien.get_points()
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    self.aliens.remove(alien)
                    break
        
        # Check alien bullet-player collisions
        for bullet in self.alien_bullets[:]:
            if bullet.get_rect().colliderect(self.player.get_rect()):
                self.lives -= 1
                self.alien_bullets.remove(bullet)
                if self.lives <= 0:
                    self.game_over = True
        
        # Move aliens
        move_down = False
        for alien in self.aliens:
            alien.x += self.alien_speed * self.alien_direction
            if alien.x <= 0 or alien.x + alien.width >= WINDOW_WIDTH:
                move_down = True
        
        if move_down:
            self.alien_direction *= -1
            for alien in self.aliens:
                alien.y += 20
                if alien.y + alien.height >= self.player.y:
                    self.game_over = True
        
        # Alien shooting
        self.alien_shoot()
        
        # Check victory
        if not self.aliens:
            self.victory = True
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw stars
        random.seed(42)
        for _ in range(100):
            x = random.randint(0, WINDOW_WIDTH)
            y = random.randint(0, WINDOW_HEIGHT)
            pygame.draw.circle(self.screen, WHITE, (x, y), 1)
        
        # Draw player
        self.player.draw(self.screen)
        
        # Draw bullets
        for bullet in self.bullets:
            bullet.draw(self.screen)
        for bullet in self.alien_bullets:
            bullet.draw(self.screen)
        
        # Draw aliens
        for alien in self.aliens:
            alien.draw(self.screen)
        
        # Draw HUD
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        lives_text = self.font.render(f"Lives: {self.lives}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(lives_text, (WINDOW_WIDTH - 100, 10))
        
        # Draw game over or victory
        if self.game_over:
            self.draw_overlay("GAME OVER", RED)
        elif self.victory:
            self.draw_overlay("VICTORY!", GREEN)
        
        pygame.display.flip()
    
    def draw_overlay(self, text, color):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        text_surface = self.big_font.render(text, True, color)
        score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
        restart_text = self.font.render("Press R to restart", True, WHITE)
        
        self.screen.blit(text_surface, (WINDOW_WIDTH // 2 - text_surface.get_width() // 2, WINDOW_HEIGHT // 2 - 60))
        self.screen.blit(score_text, (WINDOW_WIDTH // 2 - score_text.get_width() // 2, WINDOW_HEIGHT // 2))
        self.screen.blit(restart_text, (WINDOW_WIDTH // 2 - restart_text.get_width() // 2, WINDOW_HEIGHT // 2 + 40))
    
    async def run(self):
        running = True
        while running:
            running = self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(60)
            await asyncio.sleep(0)  # Critical for pygbag/asyncio
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    asyncio.run(game.run())

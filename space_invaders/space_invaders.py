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

    def run(self):
        running = True
        while running:
            running = self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()

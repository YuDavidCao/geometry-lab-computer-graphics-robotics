import pygame as pg
import math

class Segment:
    
    def __init__(self, l, theta, i, draw_circle=False, inner_radius=0, outer_radius=0):
        self.l = l
        self.theta = theta
        self.i = i
        self.draw_circle = draw_circle
        self.inner_radius = inner_radius
        self.outer_radius = outer_radius
        
    def draw(self, x1, y1, screen, font):
        x2 = x1 + self.l * math.cos(self.theta)
        y2 = y1 + self.l * math.sin(self.theta)
        pg.draw.line(screen, (255, 255, 255), (x1, y1), (x2, y2))    
        if(self.draw_circle):
            circle_surface = pg.Surface((self.outer_radius*2, self.outer_radius*2), pg.SRCALPHA)
            pg.draw.circle(circle_surface, (255, 255, 255, 50), (self.outer_radius, self.outer_radius), self.outer_radius)
            pg.draw.circle(circle_surface, (0,0,0,0), (self.outer_radius, self.outer_radius), self.inner_radius)
            screen.blit(circle_surface, (x1 - self.outer_radius, y1 - self.outer_radius))
        if(self.i != 0):
            screen.blit(font.render("joint " + str(self.i), True, pg.Color("white")), (x1, y1))
        return x2, y2
        
    def rotate(self, dtheta):
        self.theta += dtheta
        
import pygame as pg
import math
import segment
import time

text_color = (255, 255, 255)  # White text
button_hover_color = (0, 100, 200)  # Darker blue for hover effect

class Animator:
    
    def __init__(self):
        self.screen = pg.display.set_mode((800, 600))
        self.clock = pg.time.Clock()
        self.done = False
        self.font = pg.font.SysFont("Arial", 25, bold=True)
        self.starting_point = (400, 500)
        self.prev_left_clicked = time.time()
        self.prev_right_clicked = time.time()
        self.curIndex = 2
        self.config = [
            {
                "segment":[
                    segment.Segment(200, math.pi*3/2, 0),
                    segment.Segment(100, 0, 1, True),
                    segment.Segment(50, math.pi/4, 2, True, inner_radius=0, outer_radius=50),
                ],
                "rotation_speed":[
                    0,
                    0.01,
                    0.05,
                ]
            },
            {
                "segment":[
                    segment.Segment(200, math.pi*3/2, 0),
                    segment.Segment(100, 0, 1, True),
                    segment.Segment(60, 0, 2, True, inner_radius=0, outer_radius=60),
                    segment.Segment(50, math.pi/4, 3, True, inner_radius=0, outer_radius=50),
                ],
                "rotation_speed":[
                    0,
                    0.03,
                    0.07,
                    0.15,
                ]
            },
            {
                "segment":[
                    segment.Segment(200, math.pi*3/2, 0),
                    segment.Segment(30, 0, 1, True),
                    segment.Segment(160, 0, 2, True, inner_radius=110, outer_radius=210),
                    segment.Segment(50, math.pi/4, 3, True, inner_radius=0, outer_radius=50),
                ],
                "rotation_speed":[
                    0,
                    0.03,
                    0.05,
                    0.15,
                ]
            }
        ]
        self.run()

    def render(self):
        startX = self.starting_point[0]
        startY = self.starting_point[1]
        max_range = 0
        largest_segment_index = 1
        current_segments = self.config[self.curIndex]["segment"]
        for i in range(len(current_segments)):
            if i == 0: continue
            max_range += current_segments[i].l
            if current_segments[i].l > current_segments[largest_segment_index].l:
                largest_segment_index = i
        min_range = current_segments[largest_segment_index].l * 2 - max_range
        current_segments[1].inner_radius = max(0, min_range) # min range is the difference between the largest segment and the sum of all the other segments
        current_segments[1].outer_radius = max_range # max range is just the sum of all the lengths of the segments
        for segment in current_segments:
            newCoord = segment.draw(startX, startY, self.screen, self.font)
            startX = newCoord[0]
            startY = newCoord[1]
        
    def rotate(self):
        for segment, dtheta in zip(self.config[self.curIndex]["segment"], self.config[self.curIndex]["rotation_speed"]):
            segment.rotate(dtheta)
        
    def button(self, x1, y1, deltax, deltay, color, text, func):
        button_rect = pg.Rect(x1, y1, deltax, deltay)
        mouse_pos = pg.mouse.get_pos()
        hover = button_rect.collidepoint(mouse_pos)
        if hover:
            color = button_hover_color
        pg.draw.rect(self.screen, color, button_rect)
        button_text = self.font.render(text, True, text_color)
        text_rect = button_text.get_rect(center=button_rect.center)
        self.screen.blit(button_text, text_rect)
        if hover and pg.mouse.get_pressed()[0]:
            func()
        
    def on_left_button_click(self):
        if(time.time() - self.prev_left_clicked > 0.5):
            self.prev_left_clicked = time.time()
            self.curIndex -= 1
        
    def on_right_button_click(self):
        if(time.time() - self.prev_right_clicked > 0.5):
            self.prev_right_clicked = time.time()
            self.curIndex += 1
        
    def draw_label(self):
        for segment in self.config[self.curIndex]["segment"]:
            if(segment.i != 0):
                self.screen.blit(pg.font.SysFont("Arial", 20, bold=True).render(f"Segment {segment.i}, Length {segment.l}, starting at joint {segment.i}", True, pg.Color("white")), (0,0 + (segment.i-1) * 30))
        
    def run(self):
        while not self.done:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.done = True
            self.screen.fill((0, 0, 0))
            self.draw_label()
            if(self.curIndex != 0):
                self.button(0, 500, 100, 50, (0, 128, 255), "Left", self.on_left_button_click)
            if(self.curIndex != len(self.config) - 1):
                self.button(700, 500, 100, 50, (0, 128, 255), "Right", self.on_right_button_click)
            self.render()
            self.rotate()
            pg.display.flip()
            self.clock.tick(60)
        
if __name__ == '__main__':
    pg.init()
    Animator()
    pg.quit()
import turtle
import random
from config import Config

class Dino:
    def __init__(self, screen):
        self.turtle = turtle.Turtle()
        self.turtle.shape("square")
        self.turtle.color(Config.COLORS["dino"])
        self.turtle.shapesize(2.2, 1.5)  # height, width
        self.turtle.penup()
        self.turtle.goto(Config.DINO_X, Config.DINO_GROUND_Y)
        self.is_jumping = False
        self.jump_velocity = 0.0

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.jump_velocity = Config.JUMP_VELOCITY

    def update(self):
        if self.is_jumping:
            self.turtle.sety(self.turtle.ycor() + self.jump_velocity)
            self.jump_velocity += Config.GRAVITY
            if self.turtle.ycor() <= Config.DINO_GROUND_Y:
                self.turtle.sety(Config.DINO_GROUND_Y)
                self.is_jumping = False
                self.jump_velocity = 0.0

    def get_position(self):
        return self.turtle.xcor(), self.turtle.ycor()

class Obstacle:
    def __init__(self, kind):
        self.kind = kind
        self.turtle = turtle.Turtle()
        self.turtle.penup()
        if kind == "cactus_s":
            self.turtle.shape("square")
            self.turtle.shapesize(1.4, 0.6)
            self.turtle.goto(Config.WIDTH // 2 + 20, Config.GROUND_Y + 14)
        elif kind == "cactus_l":
            self.turtle.shape("square")
            self.turtle.shapesize(2.0, 0.9)
            self.turtle.goto(Config.WIDTH // 2 + 20, Config.GROUND_Y + 20)
        elif kind == "bird":
            self.turtle.shape("triangle")
            self.turtle.shapesize(0.8, 1.2)
            bird_y = random.choice([Config.GROUND_Y + 60, Config.GROUND_Y + 100])
            self.turtle.goto(Config.WIDTH // 2 + 20, bird_y)
        self.turtle.color(Config.COLORS["obstacle"])

    def move(self, speed):
        self.turtle.setx(self.turtle.xcor() - speed)

    def is_off_screen(self):
        return self.turtle.xcor() < -Config.WIDTH // 2 - 30

    def collides_with(self, dino_pos):
        dx = abs(dino_pos[0] - self.turtle.xcor())
        dy = abs(dino_pos[1] - self.turtle.ycor())
        return dx < Config.COLLISION_THRESHOLD_X and dy < Config.COLLISION_THRESHOLD_Y
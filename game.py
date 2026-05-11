import turtle
import random
import time
from config import Config
from entities import Dino, Obstacle
from ui import UI

class Game:
    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.title("Dino Run")
        self.screen.setup(width=Config.WIDTH, height=Config.HEIGHT)
        self.screen.bgcolor("#f7f7f7")
        self.screen.tracer(0)

        # Draw ground
        ground = turtle.Turtle()
        ground.hideturtle()
        ground.penup()
        ground.color(Config.COLORS["ground"])
        ground.pensize(2)
        ground.goto(-Config.WIDTH // 2, Config.GROUND_Y)
        ground.pendown()
        ground.goto(Config.WIDTH // 2, Config.GROUND_Y)
        ground.penup()

        self.dino = Dino(self.screen)
        self.ui = UI(self.screen)
        self.obstacles = []
        self.score = 0
        self.speed = Config.INITIAL_SPEED
        self.game_over = False
        self.spawn_cooldown = 0
        self.frame = 0

        self.screen.listen()
        self.screen.onkey(self.dino.jump, "space")
        self.screen.onkey(self.dino.jump, "Up")
        self.screen.onkey(self.reset, "r")

        self.ui.draw_score(self.score)

    def spawn_obstacle(self):
        kind = random.choices(["cactus_s", "cactus_l", "bird"], weights=[5, 3, 2])[0]
        self.obstacles.append(Obstacle(kind))
        self.spawn_cooldown = random.randint(Config.SPAWN_COOLDOWN_MIN, Config.SPAWN_COOLDOWN_MAX)

    def update_obstacles(self):
        for ob in list(self.obstacles):
            ob.move(self.speed)
            if ob.is_off_screen():
                ob.turtle.hideturtle()
                self.obstacles.remove(ob)
                self.score += Config.SCORE_INCREMENT
                self.speed = min(self.speed + Config.SPEED_INCREMENT, Config.MAX_SPEED)
                self.ui.draw_score(self.score)
            elif ob.collides_with(self.dino.get_position()):
                self.game_over = True
                self.ui.show_message([
                    ("G A M E   O V E R", 28),
                    (f"Score: {self.score}", 18),
                    ("Press R to restart", 14)
                ])

    def reset(self):
        for ob in self.obstacles:
            ob.turtle.hideturtle()
        self.obstacles.clear()
        self.score = 0
        self.speed = Config.INITIAL_SPEED
        self.dino.is_jumping = False
        self.dino.jump_velocity = 0.0
        self.dino.turtle.goto(Config.DINO_X, Config.DINO_GROUND_Y)
        self.game_over = False
        self.spawn_cooldown = 0
        self.ui.message_display.clear()
        self.ui.draw_score(self.score)

    def run(self):
        while True:
            if not self.game_over:
                self.dino.update()

                if self.spawn_cooldown <= 0:
                    self.spawn_obstacle()
                else:
                    self.spawn_cooldown -= 1

                self.update_obstacles()

                self.frame += 1
                if self.frame % 5 == 0:
                    self.score += Config.FRAME_SCORE_INCREMENT
                    self.ui.draw_score(self.score)

            self.screen.update()
            time.sleep(1 / 60)

if __name__ == "__main__":
    game = Game()
    game.run()
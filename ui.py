import turtle
from config import Config

class UI:
    def __init__(self, screen):
        self.screen = screen
        self.score_display = turtle.Turtle()
        self.score_display.hideturtle()
        self.score_display.penup()
        self.score_display.color(Config.COLORS["ground"])
        self.score_display.goto(Config.WIDTH // 2 - 120, Config.HEIGHT // 2 - 50)

        self.message_display = turtle.Turtle()
        self.message_display.hideturtle()
        self.message_display.penup()
        self.message_display.color(Config.COLORS["ground"])

    def draw_score(self, score):
        self.score_display.clear()
        self.score_display.write(f"HI {score:05d}", align="left", font=("Courier", 16, "bold"))

    def show_message(self, lines):
        self.message_display.clear()
        y = 40
        for text, size in lines:
            self.message_display.goto(0, y)
            self.message_display.write(text, align="center", font=("Courier", size, "bold"))
            y -= size + 10
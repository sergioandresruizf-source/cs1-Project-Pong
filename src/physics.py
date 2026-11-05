"""Physics of the game."""
import math
import random
import pygame
from config import *


class Paddle:
    def __init__(self, x):
        self.x = x
        self.y = (HEIGHT - PADDLE_H) / 2
        self.w, self.h = PADDLE_W, PADDLE_H

    def move(self, direction, dt):
        """-1 down, 0 stop, 1 up"""
        self.y += direction * PADDLE_SPEED * dt
        self.y = max(0, min(HEIGHT - self.h, self.y))

    @property
    def rect(self):
        return pygame.Rect(round(self.x), round(self.y), self.w, self.h)

    @property
    def center_y(self):
        return self.y + self.h / 2


class Ball:
    def __init__(self):
        self.size = BALL_SIZE
        self.reset()

    def reset(self):
        self.x = (WIDTH - self.size) / 2
        self.y = (HEIGHT - self.size) / 2
        self.speed = BALL_SPEED_INIT
        self.vx = self.vy = 0.0

    def serve(self, direction):
        """direction: -1 to the left, 1 to the right"""
        angle = random.uniform(-math.radians(25), math.radians(25))
        self.speed = BALL_SPEED_INIT
        self.vx = direction * self.speed * math.cos(angle)
        self.vy = self.speed * math.sin(angle)

    @property
    def rect(self):
        return pygame.Rect(round(self.x), round(self.y), self.size, self.size)

    @property
    def center(self):
        return (self.x + self.size / 2, self.y + self.size / 2)


class Game:
    """Complete state of a match."""

    def __init__(self):
        self.left = Paddle(PADDLE_MARGIN)
        self.right = Paddle(WIDTH - PADDLE_MARGIN - PADDLE_W)
        self.ball = Ball()
        self.reset()

    def reset(self):
        self.score = {"left": 0, "right": 0}
        self.state = "serving"      # serving | playing | gameover
        self.winner = None          # "left" | "right"
        self.serve_timer = SERVE_DELAY
        self.serve_dir = random.choice([-1, 1])
        self.ball.reset()

    # Fisics
    def update(self, dt, left_dir, right_dir):
        if self.state == "gameover":
            return
        self.left.move(left_dir, dt)
        self.right.move(right_dir, dt)

        if self.state == "serving":
            self.serve_timer -= dt
            if self.serve_timer <= 0:
                self.ball.serve(self.serve_dir)
                self.state = "playing"
            return

        self._move_ball(dt)
        self._bounce_walls()
        self._bounce_paddle(self.left, going_left=True)
        self._bounce_paddle(self.right, going_left=False)
        self._check_goal()

    def _move_ball(self, dt):
        self.ball.x += self.ball.vx * dt
        self.ball.y += self.ball.vy * dt

    def _bounce_walls(self):
        b = self.ball
        if b.y <= 0:
            b.y = 0
            b.vy = abs(b.vy)
        elif b.y + b.size >= HEIGHT:
            b.y = HEIGHT - b.size
            b.vy = -abs(b.vy)

    def _bounce_paddle(self, paddle, going_left):
        b = self.ball
        moving_toward = b.vx < 0 if going_left else b.vx > 0
        if not moving_toward or not b.rect.colliderect(paddle.rect):
            return
        # If ball passes the player center, its goal
        cx = b.center[0]
        if going_left and cx < paddle.x + paddle.w / 2:
            return
        if not going_left and cx > paddle.x + paddle.w / 2:
            return

        # Angle of bounce based on hit, center = 0 to 60 on the edges
        offset = (b.center[1] - paddle.center_y) / (paddle.h / 2)
        offset = max(-1.0, min(1.0, offset))
        angle = offset * MAX_BOUNCE_ANGLE
        b.speed = min(b.speed * BALL_SPEED_UP, BALL_SPEED_MAX)
        direction = 1 if going_left else -1
        b.vx = direction * b.speed * math.cos(angle)
        b.vy = b.speed * math.sin(angle)
        # sacar la bola de la raqueta para no atascarla
        b.x = paddle.x + paddle.w if going_left else paddle.x - b.size

    def _check_goal(self):
        b = self.ball
        scorer = None
        if b.x + b.size < 0:
            scorer = "right"
        elif b.x > WIDTH:
            scorer = "left"
        if scorer is None:
            return
        self.score[scorer] += 1
        if self.score[scorer] >= WIN_SCORE:
            self.state = "gameover"
            self.winner = scorer
            return
        # restart depending on who received the goal.
        self.serve_dir = -1 if scorer == "right" else 1
        self.state = "serving"
        self.serve_timer = SERVE_DELAY
        b.reset()

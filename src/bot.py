"""Here works the Bot or the AI of the game."""
from config import PADDLE_H


class SimpleBot:
    def decide(self, game):
        """-1, 0 or 1 to the right paddle"""
        ball_y = game.ball.center[1]
        diff = ball_y - game.right.center_y
        if abs(diff) < PADDLE_H * 0.15:
            return 0
        return 1 if diff > 0 else -1

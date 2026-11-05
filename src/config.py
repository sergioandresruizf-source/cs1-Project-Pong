"""The constants of the game."""
import math

WIDTH, HEIGHT = 1024, 768
FPS = 60

PADDLE_W, PADDLE_H = 34, 158
PADDLE_MARGIN = 25          # distance of the paddle to the edge
PADDLE_SPEED = 620          # px/s

BALL_SIZE = 30
BALL_SPEED_INIT = 420       # px/s
BALL_SPEED_MAX = 1000       # px/s
BALL_SPEED_UP = 1.05        # multiplier of speed after each hit
MAX_BOUNCE_ANGLE = math.radians(60)

SERVE_DELAY = 1.0           # seconds before restart after a goal
WIN_SCORE = 7

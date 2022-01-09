from res import RESOURCES_DIR

WIDTH = 700
HEIGHT = 600
FPS = 60
CAPTION = "Супер Марио"

STATE_CONTINUE = 1
STATE_END = 2
STATE_WIN = 3

LEVEL1_PATH = f"{RESOURCES_DIR}/maps/level1/MarioLevel1.tmx"
BLOCKS_PATH = f"{RESOURCES_DIR}/blocks/block.png"
QBLOCKS_PATH = f"{RESOURCES_DIR}/blocks/q_block.png"
MARIO_PATH = f"{RESOURCES_DIR}/heros/0.png"
PRINCESS_PATH = f"{RESOURCES_DIR}/heros/princess.png"
FIRE_PATH = f"{RESOURCES_DIR}/enemies/fire.png"
BUMP_PATH = f"{RESOURCES_DIR}/blocks/bump.png"

BACKGROUND_MUSIC_PATH = f"{RESOURCES_DIR}/music/background_music.mp3"
BUMBS_SOUND_PATH = f"{RESOURCES_DIR}/music/bumbs_sound.mp3"
DIE_SOUND_PATH = f"{RESOURCES_DIR}/music/die_sound.mp3"
START_SOUND_PATH = f"{RESOURCES_DIR}/music/start_sound.mp3"

ANIMATED_LEFT = f"{RESOURCES_DIR}/heros/left.png"
ANIMATED_STATE = f"{RESOURCES_DIR}/heros/0.png"
ANIMATED_RIGHT = f"{RESOURCES_DIR}/heros/right.png"
ANIMATED_JUMP = f"{RESOURCES_DIR}/heros/jump.png"
ANIMATED_LJUMP = f"{RESOURCES_DIR}/heros/jump_left.png"
ANIMATED_RJUMP = f"{RESOURCES_DIR}/heros/jump_right.png"

COLOR_WIN_BUTTON = (200, 200, 0)
COLOR_LOSE_BUTTON = (255, 0, 0)
COLOR_NEUTRAL_BUTTON = (0, 0, 0)
COLOR_TEXT_BUTTON = (255, 255, 255)

# Imports
import pygame
import sys
import os
from math import prod
from pygame import gfxdraw
from random import randint, choice
from pygame.locals import (
    K_0,
    K_1,
    K_2,
    K_3,
    K_4,
    K_SPACE,
    K_ESCAPE,
    K_RETURN,
    KEYDOWN,
    MOUSEBUTTONDOWN
)

if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)


def load_file(file_name):
    return os.path.join(os.path.dirname(__file__), file_name)


# Initialization
pygame.init()
pygame.display.set_caption('Three Men\'s Morris')
#programIcon = pygame.image.load('moris.ico')
#pygame.display.set_icon(programIcon)
_sm = 1
dataFolder = "databig" if _sm == 2 else "data"
screen = pygame.display.set_mode([640*_sm, 480*_sm])
clock = pygame.time.Clock()
fonts = {
    "Arial": pygame.font.SysFont("Arial", 18*_sm, bold=True),
    "Andy": pygame.font.Font(load_file(f"./{dataFolder}/andy.ttf"), 48*_sm, bold=True),
    "Pixel": pygame.font.Font(load_file(f"./{dataFolder}/Pixel.ttf"), 24*_sm, bold=True),
    "AndySmall": pygame.font.Font(load_file(f"./{dataFolder}/andy.ttf"), 18*_sm, bold=True)
}

sounds = {
    "grab": pygame.mixer.Sound(load_file(f"{dataFolder}/grab.wav")),
    "place": pygame.mixer.Sound(load_file(f"{dataFolder}/place.wav")),
    "win": pygame.mixer.Sound(load_file(f"{dataFolder}/winjingle.wav"))
}

sprites = {
    "hand_open":        pygame.image.load(
                            load_file(f"{dataFolder}/harrow.png")).convert_alpha(),
    "hand_tappy":     [
                        pygame.image.load(
                            load_file(f"{dataFolder}/hand1.png")).convert_alpha(),
                        pygame.image.load(
                            load_file(f"{dataFolder}/hand2.png")).convert_alpha(),
                        pygame.image.load(
                            load_file(f"{dataFolder}/hand3.png")).convert_alpha(),
                        pygame.image.load(
                            load_file(f"{dataFolder}/hand4.png")).convert_alpha(),
                    ],
    "hand_watch":    [
                        pygame.image.load(
                            load_file(f"{dataFolder}/handwait1.png")).convert_alpha(),
                        pygame.image.load(
                            load_file(f"{dataFolder}/handwait2.png")).convert_alpha(),
                        pygame.image.load(
                            load_file(f"{dataFolder}/handwait3.png")).convert_alpha(),
                        pygame.image.load(
                            load_file(f"{dataFolder}/handwait4.png")).convert_alpha(),
                        pygame.image.load(
                            load_file(f"{dataFolder}/handwait5.png")).convert_alpha(),
                        pygame.image.load(
                            load_file(f"{dataFolder}/handwait6.png")).convert_alpha(),
                        pygame.image.load(
                            load_file(f"{dataFolder}/handwait7.png")).convert_alpha(),
                        pygame.image.load(
                            load_file(f"{dataFolder}/handwait8.png")).convert_alpha(),
                    ],
    "hand_grab":        pygame.image.load(
                            load_file(f"{dataFolder}/hmove.png")).convert_alpha(),
    "board_shade":      pygame.image.load(
                            load_file(f"{dataFolder}/bshad.png")).convert_alpha(),
    "board":            pygame.image.load(
                            load_file(f"{dataFolder}/board.png")).convert_alpha(),
    "hand_shader":      pygame.image.load(
                            load_file(f"{dataFolder}/hshadr.png")).convert_alpha(),
    "hand_shadel":      pygame.image.load(
                            load_file(f"{dataFolder}/hshadl.png")).convert_alpha(),
    "game_blue":        pygame.image.load(
                            load_file(f"{dataFolder}/piecebc.png")).convert_alpha(),
    "game_red":         pygame.image.load(
                            load_file(f"{dataFolder}/piecerc.png")).convert_alpha(),
    "game_shade":       pygame.image.load(
                            load_file(f"{dataFolder}/piecesh.png")).convert_alpha(),
    "game_highlight":   pygame.image.load(
                            load_file(f"{dataFolder}/piecehi.png")).convert_alpha(),
    "bg":               pygame.image.load(
                            load_file(f"{dataFolder}/bg.png")).convert_alpha(),
    "msgbub":           pygame.image.load(
                            load_file(f"{dataFolder}/chatbubble.png")).convert_alpha(),
}

curr_sprite = "hand_open"

debug_info = {
    "mod": None, "fps": None, "opponent": None, "player": None,
    "last_move": None, "last_strat": None
}
debug = False


def debug_show():
    debug_info["fps"] = int(clock.get_fps())
    debug_t = fonts["Arial"].render(str(debug_info), 1, pygame.Color("RED"))
    screen.blit(debug_t, (0, 0))


def draw_circle(screen, x, y, radius, col, dist=0, js=False):
    w, h = pygame.display.get_surface().get_size()
    x, y = min([x, h+200]), min([y, w+200])
    if dist > 0:
        shadcol = (0, 0, 0, 64)
        gfxdraw.aacircle(screen, x+dist, y+dist, radius, shadcol)
        gfxdraw.filled_circle(screen, x+dist, y+dist, radius, shadcol)
    if not js:
        gfxdraw.aacircle(screen, x, y, radius, col)
        gfxdraw.filled_circle(screen, x, y, radius, col)


winning_line = -1
bl_len = 280
linesize = 5*_sm
pointsh = [180*_sm, (180+int(bl_len/2))*_sm, (180+bl_len)*_sm]
pointsw = [100*_sm, (100+int(bl_len/2))*_sm, (100+bl_len)*_sm]
board_lines = [
    [(pointsh[0], pointsw[0]), (pointsh[2], pointsw[0]), linesize],
    [(pointsh[0], pointsw[1]), (pointsh[2], pointsw[1]), linesize],
    [(pointsh[0], pointsw[2]), (pointsh[2], pointsw[2]), linesize],
    [(pointsh[0], pointsw[0]), (pointsh[0], pointsw[2]), linesize],
    [(pointsh[1], pointsw[0]), (pointsh[1], pointsw[2]), linesize],
    [(pointsh[2], pointsw[0]), (pointsh[2], pointsw[2]), linesize],
    [(pointsh[0], pointsw[0]), (pointsh[2], pointsw[2]), linesize+(3*_sm)],
    [(pointsh[0], pointsw[2]), (pointsh[2], pointsw[0]), linesize+(3*_sm)],
    [(0-(15*_sm), 25*_sm),  (75*_sm,  25*_sm),  linesize],
    [(0-(15*_sm), 455*_sm), (75*_sm,  455*_sm), linesize],
    [(75*_sm,  25*_sm),  (75*_sm,  455*_sm), linesize],
    [(565*_sm, 25*_sm),  (655*_sm, 25*_sm),  linesize],
    [(565*_sm, 455*_sm), (655*_sm, 455*_sm), linesize],
    [(565*_sm, 25*_sm),  (565*_sm, 455*_sm), linesize],
]

piece_lines = [  # i really didnt want to calculate this
    [0, 3, 6], [0, 4], [0, 5, 7],
    [1, 3], [1, 4, 6, 7], [1, 5],
    [2, 3, 7], [2, 4], [2, 5, 6]
]

win_lines = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]
]

hand_pos = {
    "board": [
        (pointsh[0], pointsw[0]), (pointsh[1], pointsw[0]), (pointsh[2], pointsw[0]),
        (pointsh[0], pointsw[1]), (pointsh[1], pointsw[1]), (pointsh[2], pointsw[1]),
        (pointsh[0], pointsw[2]), (pointsh[1], pointsw[2]), (pointsh[2], pointsw[2])
    ],
    "hand": [
        (620*_sm, 100*_sm), (620*_sm, 240*_sm), (620*_sm, 380*_sm)
    ],
    "idle": (530*_sm, 240*_sm)
}

curr_pos = [500*_sm, -150]


def move_hand(new_pos):
    in_pos = True
    speed = 50 + (200/(diff+1))
    if curr_pos[0] > new_pos[0]+5:
        curr_pos[0] -= (dt * ((curr_pos[0] - new_pos[0]) / speed))+5
        in_pos = False
    if curr_pos[0] < new_pos[0]-5:
        curr_pos[0] += (dt * ((new_pos[0] - curr_pos[0]) / speed))+5
        in_pos = False
    if curr_pos[1] > new_pos[1]+5:
        curr_pos[1] -= (dt * ((curr_pos[1] - new_pos[1]) / speed))+5
        in_pos = False
    if curr_pos[1] < new_pos[1]-5:
        curr_pos[1] += (dt * ((new_pos[1] - curr_pos[1]) / speed))+5
        in_pos = False
    return in_pos


def draw_text(font, text, color, pos, shadow=True):
    text_shadow = fonts[font].render(text, 1, (0, 0, 0))
    text_shadow_pos = text_shadow.get_rect(center=(pos[0], pos[1]+3))
    text_main = fonts[font].render(text, 1, color)
    text_main_pos = text_main.get_rect(center=pos)
    if shadow:
        screen.blit(text_shadow, text_shadow_pos)
    screen.blit(text_main, text_main_pos)
    return


def draw_board():
    screen.blit(sprites["board_shade"], (170*_sm, 90*_sm))
    screen.blit(sprites["hand_shader"], (555*_sm, 15*_sm))
    screen.blit(sprites["hand_shadel"], (-5*_sm, 15*_sm))
    pygame.draw.rect(screen, (237, 206, 121),
                     pygame.Rect(board_lines[6][0],
                                 (board_lines[6][1][0] - board_lines[6][0][0],
                                 board_lines[6][1][1] - board_lines[6][0][1])))
    # screen.blit(sprites["board"], (170, 90))
    pygame.draw.rect(screen, (237, 206, 121),
                     pygame.Rect((0, 25*_sm), (75*_sm, 430*_sm)))
    pygame.draw.rect(screen, (237, 206, 121),
                     pygame.Rect((disw-(75*_sm), 25*_sm), (75*_sm, 430*_sm)))
    for i, l in enumerate(board_lines):
        wl = (i == winning_line)
        pygame.draw.line(screen,
                         (255, 0, 0) if wl else (0, 0, 0),
                         l[0], l[1], width=l[2] * (2 if wl else 1))
        draw_circle(screen, l[0][0], l[0][1], 10*_sm, (0, 0, 0))
        draw_circle(screen, l[1][0], l[1][1], 10*_sm, (0, 0, 0))
    draw_circle(screen, 320*_sm, 240*_sm, 10*_sm, (0, 0, 0))


def detectWin(moves):
    brd = [moves[i:i+3] for i in range(0, len(moves), 3)]
    diag = [[moves[i] for i in [0, 4, 8]], [moves[i] for i in [2, 4, 6]]]
    alllines = brd + list(zip(*brd)) + diag
    rowsFull = len(alllines)
    for i, row in enumerate(alllines):
        winSum = sum(row)
        if prod(row):
            winSum /= 3
            if winSum == int(winSum):
                return (int(winSum), i)
            else:
                rowsFull -= 1
    if not rowsFull:
        return (-1, -1)
    return (0, -1)


squares = [
    pygame.Rect([110*_sm, 30*_sm],  [140*_sm, 140*_sm]),
    pygame.Rect([250*_sm, 30*_sm],  [140*_sm, 140*_sm]),
    pygame.Rect([390*_sm, 30*_sm],  [140*_sm, 140*_sm]),

    pygame.Rect([110*_sm, 170*_sm], [140*_sm, 140*_sm]),
    pygame.Rect([250*_sm, 170*_sm], [140*_sm, 140*_sm]),
    pygame.Rect([390*_sm, 170*_sm], [140*_sm, 140*_sm]),

    pygame.Rect([110*_sm, 310*_sm], [140*_sm, 140*_sm]),
    pygame.Rect([250*_sm, 310*_sm], [140*_sm, 140*_sm]),
    pygame.Rect([390*_sm, 310*_sm], [140*_sm, 140*_sm])
]

hands = [
    pygame.Rect([0-(70*_sm), 30*_sm],  [140*_sm, 140*_sm]),
    pygame.Rect([0-(70*_sm), 170*_sm], [140*_sm, 140*_sm]),
    pygame.Rect([0-(70*_sm), 310*_sm], [140*_sm, 140*_sm]),
    pygame.Rect([570*_sm, 30*_sm],  [140*_sm, 140*_sm]),
    pygame.Rect([570*_sm, 170*_sm], [140*_sm, 140*_sm]),
    pygame.Rect([570*_sm, 310*_sm], [140*_sm, 140*_sm])
]

moves = [0 for y in range(9)]


def draw_o(rect, col, shift, mod):
    x, y = int(rect.left + (rect.width/2) + shift), \
           int(rect.top + (rect.height/2) + mod)
    radius = 60
    screen.blit(sprites["game_shade"],
                (rect.left+10 + shift, rect.top+10 + mod))
    # draw_circle(screen, x, y, radius, (0, 0, 0), dist=3, js=True)
    if col == "red":
        screen.blit(sprites["game_red"],
                    (rect.left+10 + shift, rect.top+10 + mod))
    if col == "blue":
        screen.blit(sprites["game_blue"],
                    (rect.left+10 + shift, rect.top+10 + mod))


def draw_o_center(center, col):
    x, y = center[0], center[1]
    screen.blit(sprites["game_shade"], (x-40, y-40))
    if col == "red":
        screen.blit(sprites["game_red"], (x-60, y-60))
    if col == "blue":
        screen.blit(sprites["game_blue"], (x-60, y-60))


def highlight_square(turn):
    mouse_loc = pygame.mouse.get_pos()
    for i, square in enumerate(squares + hands):
        if square.contains(pygame.Rect(mouse_loc, (1, 1))):
            val = (moves + inhand[0] + inhand[1])[i]
            if not holding and val:
                if turn:
                    if i < 12 and val == 1:
                        center = (square.left + (square.width/2),
                                  square.top + (square.height/2))
                        radius = square.width/2
                        screen.blit(sprites["game_highlight"],
                                    (square.left+4, square.top+4))
                        break
                else:
                    if i > 11 or val == 2:
                        center = (square.left + (square.width/2),
                                  square.top + (square.height/2))
                        radius = square.width/2
                        screen.blit(sprites["game_highlight"],
                                    (square.left+4, square.top+4))
                        break
            elif holding and not (moves + inhand[0] + inhand[1])[i]:
                center = (square.left + (square.width/2),
                          square.top + (square.height/2))
                radius = square.width/2
                screen.blit(sprites["game_highlight"],
                            (square.left+4, square.top+4))
                break
    return


def moriss_move(player, holding):
    mouse_loc = pygame.mouse.get_pos()
    for i, square in enumerate(squares + hands):
        if square.contains(pygame.Rect(mouse_loc, (1, 1))):
            if i > 11:
                if player == 1:
                    return -1
                if inhand[player-1].count(True) > 0 and inhand[player-1][i-12]:
                    inhand[player-1][i-12] = False
                    return -2
                else:
                    continue
            if i > 8:
                if player == 2:
                    return -1
                if inhand[player-1].count(True) > 0 and inhand[player-1][i-9]:
                    inhand[player-1][i-9] = False
                    return -2
                else:
                    continue
            if remaining_moves > 0:
                if holding and moves[i] == 0:
                    moves[i] = player
                    return i
                else:
                    continue
            elif not holding and moves[i] == player:
                moves[i] = -1
                return -2
            elif holding and moves[i] == -1:
                moves[i] = player
                return -2
            elif holding and moves[i] == 0:
                moves[i] = player
                return i
    return -1


def make_move(player):
    mouse_loc = pygame.mouse.get_pos()
    for i, square in enumerate(squares):
        if square.contains(pygame.Rect(mouse_loc, (1, 1))) and moves[i] == 0:
            moves[i] = player
            return i
    return -1


def cpu_morris(player, difficulty):
    failChance = [0, 50, 75, 90, 105][difficulty]
    if difficulty == 0:
        if remaining_moves >= 0:
            return (cpu_move(2, difficulty, failChance), -1)
        else:
            while True:
                rand1 = choice(range(len(moves)))
                if moves[rand1] == 2:
                    break
            while True:
                rand2 = choice(range(len(moves)))
                if moves[rand2] == 0:
                    break
            return (rand2, rand1)
    if remaining_moves >= 0:
        play = cpu_move(2, difficulty, failChance)
        return (play, -1)
    else:
        valid_takes = []
        opponent = (1 if player == 2 else 2)
        for i in range(len(moves)):
            if moves[i] == 0:
                test_moves = moves.copy()
                test_moves[i] = player
                posW, wL = detectWin(test_moves)
                if posW == player:
                    for j in range(len(moves)):
                        if moves[j] == player:
                            if j not in win_lines[wL]:
                                return (i, j)
            elif moves[i] == player:
                test_moves = moves.copy()
                test_moves[i] = opponent
                if not detectWin(test_moves)[0] == opponent:
                    valid_takes += [i]
        if valid_takes:
            move = cpu_move(2, difficulty, failChance)
            moved = choice(valid_takes)
            return (move, moved)
    return (cpu_move(2, difficulty, failChance), -1)


def cpu_move(player, diff, failChance):
    if diff == 0 or randint(0, 100) > failChance:
        while True:
            new_move = randint(0, len(moves)-1)
            if moves[new_move] == 0:
                return new_move
    else:
        opponent = (1 if player == 2 else 2)
        can_win = -1
        for i in range(len(moves)):
            if moves[i] != 0:
                continue
            else:
                test_moves = moves.copy()
                test_moves[i] = player
                if detectWin(test_moves)[0] == player:
                    debug_info["last_strat"] = "win"
                    can_win = i
                    break
                else:
                    test_moves[i] = opponent
                    if detectWin(test_moves)[0] == opponent:
                        debug_info["last_strat"] = "block"
                        can_win = i
        if can_win >= 0:
            return can_win
        # block forks:
        # encirclement fork
        elif moves[0] == opponent == moves[8] or \
                moves[2] == opponent == moves[6]:
            while True:
                new_move = choice([1, 3, 5, 7])
                if moves[new_move] == 0:
                    debug_info["last_strat"] = "blockf"
                    return new_move
        # arrowhead fork
        elif moves[1] == opponent == moves[3] and moves[0] == 0:
            return 0
        elif moves[1] == opponent == moves[5] and moves[2] == 0:
            return 2
        elif moves[7] == opponent == moves[3] and moves[6] == 0:
            return 6
        elif moves[7] == opponent == moves[5] and moves[8] == 0:
            return 8
        elif moves[4] == 0:
            debug_info["last_strat"] = "center"
            return 4
        elif last_move in [0, 2, 6, 8] and \
                moves[i := [8, 6, 2, 0][[0, 2, 6, 8].index(last_move)]] == 0:
            debug_info["last_strat"] = "opcorner"
            return i
        elif 0 in [moves[0], moves[2], moves[6], moves[8]]:
            while True:
                new_move = choice([0, 2, 6, 8])
                if moves[new_move] == 0:
                    debug_info["last_strat"] = "corner"
                    return new_move
        else:
            while True:
                new_move = choice([1, 3, 5, 7])
                if moves[new_move] == 0:
                    debug_info["last_strat"] = "edge"
                    return new_move


turn = True
win_state = False
active = True
last_move = None
inhand = [[True, True, True], [True, True, True]]
remaining_moves = len(inhand[0])
cpu_moves = len(inhand[1])
holding = False
ws = ["", "Blue", "Red", "No-one"]
wf = 0
mod = -100
shifts = [randint(-15, 15) for x in range(9)]
disw, dish = pygame.display.get_surface().get_size()
hand_state = 0
frame = 0
frameup = 0
wait_time = -100
cpu_active = True
bg_shift = 0
bg_mod = 5
paused = False
pause_slide = -300
win_slide = -300
fade = 0
win_jingle = False
diff = 1
settingpieces = False
wls = [
    [0, 0] for i in range(6)
] # wins losses draws
current_msg = "I'm bored..."
newmsg = False
msgtime = 4000
msgpopup = 800
while active:
    if not paused:
        dt = clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.ACTIVEEVENT:
                try:
                    event.state
                except AttributeError:
                    continue
                if event.state & 1 == 1:
                    paused = not event.gain
            elif event.type == pygame.QUIT:
                active = False
            elif event.type == MOUSEBUTTONDOWN:
                if turn and not win_state:
                    if (last_move := moriss_move(1, holding)) > -1:
                        turn = False
                        remaining_moves -= 1
                        think_time = 0
                        holding = False
                        pygame.mixer.Sound.play(sounds["place"])
                        if -1 in moves:
                            moves[moves.index(-1)] = 0
                    if last_move == -2:
                        if holding:
                            pygame.mixer.Sound.play(sounds["place"])
                        else:
                            pygame.mixer.Sound.play(sounds["grab"])
                        holding = not holding
                elif not cpu_active and not win_state:
                    if (last_move := moriss_move(2, holding)) > -1:
                        turn = True
                        remaining_moves -= 1
                        think_time = 0
                        holding = False
                        pygame.mixer.Sound.play(sounds["place"])
                        if -1 in moves:
                            moves[moves.index(-1)] = 0
                    if last_move == -2:
                        if holding:
                            pygame.mixer.Sound.play(sounds["place"])
                        else:
                            pygame.mixer.Sound.play(sounds["grab"])
                        holding = not holding
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    if cpu_active:
                        diff = -1
                    else:
                        diff = 1
                    cpu_active = not cpu_active
                    curr_pos[1] = 1000
                    event.key = K_SPACE
                elif event.key == K_ESCAPE:
                    debug = not debug
                elif event.key in [K_1, K_2, K_3, K_4, K_0]:
                    cpu_active = True
                    if event.key == K_1:
                        diff = 1
                    elif event.key == K_2:
                        diff = 2
                    elif event.key == K_3:
                        diff = 3
                    elif event.key == K_4:
                        diff = 4
                    elif event.key == K_0:
                        diff = 0
                    event.key = K_SPACE
                if event.key == K_SPACE:
                    if win_state:
                        curr_pos[1] = 1000
                    moves = [0 for y in range(9)]
                    mod = -100
                    remaining_moves = 3
                    holding = False
                    turn = True
                    win_state = False
                    winning_line = -1
                    inhand = [[True, True, True], [True, True, True]]
                    cpu_moves = 3
                    win_jingle = False
        if not holding:
            w = detectWin(moves)[0]
            if w != 0:
                win_state = True
        if cpu_active:
            if not turn and not win_state:
                if hand_state == 0:
                    think_time += dt
                    curr_sprite = "hand_open"
                    if think_time > randint(round(500/(diff+1)), round(1000/(diff+1))):
                        hand_state = choice([1, 1] + [10 for i in range(diff+1)])
                        think_pick = randint(0, 8)
                        think_time = 0
                elif hand_state == 1:
                    if move_hand(hand_pos["board"][think_pick]):
                        think_time += dt
                        if think_time > randint(round(500/(diff+1)), round(1000/(diff+1))):
                            hand_state = choice([1] + [10 for i in range(diff+1)])
                            if hand_state == 1:
                                think_pick = randint(0, 8)
                            think_time = 0
                elif hand_state == 10:
                    if cpu_moves > 0:
                        if move_hand(hand_pos["hand"][cpu_moves-1]):
                            think_time += dt
                            if think_time > randint(round(500/(diff+1)), round(1000/(diff+1))):
                                hand_state = choice([21, 21] + [30 for i in range(diff+1)])
                                last_move, pickup = cpu_morris(2, diff)
                                pygame.mixer.Sound.play(sounds["grab"])
                                curr_sprite = "hand_grab"
                                g = -1
                                while True:
                                    if inhand[1][g]:
                                        inhand[1][g] = False
                                        break
                                    g -= 1
                                cpu_moves = inhand[1].count(True)
                    else:
                        hand_state = 20
                        last_move, pickup = cpu_morris(2, diff)
                elif hand_state == 20:
                    if move_hand(hand_pos["board"][pickup]):
                        moves[pickup] = 0
                        hand_state = choice([21] + [30 for i in range(diff+1)])
                        pygame.mixer.Sound.play(sounds["grab"])
                        curr_sprite = "hand_grab"
                elif hand_state == 21:
                    if move_hand(hand_pos["board"][think_pick]):
                        think_time += dt
                        if think_time > randint(round(500/(diff+1)), round(1000/(diff+1))):
                            hand_state = choice([21] + [30 for i in range(diff+1)])
                            if hand_state == 21:
                                think_pick = randint(0, 8)
                                while moves[think_pick] != 0:
                                    think_pick = randint(0, 8)
                            think_time = 0
                elif hand_state == 30:
                    if move_hand(hand_pos["board"][last_move]):
                        hand_state = 40
                        moves[last_move] = 2
                        pygame.mixer.Sound.play(sounds["place"])
                        curr_sprite = "hand_open"
                elif hand_state == 40:
                    turn = True
                    if remaining_moves < 0:
                        winPoss = 0
                        for i in range(len(moves)):
                            if moves[i] == 0:
                                test_moves = moves.copy()
                                test_moves[i] = 2
                                posW, wL = detectWin(test_moves)
                                if posW == 2:
                                    winPoss += 1
                        if winPoss > 1:
                            if diff == 4:
                                current_msg = "Nice try."
                            elif diff > 1:
                                current_msg = "I think I got it..."
                    wait_time = 0
            elif not win_state:
                hand_state = 0
                if move_hand(hand_pos["idle"]):
                    if wait_time < 10000:
                        curr_sprite = "hand_open"
                    elif wait_time < 20000:
                        curr_sprite = "hand_tappy"
                    else:
                        curr_sprite = "hand_watch"
                    wait_time += dt
    else:
        dt = clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.ACTIVEEVENT:
                try:
                    event.state
                except AttributeError:
                    continue
                if event.state & 1 == 1:
                    paused = not event.gain
            elif event.type == pygame.QUIT:
                active = False
    screen.fill((255, 255, 255))
    if paused:
        bg_mod -= .02*dt/3 if bg_mod > 0 else 0
    else:
        bg_mod += (dt/400)*(bg_mod+1) if bg_mod < 5 else 0
    if bg_shift > 79*_sm:
        bg_shift = 0 + (dt * (bg_mod/100))
    else:
        bg_shift += dt * (bg_mod/100)
    for i in range(-2, 9):
        for j in range(-2, 9):
            screen.blit(sprites["bg"], (bg_shift+((79*_sm)*i), -bg_shift+((79*_sm)*j)))
    draw_board()
    if not paused and not (cpu_active and not turn):
        highlight_square(turn)
    for i, move in enumerate(moves):
        if winning_line not in piece_lines[i]:
            shift = shifts[i]*((mod+100)/25)
            gmod = ((-0.1*mod)**2)-100
        else:
            shift = 0
            gmod = 0
        if move == 1:
            draw_o(squares[i], "blue", shift, gmod)
        elif move == 2:
            draw_o(squares[i], "red", shift, gmod)
    if True in inhand[0]:
        for i, p in enumerate(inhand[0]):
            if p:
                draw_o(pygame.Rect(0-(70*_sm), squares[i*3].top, 140, 140),
                       "blue", shift, gmod)
    if True in inhand[1]:
        for i, p in enumerate(inhand[1]):
            if p:
                draw_o(pygame.Rect(disw-(70*_sm), squares[i*3].top, 140, 140),
                       "red", shift, gmod)
    if not paused:
        if holding and turn:
            draw_o_center(pygame.mouse.get_pos(), "blue")
        elif holding and not turn:
            draw_o_center(pygame.mouse.get_pos(), "red")
    if cpu_active and hand_state in [30, 21]:
        draw_o_center((int(curr_pos[0]), int(curr_pos[1])), "red")
    if win_state and not paused:
        mod += dt / 5
        if cpu_active:
            curr_sprite = "hand_open"
    if debug:
        debug_info["last_move"] = last_move
        debug_show()
    if cpu_active:
        if win_state:
            mod_pos = (curr_pos[0] + shift, curr_pos[1] + gmod)
        else:
            mod_pos = curr_pos
        draw_me = sprites[curr_sprite]
        if type(draw_me) == list:  # animated sprites
            if not paused:
                if frameup > 90 or frame > len(draw_me)-1:
                    frame = frame+1 if frame < len(draw_me)-1 else 0
                    frameup = 0
                frameup += dt
            screen.blit(draw_me[frame], mod_pos)
        else:
            screen.blit(draw_me, mod_pos)

    if paused or win_state:
        fade += dt/2 if fade < 196 else 0
    else:
        if fade > 0:
            fade -= dt/3
        if fade < 0:
            fade = 0
    if paused:
        pause_slide = (pause_slide + dt * (-pause_slide/150))\
                       if pause_slide < -1 else -1
    else:
        if -200 < pause_slide < 500:
            pause_slide += (dt/8) * ((pause_slide)/10)
        else:
            pause_slide = -300
    if win_state and not paused:
        win_slide = (win_slide + dt * (-win_slide/150))\
                     if win_slide < -1 else -1
    else:
        if -200 < win_slide < 500:
            win_slide += (dt/8) * ((win_slide)/10)
        else:
            win_slide = -300
    pause_screen = pygame.Surface((640*_sm, 480*_sm))
    pause_screen.set_alpha(fade)
    pause_screen.fill((0, 0, 0))
    screen.blit(pause_screen, (0, 0))
    if win_state:
        if not win_jingle:
            #pygame.mixer.Sound.play(sounds["win"])
            current_msg = "Good game!"
            newmsg = True
            win_jingle = True
            if w == 1:
                if diff == 0:
                    current_msg = "oopsie uwu"
                elif diff == 4:
                    current_msg = "Damn it!"
                wls[diff][0] += 1
            elif w == 2:
                if diff == 0:
                    current_msg = "wowza! i won! >W<"
                if diff == 4:
                    current_msg = "Pathetic..."
                wls[diff][1] += 1
        wf = w
        winning_line = detectWin(moves)[1]
    draw_text("Andy", f'{wls[diff][0]}', (110, 134, 255), (280*_sm, 30*_sm))
    draw_text("Andy", f'-', (255, 255, 255), (320*_sm, 30*_sm))
    if diff in [0, -1]:
        difftext = ["owo", f"Player {(not turn) + 1}"][diff]
    else:
        difftext = diff
    difftext = ["uwu", "Easy", "Normal", "Hard", "Pain!", f"Player {(not turn) + 1}"][diff]
    draw_text("AndySmall", f'{difftext}', (255, 255, 255), (320*_sm, 45*_sm))
    draw_text("Andy", f'{wls[diff][1]}', (217, 65, 65), (360*_sm, 30*_sm))
    if newmsg:
        if cpu_active:
            msgpopup = max(425, msgpopup-10)
            if msgpopup == 425:
                msgtime -= dt
                if msgtime < 0:
                    newmsg = False
        else:
            newmsg = False
    else:
        msgtime = 5000
        msgpopup = min(750, msgpopup+10)
    #screen.blit(sprites["msgbub"], (125*_sm, msgpopup-100*_sm))
    draw_text("Andy", current_msg, (255, 192, 192), (320*_sm, msgpopup*_sm))
    draw_text("Andy", f'The Winner is {ws[wf]}!!',
              (255, 255, 255), (320*_sm, (200+win_slide)*_sm))
    draw_text("Andy", f'Press [Space] to restart!!',
              (255, 255, 255), (320*_sm, (260+win_slide)*_sm))
    draw_text("Andy", f'Game paused',
              (255, 255, 255), (320*_sm, (200+pause_slide)*_sm))
    draw_text("Andy", f'Focus to resume',
              (255, 255, 255), (320*_sm, (260+pause_slide)*_sm))

    pygame.display.flip()

pygame.quit()

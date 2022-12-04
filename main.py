# import module
import pygame
import random
import pyautogui
import time
import math
import keyboard
import sys

pygame.init()  # initialization

# screen setting
unit = pyautogui.size()[1] * 0.055  # size unit
screen_width = 9 * unit  # width size (9)
screen_height = 16 * unit  # height size (16)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tank")  # name of game

username = ""
userscore = {}
plant_music = pygame.mixer.Sound("media\\plant_music.wav")
mine_music = pygame.mixer.Sound("media\\mine_music.wav")
parts_music = pygame.mixer.Sound("media\\parts_music.wav")
store_music = pygame.mixer.Sound("media\\store_music.wav")
war_music = pygame.mixer.Sound("media\\war_music.wav")
button_sound = pygame.mixer.Sound("media\\button_sound.wav")


def load():
    global userscore
    userscore.clear()
    sys.stdin = open(f'users\\ranking.txt', 'r')
    n = int(input())
    for _ in range(n):
        name = input()
        score = int(input())
        userscore[name] = score
    userscore = dict(sorted(userscore.items(), key=lambda x: x[1], reverse=True))\

    global username
    load_time = time.time()
    running = True
    while running:
        screen.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT: exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: exit(0)

        opening = pygame.transform.scale(pygame.image.load("img\\opening.png"), (unit * 9, unit * 16)).convert_alpha()
        opening.set_alpha(int((time.time() - load_time) * 127))
        screen.blit(opening, opening.get_rect())

        if time.time() - load_time > 3: running = False

        pygame.display.update()

    running = True
    while running:
        screen.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT: exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: exit(0)
                elif event.key == pygame.K_RETURN: running = False
                elif event.key == pygame.K_BACKSPACE: username = username[:-1]
                else:
                    try: username += chr(event.key)
                    except: pass
                    if len(username) > 20: username = username[:20]

        blit(username, 35, unit * 4.5, unit * 2, (255, 0, 0))
        blit("Type User Name", 50, unit * 4.5, unit * 4 , (0, 0, 0))
        blit("Maximum length is 20 character", 25, unit * 4.5, unit * 6, (0, 0, 0))
        blit("Only lower and number are allowed.", 25, unit * 4.5, unit * 6.5, (0, 0, 0))
        blit("RANKING", 50, unit * 4.5, unit * 10, (0, 0, 0))
        blit("RANK", 25, unit * 2.5, unit * 11, (0, 0, 0))
        blit("NAME", 25, unit * 4.5, unit * 11, (0, 0, 0))
        blit("SCORE", 25, unit * 6.5, unit * 11, (0, 0, 0))
        for i in range(5):
            blit(f"{i+1}", 25, unit * 2.5, unit * (12 + 0.5 * i), (0, 0, 0))
            if len(userscore) > i: blit(f"{list(userscore.keys())[i]}", 25, unit * 4.5, unit * (12 + 0.5 * i), (0, 0, 0))
            if len(userscore) > i: blit(f"{list(userscore.values())[i]}", 25, unit * 6.5, unit * (12 + 0.5 * i), (0, 0, 0))

        pygame.display.update()  # update screen

    global holding, mine_entity, selected, unlock_sheets, unlock_parts, parts_list, cleared, plant_entity, store_entity
    try:
        sys.stdin = open(f'users\\{username}.txt', 'r')
        A = list(map(int, input().split()))
        holding = Resource(A[0], A[1], A[2], A[3], A[4], A[5], A[6], A[7])
        B = list(map(int, input().split()))
        for entity in mine_entity:
            if entity.name == "Mine":
                entity.level = B[0]
            if entity.name == "Miner":
                entity.level = B[1]
        C = list(map(int, input().split()))
        selected = C
        D = list(map(int, input().split()))
        for i in range(44):
            if D[i] == 1: unlock_sheets[i] = True
            else: unlock_sheets[i] = False
        E = list(map(int, input().split()))
        for i in range(44):
            if E[i] == 0: unlock_parts[i] = False
            else:
                unlock_parts[i] = True
                parts_list[i].level = E[i]
        F = int(input())
        cleared = F
        G = list(map(int, input().split()))
        for entity in plant_entity:
            if entity.name == "Plant":
                entity.level = G[0]
            if entity.name == "Sheet Plant":
                entity.level = G[1]
        H = list(map(float, input().split()))
        for entity in store_entity:
            if entity.name == "miner boost":
                entity.end_time = time.time() + H[0]
            if entity.name == "tank boost":
                entity.end_time = time.time() + H[1]
    except:
        pass


def save():
    score = 0
    sys.stdout = open(f'users\\{username}.txt', 'w')
    print("{} {} {} {} {} {} {} {}".format(
        holding.copper, holding.tin, holding.iron, holding.gold, holding.silver, holding.diamond, holding.coin, holding.gem
    ))
    mine_level = 0
    miner_level = 0
    for entity in mine_entity:
        if entity.name == "Mine":
            mine_level = entity.level
        if entity.name == "Miner":
            miner_level = entity.level
    print("{} {}".format(mine_level, miner_level))
    global selected, unlock_sheets, unlock_parts, parts_list, cleared
    print("{} {} {} {}".format(selected[0], selected[1], selected[2], selected[3]))
    for val in unlock_sheets:
        if val:
            print("1", end=' ')
            score += 1
        else: print("0", end=' ')
    print()
    for i in range(44):
        if unlock_parts[i]:
            print(parts_list[i].level, end=' ')
            score += parts_list[i].level
        else: print("0", end=' ')
    print()
    print(cleared)
    plant_level = 0
    sheet_level = 0
    for entity in plant_entity:
        if entity.name == "Plant":
            plant_level = entity.level
        if entity.name == "Sheet Plant":
            sheet_level = entity.level
    print("{} {}".format(plant_level, sheet_level))
    miner_time = 0
    tank_time = 0
    for entity in store_entity:
        if entity.name == "miner boost":
            miner_time = entity.end_time - time.time()
        if entity.name == "tank boost":
            tank_time = entity.end_time - time.time()
    print("{} {}".format(miner_time, tank_time))

    score += mine_level + miner_level + plant_level + cleared - 11

    sys.stdout = open(f'users\\ranking.txt', 'w+')
    global userscore
    userscore[username] = score
    print(len(userscore))
    for key in userscore.keys():
        print(key)
        print(userscore[key])
    
    sys.stdout.close()


def ending():
    load_time = time.time()
    running = True  # store running?
    while running:
        screen.fill((255, 255, 255))  # fill background to use RGB system

        opening = pygame.transform.scale(pygame.image.load("img\\ending.png"), (unit * 9, unit * 16)).convert_alpha()
        opening.set_alpha(int((time.time() - load_time) * 127))
        screen.blit(opening, opening.get_rect())

        if time.time() - load_time > 3: running = False

        pygame.display.update()  # update screen

# to draw English text
def blit(message, font_size, cen_x, cen_y, color, center=True):
    font = pygame.font.SysFont('consolas', int(font_size))
    text = font.render(message, True, color)
    text_rect = text.get_rect()
    text_rect.center = (cen_x, cen_y)
    if not center:
        text_rect.x = cen_x
        text_rect.y = cen_y
    screen.blit(text, text_rect)


# to draw Korean text
def blit_kor(message, font_size, cen_x, cen_y, color, center=True):
    font = pygame.font.SysFont("malgungothic", int(font_size))
    text = font.render(message, True, color)
    text_rect = text.get_rect()
    text_rect.center = (cen_x, cen_y)
    if not center:
        text_rect.x = cen_x
        text_rect.y = cen_y
    screen.blit(text, text_rect)


def mine_show(mine):
    lines = 7
    mine.messages = []
    if mine.level < 5:
        resource_list = ["", "TIN", "IRON", "SILVER & GOLD", "DIAMOND"]
        mine.messages.append([f"{mine.name} [Lv. {mine.level}]", 0, 0, (0, 0, 0)])
        mine.messages.append([f"", 1, 0, (0, 0, 0)])
        mine.messages.append([f"It products resources.", 2, 0, (128, 0, 128)])
        mine.messages.append([f"", 3, 0, (0, 0, 0)])
        mine.messages.append([f"UNLOCK: {resource_list[mine.level]}", 4, 0, (255, 0, 0)])
        mine.messages.append(["UPGRADE: {:.2e} coin".format(mine.cost[mine.level].coin), 5, 0, (0, 0, 255)])
    if mine.level == 5:
        mine.messages.append([f"{mine.name} [Lv. {mine.level}]", 0, 0, (0, 0, 0)])
        mine.messages.append([f"", 1, 0, (0, 0, 0)])
        mine.messages.append([f"It products resources", 2, 0, (128, 0, 128)])
        mine.messages.append([f"", 3, 0, (0, 0, 0)])
        mine.messages.append([f"FULL UPGRADED", 4, 0, (255, 0, 0)])

    mine.buttons = []
    if mine.level < 5:
        if mine.cost[mine.level] <= holding:
            mine.buttons.append(["upgrade button", 7, 5, 18, "UPGRADE", True])
        else:
            mine.buttons.append(["upgrade button", 7, 5, 18, "UPGRADE", False])

    mine.show(lines)


def miner_show(miner):
    lines = 8
    miner.messages = []
    if miner.level < 100:
        miner.messages.append([f"{miner.name} [Lv. {miner.level}]", 0, 0, (0, 0, 0)])
        miner.messages.append([f"", 1, 0, (0, 0, 0)])
        miner.messages.append([f"They dig resources in mine!", 2, 0, (128, 0, 128)])
        miner.messages.append([f"", 3, 0, (0, 0, 0)])
        miner.messages.append([f"COUNTS: {miner.level} -> {miner.level + 1} (+1)", 4, 0, (255, 0, 0)])
        miner.messages.append(["UPGRADE: {:.2e}".format(miner.cost[miner.level].coin), 5, 0, (0, 0, 255)])
    if miner.level == 100:
        miner.messages.append([f"{miner.name} [Lv. {miner.level}]", 0, 0, (0, 0, 0)])
        miner.messages.append([f"", 1, 0, (0, 0, 0)])
        miner.messages.append([f"They dig resources in mine!", 2, 0, (128, 0, 128)])
        miner.messages.append([f"", 3, 0, (0, 0, 0)])
        miner.messages.append([f"FULL UPGRADED", 4, 0, (255, 0, 0)])

    miner.buttons = []
    if miner.level < 100:
        if miner.cost[miner.level] <= holding:
            miner.buttons.append(["upgrade button", 8, 6, 22, "UPGRADE", True])
        else:
            miner.buttons.append(["upgrade button", 8, 6, 22, "UPGRADE", False])
    miner.show(lines)


now_trade_type = 0
trade_amount = [0, 0, 0, 0, 0]
def trade_show(trade):
    global holding, now_trade_type
    lines = 8
    resource_list = ["Copper", "Tin", "Iron", "Gold", "Silver", "Diamond"]
    resource_value = [holding.copper, holding.tin, holding.iron, holding.gold, holding.silver, holding.diamond]

    trade.messages = []
    trade.messages.append([f"{trade.name}", 0, 0, (0, 0, 0)])
    trade.messages.append([f"", 1, 0, (0, 0, 0)])
    trade.messages.append([f"Resources to coins!", 2, 0, (128, 0, 128)])
    trade.messages.append([f"", 3, 0, (0, 0, 0)])
    trade.messages.append(["{:.2e}".format(resource_value[now_trade_type]), 4, 9, (0, 0, 0)])
    trade.messages.append([f"+e", 6, 10, (0, 0, 0)])

    trade.buttons = []
    trade.buttons.append(["type button", 4, 0, 9, str(resource_list[now_trade_type]), True])
    trade.buttons.append(["number button", 6, 4, 6, str(trade_amount[0]), True])
    trade.buttons.append(["number button", 6, 6, 8, str(trade_amount[1]), True])
    trade.buttons.append(["number button", 6, 8, 10, str(trade_amount[2]), True])
    trade.buttons.append(["number button", 6, 13, 15, str(trade_amount[3]), True])
    trade.buttons.append(["number button", 6, 15, 17, str(trade_amount[4]), True])
    if (trade_amount[0] * 100 + trade_amount[1] * 10 + trade_amount[2] * 1) \
            * 10**(trade_amount[3] * 10 + trade_amount[4]) <= resource_value[now_trade_type]:
        trade.buttons.append(["sell button", 8, 6, 14, "SELL", True])
    else:
        trade.buttons.append(["sell button", 8, 6, 14, "SELL", False])

    trade.show(lines)

def parts_show(parts, group, max_level):
    lines = 1
    parts.messages = []
    if unlock_parts[parts_name_list.index(parts.name)] == False:
        parts.messages.append([f"{parts.name} [Lv. 0] ({group})", 0, 0, (0, 0, 0)])
        parts.messages.append([f"", 1, 0, (0, 0, 0)])
        parts.messages.append([f"NOT UNLOCKED", 2, 0, (255, 0, 0)])
        parts.show(2)
        return
        
    if parts.level < max_level:
        parts.messages.append([f"{parts.name} [Lv. {parts.level}] ({group})", 0, 0, (0, 0, 0)])
        parts.messages.append([f"", 1, 0, (0, 0, 0)])
        if parts.health > 0:
            lines += 1
            parts.messages.append([f"HEALTH: {parts.health} -> {parts.health + parts.health_increment} (+{parts.health_increment})",
                                   lines, 0, (255, 0, 0)])
        if parts.attack > 0:
            lines += 1
            parts.messages.append([f"ATTACK: {parts.attack} -> {parts.attack + parts.attack_increment} (+{parts.attack_increment})",
                                   lines, 0, (255, 0, 0)])
        if parts.attack_speed > 0:
            lines += 1
            parts.messages.append([f"ATTACK SPEED: {parts.attack_speed} -> {parts.attack_speed + parts.attack_speed_increment} (+{parts.attack_speed_increment})",
                                   lines, 0, (255, 0, 0)])
        if parts.move_speed > 0:
            lines += 1
            parts.messages.append([f"MOVE SPEED: {parts.move_speed} -> {parts.move_speed + parts.move_speed_increment} (+{parts.move_speed_increment})",
                                   lines, 0, (255, 0, 0)])
        if parts.max_distance > 0:
            lines += 1
            parts.messages.append([f"MAX DISTANCE: {parts.max_distance} -> {parts.max_distance + parts.max_distance_increment} (+{parts.max_distance_increment})",
                                   lines, 0, (255, 0, 0)])
        parts.messages.append([f"", lines + 1, 0, (0, 0, 0)])
        parts.messages.append(["UPGRADE: {:.2e}".format(parts.cost[parts.level].coin), lines + 2, 0, (0, 0, 255)])
    if parts.level == max_level:
        parts.messages.append([f"{parts.name} [Lv. {parts.level}]", 0, 0, (0, 0, 0)])
        parts.messages.append([f"", 1, 0, (0, 0, 0)])
        if parts.health > 0:
            lines += 1
            parts.messages.append([f"HEALTH: {parts.health}",
                                   lines, 0, (255, 0, 0)])
        if parts.attack > 0:
            lines += 1
            parts.messages.append([f"ATTACK: {parts.attack}",
                                   lines, 0, (255, 0, 0)])
        if parts.attack_speed > 0:
            lines += 1
            parts.messages.append([f"ATTACK SPEED: {parts.attack_speed}",
                                   lines, 0, (255, 0, 0)])
        if parts.move_speed > 0:
            lines += 1
            parts.messages.append([f"MOVE SPEED: {parts.move_speed}",
                                   lines, 0, (255, 0, 0)])
        if parts.max_distance > 0:
            lines += 1
            parts.messages.append([f"MAX DISTANCE: {parts.max_distance}",
                                   lines, 0, (255, 0, 0)])
        parts.messages.append([f"", lines + 1, 0, (0, 0, 0)])
        parts.messages.append([f"FULL UPGRADED", lines + 2, 0, (255, 0, 0)])

    letters = 0
    for i in range(len(parts.messages)):
        letters = max(letters, len(parts.messages[i][0]))
    parts.buttons = []
    if parts.level < max_level:
        if parts.cost[parts.level] <= holding:
            parts.buttons.append(["upgrade button", lines + 4, letters/2 - 6, letters/2 + 6, "UPGRADE", True])
        else:
            parts.buttons.append(["upgrade button", lines + 4, letters/2 - 6, letters/2 + 6, "UPGRADE", False])
    parts.show(lines + 4)


def normal_show(parts):
    parts_show(parts, "normal", 50)


def rare_show(parts):
    parts_show(parts, "rare", 40)


def epic_show(parts):
    parts_show(parts, "epic", 30)


def legend_show(parts):
    parts_show(parts, "legend", 20)


def plant_show(plant):
    lines = 7
    plant.messages = []
    if plant.level < 4:
        group_list = ["", "RARE", "EPIC", "LEGEND"]
        plant.messages.append([f"{plant.name} [Lv. {plant.level}]", 0, 0, (0, 0, 0)])
        plant.messages.append([f"", 1, 0, (0, 0, 0)])
        plant.messages.append([f"Plant can make parts.", 2, 0, (128, 0, 128)])
        plant.messages.append([f"", 3, 0, (0, 0, 0)])
        plant.messages.append([f"UNLOCK: {group_list[plant.level]}", 4, 0, (255, 0, 0)])
        plant.messages.append(["UPGRADE: {:.2e} coin".format(plant.cost[plant.level].coin), 5, 0, (0, 0, 255)])
    if plant.level == 4:
        plant.messages.append([f"{plant.name} [Lv. {plant.level}]", 0, 0, (0, 0, 0)])
        plant.messages.append([f"", 1, 0, (0, 0, 0)])
        plant.messages.append([f"Plant can make parts.", 2, 0, (128, 0, 128)])
        plant.messages.append([f"", 3, 0, (0, 0, 0)])
        plant.messages.append([f"FULL UPGRADED", 4, 0, (255, 0, 0)])

    plant.buttons = []
    if plant.level < 4:
        if plant.cost[plant.level] <= holding:
            plant.buttons.append(["upgrade button", 7, 5, 18, "UPGRADE", True])
        else:
            plant.buttons.append(["upgrade button", 7, 5, 18, "UPGRADE", False])
    plant.show(lines)

parts_number = 0
def parts_plant_show(plant):
    global holding, parts_list, parts_number, plant_entity, unlock_parts
    lines = 12
    plant.messages = []
    plant.messages.append(["        holding   parts", 0, 0, (0, 0, 0)])
    plant.messages.append(["Copper  {:.2e}  {:.2e}".format(holding.copper, parts_list[parts_number].make_cost.copper), 1, 0, (150, 75, 0)])
    plant.messages.append(["Tin     {:.2e}  {:.2e}".format(holding.tin, parts_list[parts_number].make_cost.tin), 2, 0, (255, 255, 255)])
    plant.messages.append(["Iron    {:.2e}  {:.2e}".format(holding.iron, parts_list[parts_number].make_cost.iron), 3, 0, (251, 206, 177)])
    plant.messages.append(["Gold    {:.2e}  {:.2e}".format(holding.gold, parts_list[parts_number].make_cost.gold), 4, 0, (255, 215, 0)])
    plant.messages.append(["Silver  {:.2e}  {:.2e}".format(holding.silver, parts_list[parts_number].make_cost.silver), 5, 0, (90, 90, 90)])
    plant.messages.append(["Diamond {:.2e}  {:.2e}".format(holding.diamond, parts_list[parts_number].make_cost.diamond), 6, 0, (80, 188, 223)])
    plant.messages.append(["Coin    {:.2e}  {:.2e}".format(holding.coin, parts_list[parts_number].make_cost.coin), 7, 0, (255, 255, 0)])
    plant.messages.append(["Gem     {:.2e}  {:.2e}".format(holding.gem, parts_list[parts_number].make_cost.gem), 8, 0, (128, 0, 128)])

    plant.messages.append(["NAME", 10, 0, (0, 0, 0)])

    plant.buttons = []
    plant.buttons.append(["parts button", 10, 6, 27, parts_list[parts_number].name, True])
    limit = 0
    for temp in plant_entity:
        if temp.name == "Plant":
            limit = temp.level
    if unlock_parts[parts_number]:
        plant.buttons.append(["create button", 12, 6, 22, "ALREADY GET", False])
    elif unlock_sheets[parts_number] == False:
        plant.buttons.append(["create button", 12, 6, 22, "SHEET NEED", False])
    else:
        need = 0
        if parts_number % 11 < 4: need = 1
        elif parts_number % 11 < 7: need = 2
        elif parts_number % 11 < 10: need = 3
        elif parts_number % 11 < 11: need = 4
        if limit < need: plant.buttons.append(["create button", 12, 6, 22, f"LEVEL {need} need", False])
        else:
            if parts_list[parts_number].make_cost <= holding:
                plant.buttons.append(["create button", 12, 6, 22, "CREATE", True])
            else:
                plant.buttons.append(["create button", 12, 6, 22, "CREATE", False])
    plant.show(lines)


def sheet_plant_show(plant):
    lines = 5
    plant.messages = []
    if plant.level < 40:
        plant.messages.append([f"Sheet Count: {plant.level + 4} / 44", 0, 0, (0, 0, 0)])
        plant.messages.append(["OPEN: {:.2e}".format(plant.cost[plant.level].coin), 2, 0, (255, 0, 0)])
    if plant.level == 40:
        plant.messages.append([f"Sheet Count: {plant.level + 4} / 44", 0, 0, (0, 0, 0)])
        plant.messages.append([f"ALL UNLOCK", 2, 0, (255, 0, 0)])

    plant.buttons = []
    if plant.level < 40:
        plant.buttons.append(["open button", 4, 5, 16, "OPEN", True])

    plant.show(lines)


def enemy_show(enemy):
    lines = 2
    enemy.messages = []
    enemy.messages.append([f"{enemy.name}", 0, 0, (0, 0, 0)])
    enemy.messages.append([f"HEALTH: {enemy.health} / {enemy.max_health}", 2, 0, (255, 0, 0)])

    enemy.show(lines)


def idle_mines(mine):
    if mine.level == 1:
        for i in range(1, 6):
            resources_time[i] = time.time()
    if mine.level == 2:
        for i in range(2, 6):
            resources_time[i] = time.time()
    if mine.level == 3:
        for i in range(3, 6):
            resources_time[i] = time.time()
    if mine.level == 4:
        for i in range(5, 6):
            resources_time[i] = time.time()


def idle_resources(miner):
    global resources_time, store_entity
    isboost = 0
    for entity in store_entity:
        if entity.name == "miner boost":
            if time.time() <= entity.end_time:
                isboost = 1
    if time.time() - resources_time[0] >= 1 / (isboost+1):
        resources_time[0] = time.time()
        holding.copper += miner.level
    if time.time() - resources_time[1] >= 1 / (isboost+1):
        resources_time[1] = time.time()
        holding.tin += miner.level
    if time.time() - resources_time[2] >= 5 / (isboost+1):
        resources_time[2] = time.time()
        holding.iron += miner.level
    if time.time() - resources_time[3] >= 7 / (isboost+1):
        resources_time[3] = time.time()
        if random.random() < 0.07:
            holding.gold += miner.level
    if time.time() - resources_time[4] >= 7 / (isboost+1):
        resources_time[4] = time.time()
        if random.random() < 0.07:
            holding.silver += miner.level
    if time.time() - resources_time[5] >= 60 / (isboost+1):
        resources_time[5] = time.time()
        if random.random() < 0.0314:
            holding.diamond += miner.level

damaged_time = time.time()
def enemy_idle(enemy):
    global war_start_time, tank_health, damaged_time
    if time.time() - war_start_time > enemy.appear_time:
        if enemy.coord[1] > 13.0 * unit:
            if time.time() - damaged_time > 60 / enemy.attack_speed:
                damaged_time = time.time()
                tank_health -= enemy.damage
        else:
            enemy.move([0, enemy.move_speed, 0])
        pygame.draw.rect(screen, (0, 0, 0),
                         [enemy.coord[0] - enemy.size[0] / 2,
                          enemy.coord[1] - enemy.size[1] / 2 - 20,
                          enemy.size[0], 10], 3)
        pygame.draw.rect(screen, (255, 0, 0),
                         [enemy.coord[0] - enemy.size[0] / 2,
                          enemy.coord[1] - enemy.size[1] / 2 - 20,
                          enemy.size[0] * enemy.health / enemy.max_health, 10])


class Entity:
    def __init__(self, name, opaque, path, size, coord, window_func="", idle_func="", moved=True, selection=False):
        self.name = name
        self.opaque = opaque
        try:
            self.graphics = pygame.transform.scale(pygame.image.load(path), (size[0] * unit, size[1] * unit))
            self.graphics.convert_alpha()
            self.graphics.set_alpha(self.opaque)
        except: self.graphics = None
        self.size = size
        self.coord = coord
        self.window_func = window_func
        self.idle_func = idle_func
        self.moved = moved
        self.selection = selection
        self.size[0] *= unit
        self.size[1] *= unit
        self.coord[0] *= unit
        self.coord[1] *= unit
        self.messages = []
        self.buttons = []

    def __lt__(self, other):
        if self.coord[2] > other.coord[2]:
            return True
        else:
            return False

    def draw(self):
        screen.blit(self.graphics, (self.coord[0] - self.size[0]/2, self.coord[1] - self.size[1]/2))

    def move(self, delta):
        self.coord[0] += delta[0] * unit
        self.coord[1] += delta[1] * unit
        self.coord[2] += delta[2] * unit

    def move_to(self, new):
        self.coord[0] = new[0] * unit
        self.coord[1] = new[1] * unit
        self.coord[2] = new[2] * unit

    def ispointed(self):
        if self.coord[0] - self.size[0]/2 <= pygame.mouse.get_pos()[0] <= self.coord[0] + self.size[0]/2 \
                and self.coord[1] - self.size[1]/2 <= pygame.mouse.get_pos()[1] <= self.coord[1] + self.size[1]/2:
            return True
        else:
            return False

    def isclicked(self):
        if self.coord[0] - self.size[0] / 2 <= pygame.mouse.get_pos()[0] <= self.coord[0] + self.size[0] / 2 \
                and self.coord[1] - self.size[1] / 2 <= pygame.mouse.get_pos()[1] <= self.coord[1] + self.size[1] / 2:
            return True
        else:
            return False

    def drag(self):
        if not self.moved:
            return
        if self.ispointed():
            self.move(pygame.mouse.get_rel())

    def idle(self):
        try:
            exec(self.idle_func + "(self)")
        except:
            pass

    def window(self):
        try:
            exec(self.window_func + "(self)")
        except:
            pass

    def show(self, lines):
        global unit
        font_size = int(unit * 0.3)
        font_width = int(unit * 0.3 * 0.55)
        line_gaps = int(unit * 0.4)
        letters = 0
        for i in range(len(self.messages)):
            letters = max(letters, len(self.messages[i][0]))
        letters = letters + 1

        def blits(edge_x, edge_y):
            pygame.draw.rect(screen, (225, 225, 225),
                             [edge_x, edge_y, letters * font_width + 0.3 * unit, (lines + 1) * line_gaps + 0.3 * unit],
                             0, font_size)
            for i in range(len(self.messages)):
                blit(self.messages[i][0], font_size,
                     edge_x + 0.2 * unit + font_width * self.messages[i][2],
                     edge_y + 0.2 * unit + line_gaps * self.messages[i][1],
                     self.messages[i][3], center=False)
            for i in range(len(self.buttons)):
                self.buttons[i] = Button(self.buttons[i][0],
                                         [(self.buttons[i][3] - self.buttons[i][2]) * font_width / unit, 0.4],
                                         [(edge_x + ((self.buttons[i][2] + self.buttons[i][3]) * font_width + 0.2 * unit) / 2) / unit,
                                            (edge_y + self.buttons[i][1] * line_gaps + 0.3 * unit) / unit, 10],
                                         self.buttons[i][4], 0.3, enabled=self.buttons[i][5])
                self.buttons[i].draw()

        if self.coord[0] + self.size[0]/2 + 0.1 * unit + letters * font_width + 0.3 * unit < 9 * unit:
            blits(self.coord[0] + self.size[0]/2 + 0.1 * unit, self.coord[1] - self.size[1]/2)
        elif self.coord[1] + self.size[1]/2 + 0.1 * unit + (lines + 1) * line_gaps + 0.3 * unit < 16 * unit:
            blits(min(9 * unit - (letters * font_width + 0.3 * unit) - 0.1 * unit, self.coord[0] - self.size[0]/2),
                  self.coord[1] + self.size[1] / 2 + 0.1 * unit)
        elif self.coord[0] - self.size[0]/2  - 0.1 * unit - (letters * font_width + 0.3 * unit) > 0:
            blits(self.coord[0] - self.size[0]/2 - 0.1 * unit - (letters * font_width + 0.3 * unit),
                  min(16 * unit - ((lines + 1) * line_gaps + 0.3 * unit) - 0.1 * unit, self.coord[1] + self.size[1]/2))
        else:
            blits(max(0.1 * unit, self.coord[0] + self.size[0]/2 - (letters * font_width + 0.3 * unit)),
                  self.coord[1] - self.size[1]/2 - ((lines + 1) * line_gaps + 0.3 * unit) - 0.1 * unit)

            
    def set_opaque(self, new_opaque):
        self.opaque = new_opaque
        self.graphics.set_alpha(self.opaque)


class Button(Entity):
    def __init__(self, name, size, coord, message, font_size, window_func="", idle_func="", border=True, enabled=True, moved=False, selection=False):
        super().__init__(name, 255, None, size, coord, window_func, idle_func, moved, selection)
        self.message = message
        self.font_size = font_size * unit
        self.enabled = enabled
        self.border = border

    def isclicked(self):
        if self.enabled and super().isclicked():
            button_sound.play()
            return True
        else:
            return False

    def draw(self):
        color = (0, 0, 0)
        if not self.enabled: color = (255, 0, 0)
        if self.border:
            pygame.draw.polygon(screen, color, [
                [self.coord[0] - self.size[0]/2, self.coord[1] - self.size[1]/2],
                [self.coord[0] - self.size[0]/2, self.coord[1] + self.size[1]/2],
                [self.coord[0] + self.size[0]/2, self.coord[1] + self.size[1]/2],
                [self.coord[0] + self.size[0]/2, self.coord[1] - self.size[1]/2]
            ], 3)
        blit(self.message, self.font_size, self.coord[0], self.coord[1] + self.font_size / 20, color)


class Resource:  # 추후 광물 종류 추가
    coin_cost = [1, 2, 10, 100000, 20000, 1000000]

    def __init__(self, copper, tin, iron, gold, silver, diamond, coin, gem):
        self.copper = copper
        self.tin = tin
        self.iron = iron
        self.gold = gold
        self.silver = silver
        self.diamond = diamond
        self.coin = coin
        self.gem = gem

    def __le__(self, other):
        if self.iron > other.iron:
            return False
        if self.copper > other.copper:
            return False
        if self.tin > other.tin:
            return False
        if self.silver > other.silver:
            return False
        if self.gold > other.gold:
            return False
        if self.diamond > other.diamond:
            return False
        if self.coin > other.coin:
            return False
        if self.gem > other.gem:
            return False
        return True

    def __sub__(self, other):
        return Resource(
            self.copper - other.copper,
            self.tin - other.tin,
            self.iron - other.iron,
            self.gold - other.gold,
            self.silver - other.silver,
            self.diamond - other.diamond,
            self.coin - other.coin,
            self.gem - other.gem
        )

    def draw(self):
        blit("coin", 25, 150, 30, (0, 0, 0), center=False)
        blit("{:.2e}".format(self.coin), 25, 220, 30, (255, 255, 0), center=False)
        blit("gem", 25, 365, 30, (0, 0, 0), center=False)
        blit("{0}".format(self.gem), 25, 420, 30, (128, 0, 128), center=False)
        if int(time.time() - start_time) % 6 == 0:
            blit("copper", 25, 150, 90, (0, 0, 0), center=False)
            blit("{:.2e}".format(self.copper), 25, 250, 90, (150, 75, 0), center=False)
        if int(time.time() - start_time) % 6 == 1:
            blit("Tin", 25, 150, 90, (0, 0, 0), center=False)
            blit("{:.2e}".format(self.tin), 25, 208, 90, (255, 255, 255), center=False)
        if int(time.time() - start_time) % 6 == 2:
            blit("Iron", 25, 150, 90, (0, 0, 0), center=False)
            blit("{:.2e}".format(self.iron), 25, 222, 90, (251, 206, 177), center=False)
        if int(time.time() - start_time) % 6 == 3:
            blit("Gold", 25, 150, 90, (0, 0, 0), center=False)
            blit("{:.2e}".format(self.gold), 25, 222, 90, (255, 215, 0), center=False)
        if int(time.time() - start_time) % 6 == 4:
            blit("Silver", 25, 150, 90, (0, 0, 0), center=False)
            blit("{:.2e}".format(self.silver), 25, 250, 90, (90, 90, 90), center=False)
        if int(time.time() - start_time) % 6 == 5:
            blit("diamond", 25, 150, 90, (0, 0, 0), center=False)
            blit("{:.2e}".format(self.diamond), 25, 264, 90, (80, 188, 223), center=False)


class Upgraded(Entity):
    def __init__(self, name, opaque, path, size, coord, cost, product, window_func="", idle_func="", level=0, moved=True, selection=False):
        super().__init__(name, opaque, path, size, coord, window_func, idle_func, moved, selection)
        self.cost = cost
        self.product = product
        self.level = level
        self.upgrade_button = None
        self.window_func = window_func

    def draw(self):
        super().draw()
        if self.selection:
            pygame.draw.rect(screen, (0, 0, 0), (self.coord[0] - self.size[0] / 2, self.coord[1] - self.size[1] / 2, self.size[0], self.size[1]), 3)

    def upgrade(self):
        global holding
        if self.cost[self.level] <= holding:
            holding = holding - self.cost[self.level]
            self.level += 1
        else:
            pass  # there are not enough resources to upgrade.

class Parts(Upgraded):
    def __init__(self, stats, increment, name, opaque, path, size, coord, make_cost, cost, product, window_func="", idle_func="", skill_func="", level=0, moved=True, selection=False):
        super().__init__(name, opaque, path, size, coord, cost, product, window_func, idle_func, level, moved, selection)
        self.health = stats[0]
        self.attack = stats[1]
        self.attack_speed = stats[2]
        self.move_speed = stats[3]
        self.max_distance = stats[4]
        self.health_increment = increment[0]
        self.attack_increment = increment[1]
        self.attack_speed_increment = increment[2]
        self.move_speed_increment = increment[3]
        self.max_distance_increment = increment[4]
        self.skill_func = skill_func
        self.make_cost = make_cost

    def skill_activate(self):
        exec(self.skill_func + "(self)")

class Goods(Entity):
    def __init__(self, number, name, description, cost, effect, duration):
        super().__init__(name, 255, None, [6, 3], [4.5, number * 2.0 + 6.0, 2], moved=False, selection=False)
        self.number = number
        self.description = description
        self.cost = cost
        self.effect = effect
        self.duration = duration
        self.end_time = time.time()
    
    def draw(self):
        global holding
        pygame.draw.rect(screen, (255, 255, 255), [1 * unit, (self.number * 2.0 + 5.0) * unit, 7 * unit, 2 * unit])
        pygame.draw.rect(screen, (0, 0, 0), [1 * unit, (self.number * 2.0 + 5.0) * unit, 7 * unit, 2 * unit], 5)
        blit(self.name, 0.5 * unit, 1.3 * unit, (self.number * 2.0 + 5.3) * unit, (0, 0, 0), center=False)
        blit(self.description[0:20], 0.3 * unit, 1.3 * unit, (self.number * 2.0 + 6.0) * unit, (128, 0, 128), center=False)
        blit(self.description[20:], 0.3 * unit, 1.3 * unit, (self.number * 2.0 + 6.4) * unit, (128, 0, 128), center=False)
        blit(f"{self.cost.gem} gem", 0.4 * unit, 7.0 * unit, (self.number * 2.0 + 5.7) * unit, (0, 0, 255))
        if self.end_time < time.time():
            if self.cost <= holding: self.button = Button("", [1.5, 0.5], [7, self.number * 2.0 + 6.3], "BUY", 0.4)
            else: self.button = Button("", [1.5, 0.5], [7, self.number * 2.0 + 6.3], "BUY", 0.4, enabled=False)
        else:
            remaining = int(self.end_time - time.time())
            self.button = Button("", [1.5, 0.5], [7, self.number * 2.0 + 6.3], f"{str(remaining//60).zfill(2)}:{str(remaining%60).zfill(2)}", 0.4, enabled=False)
        self.button.draw()

    def buy(self):
        global holding
        holding = holding - self.cost
        self.end_time = time.time() + self.duration


class Enemy(Entity):
    def __init__(self, name, path, size, coord, appear_time, max_health, damage, attack_speed, move_speed, ):
        super().__init__(name, 255, path, size, coord, window_func="enemy_show", idle_func="enemy_idle", moved=False, selection=False)
        self.appear_time = appear_time
        self.max_health = max_health
        self.health = max_health
        self.damage = damage
        self.attack_speed = attack_speed
        self.move_speed = move_speed / 1000

    def draw(self):
        global war_start_time
        if time.time() - war_start_time >= self.appear_time:
            super().draw()


mine_entity = [
    Entity("main background", 255, "img\\main.png", [9, 16], [4.5, 8, 0], moved=False),
    Entity("mine background", 128, "img\\mine_background.png", [9, 16], [4.5, 8, 0.5], moved=False),
    Button("mine button", [1.5, 1.5], [0.95, 15.05, 1], "MINE", 0.6, border=False),
    Button("tank button", [1.5, 1.5], [2.75, 15.05, 1], "TANK", 0.6, border=False),
    Button("war button", [1.5, 1.5], [4.55, 15.05, 1], "WAR", 0.6, border=False),
    Button("plant button", [1.5, 1.5], [6.35, 15.05, 1], "PLANT", 0.6, border=False),
    Button("store button", [1.5, 1.5], [8.15, 15.05, 1], "STORE", 0.6, border=False),
    Upgraded("Mine", 255, "img\\mine.png", [2.4, 2.4], [3, 5, 1],
        [
            Resource(0, 0, 0, 0, 0, 0, 0, 0),
            Resource(0, 0, 0, 0, 0, 0, 1000, 0),
            Resource(0, 0, 0, 0, 0, 0, 100000, 0),
            Resource(0, 0, 0, 0, 0, 0, 1500000, 0),
            Resource(0, 0, 0, 0, 0, 0, 20000000, 0),
        ], [], window_func="mine_show", idle_func="idle_mines", level=1, moved=False),
    Upgraded("Miner", 255, "img\\miner.png", [2.4, 2.0], [3, 8, 2],
        [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [
            Resource(0, 0, 0, 0, 0, 0, int(50 * 1.2**n), 0) for n in range(0, 99)
        ], [], window_func="miner_show", idle_func="idle_resources", level=1, moved=False),
    Upgraded("Trade Center", 255, "img\\trade.png", [2.0, 2.4], [3, 11, 2],
        [], [], window_func="trade_show", level=1, moved=False)
]


def mine_screen():
    mine_music.play(-1)
    global now_trade_type, trade_amount
    next_screen = 0
    mouse_button = [False, False, False, False]
    running = True  # store running?
    while running:
        screen.fill((255, 255, 255))  # fill background to use RGB system
        mine_entity.sort()

        for event in pygame.event.get():  # detect event
            if event.type == pygame.QUIT: running = False  # quit when exit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: running = False  # quit when press ESC
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button <= 3: mouse_button[event.button] = True
                temp_selection = 0
                if event.button == 1:
                    for entity in mine_entity:
                        if entity.isclicked():
                            if entity.name in ["mine button", "tank button", "war button", "plant button", "store button"]:
                                next_screen = entity.name
                                running = False
                        if entity.selection:
                            if entity.name == "Mine":
                                if len(entity.buttons) >= 1 and entity.buttons[0].isclicked():
                                    temp_selection = 1
                                    entity.upgrade()
                            if entity.name == "Miner":
                                if len(entity.buttons) >= 1 and entity.buttons[0].isclicked():
                                    temp_selection = 1
                                    entity.upgrade()
                            if entity.name == "Trade Center":
                                if len(entity.buttons) >= 1 and entity.buttons[0].isclicked():
                                    temp_selection = 1
                                    now_trade_type = (now_trade_type + 1) % 6
                                for i in range(5):
                                    if len(entity.buttons) >= i+2 and entity.buttons[i+1].isclicked():
                                        temp_selection = 1
                                        trade_amount[i] = (trade_amount[i] + 1) % 10
                                if len(entity.buttons) >= 7 and entity.buttons[6].isclicked():
                                    temp_selection = 1
                                    amount = (trade_amount[0] * 100 + trade_amount[1] * 10 + trade_amount[2] * 1) * 10 ** (trade_amount[3] * 10 + trade_amount[4])
                                    if now_trade_type == 0:
                                        holding.copper -= amount
                                        holding.coin += amount * 1
                                    if now_trade_type == 1:
                                        holding.tin -= amount
                                        holding.coin += amount * 2
                                    if now_trade_type == 2:
                                        holding.iron -= amount
                                        holding.coin += amount * 10
                                    if now_trade_type == 3:
                                        holding.gold -= amount
                                        holding.coin += amount * 100000
                                    if now_trade_type == 4:
                                        holding.silver -= amount
                                        holding.coin += amount * 20000
                                    if now_trade_type == 5:
                                        holding.diamond -= amount
                                        holding.coin += amount * 1000000
                if temp_selection == 0:
                    for entity in mine_entity:
                        entity.selection = False
                    if event.button == 3:
                        for entity in mine_entity:
                            if pygame.mouse.get_focused() and entity.ispointed():
                                entity.selection = True
                                break
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button <= 3: mouse_button[event.button] = False

        for entity in reversed(mine_entity):
            entity.idle()
            entity.draw()

        Entity("", 255, "img\\wheel\\wheel" + str(selected[1] - 10) + ".png", [2.5, 2.5], [1.2, 1.2, 4], moved=False).draw()
        Entity("", 255, "img\\body\\body" + str(selected[0] + 1) + ".png", [2.5, 2.5], [1.2, 1.2, 4], moved=False).draw()
        Entity("", 255, "img\\barrel\\barrel" + str(selected[2] - 21) + ".png", [2.5, 2.5], [1.2, 1.2, 4], moved=False).draw()

        for entity in reversed(mine_entity):
            try:
                if entity.selection:
                    entity.window()
            except: pass

        if mouse_button[1]:
            for entity in mine_entity:
                if pygame.mouse.get_focused() and entity.ispointed():
                    entity.drag()
                    break
        else:
            pygame.mouse.get_rel()

        holding.draw()
        pygame.display.update()  # update screen

    mine_music.stop()
    try:
        exec(next_screen[0:-7] + "_screen()")
    except:
        save()
        exit(0)


tank_entity = [
    Entity("main background", 255, "img\\main.png", [9, 16], [4.5, 8, 0], moved=False),
    Entity("part grid", 255, "img\\parts_grid.png", [8, 6.4], [4.5, 10.5, 0.5], moved=False),
    Button("mine button", [1.5, 1.5], [0.95, 15.05, 1], "MINE", 0.6, border=False),
    Button("tank button", [1.5, 1.5], [2.75, 15.05, 1], "TANK", 0.6, border=False),
    Button("war button", [1.5, 1.5], [4.55, 15.05, 1], "WAR", 0.6, border=False),
    Button("plant button", [1.5, 1.5], [6.35, 15.05, 1], "PLANT", 0.6, border=False),
    Button("store button", [1.5, 1.5], [8.15, 15.05, 1], "STORE", 0.6, border=False),
    Upgraded("Mine", 255, "img\\mine.png", [0, 0], [3, 5, 1],
        [
            Resource(0, 0, 0, 0, 0, 0, 0, 0),
            Resource(0, 0, 0, 0, 0, 0, 1000, 0),
            Resource(0, 0, 0, 0, 0, 0, 100000, 0),
            Resource(0, 0, 0, 0, 0, 0, 1500000, 0),
            Resource(0, 0, 0, 0, 0, 0, 20000000, 0),
        ], [], window_func="mine_show", idle_func="idle_mines", level=1, moved=False),
    Upgraded("Miner", 255, "img\\miner.png", [0, 0], [3, 8, 2],
        [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [
            Resource(0, 0, 0, 0, 0, 0, int(50 * 1.2**n), 0) for n in range(0, 99)
        ], [], window_func="miner_show", idle_func="idle_resources", level=1, moved=False)
]

parts_list = [
    Parts([500, 100, 30, 0, 0], [15, 4, 1, 0, 0], "toy tank body", 128, "img\\body\\body1.png", [1.5, 1.5], [4.5, 8, 10],
          Resource(200, 100, 0, 0, 0, 0, 0, 5),
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(40, 20, 0, 0, 0, 0, 1500 * 1.2 ** (j - 1), 0) for j in
                                                range(1, 50)],
          [], window_func="normal_show", level=1, moved=False),
    Parts([600, 105, 30, 0, 0], [15, 4, 1, 0, 0], "model tank body", 128, "img\\body\\body2.png", [1.5, 1.5], [4.5, 8, 10],
          Resource(300, 400, 0, 0, 0, 0, 0, 10),
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(60, 80, 0, 0, 0, 0, 2000 * 1.2 ** (j - 1), 0) for j in
                                                range(1, 50)],
          [], window_func="normal_show", level=1, moved=False),
    Parts([650, 110, 30, 0, 0], [15, 5, 1, 0, 0], "water tank body", 128, "img\\body\\body3.png", [1.5, 1.5], [4.5, 8, 10],
          Resource(400, 300, 0, 0, 0, 0, 0, 12),
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(80, 60, 0, 0, 0, 0, 2500 * 1.2 ** (j - 1), 0) for j in
                                                range(1, 50)],
          [], window_func="normal_show", level=1, moved=False),
    Parts([700, 120, 30, 0, 0], [15, 5, 1, 0, 0], "tank body", 128, "img\\body\\body4.png", [1.5, 1.5], [4.5, 8, 10],
          Resource(400, 500, 0, 0, 0, 0, 0, 15),
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(80, 100, 0, 0, 0, 0, 3000 * 1.2 ** (j - 1), 0) for j in
                                                range(1, 50)],
          [], window_func="normal_show", level=1, moved=False),
    Parts([2000, 400, 30, 0, 0], [50, 10, 1, 0, 0], "armored tank body", 128, "img\\body\\body5.png", [1.5, 1.5], [4.5, 8, 10],
          Resource(1000, 1500, 100, 0, 0, 0, 0, 40),
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(200, 300, 20, 0, 0, 0, 10000 * 1.2 ** (j - 1), 0) for j in
                                                range(1, 40)],
          [], window_func="rare_show", level=1, moved=False),
    Parts([3000, 500, 30, 0, 0], [80, 12, 1, 0, 0], "machine gun tank body", 128, "img\\body\\body6.png", [1.5, 1.5], [4.5, 8, 10],
          Resource(1500, 1500, 120, 0, 0, 0, 0, 45),
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(300, 300, 24, 0, 0, 0, 12000 * 1.2 ** (j - 1), 0) for j in
                                                range(1, 40)],
          [], window_func="rare_show", level=1, moved=False),
    Parts([5000, 600, 30, 0, 0], [120, 15, 1, 0, 0], "sniper tank body", 128, "img\\body\\body7.png", [1.5, 1.5], [4.5, 8, 10],
          Resource(2000, 1500, 150, 0, 0, 0, 0, 50),
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(400, 300, 30, 0, 0, 0, 15000 * 1.2 ** (j - 1), 0) for j in
                                                range(1, 40)],
          [], window_func="rare_show", level=1, moved=False),
    Parts([15000, 1000, 30, 0, 0], [200, 25, 2, 0, 0], "UFO tank body", 128, "img\\body\\body8.png", [1.5, 1.5], [4.5, 8, 10],
          Resource(0, 0, 500, 100, 0, 0, 0, 150),
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(0, 0, 100, 20, 0, 0, 1000000 * 1.2 ** (j - 1), 0) for j in
                                                range(1, 30)],
          [], window_func="epic_show", level=1, moved=False),
    Parts([18000, 1200, 30, 0, 0], [250, 35, 2, 0, 0], "epic tank body", 128, "img\\body\\body9.png", [1.5, 1.5], [4.5, 8, 10],
          Resource(0, 0, 600, 0, 100, 0, 0, 180),
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(0, 0, 120, 0, 20, 0, 120000 * 1.2 ** (j - 1), 0) for j in
                                                range(1, 30)],
          [], window_func="epic_show", level=1, moved=False),
    Parts([20000, 1500, 30, 0, 0], [300, 45, 2, 0, 0], "Russian tank body", 128, "img\\body\\body10.png", [1.5, 1.5],
          [4.5, 8, 10],
          Resource(0, 0, 800, 100, 100, 0, 0, 200),
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(0, 0, 160, 20, 20, 0, 150000 * 1.2 ** (j - 1), 0) for j in
                                                range(1, 30)],
          [], window_func="epic_show", level=1, moved=False),
    Parts([100000, 5000, 30, 0, 0], [2000, 100, 3, 0, 0], "legendary body", 128, "img\\body\\body11.png", [1.5, 1.5],
          [4.5, 8, 10],
          Resource(0, 0, 0, 1000, 1000, 500, 0, 1000),
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(0, 0, 0, 200, 200, 100, 1000000 * 1.2 ** (j - 1), 0) for j in
                                                range(1, 20)],
          [], window_func="legend_show", level=1, moved=False),

    Parts([500, 0, 0, 100, 0], [15, 0, 0, 2, 0], "toy tank wheel", 128, "img\\wheel\\wheel1.png", [1.5, 1.5], [4.5, 8, 10],
          Resource(200, 100, 0, 0, 0, 0, 0, 5),
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(40, 20, 0, 0, 0, 0, 1500 * 1.2 ** (j - 1), 0) for j in
                                                range(1, 50)],
          [], window_func="normal_show", level=1, moved=False),
    Parts([600, 0, 0, 105, 0], [15, 0, 0, 2, 0], "model tank wheel", 128, "img\\wheel\\wheel2.png", [1.5, 1.5], [4.5, 8, 10],
          Resource(300, 400, 0, 0, 0, 0, 0, 10),
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(60, 80, 0, 0, 0, 0, 2000 * 1.2 ** (j - 1), 0) for j in
                                                range(1, 50)],
          [], window_func="normal_show", level=1, moved=False),
    Parts([650, 0, 0, 110, 0], [15, 0, 0, 2, 0], "water tank wheel", 128, "img\\wheel\\wheel3.png", [1.5, 1.5], [4.5, 8, 10],
          Resource(400, 300, 0, 0, 0, 0, 0, 12),
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(80, 60, 0, 0, 0, 0, 2500 * 1.2 ** (j - 1), 0) for j in
                                                range(1, 50)],
          [], window_func="normal_show", level=1, moved=False),
    Parts([700, 0, 0, 120, 0], [15, 0, 0, 2, 0], "tank wheel", 128, "img\\wheel\\wheel4.png", [1.5, 1.5], [4.5, 8, 10],
          Resource(400, 500, 0, 0, 0, 0, 0, 15),
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(80, 100, 0, 0, 0, 0, 3000 * 1.2 ** (j - 1), 0) for j in
                                                range(1, 50)],
          [], window_func="normal_show", level=1, moved=False),
    Parts([2000, 0, 0, 150, 0], [50, 0, 0, 3, 0], "armored tank wheel", 128, "img\\wheel\\wheel5.png", [1.5, 1.5], [4.5, 8, 10],
          Resource(1000, 1500, 100, 0, 0, 0, 0, 40),
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(200, 300, 20, 0, 0, 0, 10000 * 1.2 ** (j - 1), 0) for j in
                                                range(1, 40)],
          [], window_func="rare_show", level=1, moved=False),
    Parts([3000, 0, 0, 160, 0], [80, 0, 0, 3, 0], "machine gun tank wheel", 128, "img\\wheel\\wheel6.png", [1.5, 1.5], [4.5, 8, 10],
          Resource(1500, 1500, 120, 0, 0, 0, 0, 45),
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(300, 300, 24, 0, 0, 0, 12000 * 1.2 ** (j - 1), 0) for j in
                                                range(1, 40)],
          [], window_func="rare_show", level=1, moved=False),
    Parts([5000, 0, 0, 170, 0], [120, 0, 0, 3, 0], "sniper tank wheel", 128, "img\\wheel\\wheel7.png", [1.5, 1.5], [4.5, 8, 10],
          Resource(2000, 1500, 150, 0, 0, 0, 0, 50),
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(400, 300, 30, 0, 0, 0, 15000 * 1.2 ** (j - 1), 0) for j in
                                                range(1, 40)],
          [], window_func="rare_show", level=1, moved=False),
    Parts([15000, 0, 0, 200, 0], [200, 0, 0, 4, 0], "UFO tank wheel", 128, "img\\wheel\\wheel8.png", [1.5, 1.5], [4.5, 8, 10],
          Resource(0, 0, 500, 100, 0, 0, 0, 150),
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(0, 0, 100, 20, 0, 0, 1000000 * 1.2 ** (j - 1), 0) for j in
                                                range(1, 30)],
          [], window_func="epic_show", level=1, moved=False),
    Parts([18000, 0, 0, 225, 0], [250, 0, 0, 4, 0], "epic tank wheel", 128, "img\\wheel\\wheel9.png", [1.5, 1.5], [4.5, 8, 10],
          Resource(0, 0, 600, 0, 100, 0, 0, 180),
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(0, 0, 120, 0, 20, 0, 120000 * 1.2 ** (j - 1), 0) for j in
                                                range(1, 30)],
          [], window_func="epic_show", level=1, moved=False),
    Parts([20000, 0, 0, 250, 0], [300, 0, 0, 4, 0], "Russian tank wheel", 128, "img\\wheel\\wheel10.png", [1.5, 1.5],
          [4.5, 8, 10],
          Resource(0, 0, 800, 100, 100, 0, 0, 200),
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(0, 0, 160, 20, 20, 0, 150000 * 1.2 ** (j - 1), 0) for j in
                                                range(1, 30)],
          [], window_func="epic_show", level=1, moved=False),
    Parts([100000, 0, 0, 300, 0], [2000, 0, 0, 6, 0], "legendary tank wheel", 128, "img\\wheel\\wheel11.png", [1.5, 1.5],
          [4.5, 8, 10],
          Resource(0, 0, 0, 1000, 1000, 500, 0, 1000),
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(0, 0, 0, 200, 200, 100, 1000000 * 1.2 ** (j - 1), 0) for j in
                                                range(1, 20)],
          [], window_func="legend_show", level=1, moved=False),

    Parts([500, 0, 0, 0, 100], [15, 0, 0, 0, 2], "toy tank barrel", 128, "img\\barrel\\barrel1.png", [1.5, 1.5], [4.5, 8, 10],
          Resource(200, 100, 0, 0, 0, 0, 0, 5),
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(40, 20, 0, 0, 0, 0, 1500 * 1.2 ** (j - 1), 0) for j in
                                                range(1, 50)],
          [], window_func="normal_show", level=1, moved=False),
    Parts([600, 0, 0, 0, 105], [15, 0, 0, 0, 2], "model tank barrel", 128, "img\\barrel\\barrel2.png", [1.5, 1.5], [4.5, 8, 10],
          Resource(300, 400, 0, 0, 0, 0, 0, 10),
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(60, 80, 0, 0, 0, 0, 2000 * 1.2 ** (j - 1), 0) for j in
                                                range(1, 50)],
          [], window_func="normal_show", level=1, moved=False),
    Parts([650, 0, 0, 0, 110], [15, 0, 0, 0, 2], "water tank barrel", 128, "img\\barrel\\barrel3.png", [1.5, 1.5], [4.5, 8, 10],
          Resource(400, 300, 0, 0, 0, 0, 0, 12),
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(80, 60, 0, 0, 0, 0, 2500 * 1.2 ** (j - 1), 0) for j in
                                                range(1, 50)],
          [], window_func="normal_show", level=1, moved=False),
    Parts([700, 0, 0, 0, 120], [15, 0, 0, 0, 2], "tank barrel", 128, "img\\barrel\\barrel4.png", [1.5, 1.5], [4.5, 8, 10],
          Resource(400, 500, 0, 0, 0, 0, 0, 15),
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(80, 100, 0, 0, 0, 0, 3000 * 1.2 ** (j - 1), 0) for j in
                                                range(1, 50)],
          [], window_func="normal_show", level=1, moved=False),
    Parts([2000, 0, 0, 0, 150], [50, 0, 0, 0, 4], "armored barrel", 128, "img\\barrel\\barrel5.png", [1.5, 1.5], [4.5, 8, 10],
          Resource(1000, 1500, 100, 0, 0, 0, 0, 40),
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(200, 300, 20, 0, 0, 0, 10000 * 1.2 ** (j - 1), 0) for j in
                                                range(1, 40)],
          [], window_func="rare_show", level=1, moved=False),
    Parts([3000, 0, 0, 0, 160], [80, 0, 0, 0, 4], "machine gun tank barrel", 128, "img\\barrel\\barrel6.png", [1.5, 1.5], [4.5, 8, 10],
          Resource(1500, 1500, 120, 0, 0, 0, 0, 45),
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(300, 300, 24, 0, 0, 0, 12000 * 1.2 ** (j - 1), 0) for j in
                                                range(1, 40)],
          [], window_func="rare_show", level=1, moved=False),
    Parts([5000, 0, 0, 0, 170], [120, 0, 0, 0, 4], "sniper tank barrel", 128, "img\\barrel\\barrel7.png", [1.5, 1.5],
          [4.5, 8, 10],
          Resource(2000, 1500, 150, 0, 0, 0, 0, 50),
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(400, 300, 30, 0, 0, 0, 15000 * 1.2 ** (j - 1), 0) for j in
                                                range(1, 40)],
          [], window_func="rare_show", level=1, moved=False),
    Parts([15000, 0, 0, 0, 200], [200, 0, 0, 0, 4], "UFO tank barrel", 128, "img\\barrel\\barrel8.png", [1.5, 1.5],
          [4.5, 8, 10],
          Resource(0, 0, 500, 100, 0, 0, 0, 150),
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(0, 0, 100, 20, 0, 0, 1000000 * 1.2 ** (j - 1), 0) for j in
                                                range(1, 30)],
          [], window_func="epic_show", level=1, moved=False),
    Parts([18000, 0, 0, 0, 225], [250, 0, 0, 0, 4], "epic tank barrel", 128, "img\\barrel\\barrel9.png", [1.5, 1.5],
          [4.5, 8, 10],
          Resource(0, 0, 600, 0, 100, 0, 0, 180),
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(0, 0, 120, 0, 20, 0, 120000 * 1.2 ** (j - 1), 0) for j in
                                                range(1, 30)],
          [], window_func="epic_show", level=1, moved=False),
    Parts([20000, 0, 0, 0, 250], [300, 0, 0, 0, 4], "Russian tank barrel", 128, "img\\barrel\\barrel10.png", [1.5, 1.5],
          [4.5, 8, 10],
          Resource(0, 0, 800, 100, 100, 0, 0, 200),
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(0, 0, 160, 20, 20, 0, 150000 * 1.2 ** (j - 1), 0) for j in
                                                range(1, 30)],
          [], window_func="epic_show", level=1, moved=False),
    Parts([100000, 0, 0, 0, 300], [2000, 0, 0, 0, 6], "legendary tank barrel", 128, "img\\barrel\\barrel11.png", [1.5, 1.5],
          [4.5, 8, 10],
          Resource(0, 0, 0, 1000, 1000, 500, 0, 1000),
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(0, 0, 0, 200, 200, 100, 1000000 * 1.2 ** (j - 1), 0) for j in
                                                range(1, 20)],
          [], window_func="legend_show", level=1, moved=False),

    Parts([0, 100, 0, 0, 0], [0, 4, 0, 0, 0], "shell", 128, "img\\shell\\shell1.png", [1.5, 1.5], [4.5, 8, 10],
          Resource(200, 100, 0, 0, 0, 0, 0, 5),
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(40, 20, 0, 0, 0, 0, 1500 * 1.2 ** (j - 1), 0) for j in
                                                range(1, 50)],
          [], window_func="normal_show", level=1, moved=False),
    Parts([0, 105, 0, 0, 0], [0, 4, 0, 0, 0], "cannonball", 128, "img\\shell\\shell2.png", [1.5, 1.5], [4.5, 8, 10],
          Resource(300, 400, 0, 0, 0, 0, 0, 10),
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(60, 80, 0, 0, 0, 0, 2000 * 1.2 ** (j - 1), 0) for j in
                                                range(1, 50)],
          [], window_func="normal_show", level=1, moved=False),
    Parts([0, 110, 0, 0, 0], [0, 5, 0, 0, 0], "white shell", 128, "img\\shell\\shell3.png", [1.5, 1.5], [4.5, 8, 10],
          Resource(400, 300, 0, 0, 0, 0, 0, 12),
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(80, 60, 0, 0, 0, 0, 2500 * 1.2 ** (j - 1), 0) for j in
                                                range(1, 50)],
          [], window_func="normal_show", level=1, moved=False),
    Parts([0, 120, 0, 0, 0], [0, 5, 0, 0, 0], "black shell", 128, "img\\shell\\shell4.png", [1.5, 1.5], [4.5, 8, 10],
          Resource(400, 500, 0, 0, 0, 0, 0, 15),
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(80, 100, 0, 0, 0, 0, 3000 * 1.2 ** (j - 1), 0) for j in
                                                range(1, 50)],
          [], window_func="normal_show", level=1, moved=False),
    Parts([0, 400, 0, 0, 0], [0, 10, 0, 0, 0], "fire shell", 128, "img\\shell\\shell5.png", [1.5, 1.5], [4.5, 8, 10],
          Resource(1000, 1500, 100, 0, 0, 0, 0, 40),
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(200, 300, 20, 0, 0, 0, 10000 * 1.2 ** (j - 1), 0) for j in
                                                range(1, 40)],
          [], window_func="rare_show", level=1, moved=False),
    Parts([0, 500, 0, 0, 0], [0, 12, 0, 0, 0], "poison shell", 128, "img\\shell\\shell6.png", [1.5, 1.5], [4.5, 8, 10],
          Resource(1500, 1500, 120, 0, 0, 0, 0, 45),
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(300, 300, 24, 0, 0, 0, 12000 * 1.2 ** (j - 1), 0) for j in
                                                range(1, 40)],
          [], window_func="rare_show", level=1, moved=False),
    Parts([0, 1000, 0, 0, 0], [0, 30, 0, 0, 0], "bomb", 128, "img\\shell\\shell7.png", [1.5, 1.5], [4.5, 8, 10],
          Resource(2000, 1500, 150, 0, 0, 0, 0, 50),
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(400, 300, 30, 0, 0, 0, 15000 * 1.2 ** (j - 1), 0) for j in
                                                range(1, 40)],
          [], window_func="rare_show", level=1, moved=False),
    Parts([0, 1250, 0, 0, 0], [0, 30, 0, 0, 0], "electric shell", 128, "img\\shell\\shell8.png", [1.5, 1.5],
          [4.5, 8, 10],
          Resource(0, 0, 500, 100, 0, 0, 0, 150),
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(0, 0, 100, 20, 0, 0, 1000000 * 1.2 ** (j - 1), 0) for j in
                                                range(1, 30)],
          [], window_func="epic_show", level=1, moved=False),
    Parts([0, 1500, 0, 0, 0], [0, 40, 0, 0, 0], "ice shell", 128, "img\\shell\\shell9.png", [1.5, 1.5], [4.5, 8, 10],
          Resource(0, 0, 600, 0, 100, 0, 0, 180),
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(0, 0, 120, 0, 20, 0, 120000 * 1.2 ** (j - 1), 0) for j in
                                                range(1, 30)],
          [], window_func="epic_show", level=1, moved=False),
    Parts([0, 2000, 0, 0, 0], [0, 50, 0, 0, 0], "natural shell", 128, "img\\shell\\shell10.png", [1.5, 1.5],
          [4.5, 8, 10],
          Resource(0, 0, 800, 100, 100, 0, 0, 200),
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(0, 0, 160, 20, 20, 0, 150000 * 1.2 ** (j - 1), 0) for j in
                                                range(1, 30)],
          [], window_func="epic_show", level=1, moved=False),
    Parts([0, 10000, 0, 0, 0], [0, 500, 0, 0, 0], "nuclear bomb", 128, "img\\shell\\shell11.png", [1.5, 1.5],
          [4.5, 8, 10],
          Resource(0, 0, 0, 1000, 1000, 500, 0, 1000),
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(0, 0, 0, 200, 200, 100, 1000000 * 1.2 ** (j - 1), 0) for j in
                                                range(1, 20)],
          [], window_func="legend_show", level=1, moved=False),
]
parts_name_list = []
for i in range(0, 44): parts_name_list.append(parts_list[i].name)
st = 0

def part_grid_scroll(diff):
    global st
    st = st + diff
    if st < 0: st = 0; return
    if st > 5: st = 5; return
    for i in range(len(tank_entity)-1, -1, -1):
        if tank_entity[i].name in parts_name_list:
            del tank_entity[i]
    p, q = 0, 0
    for i in range(0, 44):
        if unlock_parts[i]: parts_list[i].set_opaque(255)
        parts_list[i].move_to([1.6 * p + 1.3, 1.6 * (q - st) + 8.1, 3])
        p = p + 1
        q = q + (p // 5)
        p = p % 5
    for i in range(5 * st, min(5 * st + 20, 44)):
        tank_entity.append(parts_list[i])

def tank_screen():
    parts_music.play(-1)
    part_grid_scroll(0)
    next_screen = 0
    mouse_button = [False, False, False, False]
    running = True  # store running?
    while running:
        screen.fill((255, 255, 255))  # fill background to use RGB system
        tank_entity.sort()

        for event in pygame.event.get():  # detect event
            if event.type == pygame.QUIT: running = False  # quit when exit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: running = False  # quit when press ESC
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button <= 3: mouse_button[event.button] = True
                temp_selection = 0
                if event.button == 1:
                    for entity in tank_entity:
                        if entity.isclicked():
                            if entity.name in ["mine button", "tank button", "war button", "plant button", "store button"]:
                                next_screen = entity.name
                                running = False
                            if entity.name in parts_name_list:
                                number = parts_name_list.index(entity.name)
                                if unlock_parts[number]:
                                    global selected
                                    selected[number//11] = number
                        if entity.selection:
                            if entity.name in parts_name_list:
                                if len(entity.buttons) >= 1 and entity.buttons[0].isclicked():
                                    temp_selection = 1
                                    entity.health += entity.health_increment
                                    entity.attack += entity.attack_increment
                                    entity.attack_speed += entity.attack_speed_increment
                                    entity.move_speed += entity.move_speed_increment
                                    entity.max_distance += entity.max_distance_increment
                                    entity.upgrade()
                if event.button >= 4 and event.button % 2 == 0:
                    for entity in tank_entity:
                        if entity.name == "part grid" and entity.ispointed():
                            part_grid_scroll(-1)
                if event.button >= 4 and event.button % 2 == 1:
                    for entity in tank_entity:
                        if entity.name == "part grid" and entity.ispointed():
                            part_grid_scroll(+1)

                if temp_selection == 0:
                    for entity in tank_entity:
                        entity.selection = False
                    if event.button == 3:
                        for entity in tank_entity:
                            if pygame.mouse.get_focused() and entity.ispointed():
                                entity.selection = True
                                break
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button <= 3: mouse_button[event.button] = False

        for entity in reversed(tank_entity):
            entity.idle()
            entity.draw()

        Entity("", 255, "img\\wheel\\wheel" + str(selected[1] - 10) + ".png", [2.5, 2.5], [1.2, 1.2, 4], moved=False).draw()
        Entity("", 255, "img\\body\\body" + str(selected[0] + 1) + ".png", [2.5, 2.5], [1.2, 1.2, 4], moved=False).draw()
        Entity("", 255, "img\\barrel\\barrel" + str(selected[2] - 21) + ".png", [2.5, 2.5], [1.2, 1.2, 4], moved=False).draw()

        for number in selected:
            if 5 * st <= number < 5 * st + 20:
                pygame.draw.rect(screen, (255, 127, 0), 
                                [(1.6 * (number%5) + 0.5) * unit, (1.6 * (number//5 - st) + 7.3) * unit, 1.6 * unit, 1.6 * unit], 3)

        pygame.draw.rect(screen, (255, 128, 0), [1.0 * unit, 3.0 * unit, 1.6 * unit, 1.6 * unit], 3)
        Entity("", 255, "img\\body\\body" + str(selected[0] + 1) + ".png", [1.5, 1.5], [1.8, 3.8, 4], moved=False).draw()
        pygame.draw.rect(screen, (255, 128, 0), [6.4 * unit, 3.0 * unit, 1.6 * unit, 1.6 * unit], 3)
        Entity("", 255, "img\\wheel\\wheel" + str(selected[1] - 10) + ".png", [1.5, 1.5], [7.2, 3.8, 4], moved=False).draw()
        pygame.draw.rect(screen, (255, 128, 0), [1.0 * unit, 5.4 * unit, 1.6 * unit, 1.6 * unit], 3)
        Entity("", 255, "img\\barrel\\barrel" + str(selected[2] - 21) + ".png", [1.5, 1.5], [1.8, 6.2, 4], moved=False).draw()
        pygame.draw.rect(screen, (255, 128, 0), [6.4 * unit, 5.4 * unit, 1.6 * unit, 1.6 * unit], 3)
        Entity("", 255, "img\\shell\\shell" + str(selected[3] - 32) + ".png", [1.5, 1.5], [7.2, 6.2, 4], moved=False).draw()

        pygame.draw.rect(screen, (255, 128, 0), [3.7 * unit, 3.0 * unit, 1.6 * unit, 1.6 * unit], 3)
        Entity("", 255, "img\\wheel\\wheel" + str(selected[1] - 10) + ".png", [1.5, 1.5], [4.5, 3.8, 4], moved=False).draw()
        Entity("", 255, "img\\body\\body" + str(selected[0] + 1) + ".png", [1.5, 1.5], [4.5, 3.8, 4], moved=False).draw()
        Entity("", 255, "img\\barrel\\barrel" + str(selected[2] - 21) + ".png", [1.5, 1.5], [4.5, 3.8, 4], moved=False).draw()

        if selected[0] % 11 == selected[1] % 11 == selected[2] % 11:
            blit(f"SET BONUS: O", 18, 4.5 * unit, 7.0 * unit, (0, 0, 255))
            blit(f"Health: {2 * sum([parts_list[selected[i]].health for i in range(4)])}", 18, 4.5 * unit, 5.0 * unit, (0, 0, 255))
        else:
            blit(f"SET BONUS: X", 18, 4.5 * unit, 7.0 * unit, (255, 0, 0))
            blit(f"Health: {sum([parts_list[selected[i]].health for i in range(4)])}", 18, 4.5 * unit, 5.0 * unit, (0, 0, 0))
        for entity in store_entity:
            if entity.name == "tank boost":
                if time.time() <= entity.end_time:
                    blit(f"Attack: {2 * sum([parts_list[selected[i]].attack for i in range(4)])}", 18, 4.5 * unit,
                         5.4 * unit, (255, 0, 0))
                else: blit(f"Attack: {sum([parts_list[selected[i]].attack for i in range(4)])}", 18, 4.5 * unit, 5.4 * unit, (0, 0, 0))
        blit(f"Attack Speed: {sum([parts_list[selected[i]].attack_speed for i in range(4)])}", 18, 4.5 * unit, 5.8 * unit, (0, 0, 0))
        blit(f"Move Speed: {sum([parts_list[selected[i]].move_speed for i in range(4)])}", 18, 4.5 * unit, 6.2 * unit, (0, 0, 0))
        blit(f"Max Distance: {sum([parts_list[selected[i]].max_distance for i in range(4)])}", 18, 4.5 * unit, 6.6 * unit, (0, 0, 0))


        for entity in reversed(tank_entity):
            try:
                if entity.selection:
                    entity.window()
            except: pass

        if mouse_button[1]:
            for entity in tank_entity:
                if pygame.mouse.get_focused() and entity.ispointed():
                    entity.drag()
                    break
        else:
            pygame.mouse.get_rel()


        holding.draw()
        pygame.display.update()  # update screen

    parts_music.stop()
    try:
        exec(next_screen[0:-7] + "_screen()")
    except:
        save()
        exit(0)

war_entity = [
    Entity("main background", 255, "img\\main.png", [9, 16], [4.5, 8, 0], moved=False),
    Button("mine button", [1.5, 1.5], [0.95, 15.05, 1], "MINE", 0.6, border=False),
    Button("tank button", [1.5, 1.5], [2.75, 15.05, 1], "TANK", 0.6, border=False),
    Button("war button", [1.5, 1.5], [4.55, 15.05, 1], "WAR", 0.6, border=False),
    Button("plant button", [1.5, 1.5], [6.35, 15.05, 1], "PLANT", 0.6, border=False),
    Button("store button", [1.5, 1.5], [8.15, 15.05, 1], "STORE", 0.6, border=False),
    Upgraded("Mine", 255, "img\\mine.png", [0, 0], [3, 5, 1],
        [
            Resource(0, 0, 0, 0, 0, 0, 0, 0),
            Resource(0, 0, 0, 0, 0, 0, 1000, 0),
            Resource(0, 0, 0, 0, 0, 0, 100000, 0),
            Resource(0, 0, 0, 0, 0, 0, 1500000, 0),
            Resource(0, 0, 0, 0, 0, 0, 20000000, 0),
        ], [], window_func="mine_show", idle_func="idle_mines", level=1, moved=False),
    Upgraded("Miner", 255, "img\\miner.png", [0, 0], [3, 8, 2],
        [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [
            Resource(0, 0, 0, 0, 0, 0, int(50 * 1.2**n), 0) for n in range(0, 99)
        ], [], window_func="miner_show", idle_func="idle_resources", level=1, moved=False),
]
for i in range(5):
    for j in range(6):
        war_entity.append(Button(f"Stage {6 * i + j + 1}", [1.0, 1.0], [1.5 + 1.2 * j, 5 + 1.2 * i, 2], f"{6 * i + j + 1}", 0.5))

def war_screen():
    war_music.play(-1)
    next_screen = 0
    mouse_button = [False, False, False, False]
    running = True  # store running?
    while running:
        screen.fill((255, 255, 255))  # fill background to use RGB system
        war_entity.sort()

        for event in pygame.event.get():  # detect event
            if event.type == pygame.QUIT: running = False  # quit when exit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: running = False  # quit when press ESC
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button <= 3: mouse_button[event.button] = True
                temp_selection = 0
                if event.button == 1:
                    for entity in war_entity:
                        if entity.isclicked():
                            if entity.name in ["mine button", "tank button", "war button", "plant button", "store button"]:
                                next_screen = entity.name
                                running = False
                            if entity.name[0:5] == "Stage":
                                stage_level = int(entity.name[6:])
                                stage_screen(stage_level)
                        if entity.selection:
                            pass
                if temp_selection == 0:
                    for entity in war_entity:
                        entity.selection = False
                    if event.button == 3:
                        for entity in war_entity:
                            if pygame.mouse.get_focused() and entity.ispointed():
                                entity.selection = True
                                break
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button <= 3: mouse_button[event.button] = False

        for entity in war_entity:
            global cleared
            if entity.name[0:5] == "Stage":
                if int(entity.name[6:]) <= cleared + 1: entity.enabled = True
                else: entity.enabled = False

        for entity in reversed(war_entity):
            entity.idle()
            entity.draw()

        Entity("", 255, "img\\wheel\\wheel" + str(selected[1] - 10) + ".png", [2.5, 2.5], [1.2, 1.2, 4], moved=False).draw()
        Entity("", 255, "img\\body\\body" + str(selected[0] + 1) + ".png", [2.5, 2.5], [1.2, 1.2, 4], moved=False).draw()
        Entity("", 255, "img\\barrel\\barrel" + str(selected[2] - 21) + ".png", [2.5, 2.5], [1.2, 1.2, 4], moved=False).draw()

        blit("STAGES", 72, 4.5 * unit, 3.5 * unit, (0, 0, 0))
        if selected[0] % 11 == selected[1] % 11 == selected[2] % 11:
            blit(f"SET BONUS: O", 18, 6.0 * unit, 13.0 * unit, (0, 0, 255))
            blit(f"Health: {2 * sum([parts_list[selected[i]].health for i in range(4)])}", 18, 6.0 * unit, 11.0 * unit,
                 (0, 0, 255))
        else:
            blit(f"SET BONUS: X", 18, 6.0 * unit, 13.0 * unit, (255, 0, 0))
            blit(f"Health: {sum([parts_list[selected[i]].health for i in range(4)])}", 18, 6.0 * unit, 11.0 * unit,
                 (0, 0, 0))
        for entity in store_entity:
            if entity.name == "tank boost":
                if time.time() <= entity.end_time:
                    blit(f"Attack: {2 * sum([parts_list[selected[i]].attack for i in range(4)])}", 18, 6.0 * unit,
                         11.4 * unit, (255, 0, 0))
                else: blit(f"Attack: {sum([parts_list[selected[i]].attack for i in range(4)])}", 18, 6.0 * unit, 11.4 * unit, (0, 0, 0))
        blit(f"Attack Speed: {sum([parts_list[selected[i]].attack_speed for i in range(4)])}", 18, 6.0 * unit, 11.8 * unit, (0, 0, 0))
        blit(f"Move Speed: {sum([parts_list[selected[i]].move_speed for i in range(4)])}", 18, 6.0 * unit, 12.2 * unit, (0, 0, 0))
        blit(f"Max Distance: {sum([parts_list[selected[i]].max_distance for i in range(4)])}", 18, 6.0 * unit, 12.6 * unit, (0, 0, 0))

        Entity("", 255, "img\\wheel\\wheel" + str(selected[1] - 10) + ".png", [3.5, 3.5], [3.0, 12.0, 4], moved=False).draw()
        Entity("", 255, "img\\body\\body" + str(selected[0] + 1) + ".png", [3.5, 3.5], [3.0, 12.0, 4], moved=False).draw()
        Entity("", 255, "img\\barrel\\barrel" + str(selected[2] - 21) + ".png", [3.5, 3.5], [3.0, 12.0, 4], moved=False).draw()

        for entity in reversed(war_entity):
            try:
                if entity.selection:
                    entity.window()
            except: pass

        if mouse_button[1]:
            for entity in war_entity:
                if pygame.mouse.get_focused() and entity.ispointed():
                    entity.drag()
                    break
        else:
            pygame.mouse.get_rel()

        holding.draw()
        pygame.display.update()  # update screen

    war_music.stop()
    try:
        exec(next_screen[0:-7] + "_screen()")
    except:
        save()
        exit(0)

stage_entity = [
    Entity("main background", 255, "img\\main.png", [9, 16], [4.5, 8, 0], moved=False),
    Entity("war background", 255, "img\\war_background.png", [9, 13.6], [4.5, 9.2, 0.5], moved=False),
    Upgraded("Mine", 255, "img\\mine.png", [0, 0], [3, 5, 1],
        [
            Resource(0, 0, 0, 0, 0, 0, 0, 0),
            Resource(0, 0, 0, 0, 0, 0, 1000, 0),
            Resource(0, 0, 0, 0, 0, 0, 100000, 0),
            Resource(0, 0, 0, 0, 0, 0, 1500000, 0),
            Resource(0, 0, 0, 0, 0, 0, 20000000, 0),
        ], [], window_func="mine_show", idle_func="idle_mines", level=1, moved=False),
    Upgraded("Miner", 255, "img\\miner.png", [0, 0], [3, 8, 2],
        [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [
            Resource(0, 0, 0, 0, 0, 0, int(50 * 1.2**n), 0) for n in range(0, 99)
        ], [], window_func="miner_show", idle_func="idle_resources", level=1, moved=False),
]

war_start_time = 0
tank_health = 0
tank_attack = 0
tank_attack_speed = 0
tank_move_speed = 0
tank_max_distance = 0
tank_max_health = 0
def stage_screen(stage_level):
    win = False
    global war_start_time, stage_entity, tank_health, tank_max_health, tank_attack, tank_attack_speed, tank_move_speed, tank_max_distance
    for entity in stage_entity:
        if entity.name in ["Green Silme", "Blue Silme", "Pink Silme"]:
            stage_entity.remove(entity)
    if 1 <= stage_level <= 10:
        for idx in range(20 + stage_level % 10):
            stage_entity.append(Enemy("Green Silme", "img/enemy/green_silme.png", [1.0, 1.0], [random.random() * 7 + 1.0, 4.5, 4],
                                      idx * 1, 100 * stage_level, 100 * stage_level, random.randint(60, 90), random.randint(10, 15)))
    if 11 <= stage_level <= 20:
        for idx in range(20 + stage_level % 10):
            stage_entity.append(Enemy("Green Silme", "img/enemy/blue_silme.png", [1.0, 1.0], [random.random() * 7 + 1.0, 4.5, 4],
                                      idx * 1, 3000 * stage_level, 100 * stage_level, random.randint(60, 120), random.randint(10, 20)))
    if 21 <= stage_level <= 30:
        for idx in range(20 + stage_level % 10):
            stage_entity.append(Enemy("Green Silme", "img/enemy/pink_silme.png", [1.0, 1.0], [random.random() * 7 + 1.0, 4.5, 4],
                                      idx * 1, 100000 * stage_level, 100 * stage_level, random.randint(60, 180), random.randint(10, 30)))
    global selected
    tank_health = tank_max_health = sum([parts_list[selected[i]].health for i in range(4)])
    if selected[0] % 11 == selected[1] % 11 == selected[2] % 11:
        tank_health *= 2
        tank_max_health *= 2
    tank_attack = sum([parts_list[selected[i]].attack for i in range(4)])
    for entity in store_entity:
        if entity.name == "tank boost":
            if time.time() <= entity.end_time:
                tank_attack *= 2
    tank_attack_speed = sum([parts_list[selected[i]].attack_speed for i in range(4)])
    tank_move_speed = sum([parts_list[selected[i]].move_speed for i in range(4)])
    tank_max_distance = sum([parts_list[selected[i]].max_distance for i in range(4)])
    tank_x = 4.5
    mouse_button = [False, False, False, False]
    keyboard_input = [False, False]
    last_shooting = time.time()
    war_start_time = time.time()
    running = True  # store running?
    while running:
        screen.fill((255, 255, 255))  # fill background to use RGB system
        stage_entity.sort()

        for event in pygame.event.get():  # detect event
            if event.type == pygame.QUIT: running = False  # quit when exit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: running = False  # quit when press ESC
                if event.key == pygame.K_LEFT:
                    keyboard_input[0] = True
                if event.key == pygame.K_RIGHT:
                    keyboard_input[1] = True
                if event.key == pygame.K_SPACE:
                    if time.time() - last_shooting > 10 / tank_attack_speed:
                        last_shooting = time.time()
                        stage_entity.append(Entity("Shell", 255, f"img\\shell\\shell{selected[3] - 32}.png", [0.5, 0.5], [tank_x, 14.0, 4], moved=False))
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    keyboard_input[0] = False
                if event.key == pygame.K_RIGHT:
                    keyboard_input[1] = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button <= 3: mouse_button[event.button] = True
                temp_selection = 0
                if event.button == 1:
                    for entity in stage_entity:
                        if entity.isclicked():
                            pass
                        if entity.selection:
                            pass
                if temp_selection == 0:
                    for entity in stage_entity:
                        entity.selection = False
                    if event.button == 3:
                        for entity in stage_entity:
                            if pygame.mouse.get_focused() and entity.ispointed():
                                entity.selection = True
                                break
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button <= 3: mouse_button[event.button] = False

        if keyboard_input[0]: tank_x -= tank_move_speed / 1000
        if keyboard_input[1]: tank_x += tank_move_speed / 1000
        if tank_x < 1: tank_x = 1
        if tank_x > 8: tank_x = 8

        for entity in stage_entity:
            if entity.name == "Shell":
                entity.move([0, -0.5, 0])
                if entity.coord[1] < (10.0 - tank_max_distance / 60) * unit:
                    stage_entity.remove(entity)
                else:
                    for enemy in stage_entity:
                        if enemy.name in ["Green Silme", "Blue Silme", "Pink Silme"]:
                            if enemy.coord[0] - enemy.size[0]/2 <= entity.coord[0] <= enemy.coord[0] + enemy.size[0]/2 \
                                and enemy.coord[1] - enemy.size[1]/2 <= entity.coord[1] <= enemy.coord[1] + enemy.size[1]/2:
                                stage_entity.remove(entity)
                                enemy.health -= tank_attack

        for enemy in stage_entity:
            if enemy.name in ["Green Silme", "Blue Silme", "Pink Silme"]:
                if enemy.health <= 0:
                    stage_entity.remove(enemy)

        for entity in reversed(stage_entity):
            entity.idle()
            entity.draw()

        Entity("", 255, "img\\wheel\\wheel" + str(selected[1] - 10) + ".png", [2.5, 2.5], [1.2, 1.2, 4],
               moved=False).draw()
        Entity("", 255, "img\\body\\body" + str(selected[0] + 1) + ".png", [2.5, 2.5], [1.2, 1.2, 4],
               moved=False).draw()
        Entity("", 255, "img\\barrel\\barrel" + str(selected[2] - 21) + ".png", [2.5, 2.5], [1.2, 1.2, 4],
               moved=False).draw()

        Entity("", 255, "img\\wheel\\wheel" + str(selected[1] - 10) + ".png", [2.0, 2.0], [tank_x, 15.0, 4],
               moved=False).draw()
        Entity("", 255, "img\\body\\body" + str(selected[0] + 1) + ".png", [2.0, 2.0], [tank_x, 15.0, 4],
               moved=False).draw()
        Entity("", 255, "img\\barrel\\barrel" + str(selected[2] - 21) + ".png", [2.0, 2.0], [tank_x, 15.0, 4],
               moved=False).draw()
        pygame.draw.line(screen, (255, 128, 0), [1 * unit, (10.0 - tank_max_distance / 60) * unit], [8 * unit, (10.0 - tank_max_distance / 60) * unit], 5)
        pygame.draw.line(screen, (0, 0, 0), [1 * unit, 13.5 * unit], [8 * unit, 13.5 * unit], 5)
        pygame.draw.rect(screen, (0, 0, 0),
                         [(tank_x - 1.0) * unit,
                          14 * unit - 20,
                          2 * unit, 10], 3)
        pygame.draw.rect(screen, (255, 0, 0),
                         [(tank_x - 1.0) * unit,
                          14 * unit - 20,
                          2 * unit * tank_health / tank_max_health, 10])

        for entity in reversed(stage_entity):
            try:
                if entity.selection:
                    entity.window()
            except:
                pass

        if mouse_button[1]:
            for entity in stage_entity:
                if pygame.mouse.get_focused() and entity.ispointed():
                    entity.drag()
                    break
        else:
            pygame.mouse.get_rel()

        holding.draw()

        if tank_health <= 0:
            blit("GAME OVER", 100, 4.5 * unit, 8 * unit, (0, 0, 0))
            blit("Press esc to back", 50, 4.5 * unit, 9.5 * unit, (0, 0, 0))

        count = 0
        for enemy in stage_entity:
            if enemy.name in ["Green Silme", "Blue Silme", "Pink Silme"]:
                count += 1
        if count == 0:
            blit("CLEAR", 100, 4.5 * unit, 8 * unit, (0, 0, 0))
            blit("Press esc to back", 50, 4.5 * unit, 9.5 * unit, (0, 0, 0))
            win = True

        pygame.display.update()  # update screen

    if win:
        global cleared
        holding.gem += stage_level
        cleared = max(cleared, stage_level)
        if stage_level == 30:
            ending()

plant_entity = [
    Entity("main background", 255, "img\\main.png", [9, 16], [4.5, 8, 0], moved=False),
    Entity("plant background", 128, "img\\plant_background.png", [9, 16], [4.5, 8, 0.5], moved=False),
    Button("mine button", [1.5, 1.5], [0.95, 15.05, 1], "MINE", 0.6, border=False),
    Button("tank button", [1.5, 1.5], [2.75, 15.05, 1], "TANK", 0.6, border=False),
    Button("war button", [1.5, 1.5], [4.55, 15.05, 1], "WAR", 0.6, border=False),
    Button("plant button", [1.5, 1.5], [6.35, 15.05, 1], "PLANT", 0.6, border=False),
    Button("store button", [1.5, 1.5], [8.15, 15.05, 1], "STORE", 0.6, border=False),
    Upgraded("Mine", 255, "img\\mine.png", [0, 0], [3, 5, 1],
             [
                 Resource(0, 0, 0, 0, 0, 0, 0, 0),
                 Resource(0, 0, 0, 0, 0, 0, 1000, 0),
                 Resource(0, 0, 0, 0, 0, 0, 100000, 0),
                 Resource(0, 0, 0, 0, 0, 0, 1500000, 0),
                 Resource(0, 0, 0, 0, 0, 0, 20000000, 0),
             ], [], window_func="mine_show", idle_func="idle_mines", level=1, moved=False),
    Upgraded("Miner", 255, "img\\miner.png", [0, 0], [3, 8, 2],
             [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [
                 Resource(0, 0, 0, 0, 0, 0, int(50 * 1.2 ** n), 0) for n in range(0, 99)
             ], [], window_func="miner_show", idle_func="idle_resources", level=1, moved=False),
    Upgraded("Plant", 255, "img\\plant.png", [3, 3], [2.8, 5.8, 3],
        [
            Resource(0, 0, 0, 0, 0, 0, 0, 0),
            Resource(0, 0, 0, 0, 0, 0, 200000, 0),
            Resource(0, 0, 0, 0, 0, 0, 5000000, 0),
            Resource(0, 0, 0, 0, 0, 0, 100000000, 0),
        ], [], window_func="plant_show", level=1, moved=False),
    Upgraded("Parts Plant", 255, "img\\parts.png", [1.5, 1.5], [7.0, 5.0, 3],
        [], [], window_func="parts_plant_show", level=1, moved=False),
    Upgraded("Sheet Plant", 255, "img\\chest.png", [1.5, 1.5], [2.0, 11.0, 3],
             [
                 Resource(0, 0, 0, 0, 0, 0, int(10000 * 1.2 ** n), 0) for n in range(0, 40)
             ], [], window_func="sheet_plant_show", level=0, moved=False),
]

def plant_screen():
    plant_music.play(-1)
    next_screen = 0
    mouse_button = [False, False, False, False]
    running = True  # store running?
    while running:
        screen.fill((255, 255, 255))  # fill background to use RGB system
        plant_entity.sort()

        for event in pygame.event.get():  # detect event
            if event.type == pygame.QUIT: running = False  # quit when exit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: running = False  # quit when press ESC
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button <= 3: mouse_button[event.button] = True
                temp_selection = 0
                if event.button == 1:
                    for entity in plant_entity:
                        if entity.isclicked():
                            if entity.name in ["mine button", "tank button", "war button", "plant button", "store button"]:
                                next_screen = entity.name
                                running = False
                        if entity.selection:
                            if entity.name == "Plant":
                                if len(entity.buttons) >= 1 and entity.buttons[0].isclicked():
                                    temp_selection = 1
                                    entity.upgrade()
                            if entity.name == "Parts Plant":
                                global holding, parts_number, unlock_parts
                                if len(entity.buttons) >= 1 and entity.buttons[0].isclicked():
                                    temp_selection = 1
                                    parts_number = (parts_number + 1) % 44
                                if len(entity.buttons) >= 2 and entity.buttons[1].isclicked():
                                    temp_selection = 1
                                    holding -= parts_list[parts_number].make_cost
                                    unlock_parts[parts_number] = True
                            if entity.name == "Sheet Plant":
                                if len(entity.buttons) >= 1 and entity.buttons[0].isclicked():
                                    temp_selection = 1
                                    result = random.randint(1, 40 - entity.level)
                                    for i in range(44):
                                        if unlock_sheets[i] == False: result = result - 1
                                        if result == 0:
                                            unlock_sheets[i] = True
                                            break
                                    entity.upgrade()
                if temp_selection == 0:
                    for entity in plant_entity:
                        entity.selection = False
                    if event.button == 3:
                        for entity in plant_entity:
                            if pygame.mouse.get_focused() and entity.ispointed():
                                entity.selection = True
                                break
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button <= 3: mouse_button[event.button] = False

        for entity in reversed(plant_entity):
            entity.idle()
            entity.draw()

        Entity("", 255, "img\\wheel\\wheel" + str(selected[1] - 10) + ".png", [2.5, 2.5], [1.2, 1.2, 4], moved=False).draw()
        Entity("", 255, "img\\body\\body" + str(selected[0] + 1) + ".png", [2.5, 2.5], [1.2, 1.2, 4], moved=False).draw()
        Entity("", 255, "img\\barrel\\barrel" + str(selected[2] - 21) + ".png", [2.5, 2.5], [1.2, 1.2, 4], moved=False).draw()

        for entity in reversed(plant_entity):
            try:
                if entity.selection:
                    entity.window()
            except: pass

        if mouse_button[1]:
            for entity in plant_entity:
                if pygame.mouse.get_focused() and entity.ispointed():
                    entity.drag()
                    break
        else:
            pygame.mouse.get_rel()

        holding.draw()
        pygame.display.update()  # update screen

    plant_music.stop()
    try:
        exec(next_screen[0:-7] + "_screen()")
    except:
        save()
        exit(0)


store_entity = [
    Entity("main background", 255, "img\\main.png", [9, 16], [4.5, 8, 0], moved=False),
    Entity("store background", 255, "img\\store_background.png", [9, 11.5], [4.5, 8, 0.5], moved=False),
    Goods(1, "miner boost", "Resource product is increased by DOUBLE", Resource(0, 0, 0, 0, 0, 0, 0, 10), "miner_boost", 600),
    Goods(2, "tank boost", "Attack of tank is increased by DOUBLE", Resource(0, 0, 0, 0, 0, 0, 0, 10), "tank_boost", 600),
    Button("mine button", [1.5, 1.5], [0.95, 15.05, 1], "MINE", 0.6, border=False),
    Button("tank button", [1.5, 1.5], [2.75, 15.05, 1], "TANK", 0.6, border=False),
    Button("war button", [1.5, 1.5], [4.55, 15.05, 1], "WAR", 0.6, border=False),
    Button("plant button", [1.5, 1.5], [6.35, 15.05, 1], "PLANT", 0.6, border=False),
    Button("store button", [1.5, 1.5], [8.15, 15.05, 1], "STORE", 0.6, border=False),
    Upgraded("Mine", 255, "img\\mine.png", [0, 0], [3, 5, 1],
             [
                 Resource(0, 0, 0, 0, 0, 0, 0, 0),
                 Resource(0, 0, 0, 0, 0, 0, 1000, 0),
                 Resource(0, 0, 0, 0, 0, 0, 100000, 0),
                 Resource(0, 0, 0, 0, 0, 0, 1500000, 0),
                 Resource(0, 0, 0, 0, 0, 0, 20000000, 0),
             ], [], window_func="mine_show", idle_func="idle_mines", level=1, moved=False),
    Upgraded("Miner", 255, "img\\miner.png", [0, 0], [3, 8, 2],
             [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [
                 Resource(0, 0, 0, 0, 0, 0, int(50 * 1.2 ** n), 0) for n in range(0, 99)
             ], [], window_func="miner_show", idle_func="idle_resources", level=1, moved=False),
]


def store_screen():
    store_music.play(-1)
    part_grid_scroll(0)
    next_screen = 0
    mouse_button = [False, False, False, False]
    running = True  # store running?
    while running:
        screen.fill((255, 255, 255))  # fill background to use RGB system
        store_entity.sort()

        for event in pygame.event.get():  # detect event
            if event.type == pygame.QUIT: running = False  # quit when exit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: running = False  # quit when press ESC
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button <= 3: mouse_button[event.button] = True
                temp_selection = 0
                if event.button == 1:
                    for entity in store_entity:
                        if entity.isclicked():
                            if entity.name in ["mine button", "tank button", "war button", "plant button", "store button"]:
                                next_screen = entity.name
                                running = False
                        if entity.name in ["miner boost", "tank boost"]:
                            if entity.button.isclicked():
                                entity.buy()
                        if entity.selection:
                            pass
                if temp_selection == 0:
                    for entity in store_entity:
                        entity.selection = False
                    if event.button == 3:
                        for entity in store_entity:
                            if pygame.mouse.get_focused() and entity.ispointed():
                                entity.selection = True
                                break
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button <= 3: mouse_button[event.button] = False

        for entity in reversed(store_entity):
            entity.idle()
            entity.draw()

        Entity("", 255, "img\\wheel\\wheel" + str(selected[1] - 10) + ".png", [2.5, 2.5], [1.2, 1.2, 4], moved=False).draw()
        Entity("", 255, "img\\body\\body" + str(selected[0] + 1) + ".png", [2.5, 2.5], [1.2, 1.2, 4], moved=False).draw()
        Entity("", 255, "img\\barrel\\barrel" + str(selected[2] - 21) + ".png", [2.5, 2.5], [1.2, 1.2, 4], moved=False).draw()

        for entity in reversed(store_entity):
            try:
                if entity.selection:
                    entity.window()
            except: pass

        if mouse_button[1]:
            for entity in store_entity:
                if pygame.mouse.get_focused() and entity.ispointed():
                    entity.drag()
                    break
        else:
            pygame.mouse.get_rel()

        holding.draw()
        pygame.display.update()  # update screen

    store_music.stop()
    try:
        exec(next_screen[0:-7] + "_screen()")
    except:
        save()
        exit(0)


if __name__ == "__main__":
    resources_time = [time.time(), time.time(), time.time(), time.time(), time.time(), time.time()]
    holding = Resource(0, 0, 0, 0, 0, 0, 0, 0)
    unlock_parts = [False for _ in range(44)]
    unlock_parts[0] = True
    unlock_parts[11] = True
    unlock_parts[22] = True
    unlock_parts[33] = True
    unlock_sheets = [False for _ in range(44)]
    unlock_sheets[0] = True
    unlock_sheets[11] = True
    unlock_sheets[22] = True
    unlock_sheets[33] = True
    selected = [0, 11, 22, 33]
    cleared = 0
    load()
    start_time = time.time()
    mine_screen()  # game start

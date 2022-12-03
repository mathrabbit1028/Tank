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

resources = []


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
        resourcelist = ["", "TIN", "IRON", "SILVER & GOLD", "DIAMOND"]
        cost = [0, 1000, 100000, 271000000, 3140000000000000]
        cost_express = ["", "1.00e3", "1.00e5", "2.71e8", "3.14e15"]
        mine.messages.append([f"{mine.name} [Lv. {mine.level}]", 0, 0, (0, 0, 0)])
        mine.messages.append([f"", 1, 0, (0, 0, 0)])
        mine.messages.append([f"It products resources.", 2, 0, (128, 0, 128)])
        mine.messages.append([f"", 3, 0, (0, 0, 0)])
        mine.messages.append([f"UNLOCK: {resourcelist[mine.level]}", 4, 0, (255, 0, 0)])
        mine.messages.append([f"UPGRADE: {cost_express[mine.level]} coin", 5, 0, (0, 0, 255)])
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
    if miner.level < 50:
        cost = 250 * 2**miner.level
        miner.messages.append([f"{miner.name} [Lv. {miner.level}]", 0, 0, (0, 0, 0)])
        miner.messages.append([f"", 1, 0, (0, 0, 0)])
        miner.messages.append([f"They dig resources in mine!", 2, 0, (128, 0, 128)])
        miner.messages.append([f"", 3, 0, (0, 0, 0)])
        miner.messages.append([f"COUNTS: {miner.level} -> {miner.level + 1} (+1)", 4, 0, (255, 0, 0)])
        miner.messages.append(["UPGRADE: {:.2e}".format(cost), 5, 0, (0, 0, 255)])
    if miner.level == 50:
        miner.messages.append([f"{miner.name} [Lv. {miner.level}]", 0, 0, (0, 0, 0)])
        miner.messages.append([f"", 1, 0, (0, 0, 0)])
        miner.messages.append([f"They dig resources in mine!", 2, 0, (128, 0, 128)])
        miner.messages.append([f"", 3, 0, (0, 0, 0)])
        miner.messages.append([f"FULL UPGRADED", 4, 0, (255, 0, 0)])

    miner.buttons = []
    if miner.level < 50:
        if miner.cost[miner.level] <= holding:
            miner.buttons.append(["upgrade button", 8, 8, 20, "UPGRADE", True])
        else:
            miner.buttons.append(["upgrade button", 8, 8, 20, "UPGRADE", False])
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
    if parts.level < 50:
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
        pygame.draw.rect(screen, (225, 225, 225),
                         [self.coord[0] + self.size[0] / 2 + 0.1 * unit,
                          self.coord[1] - self.size[1] / 2,
                          letters * font_width + 0.3 * unit,
                          (lines + 1) * line_gaps + 0.3 * unit],
                         0, font_size)
        for i in range(len(self.messages)):
            blit(self.messages[i][0], font_size,
                 self.coord[0] + self.size[0] / 2 + 0.3 * unit + font_width * self.messages[i][2],
                 self.coord[1] - self.size[1] / 2 + 0.2 * unit + line_gaps * self.messages[i][1], self.messages[i][3], center=False)
        for i in range(len(self.buttons)):
            self.buttons[i] = Button(self.buttons[i][0], [(self.buttons[i][3] - self.buttons[i][2]) * font_width / unit, 0.4],
                                [(self.coord[0] + self.size[0] / 2 + (
                                 (self.buttons[i][2] + self.buttons[i][3]) * font_width + 0.4 * unit) / 2) / unit,
                                    (self.coord[1] - self.size[1] / 2 + (
                                  self.buttons[i][1]) * line_gaps + 0.3 * unit) / unit, 10],
                                self.buttons[i][4], 0.3, enabled=self.buttons[i][5])
            self.buttons[i].draw()
            
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
    def __init__(self, stats, increment, name, opaque, path, size, coord, cost, product, window_func="", idle_func="", skill_func="", level=0, moved=True, selection=False):
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
            Resource(0, 0, 0, 0, 0, 0, 271000000, 0),
            Resource(0, 0, 0, 0, 0, 0, 3140000000000000, 0),
        ], [], window_func="mine_show", idle_func="idle_mines", level=1, moved=False),
    Upgraded("Miner", 255, "img\\miner.png", [2.4, 2.0], [3, 8, 2],
        [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [
            Resource(0, 0, 0, 0, 0, 0, 250 * 2**n, 0) for n in range(1, 50)
        ], [], window_func="miner_show", idle_func="idle_resources", level=1, moved=False),
    Upgraded("Trade Center", 255, "img\\trade.png", [2.0, 2.4], [3, 11, 2],
        [], [], window_func="trade_show", level=1, moved=False)
]


def mine_screen():
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

    try:
        exec(next_screen[0:-7] + "_screen()")
    except:
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
            Resource(0, 0, 0, 0, 0, 0, 271000000, 0),
            Resource(0, 0, 0, 0, 0, 0, 3140000000000000, 0),
        ], [], window_func="mine_show", idle_func="idle_mines", level=1, moved=False),
    Upgraded("Miner", 255, "img\\miner.png", [0, 0], [3, 8, 2],
        [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [
            Resource(0, 0, 0, 0, 0, 0, 250 * 2**n, 0) for n in range(1, 50)
        ], [], window_func="miner_show", idle_func="idle_resources", level=1, moved=False)
]

parts_list = [
    Parts([500, 100, 30, 0, 0], [15, 4, 1, 0, 0], "1 Body", 128, "img\\body\\body1.png", [1.5, 1.5], [4.5, 8, 10],
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(0, 0, 0, 0, 0, 0, 1500 * 2**j, 0) for j in range(1, 50)],
          [], window_func="normal_show", level=1, moved=False),
    Parts([500, 100, 30, 0, 0], [15, 4, 1, 0, 0], "2 Body", 128, "img\\body\\body2.png", [1.5, 1.5], [4.5, 8, 10],
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(0, 0, 0, 0, 0, 0, 8000 * 2**j, 0) for j in range(1, 50)],
          [], window_func="normal_show", level=1, moved=False),
    Parts([500, 100, 30, 0, 0], [15, 4, 1, 0, 0], "3 Body", 128, "img\\body\\body3.png", [1.5, 1.5], [4.5, 8, 10],
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(0, 0, 0, 0, 0, 0, 20000 * 2**j, 0) for j in range(1, 50)],
          [], window_func="normal_show", level=1, moved=False),
    Parts([500, 100, 30, 0, 0], [15, 4, 1, 0, 0], "4 Body", 128, "img\\body\\body4.png", [1.5, 1.5], [4.5, 8, 10],
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(0, 0, 0, 0, 0, 0, 80000 * 2**j, 0) for j in range(1, 50)],
          [], window_func="normal_show", level=1, moved=False),
    Parts([500, 100, 30, 0, 0], [15, 4, 1, 0, 0], "5 Body", 128, "img\\body\\body5.png", [1.5, 1.5], [4.5, 8, 10],
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(0, 0, 0, 0, 0, 0, 150000 * 2**j, 0) for j in range(1, 40)],
          [], window_func="rare_show", level=1, moved=False),
    Parts([500, 100, 30, 0, 0], [15, 4, 1, 0, 0], "6 Body", 128, "img\\body\\body6.png", [1.5, 1.5], [4.5, 8, 10],
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(0, 0, 0, 0, 0, 0, 2000000 * 2**j, 0) for j in range(1, 40)],
          [], window_func="rare_show", level=1, moved=False),
    Parts([500, 100, 30, 0, 0], [15, 4, 1, 0, 0], "7 Body", 128, "img\\body\\body7.png", [1.5, 1.5], [4.5, 8, 10],
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(0, 0, 0, 0, 0, 0, 30000000 * 2**j, 0) for j in range(1, 40)],
          [], window_func="rare_show", level=1, moved=False),
    Parts([500, 100, 30, 0, 0], [15, 4, 1, 0, 0], "8 Body", 128, "img\\body\\body8.png", [1.5, 1.5], [4.5, 8, 10],
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(0, 0, 0, 0, 0, 0, 500000000 * 2**j, 0) for j in range(1, 30)],
          [], window_func="epic_show", level=1, moved=False),
    Parts([500, 100, 30, 0, 0], [15, 4, 1, 0, 0], "9 Body", 128, "img\\body\\body9.png", [1.5, 1.5], [4.5, 8, 10],
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(0, 0, 0, 0, 0, 0, 7500000000 * 2**j, 0) for j in range(1, 30)],
          [], window_func="epic_show", level=1, moved=False),
    Parts([500, 100, 30, 0, 0], [15, 4, 1, 0, 0], "10 Body", 128, "img\\body\\body10.png", [1.5, 1.5], [4.5, 8, 10],
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(0, 0, 0, 0, 0, 0, 100000000000 * 2**j, 0) for j in range(1, 30)],
          [], window_func="epic_show", level=1, moved=False),
    Parts([500, 100, 30, 0, 0], [15, 4, 1, 0, 0], "11 Body", 128, "img\\body\\body11.png", [1.5, 1.5], [4.5, 8, 10],
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(0, 0, 0, 0, 0, 0, 10000000000000 * 2**j, 0) for j in range(1, 20)],
          [], window_func="legend_show", level=1, moved=False),

    Parts([300, 0, 0, 100, 0], [9, 0, 0, 4, 0], "1 Wheel", 128, "img\\wheel\\wheel1.png", [1.5, 1.5], [4.5, 8, 10],
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(0, 0, 0, 0, 0, 0, 1500 * 2**j, 0) for j in range(1, 50)],
          [], window_func="normal_show", level=1, moved=False),
    Parts([300, 0, 0, 100, 0], [9, 0, 0, 4, 0], "2 Wheel", 128, "img\\wheel\\wheel2.png", [1.5, 1.5], [4.5, 8, 10],
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(0, 0, 0, 0, 0, 0, 1500 * 2**j, 0) for j in range(1, 50)],
          [], window_func="normal_show", level=1, moved=False),
    Parts([300, 0, 0, 100, 0], [9, 0, 0, 4, 0], "3 Wheel", 128, "img\\wheel\\wheel3.png", [1.5, 1.5], [4.5, 8, 10],
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(0, 0, 0, 0, 0, 0, 1500 * 2**j, 0) for j in range(1, 50)],
          [], window_func="normal_show", level=1, moved=False),
    Parts([300, 0, 0, 100, 0], [9, 0, 0, 4, 0], "4 Wheel", 128, "img\\wheel\\wheel4.png", [1.5, 1.5], [4.5, 8, 10],
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(0, 0, 0, 0, 0, 0, 1500 * 2**j, 0) for j in range(1, 50)],
          [], window_func="normal_show", level=1, moved=False),
    Parts([300, 0, 0, 100, 0], [9, 0, 0, 4, 0], "5 Wheel", 128, "img\\wheel\\wheel5.png", [1.5, 1.5], [4.5, 8, 10],
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(0, 0, 0, 0, 0, 0, 1500 * 2**j, 0) for j in range(1, 50)],
          [], window_func="rare_show", level=1, moved=False),
    Parts([300, 0, 0, 100, 0], [9, 0, 0, 4, 0], "6 Wheel", 128, "img\\wheel\\wheel6.png", [1.5, 1.5], [4.5, 8, 10],
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(0, 0, 0, 0, 0, 0, 1500 * 2**j, 0) for j in range(1, 50)],
          [], window_func="rare_show", level=1, moved=False),
    Parts([300, 0, 0, 100, 0], [9, 0, 0, 4, 0], "7 Wheel", 128, "img\\wheel\\wheel7.png", [1.5, 1.5], [4.5, 8, 10],
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(0, 0, 0, 0, 0, 0, 1500 * 2**j, 0) for j in range(1, 50)],
          [], window_func="rare_show", level=1, moved=False),
    Parts([300, 0, 0, 100, 0], [9, 0, 0, 4, 0], "8 Wheel", 128, "img\\wheel\\wheel8.png", [1.5, 1.5], [4.5, 8, 10],
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(0, 0, 0, 0, 0, 0, 1500 * 2**j, 0) for j in range(1, 50)],
          [], window_func="epic_show", level=1, moved=False),
    Parts([300, 0, 0, 100, 0], [9, 0, 0, 4, 0], "9 Wheel", 128, "img\\wheel\\wheel9.png", [1.5, 1.5], [4.5, 8, 10],
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(0, 0, 0, 0, 0, 0, 1500 * 2**j, 0) for j in range(1, 50)],
          [], window_func="epic_show", level=1, moved=False),
    Parts([300, 0, 0, 100, 0], [9, 0, 0, 4, 0], "10 Wheel", 128, "img\\wheel\\wheel10.png", [1.5, 1.5], [4.5, 8, 10],
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(0, 0, 0, 0, 0, 0, 1500 * 2**j, 0) for j in range(1, 50)],
          [], window_func="epic_show", level=1, moved=False),
    Parts([300, 0, 0, 100, 0], [9, 0, 0, 4, 0], "11 Wheel", 128, "img\\wheel\\wheel11.png", [1.5, 1.5], [4.5, 8, 10],
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(0, 0, 0, 0, 0, 0, 1500 * 2**j, 0) for j in range(1, 50)],
          [], window_func="legend_show", level=1, moved=False),

    Parts([100, 300, 60, 0, 500], [3, 10, 2, 0, 10], "1 Barrel", 128, "img\\barrel\\barrel1.png", [1.5, 1.5], [4.5, 8, 10],
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(0, 0, 0, 0, 0, 0, 1500 * 2**j, 0) for j in range(1, 50)],
          [], window_func="normal_show", level=1, moved=False),
    Parts([100, 300, 60, 0, 500], [3, 10, 2, 0, 10], "2 Barrel", 128, "img\\barrel\\barrel2.png", [1.5, 1.5], [4.5, 8, 10],
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(0, 0, 0, 0, 0, 0, 1500 * 2**j, 0) for j in range(1, 50)],
          [], window_func="normal_show", level=1, moved=False),
    Parts([100, 300, 60, 0, 500], [3, 10, 2, 0, 10], "3 Barrel", 128, "img\\barrel\\barrel3.png", [1.5, 1.5], [4.5, 8, 10],
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(0, 0, 0, 0, 0, 0, 1500 * 2**j, 0) for j in range(1, 50)],
          [], window_func="normal_show", level=1, moved=False),
    Parts([100, 300, 60, 0, 500], [3, 10, 2, 0, 10], "4 Barrel", 128, "img\\barrel\\barrel4.png", [1.5, 1.5], [4.5, 8, 10],
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(0, 0, 0, 0, 0, 0, 1500 * 2**j, 0) for j in range(1, 50)],
          [], window_func="normal_show", level=1, moved=False),
    Parts([100, 300, 60, 0, 500], [3, 10, 2, 0, 10], "5 Barrel", 128, "img\\barrel\\barrel5.png", [1.5, 1.5], [4.5, 8, 10],
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(0, 0, 0, 0, 0, 0, 1500 * 2**j, 0) for j in range(1, 50)],
          [], window_func="rare_show", level=1, moved=False),
    Parts([100, 300, 60, 0, 500], [3, 10, 2, 0, 10], "6 Barrel", 128, "img\\barrel\\barrel6.png", [1.5, 1.5], [4.5, 8, 10],
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(0, 0, 0, 0, 0, 0, 1500 * 2**j, 0) for j in range(1, 50)],
          [], window_func="rare_show", level=1, moved=False),
    Parts([100, 300, 60, 0, 500], [3, 10, 2, 0, 10], "7 Barrel", 128, "img\\barrel\\barrel7.png", [1.5, 1.5], [4.5, 8, 10],
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(0, 0, 0, 0, 0, 0, 1500 * 2**j, 0) for j in range(1, 50)],
          [], window_func="rare_show", level=1, moved=False),
    Parts([100, 300, 60, 0, 500], [3, 10, 2, 0, 10], "8 Barrel", 128, "img\\barrel\\barrel8.png", [1.5, 1.5], [4.5, 8, 10],
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(0, 0, 0, 0, 0, 0, 1500 * 2**j, 0) for j in range(1, 50)],
          [], window_func="epic_show", level=1, moved=False),
    Parts([100, 300, 60, 0, 500], [3, 10, 2, 0, 10], "9 Barrel", 128, "img\\barrel\\barrel9.png", [1.5, 1.5], [4.5, 8, 10],
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(0, 0, 0, 0, 0, 0, 1500 * 2**j, 0) for j in range(1, 50)],
          [], window_func="epic_show", level=1, moved=False),
    Parts([100, 300, 60, 0, 500], [3, 10, 2, 0, 10], "10 Barrel", 128, "img\\barrel\\barrel10.png", [1.5, 1.5], [4.5, 8, 10],
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(0, 0, 0, 0, 0, 0, 1500 * 2**j, 0) for j in range(1, 50)],
          [], window_func="epic_show", level=1, moved=False),
    Parts([100, 300, 60, 0, 500], [3, 10, 2, 0, 10], "11 Barrel", 128, "img\\barrel\\barrel11.png", [1.5, 1.5], [4.5, 8, 10],
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(0, 0, 0, 0, 0, 0, 1500 * 2**j, 0) for j in range(1, 50)],
          [], window_func="legend_show", level=1, moved=False),

    Parts([0, 500, 30, 0, 200], [0, 20, 1, 0, 0.0], "Shell", 128, "img\\shell\\shell1.png", [1.5, 1.5], [4.5, 8, 10],
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(0, 0, 0, 0, 0, 0, 1500 * 2**j, 0) for j in range(1, 50)],
          [], window_func="normal_show", skill_func="", level=1, moved=False),
    Parts([0, 500, 30, 0, 200], [0, 20, 1, 0, 0.0], "Cannonball", 128, "img\\shell\\shell2.png", [1.5, 1.5], [4.5, 8, 10],
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(0, 0, 0, 0, 0, 0, 1500 * 2**j, 0) for j in range(1, 50)],
          [], window_func="normal_show", skill_func="", level=1, moved=False),
    Parts([0, 500, 30, 0, 200], [0, 20, 1, 0, 0.0], "White Shell", 128, "img\\shell\\shell3.png", [1.5, 1.5], [4.5, 8, 10],
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(0, 0, 0, 0, 0, 0, 1500 * 2**j, 0) for j in range(1, 50)],
          [], window_func="rare_show", skill_func="", level=1, moved=False),
    Parts([0, 500, 30, 0, 200], [0, 20, 1, 0, 0.0], "Black Shell", 128, "img\\shell\\shell4.png", [1.5, 1.5], [4.5, 8, 10],
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(0, 0, 0, 0, 0, 0, 1500 * 2**j, 0) for j in range(1, 50)],
          [], window_func="rare_show", skill_func="", level=1, moved=False),
    Parts([0, 500, 30, 0, 200], [0, 20, 1, 0, 0.0], "Fire Shell", 128, "img\\shell\\shell5.png", [1.5, 1.5], [4.5, 8, 10],
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(0, 0, 0, 0, 0, 0, 1500 * 2**j, 0) for j in range(1, 50)],
          [], window_func="epic_show", skill_func="", level=1, moved=False),
    Parts([0, 500, 30, 0, 200], [0, 20, 1, 0, 0.0], "Poison Shell", 128, "img\\shell\\shell6.png", [1.5, 1.5], [4.5, 8, 10],
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(0, 0, 0, 0, 0, 0, 1500 * 2**j, 0) for j in range(1, 50)],
          [], window_func="epic_show", skill_func="", level=1, moved=False),
    Parts([0, 500, 30, 0, 200], [0, 20, 1, 0, 0.0], "Bomb", 128, "img\\shell\\shell7.png", [1.5, 1.5], [4.5, 8, 10],
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(0, 0, 0, 0, 0, 0, 1500 * 2**j, 0) for j in range(1, 50)],
          [], window_func="epic_show", skill_func="", level=1, moved=False),
    Parts([0, 500, 30, 0, 200], [0, 20, 1, 0, 0.0], "Electric Shell", 128, "img\\shell\\shell8.png", [1.5, 1.5], [4.5, 8, 10],
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(0, 0, 0, 0, 0, 0, 1500 * 2**j, 0) for j in range(1, 50)],
          [], window_func="legend_show", skill_func="", level=1, moved=False),
    Parts([0, 500, 30, 0, 200], [0, 20, 1, 0, 0.0], "Ice Shell", 128, "img\\shell\\shell9.png", [1.5, 1.5], [4.5, 8, 10],
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(0, 0, 0, 0, 0, 0, 1500 * 2**j, 0) for j in range(1, 50)],
          [], window_func="legend_show", skill_func="", level=1, moved=False),
    Parts([0, 500, 30, 0, 200], [0, 20, 1, 0, 0.0], "Natural Shell", 128, "img\\shell\\shell10.png", [1.5, 1.5], [4.5, 8, 10],
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(0, 0, 0, 0, 0, 0, 1500 * 2**j, 0) for j in range(1, 50)],
          [], window_func="legend_show", skill_func="", level=1, moved=False),
    Parts([0, 500, 30, 0, 200], [0, 20, 1, 0, 0.0], "Nuclear Bomb", 128, "img\\shell\\shell11.png", [1.5, 1.5], [4.5, 8, 10],
          [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [Resource(0, 0, 0, 0, 0, 0, 1500 * 2**j, 0) for j in range(1, 50)],
          [], window_func="legend_show", skill_func="", level=1, moved=False),
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

    try:
        exec(next_screen[0:-7] + "_screen()")
    except:
        exit(0)


plant_entity = [
    Entity("main background", 255, "img\\main.png", [9, 16], [4.5, 8, 0], moved=False),
    Entity("plant", 255, "img\\mine.png", [3, 3], [4.5, 8, 0.5], moved=False),
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
            Resource(0, 0, 0, 0, 0, 0, 271000000, 0),
            Resource(0, 0, 0, 0, 0, 0, 3140000000000000, 0),
        ], [], window_func="mine_show", idle_func="idle_mines", level=1, moved=False),
    Upgraded("Miner", 255, "img\\miner.png", [0, 0], [3, 8, 2],
        [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [
            Resource(0, 0, 0, 0, 0, 0, 250 * 2**n, 0) for n in range(1, 50)
        ], [], window_func="miner_show", idle_func="idle_resources", level=1, moved=False)
]

def plant_screen():
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
                            pass

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

    try:
        exec(next_screen[0:-7] + "_screen()")
    except:
        exit(0)


store_entity = [
    Entity("main background", 255, "img\\main.png", [9, 16], [4.5, 8, 0], moved=False),
    Entity("store background", 255, "img\\store_background.png", [9, 11.5], [4.5, 8, 0.5], moved=False),
    Goods(1, "miner boost", "Resource product is increased by DOUBLE", Resource(0, 0, 0, 0, 0, 0, 0, 10), "miner_boost", 600),
    Goods(2, "tank boost", "Attack of tank is increased by DOUBLE", Resource(0, 0, 0, 0, 0, 0, 0, 100), "tank_boost", 600),
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
            Resource(0, 0, 0, 0, 0, 0, 271000000, 0),
            Resource(0, 0, 0, 0, 0, 0, 3140000000000000, 0),
        ], [], window_func="mine_show", idle_func="idle_mines", level=1, moved=False),
    Upgraded("Miner", 255, "img\\miner.png", [0, 0], [3, 8, 2],
        [Resource(0, 0, 0, 0, 0, 0, 0, 0)] + [
            Resource(0, 0, 0, 0, 0, 0, 250 * 2**n, 0) for n in range(1, 50)
        ], [], window_func="miner_show", idle_func="idle_resources", level=1, moved=False)
]


def store_screen():
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

    try:
        exec(next_screen[0:-7] + "_screen()")
    except:
        exit(0)


if __name__ == "__main__":
    holding = Resource(0, 0, 0, 0, 0, 0, 10**10, 90)
    resources_time = [time.time(), time.time(), time.time(), time.time(), time.time(), time.time()]
    unlock_parts = [False for _ in range(47)]
    unlock_parts[0] = True
    unlock_parts[11] = True
    unlock_parts[22] = True
    unlock_parts[33] = True
    selected = [0, 11, 22, 33]
    start_time = time.time()
    mine_screen()  # game start

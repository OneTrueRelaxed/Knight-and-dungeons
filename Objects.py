from abc import ABC, abstractmethod
import pygame
import random
import math


def create_sprite(img, sprite_size):
    icon = pygame.image.load(img).convert_alpha()
    icon = pygame.transform.scale(icon, (sprite_size, sprite_size))
    sprite = pygame.Surface((sprite_size, sprite_size), pygame.HWSURFACE)
    sprite.blit(icon, (0, 0))
    return sprite


class Interactive(ABC):

    @abstractmethod
    def interact(self, engine, hero):
        pass


class AbstractObject(ABC):
    @abstractmethod
    def __init__(self):
        pass

    def draw(self, display):
        pass


class Ally(AbstractObject, Interactive):

    def __init__(self, icon, action, position, sound):
        self.sprite = icon
        self.action = action
        self.position = position
        self.sound = sound

    def interact(self, engine, hero):
        if self.sound is not None:
            pygame.mixer.music.load(self.sound)
            pygame.mixer.Channel(1).play(pygame.mixer.Sound(self.sound))
        self.action(engine, hero)


class Creature(AbstractObject):

    def __init__(self, icon, stats, position):
        self.sprite = icon
        self.stats = stats
        self.position = position
        self.calc_max_HP()
        self.hp = self.max_hp

    def calc_max_HP(self):
        self.max_hp = 5 + self.stats["endurance"] * 2


class Enemy(Creature, Interactive):

    def __init__(self, name, icon, stats, xp, position, sound):
        self.name = name
        self.sprite = icon
        self.stats = stats
        self.xp = xp
        self.position = position
        self.sound = sound


    def interact(self, engine, hero):
        hero.hp -= int(self.stats["strength"] * 1.5)
        chance = random.randint(1, 31)
        if self.stats["luck"] >= chance:
            hero.hp -= math.ceil(self.stats["agility"] * random.uniform(0.25, 0.75))
            engine.notify("crit was taken!")
        if hero.hp <= 0:
            hero.hp = 0
            engine.lost = True
        else:
            hero.exp += self.xp
            hero.level_up(engine)
            engine.notify(f"{self.name} is killed!")
            if self.sound is not None:
                pygame.mixer.music.load(self.sound)
                pygame.mixer.Channel(1).play(pygame.mixer.Sound(self.sound))


class Hero(Creature):

    def __init__(self, stats, icon):
        pos = [1, 1]
        self.level = 2
        self.exp = 0
        self.gold = 0
        super().__init__(icon, stats, pos)

    def level_up(self, engine):
        while self.exp >= 100 * (2 ** (self.level - 1)):
            self.level += 1
            engine.notify(f"level {self.level} reached!")
            self.stats["strength"] += 2
            self.stats["endurance"] += 2
            self.calc_max_HP()
            self.hp = self.max_hp


    def draw(self, display, map, sprite_size):
        if self.position[0] <= 6:
            x = self.position[0] * sprite_size
        elif self.position[0] > len(map[0]) - 6:
            x = self.position[0] % 10 * sprite_size
        else:
            x = 6 * sprite_size

        if self.position[1] <= 4:
            y = self.position[1] * sprite_size
        elif self.position[1] > len(map) - 4:
            y = (self.position[1] % 8 - 1) * sprite_size
        else:
            y = 4 * sprite_size

        position = (x, y)
        display.blit(self.sprite, position)


class Effect(Hero):

    def __init__(self, base):
        self.base = base
        self.stats = self.base.stats.copy()
        self.apply_effect()

    @property
    def position(self):
        return self.base.position

    @position.setter
    def position(self, value):
        self.base.position = value

    @property
    def level(self):
        return self.base.level

    @level.setter
    def level(self, value):
        self.base.level = value

    @property
    def gold(self):
        return self.base.gold

    @gold.setter
    def gold(self, value):
        self.base.gold = value

    @property
    def hp(self):
        return self.base.hp

    @hp.setter
    def hp(self, value):
        self.base.hp = value

    @property
    def max_hp(self):
        return self.base.max_hp

    @max_hp.setter
    def max_hp(self, value):
        self.base.max_hp = value

    @property
    def exp(self):
        return self.base.exp

    @exp.setter
    def exp(self, value):
        self.base.exp = value

    @property
    def sprite(self):
        return self.base.sprite

    @abstractmethod
    def apply_effect(self):
        pass


#FIXME?
class Berserk(Effect):

    def apply_effect(self):
        self.hp += 10
        self.stats["strength"] += 7
        self.stats["endurance"] += 7
        self.stats["agility"] += 7
        self.stats["luck"] += 7
        self.stats["perception"] -= 3
        self.stats["charisma"] -= 3
        self.stats["intelligence"] -= 3


#FIXME?
class Blessing(Effect):

    def apply_effect(self):
        self.stats["strength"] += 2
        self.stats["endurance"] += 2
        self.stats["agility"] += 2
        self.stats["luck"] += 2
        self.stats["perception"] += 2
        self.stats["charisma"] += 2
        self.stats["intelligence"] += 2


#FIXME?
class Weakness(Effect):
    
    def apply_effect(self):
        self.stats["strength"] -= 4
        self.stats["endurance"] -= 4
        self.stats["agility"] -= 4    
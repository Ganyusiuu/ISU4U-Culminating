import pygame, os

pygame.init()
pygame.mixer.init()


class Player(pygame.sprite.Sprite):
    def __init__(self, screen, name, position):

        pygame.sprite.Sprite.__init__(self)

        # Sound effects
        self.__ironFist = pygame.mixer.Sound("FDIF.mp3")
        self.__roar = pygame.mixer.Sound("FDR.mp3")
        self.__iceHammer = pygame.mixer.Sound("IMH.mp3")
        self.__iceGeyser = pygame.mixer.Sound("IMG.mp3")

        # Attributes
        self.__name = name
        self.__playerPos = position
        self.__screen = screen
        self.__dx = 0
        self.__kO = False
        self.__block = False
        self.__oldDX = None
        self.__state_locked = False
        self.__health = 100
        self.__moving = False
        self.__state_list = ["righthook", "lefthook", "uppercut", "special", "block", "laydown"]
        self.__state = "stance"
        self.__image_index = 1

        # Gravity attributes
        self.__gravity = 1
        self.__jumpAcc = 15
        self.__ground = 377
        self.__on_ground = True
        self.__dy = 0

        # Setting pathways for images and animations
        # desktop pathways
        self.__desk_path = os.path.join(os.path.expanduser("~"),"OneDrive", "Desktop")
        if not os.path.exists(self.__desk_path):
            self.__desk_path = os.path.join(os.path.expanduser("~"), "Desktop")

        self.__base_path = os.path.join(self.__desk_path, "ISU4U Culminating", self.__name)

        self.__image_file = f"{self.__state}{int(self.__image_index)}.png"
        self.__image_path = os.path.join(self.__base_path, self.__state, self.__image_file)
        self.__index_path = os.path.join(self.__desk_path, "ISU4U Culminating", self.__name, self.__state)
        self.image = pygame.image.load(self.__image_path)

        # colour keys and animation frames (lens(os.listdir(self.__index_path) did not work well)
        if self.__name == "Natsu Dragneel":
            self.image.set_colorkey((0, 128, 0, 255))
            self.__animation_frames = {
            "walk" : 6,
            "uppercut" : 4,
            "righthook" : 4,
            "lefthook" : 3,
            "stance" : 4,
            "special" : 10,
            "jump" : 1,
            "laydown" : 1,
            "block" : 1
            }

        elif self.__name == "Gray Fullbuster":
            self.image.set_colorkey((0, 150, 0, 255))
            self.__animation_frames = {
            "walk" : 6,
            "uppercut" : 5,
            "righthook" : 4,
            "lefthook" : 4,
            "stance" : 4,
            "special" : 6,
            "jump" : 1,
            "laydown" : 1,
            "block" : 1
            }
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.__playerPos

    def attack(self, atkNum):

        if atkNum == 1:
            self.__state = "righthook"
        elif atkNum == 2:
            self.__state = "lefthook"
        elif atkNum == 3:
            self.__state = "uppercut"

        print("attacked by %s" % self.__name)

    def specialATK(self):
        if self.__name == "Gray Fullbuster":
            self.__iceHammer.play()

        elif self.__name == "Natsu Dragneel":
            self.__ironFist.play()

        self.__state = "special"

        print("Special attack by %s!" % self.__name)

    def ultATK(self):
        if self.__name == "Gray Fullbuster":
            self.__iceGeyser.play()

        elif self.__name == "Natsu Dragneel":
            self.__roar.play()
        print("Ultimate attack by %s!" % self.__name)

    def takeDMG(self, dmg):
        self.__health -= dmg
        print(self.__name, self.__health)

    def getHealth(self):
        return self.__health

    def change_xdirection(self, xy_change):
        if self.__on_ground and not self.__block:
            self.__state = "walk"
        self.__dx = xy_change[0]
        self.__moving = True

    def getDX(self):
        return self.__dx

    def block(self, blockStatus):
        self.__block = blockStatus
        self.__dy, self.__dx = 0,0
        print(self.__block)

    def jump(self):
        if self.__on_ground:
            self.__dy -= self.__jumpAcc
            self.__state = "jump"
            self.__on_ground = False

    def kO(self):
        if self.__health <= 0:
            self.__kO = True
        return self.__kO

    def update(self):

        self.__index_path = os.path.join(self.__desk_path, "ISU4U Culminating", self.__name, self.__state)

        #DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE
        if self.__state == "stance":
            if self.__image_index > 4:
                self.__image_index = 1

        # hold old variables/attributes
        self.__oldDX = self.__dx
        self.__last_state = self.__state

        #Cycle through images
        self.__image_index += 0.3 #Add in increments to make it slower, use int()
        if self.__image_index >= len(os.listdir(self.__index_path)):
            self.__image_index = 1

        # Check for wall collisions
        if ((self.rect.left > 0) and (self.__dx < 0)) or (
            (self.rect.right < self.__screen.get_width()) and (self.__dx > 0)
        ):
            self.rect.centerx += self.__dx * 10

        # Add back gravity to bring character down (parabola)
        self.__dy += self.__gravity
        self.rect.centery += self.__dy

        # Ground collision
        if self.rect.bottom >= self.__ground:
            self.rect.bottom = self.__ground
            self.__dy = 0
            self.__on_ground = True

        if self.__on_ground:
            if not self.__moving and self.__last_state == "jump":
                self.__state = "stance"

            if self.__moving and self.__state not in self.__state_list:
                self.__state = "walk"

        if self.__dx == 0 and self.__state not in self.__state_list and self.__state != "jump":
            self.__moving = False
            self.__state = "stance"

        # Resetting everything to display
        self.__oldX, self.__oldY = self.rect.midbottom

        self.__image_file = f"{self.__state}{int(self.__image_index)}.png"
        self.__image_path = os.path.join(self.__base_path, self.__state, self.__image_file)

        self.image = pygame.image.load(self.__image_path)
        if self.__name == "Natsu Dragneel":
            self.image.set_colorkey((0, 128, 0, 255))
        elif self.__name == "Gray Fullbuster":
            self.image.set_colorkey((0, 150, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.midbottom = (self.__oldX, self.__oldY)

        # Check for a kO
        if self.__kO == True:
            self.__dx, self.__dy = 0,0
            self.__state = "laydown"

        # check for blocking
        if self.__block != False:
            self.__state = "block"

class Healthbar(pygame.sprite.Sprite):
    def __init__(self, player):

        pygame.sprite.Sprite.__init__(self)

        self.__player = player

        self.image = pygame.Surface((75, 20), pygame.SRCALPHA)

        self.image.fill((0, 0, 0, 0))

        self.rect = self.image.get_rect()

    def update(self):
        self.rect.midbottom = self.__player.rect.midtop

        # self.image.fill((0,0,0,0))

        self.__healthRatio = self.__player.getHealth() / 100

        pygame.draw.rect(self.image, (255, 0, 0), ((0, 0), (75, 10)), width=0)
        pygame.draw.rect(self.image, (0, 255, 0), ((0, 0), (int(75 * self.__healthRatio), 10)), width=0)


class Label(pygame.sprite.Sprite):
    def __init__(self, font, colour, size, x_y_center):
        pygame.sprite.Sprite.__init__(self)
        self.__font = pygame.font.Font(font, size)
        self.__text = ""
        self.__colour = colour
        self.__center = x_y_center

    def set_text(self, message):
        self.__text = message

    def update(self):
        self.image = self.__font.render(self.__text, 1, (self.__colour))
        self.rect = self.image.get_rect()
        self.rect.center = self.__center


class SpecialLabel(pygame.sprite.Sprite):
    def __init__(self, player, colour, size, amount):

        pygame.sprite.Sprite.__init__(self)

        self.__player = player
        self.__font = pygame.font.SysFont("Arial", size)
        self.__text = ""
        self.__colour = colour
        self.__error = amount

    def set_text(self, message):
        self.__text = message

    def update(self):
        self.image = self.__font.render(self.__text, 1, self.__colour)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.__player.rect.centerx
        self.rect.centery = self.__player.rect.centery - self.__error


class Startbuttons(pygame.sprite.Sprite):
    def __init__(self, x_y_center):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("r3.png")
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect()
        self.rect.center = x_y_center

    def ready(self):
        self.image = pygame.image.load("r3Ready.png")
        self.image = pygame.transform.scale(self.image, (70, 70))

    def notReady(self):
        self.image = pygame.image.load("r3.png")
        self.image = pygame.transform.scale(self.image, (70, 70))

    def update(self):
        pass

class HammerBox(pygame.sprite.Sprite):

    def __init__(self, gray):
        pygame.sprite.Sprite.__init__(self)

        self.__gray = gray
        self.__image_index = 1
        self.__animate = False

        self.__desk_path = os.path.join(os.path.expanduser("~"),"OneDrive", "Desktop")
        if not os.path.exists(self.__desk_path):
            self.__desk_path = os.path.join(os.path.expanduser("~"), "Desktop")

        self.__base_path = os.path.join(self.__desk_path, "ISU4U Culminating", "Gray Fullbuster", "hammer")

        self.__image_file = f"hammer{int(self.__image_index)}.png"
        self.__image_path = os.path.join(self.__base_path, self.__image_file)
        self.image = pygame.image.load(self.__image_path)
        self.rect = self.image.get_rect()
        self.rect.right = self.__gray.rect.left

    def animate(self):
        self.__animate = True

    def update(self):

        if self.__animate == True:
            self.__image_index += 0.2
            if self.__image_index >= 6:
                self.__image_index = 1
                self.__animate = False

        self.__image_file = f"hammer{int(self.__image_index)}.png"
        self.__image_path = os.path.join(self.__base_path, self.__image_file)
        self.image = pygame.image.load(self.__image_path)
        self.image.set_colorkey((0, 150, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.centerx = self.__gray.rect.centerx - 100
        self.rect.centery = self.__gray.rect.centery


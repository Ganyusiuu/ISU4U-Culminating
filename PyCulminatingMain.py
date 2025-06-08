# I - Import and Initialize
import pygame, PyCulmSprites, stopwatch

pygame.init()
pygame.mixer.init()

def main():

    # Display
    pygame.display.set_caption("Super Smash FairyTail!")
    screen = pygame.display.set_mode((800, 450))
    # Entities
    gamebackground = pygame.image.load("bg2.jpg")
    gamebackground = pygame.transform.scale(gamebackground, screen.get_size())

    startbackground = pygame.image.load("opening2.jpg")
    startbackground = pygame.transform.scale(startbackground, screen.get_size())

    joysticks = []

    for joystick_no in range(pygame.joystick.get_count()):
        stick = pygame.joystick.Joystick(joystick_no)
        stick.init()
        joysticks.append(stick)

    natsu = PyCulmSprites.Player(screen, "Natsu Dragneel", (150,377))
    gray = PyCulmSprites.Player(screen, "Gray Fullbuster", (650,377))
    natsuHealth = PyCulmSprites.Healthbar(natsu)
    grayHealth = PyCulmSprites.Healthbar(gray)
    natsuSpecialLabel = PyCulmSprites.SpecialLabel(natsu, "black", 20, 85)
    graySpecialLabel = PyCulmSprites.SpecialLabel(gray, "black", 20, 85)
    natsuULTLabel = PyCulmSprites.SpecialLabel(natsu, "red", 20, 110)
    grayULTLabel = PyCulmSprites.SpecialLabel(gray, "blue", 20, 110)
    winLabel = PyCulmSprites.Label("clearbold.ttf", "blue", 30, ((screen.get_width()//2),150))

    allSprites = pygame.sprite.Group(natsu, gray, natsuHealth, grayHealth, natsuSpecialLabel, graySpecialLabel, natsuULTLabel, grayULTLabel, winLabel)

    startLabel = PyCulmSprites.Label("clearbold.ttf", "blue", 30, ((screen.get_width()//2),350))
    natsuReady = PyCulmSprites.Startbuttons((100,350))
    grayReady = PyCulmSprites.Startbuttons((700,350))

    startSprites = pygame.sprite.Group(startLabel, natsuReady, grayReady)

    #hammerbox = PyCulmSprites.HammerBox(gray)

    #hitboxsprites = pygame.sprite.Group(hammerbox)

    natsuSpecialWatch = stopwatch.Stopwatch(1)
    graySpecialWatch = stopwatch.Stopwatch(1)
    natsuSpecialWatch.stop()
    graySpecialWatch.stop()

    natsuChargeWatch = stopwatch.Stopwatch(1)
    grayChargeWatch = stopwatch.Stopwatch(1)
    natsuChargeWatch.stop()
    grayChargeWatch.stop()

    # ACTION
    # Assign
    keepGoing = False
    clock = pygame.time.Clock()
    natsublock = False
    grayblock = False
    start1 = False
    start2 = False
    starting = False
    start_music = True
    natsuSpecial = False
    graySpecial = False
    natsuCharged = False
    grayCharged = False

    trackNatsuAtk = 1
    trackGrayAtk = 1

    while not starting:

        if start_music:
            pygame.mixer.music.load("start.mp3")
            pygame.mixer.music.play(-1)
            start_music = False

        clock.tick(30)

        startLabel.set_text("Press R3 to start")

        # Events
        for event in pygame.event.get():

            if event.type == pygame.JOYBUTTONDOWN:
                if event.joy == 0:
                    if event.button == 9:
                        natsuReady.ready()
                        start1 = True

                if event.joy == 1:
                    if event.button == 9:
                        grayReady.ready()
                        start2 = True

            if event.type == pygame.JOYBUTTONUP:
                if event.joy == 0:
                    if event.button == 9:
                        natsuReady.notReady()
                        start1 = False

                if event.joy == 1:
                    if event.button == 9:
                        grayReady.notReady()
                        start2 = False

        if start1 == True and start2 == True:
            pygame.mixer.music.fadeout(500)
            pygame.mixer.music.load("bgm.mp3")
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.2)
            starting, keepGoing = True, True

        screen.blit(startbackground, (0, 0))
        startSprites.clear(screen, startbackground)
        startSprites.update()
        startSprites.draw(screen)
        pygame.display.flip()

    # Loop
    while keepGoing:

        # Time
        clock.tick(30)
        natsuSpecialWatch.start()
        graySpecialWatch.start()

        if natsuSpecialWatch.duration >= 10.0:
            natsuSpecial = True
            natsuSpecialLabel.set_text("Special ATK!")

        if graySpecialWatch.duration >= 10.0:
            graySpecial = True
            graySpecialLabel.set_text("Special ATK!")

        if natsuChargeWatch.duration >= 15.0:
            natsuCharged = True
            natsuULTLabel.set_text("Ultimate Attack!")

        if grayChargeWatch.duration >= 15.0:
            grayCharged = True
            grayULTLabel.set_text("Ultimate Attack!")

        if natsu.kO():
            #natsu.laydown()
            natsuSpecialLabel.set_text("")
            natsuULTLabel.set_text("")
            winLabel.set_text("Gray Wins!")

        if gray.kO():
            #gray.laydown()
            graySpecialLabel.set_text("")
            grayULTLabel.set_text("")
            winLabel.set_text("Natsu Wins!")

        if trackNatsuAtk > 3:
            trackNatsuAtk = 1

        if trackGrayAtk > 3:
            trackGrayAtk = 1

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False

            if event.type == pygame.JOYBUTTONDOWN:

                if event.joy == 0 and not natsu.kO():

                    if event.button == 2:
                        natsublock = True
                        natsu.block(True)

                    if natsu.rect.colliderect(gray.rect) and event.button == 1 and not grayblock and not natsublock:
                        natsu.attack(trackNatsuAtk)
                        gray.takeDMG(1)
                        trackNatsuAtk +=1

                    if natsu.rect.colliderect(gray.rect) and event.button == 5 and not natsublock and natsuSpecial:
                        natsu.specialATK()
                        gray.takeDMG(10)
                        natsuSpecialLabel.set_text("")
                        natsuSpecial = False
                        natsuSpecialWatch.restart()

                    if event.button == 0:
                        natsu.jump()

                    if event.button == 3:
                        natsuChargeWatch.start()

                    if natsu.rect.colliderect(gray.rect) and event.button == 4 and natsuCharged and not natsublock:
                        natsu.ultATK()
                        gray.takeDMG(25)
                        natsuULTLabel.set_text("")
                        natsuCharged = False
                        natsuChargeWatch.reset()

                if event.joy == 1 and not gray.kO():

                    if event.button == 2:
                        grayblock = True
                        gray.block(True)

                    if gray.rect.colliderect(natsu.rect) and event.button == 1 and not natsublock and not grayblock:
                        gray.attack(trackGrayAtk)
                        natsu.takeDMG(1)
                        trackGrayAtk +=1

                    if gray.rect.colliderect(natsu.rect) and event.button == 5 and not grayblock and graySpecial:
                        gray.specialATK()
                        #hammerbox.animate()
                        natsu.takeDMG(10)
                        graySpecialLabel.set_text("")
                        graySpecial = False
                        graySpecialWatch.restart()

                    if event.button == 3:
                        grayChargeWatch.start()

                    if gray.rect.colliderect(natsu.rect) and event.button == 4 and grayCharged and not grayblock:
                        gray.ultATK()
                        natsu.takeDMG(25)
                        grayULTLabel.set_text("")
                        grayCharged = False
                        grayChargeWatch.reset()

                    if event.button == 0:
                        gray.jump()

            if event.type == pygame.JOYBUTTONUP:

                if event.joy == 0 and not natsu.kO():
                    if event.button == 2:
                        natsublock = False
                        natsu.block(False)

                    if event.button == 3:
                        natsuChargeWatch.stop()

                if event.joy == 1 and not gray.kO():
                    if event.button == 2:
                        grayblock = False
                        gray.block(False)

                    if event.button == 3:
                        grayChargeWatch.stop()


            if event.type == pygame.JOYHATMOTION:
                if event.joy == 0 and not natsu.kO() and not natsublock:
                    natsu.change_xdirection(event.value)

                if event.joy == 1 and not gray.kO() and not grayblock:
                    gray.change_xdirection(event.value)

        # Refresh screen
        screen.blit(gamebackground, (0, 0))
        allSprites.clear(screen, gamebackground)
        allSprites.update()
        allSprites.draw(screen)
        #hitboxsprites.clear(screen, gamebackground)
        #hitboxsprites.update()
        #hitboxsprites.draw(screen)
        pygame.display.flip()

# Call the main function
main()

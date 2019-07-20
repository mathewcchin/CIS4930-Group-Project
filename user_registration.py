import pygame, sys, os
from setting import Settings

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.init()
spriteGroup = pygame.sprite.OrderedUpdates()
textboxGroup = pygame.sprite.OrderedUpdates()
screenRefresh = True
background = None



class Background():
    def __init__(self):
        self.color = pygame.Color("black")

    def setTiles(self, tiles):
        if type(tiles) is str:
            self.tiles = [[loadImage(tiles)]]
        elif type(tiles[0]) is str:
            self.tiles = [[loadImage(i) for i in tiles]]
        else:
            self.tiles = [[loadImage(i) for i in row] for row in tiles]
        self.stagePosX = 0
        self.stagePosY = 0
        self.tileWidth = self.tiles[0][0].get_width()
        self.tileHeight = self.tiles[0][0].get_height()
        screen.blit(self.tiles[0][0], [0, 0])
        self.surface = screen.copy()

    def setColor(self, color):
        self.color = parseColor(color)
        screen.fill(self.color)
        pygame.display.update()
        self.surface = screen.copy()


class newTextBox(pygame.sprite.Sprite):
    def __init__(self, text, xpos, ypos, width, case, maxLength, fontSize):
        pygame.sprite.Sprite.__init__(self)
        self.text = ""
        self.width = width
        self.initialText = text
        self.case = case
        self.maxLength = maxLength
        self.boxSize = int(fontSize * 1.7)
        self.image = pygame.Surface((width, self.boxSize))
        self.image.fill((255, 255, 255))
        pygame.draw.rect(self.image, (0, 0, 0), [0, 0, width - 1, self.boxSize - 1], 2)
        self.rect = self.image.get_rect()
        self.fontFace = pygame.font.match_font("Arial")
        self.fontColor = pygame.Color("black")
        self.initialColor = (180, 180, 180)
        self.font = pygame.font.Font(self.fontFace, fontSize)
        self.rect.topleft = [xpos, ypos]
        newSurface = self.font.render(self.initialText, True, self.initialColor)
        self.image.blit(newSurface, [10, 5])

    def update(self, keyevent):
        key = keyevent.key
        unicode = keyevent.unicode
        if key > 31 and key < 127 and (
                self.maxLength == 0 or len(self.text) < self.maxLength):  # only printable characters
            if keyevent.mod in (1, 2) and self.case == 1 and key >= 97 and key <= 122:
                # force lowercase letters
                self.text += chr(key)
            elif keyevent.mod == 0 and self.case == 2 and key >= 97 and key <= 122:
                self.text += chr(key - 32)
            else:
                # use the unicode char
                self.text += unicode

        elif key == 8:
            # backspace. repeat until clear
            keys = pygame.key.get_pressed()
            nexttime = pygame.time.get_ticks() + 200
            deleting = True
            while deleting:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_BACKSPACE]:
                    thistime = pygame.time.get_ticks()
                    if thistime > nexttime:
                        self.text = self.text[0:len(self.text) - 1]
                        self.image.fill((255, 255, 255))
                        pygame.draw.rect(self.image, (0, 0, 0), [0, 0, self.width - 1, self.boxSize - 1], 2)
                        newSurface = self.font.render(self.text, True, self.fontColor)
                        self.image.blit(newSurface, [10, 5])
                        updateDisplay()
                        nexttime = thistime + 50
                        pygame.event.clear()
                else:
                    deleting = False

        self.image.fill((255, 255, 255))
        pygame.draw.rect(self.image, (0, 0, 0), [0, 0, self.width - 1, self.boxSize - 1], 2)
        newSurface = self.font.render(self.text, True, self.fontColor)
        self.image.blit(newSurface, [10, 5])
        if screenRefresh:
            updateDisplay()


    def clear(self):
        self.image.fill((255, 255, 255))
        pygame.draw.rect(self.image, (0, 0, 0), [0, 0, self.width - 1, self.boxSize - 1], 2)
        newSurface = self.font.render(self.initialText, True, self.initialColor)
        self.image.blit(newSurface, [10, 5])
        if screenRefresh:
            updateDisplay()


class newLabel(pygame.sprite.Sprite):
    def __init__(self, text, fontSize, font, fontColor, xpos, ypos, background):
        pygame.sprite.Sprite.__init__(self)
        self.text = text
        self.fontColor = parseColor(fontColor)
        self.fontSize = fontSize
        self.background = background
        self.font = pygame.font.Font("img/INVASION2000.TTF", self.fontSize)
        self.renderText()
        self.rect.topleft = [xpos, ypos]

    def update(self, newText, fontColor, background):
        self.text = newText
        if fontColor:
            self.fontColor = parseColor(fontColor)
        if background:
            self.background = parseColor(background)

        oldTopLeft = self.rect.topleft
        self.renderText()
        self.rect.topleft = oldTopLeft
        if screenRefresh:
            updateDisplay()

    def renderText(self):
        lineSurfaces = []
        textLines = self.text.split("<br>")
        maxWidth = 0
        maxHeight = 0
        for line in textLines:
            lineSurfaces.append(self.font.render(line, True, self.fontColor))
            thisRect = lineSurfaces[-1].get_rect()
            if thisRect.width > maxWidth:
                maxWidth = thisRect.width
            if thisRect.height > maxHeight:
                maxHeight = thisRect.height
        self.image = pygame.Surface((maxWidth, (self.fontSize + 1) * len(textLines) + 5), pygame.SRCALPHA, 32)
        self.image.convert_alpha()
        if self.background != "clear":
            self.image.fill(parseColor(self.background))
        linePos = 0
        for lineSurface in lineSurfaces:
            self.image.blit(lineSurface, [0, linePos])
            linePos += self.fontSize + 1
        self.rect = self.image.get_rect()


def loadImage(fileName, useColorKey=False):
    if os.path.isfile(fileName):
        image = pygame.image.load(fileName)
        image = image.convert_alpha()
        # Return the image
        return image
    else:
        raise Exception("Error loading image: " + fileName + " - Check filename and path?")


def loadImage(fileName, useColorKey=False):
    if os.path.isfile(fileName):
        image = pygame.image.load(fileName)
        image = image.convert_alpha()
        # Return the image
        return image
    else:
        raise Exception("Error loading image: " + fileName + " - Check filename and path?")


def screenSize(sizex, sizey, xpos=None, ypos=None, fullscreen=False):
    global screen
    global background
    if xpos != None and ypos != None:
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" % (xpos, ypos + 50)
    else:
        windowInfo = pygame.display.Info()
        monitorWidth = windowInfo.current_w
        monitorHeight = windowInfo.current_h
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" % ((monitorWidth - sizex) / 2, (monitorHeight - sizey) / 2)
    if fullscreen:
        screen = pygame.display.set_mode([sizex, sizey], pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode([sizex, sizey])
        ###########set background to image here####################
    background = Background()
    screen.fill(background.color)
    #pygame.display.set_caption("Graphics Window")
    background.surface = screen.copy()
    pygame.display.update()
    return screen


def setBackgroundColor(color):
    background.setColor(color)
    if screenRefresh:
        updateDisplay()


def setBackgroundImage(img):
    global background
    background.setTiles(img)
    if screenRefresh:
        updateDisplay()


def keyPressed(keyCheck=""):
    global keydict
    pygame.event.clear()
    keys = pygame.key.get_pressed()
    if sum(keys) > 0:
        if keyCheck == "" or keys[keydict[keyCheck.lower()]]:
            return True
    return False

def makeLabel(text, fontSize, xpos, ypos, fontColor, font, background="clear"):
    # make a text sprite
    thisText = newLabel(text, fontSize, font, fontColor, xpos, ypos, background)
    return thisText


def makeTextBox(xpos, ypos, width, case=0, startingText="Please type here", maxLength=0, fontSize=22):
    thisTextBox = newTextBox(startingText, xpos, ypos, width, case, maxLength, fontSize)
    textboxGroup.add(thisTextBox)
    return thisTextBox



def textBoxInput(textbox, functionToCall=None, args=[]):
    # starts grabbing key inputs, putting into textbox until enter pressed

    textbox.text = ""
    returnVal = None

    while True:
        updateDisplay()
        #if functionToCall:
         #   returnVal = functionToCall(*args)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if returnVal:
                        return textbox.text #,  returnVal
                    else:
                        return textbox.text
                elif event.key == pygame.K_BACKSPACE:
                    textbox.clear()

                else:
                    textbox.update(event)
            elif event.type == pygame.QUIT:
                sys.exit()


def showLabel(labelName):
    textboxGroup.add(labelName)
    if screenRefresh:
        updateDisplay()


def showTextBox(textBoxName):
    textboxGroup.add(textBoxName)
    if screenRefresh:
        updateDisplay()


def updateDisplay():
    global background
    spriteRects = spriteGroup.draw(screen)
    textboxRects = textboxGroup.draw(screen)
    pygame.display.update()
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_ESCAPE]):
        pygame.quit()
        sys.exit()
    spriteGroup.clear(screen, background.surface)
    textboxGroup.clear(screen, background.surface)


def parseColor(color):
    if type(color) == str:
        # check to see if valid color
        return pygame.Color(color)
    else:
        colorRGB = pygame.Color("white")
        colorRGB.r = color[0]
        colorRGB.g = color[1]
        colorRGB.b = color[2]
        return colorRGB




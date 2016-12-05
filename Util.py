import pygame,sys
from pygame.locals import *
#carga las imagenes al programa
def imagen(filename, transparent=False,expandir=False):
        try: image = pygame.image.load(filename)
        except pygame.error, message:
                raise SystemExit, message
        image = image.convert()
        if transparent:
                color = image.get_at((0,0))
                image.set_colorkey(color, RLEACCEL)

        if expandir:
            image=pygame.transform.scale2x(image)

        return image
#crea un objeto que puede mostrarse por la pantalla, en este caso son palabras o numeros
def text_objects(text, font,color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()
#despliega la palabras creadas por text_objects
def text(screen,txt,color,posX,posY,size):
    largeText = pygame.font.Font('happytreefriends.ttf', size)
    TextSurf, TextRect =text_objects(txt, largeText,color)
    TextRect.center = (posX, posY)
    screen.blit(TextSurf, TextRect)
def musica():
    pygame.mixer.music.load("music/Happy tree friends 8-bit remix.mp3")
    #pygame.mixer.music.play(-1, 0.0)
    return


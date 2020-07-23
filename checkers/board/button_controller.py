import pygame

class ButtonController:
    buttons = []
    pressed = []

    @staticmethod
    def addButton(button):
        ButtonController.buttons.append(button)

    @staticmethod
    def updatePressed():
        ButtonController.pressed = []
        for event in pygame.event.get():
            if event.type != pygame.MOUSEBUTTONDOWN:
                continue
            if event.button != 1:
                continue
            for button in ButtonController.buttons:
                if button.contains(event.pos):
                    ButtonController.pressed.append(button)

    @staticmethod
    def getPressed():
        return ButtonController.pressed
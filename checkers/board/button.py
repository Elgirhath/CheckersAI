from checkers.board.button_controller import ButtonController

class Button():
    def __init__(self, position, size):
        self.position = position
        self.size = size
        self.isPressed = False

        ButtonController.addButton(self)

    def contains(self, pos):
        if pos[0] < self.position[0] or pos[0] > self.position[0] + self.size[0]:
            return False
        elif pos[1] < self.position[1] or pos[1] > self.position[1] + self.size[1]:
            return False
        else:
            return True
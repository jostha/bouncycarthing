import arcade
import array as arr
from random import seed
from random import randint

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Car:
    def __init__(self, xpos, ypos, changex, changey, ybump):
        
        self.xpos  = xpos
        self.ypos  = ypos
        self.ybump = ybump
        self.changex = changex
        self.changey = changey

    def draw(self):
        arcade.draw_rectangle_filled(60 + self.xpos, 50 + self.ypos + self.ybump, 60, 60, arcade.color.ORANGE)
        arcade.draw_rectangle_filled(60 + self.xpos, 35 + self.ypos + self.ybump, 120, 30, arcade.color.ORANGE)
        arcade.draw_circle_filled(18 + self.xpos, 20 + self.ypos, 11, arcade.color.BLACK)
        arcade.draw_circle_filled(100 + self.xpos, 20 + self.ypos, 11, arcade.color.BLACK)

    def update(self):
        if self.ypos == (SCREEN_HEIGHT/6) - 4:
            self.ypos += -1
        elif self.ypos == -7:
            self.ypos += 1
        else:
            self.ypos += self.changey
        self.xpos += self.changex
        if self.xpos == 2:
            self.xpos = 3


class Tree:
    def __init__(self, xpos, scale, changex):
        
        self.y = 360
        self.xpos = xpos
        self.scale = scale
        self.changex = changex
        
    def draw(self):
        arcade.draw_triangle_filled(self.xpos + (self.scale * 4), self.y,
                                    self.xpos, self.y - (self.scale * 10),
                                    self.xpos + (self.scale * 8), self.y - (self.scale * 10),
                                    arcade.color.DARK_GREEN)
        arcade.draw_lrtb_rectangle_filled(self.xpos + (self.scale * 3), self.xpos + (self.scale * 5), self.y - (self.scale * 10), self.y - (self.scale * 14),
                                          arcade.color.DARK_BROWN)

    def update(self):
#        print (self.xpos)
        if self.xpos < -100 and self.changex < 0:
            self.xpos = SCREEN_WIDTH + 50 + randint(0,100)
        elif self.xpos > (SCREEN_WIDTH + 100) and self.changex > 0:
            self.xpos = -50 - randint(0,100)
        else:
            self.xpos += self.changex


class MyGame(arcade.Window):

    def __init__(self, width, height):
        super().__init__(width, height)

        arcade.set_background_color(arcade.color.BABY_BLUE)

    def setup(self):
        self.car = Car(10, 10, 0, 0, 0)
        self.carYtimer = 0                  # For the chug up and down
        self.accel = 1

        self.treeListc = []
        self.treeListb = []
        self.treeLista = []                 # Closest Row
        for i in range (5):
            self.treeListc.append(Tree(randint(0, SCREEN_WIDTH), 5, 0))
            self.treeListb.append(Tree(randint(0, SCREEN_WIDTH), 10, 0))
            self.treeLista.append(Tree(randint(0, SCREEN_WIDTH), 16, 0))

    def on_draw(self):
        """ Render the screen """
        arcade.start_render()

        # Draw green gloor
        arcade.draw_lrtb_rectangle_filled(0, SCREEN_WIDTH, SCREEN_HEIGHT/2, 0, arcade.color.DARK_SPRING_GREEN),
        arcade.draw_lrtb_rectangle_filled(0, SCREEN_WIDTH, SCREEN_HEIGHT/6, 0, arcade.color.BATTLESHIP_GREY),

        for i in range(5):
            self.treeListc[i].draw()
        for i in range(5):
            self.treeListb[i].draw()
        for i in range(5):
            self.treeLista[i].draw()        # draw furthest away first, separate loops needed

        self.car.draw()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP:
            self.car.changey += 1
        elif key == arcade.key.DOWN:
            self.car.changey += -1
        elif key == arcade.key.LEFT:
            self.car.changex += -1
            for i in range(5):
                self.treeLista[i].changex += 3
                self.treeListb[i].changex += 2
                self.treeListc[i].changex += 1
            self.accel -= 1
        elif key == arcade.key.RIGHT:
            self.car.changex += 1
            for i in range(5):
                self.treeLista[i].changex -= 3
                self.treeListb[i].changex -= 2
                self.treeListc[i].changex -= 1
            self.accel += 1

    def on_key_release(self, key, modifiers):
        """ Called whenever a user releases a key. """
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.car.changex = 0
        elif key == arcade.key.UP or key == arcade.key.DOWN:
            self.car.changey = 0

    def update(self, delta_time):
        self.carYtimer +=1
        if self.carYtimer > 20:
            self.car.ybump = 5
        if self.carYtimer == 40:
            self.car.ybump = 0
            self.carYtimer = 0

        for i in range(5):
            self.treeListc[i].update()
            self.treeListb[i].update()
            self.treeLista[i].update()

        self.car.update()


def main():
    seed(2)
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()



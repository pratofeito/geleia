"""
Sprite Change Coins

This shows how you can change a sprite once it is hit, rather than eliminate it.

Artwork from https://kenney.nl

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.sprite_change_coins
"""

import random
import arcade
import os

SPRITE_SCALING = 1

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Sprite Change Coins"
DEFAULT_FONT_SIZE = 20
DEFAULT_LINE_HEIGHT = 45


class Memory(arcade.Sprite):
    """ This class represents something the player collects. """

    def __init__(self, filename, scale):
        super().__init__(filename, scale)
        # Flip this once the coin has been collected.
        self.dialogue = False
        self.start_y = 0
        self.start_x = 0
        self.text_list = [None]
        self.text = None
        self.object_list = [self]


    def devaneio(self):
        self.dialogue = True

class MyGame(arcade.Window):
    """
    Main application class.a'
    """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Sprite lists
        self.player_list = None
        self.coin_list = None
        self.bomb_list = None

        # Set up the player
        self.score = 0
        self.player_sprite = None

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.bomb_list = arcade.SpriteList()

        # Set up the player
        self.score = 0
        self.player_sprite = arcade.Sprite(":resources:images/animated_characters/female_person/"
                                           "femalePerson_idle.png", 0.5)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

        # Create the coin instance
        coin = Memory(":resources:images/items/coinGold.png", SPRITE_SCALING)
        coin.width = 30
        coin.height = 30
        coin.object_list = arcade.SpriteList()

        with open('dialogos.txt') as f:
         while True:
            line = f.readline()
            if not line:
                break
            coin.text_list.append(line.strip())

        coin.text = coin.text_list[1]

        coin.center_x = random.randrange(SCREEN_WIDTH)
        coin.center_y = random.randrange(SCREEN_HEIGHT)

        coin.object_list.append(coin)
        self.coin_list = coin.object_list

        # Create the coin instance
        bomb = Memory(":resources:images/items/star.png", SPRITE_SCALING)
        bomb.width = 30
        bomb.height = 30
        bomb.object_list = arcade.SpriteList()

        with open('dialogos.txt') as f:
         while True:
            line = f.readline()
            if not line:
                break
            bomb.text_list.append(line.strip())

        bomb.text = bomb.text_list[2]

        # Position the coin
        bomb.center_x = random.randrange(SCREEN_WIDTH)
        bomb.center_y = random.randrange(SCREEN_HEIGHT)

        bomb.object_list.append(bomb)
        self.bomb_list = bomb.object_list

        # Don't show the mouse cursor
        self.set_mouse_visible(True)

        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        self.clear()

        # Draw all the sprites.
        self.coin_list.draw()
        self.bomb_list.draw()
        self.player_list.draw()

        for coin in self.coin_list:
            if coin.dialogue == True:
              arcade.draw_text(coin.text,
        50,
        50,
        arcade.color.BLACK,
        DEFAULT_FONT_SIZE / 2,
        multiline=True,
        width=300)

        for bomb in self.bomb_list:
            if bomb.dialogue == True:
              arcade.draw_text(bomb.text,
        50,
        50,
        arcade.color.BLACK,
        DEFAULT_FONT_SIZE / 2,
        multiline=True,
        width=300)

        # Put the text on the screen.
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

    def on_mouse_motion(self, x, y, dx, dy):
        """
        Called whenever the mouse moves.
        """
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.player_list.update()
        self.coin_list.update()
        self.bomb_list.update()

        all_lists = arcade.SpriteList()
        all_lists.extend(self.coin_list)
        all_lists.extend(self.bomb_list)
        # Generate a list of all sprites that collided with the player.
        hit_list = arcade.check_for_collision_with_list(self.player_sprite, all_lists)

        # Loop through each colliding sprite, change it, and add to the score.
        for coin in hit_list:
            # Have we collected this?
            if not coin.dialogue:
                # No? Then do so
                coin.append_texture(arcade.load_texture(":resources:images/pinball/bumper.png"))
                coin.set_texture(1)
                coin.devaneio()
                coin.width = 30
                coin.height = 30
                self.score += 1


def main():
    """ Main function """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
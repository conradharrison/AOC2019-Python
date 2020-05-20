import arcade
import os

SCREEN_WIDTH = 100
SCREEN_HEIGHT = 100
CELL_WIDTH = 10
CELL_HEIGHT = 10

DPI = 72
PIXELS_TO_POINTS = (1/72) * DPI

class PaddleGame(arcade.Window):
    def __init__(self, w, h, machine):
        super().__init__(w, h, "Paddle", resizable=True)

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Place holder for 1:1 setting
        self.unit_w = w
        self.unit_h = h
       
        # Machine
        self.machine = machine

        # For game logic
        self.game_over = False
        self.success = False
        self.score = 0
        self.frame_count = 0
        self.ball_speed = 10
        self.hpaddle_x = None
        self.ball_x = None
        self.autoplay = False
        self.show_help = False
        
        # For display
        self.all_sprites = arcade.SpriteList()
        self.all_sprites_by_xy = {}

        self.blank_image = "blank10x10.png"
        self.block_image = "block10x10.png"
        self.wall_image = "wall10x10.png"
        self.hpaddle_image = "hpaddle10x10.png"
        self.ball_image = "ball10x10.png"

        self.score_font_size = int((CELL_HEIGHT-2)*PIXELS_TO_POINTS)
        self.game_over_font_size = 20
        self.success_font_size = 20
        self.help_font_size = 6

        self.score_text = arcade.TextLabel("SCORE:"+str(self.score), 
                0, int(CELL_HEIGHT/2), 
                arcade.color.WHITE, font_name="Courier", font_size=self.score_font_size,
                anchor_x="left", anchor_y="center", bold=True)

        self.game_over_text = arcade.TextLabel("GAME OVER!!! :(", 
                int(self.unit_w/2), int(self.unit_h/2), 
                arcade.color.RED, font_name="Courier", font_size=self.game_over_font_size,
                anchor_x="center", anchor_y="center", bold=True)

        self.success_text = arcade.TextLabel("SUCCESS!!! :)", 
                int(self.unit_w/2), int(self.unit_h/2), 
                arcade.color.GREEN, font_name="Courier", font_size=self.success_font_size,
                anchor_x="center", anchor_y="center", bold=True)

        help = "F1-Toggle Help, A-Toggle Autoplay, Q-Quit, ESC-Restart, Left/Right-Move Paddle, Up/Down-Change Speed"
        self.help_text = arcade.TextLabel(help,
                self.unit_w, int(CELL_HEIGHT/2), 
                arcade.color.WHITE, font_name="Courier", font_size=self.help_font_size,
                anchor_x="right", anchor_y="center", bold=True)

        arcade.set_background_color(arcade.color.BLACK)

    def reset_game(self):
        self.all_sprites = arcade.SpriteList() # Hopefully, ref_count based garbage collection will happen
        self.all_sprites_by_xy = {}
        self.machine.reset()
        self.machine.imem[0] = 2
        self.game_over = False
        self.score = 0
        self.frame_count = 0
        self.ball_speed = 10
        self.hpaddle_x = None
        self.ball_x = None
        self.autoplay = False
        self.show_help = False

        # First call will provide a grid and the first move
        self.step_machine(0)

    def add_sprite(self, x, y, sprite_type):
        if sprite_type == "BLANK":
            s = arcade.Sprite(self.blank_image, 1.0)
        elif sprite_type == "WALL":
            s = arcade.Sprite(self.wall_image, 1.0)
        elif sprite_type == "BLOCK":
            s = arcade.Sprite(self.block_image, 1.0)
        elif sprite_type == "HPADDLE":
            s = arcade.Sprite(self.hpaddle_image, 1.0)
        elif sprite_type == "BALL":
            s = arcade.Sprite(self.ball_image, 1.0)

        s.left = x*CELL_WIDTH
        s.bottom = y*CELL_HEIGHT
        self.all_sprites.append(s)
        self.all_sprites_by_xy[(x,y)] = (s, sprite_type)

    def step_machine(self, i):

        if self.game_over:
            return

        self.machine.inputs = [i]
        self.machine.run(stop_on_output=False, wait_for_input=True)
        #print(self.machine.outputs)
        while self.machine.outputs:
            x = self.machine.outputs.pop(0)
            y = self.machine.outputs.pop(0)
            t = self.machine.outputs.pop(0)
            
            if (x==-1 and y==0):
                #print("Score=", t, self.score)

                # All blocks done
                self.game_over = True
                self.success = True
                for (s, sprite_type) in self.all_sprites_by_xy.values():
                    if sprite_type == "BLOCK":
                        self.game_over = False
                        self.success = False

                if len(self.machine.outputs) == 0:
                    self.game_over = True
                else:
                    self.score = t
                    self.score_text.text = "SCORE:"+str(self.score)
            else:
                y = y + 1 # Leave a row for score
                if (x,y) in self.all_sprites_by_xy:
                    (s, _) = self.all_sprites_by_xy[(x,y)]
                    self.all_sprites.remove(s)
                if t==0:
                    self.add_sprite(x, y, "BLANK")
                elif t==1:
                    self.add_sprite(x, y, "WALL")
                elif t==2:
                    self.add_sprite(x, y, "BLOCK")
                elif t==3:
                    self.add_sprite(x, y, "HPADDLE")
                    self.hpaddle_x = x
                elif t==4:
                    self.add_sprite(x, y, "BALL")
                    self.ball_x = x

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.step_machine(-1)
        if key == arcade.key.RIGHT:
            self.step_machine(1)
        if key == arcade.key.ESCAPE:
            self.reset_game()
        if key == arcade.key.UP:
            self.ball_speed -= 2
            self.ball_speed = max(1, self.ball_speed)
        if key == arcade.key.DOWN:
            self.ball_speed += 2
            self.ball_speed = min(60, self.ball_speed)
        if key == arcade.key.Q:
            self.close()
        if key == arcade.key.A:
            self.autoplay = not self.autoplay
        if key == arcade.key.F1:
            self.show_help = not self.show_help

    def on_update(self, delta_time):
        if self.autoplay:
            self.frame_count += 1
            if self.frame_count % self.ball_speed == 0:
                if self.hpaddle_x!=None and self.ball_x!=None:
                    if (self.hpaddle_x > self.ball_x):
                        self.step_machine(-1)
                    elif (self.hpaddle_x < self.ball_x):
                        self.step_machine(1)
                    else:
                        self.step_machine(0)

    def set_unit_scale(self, w, h):
        self.unit_w = w
        self.unit_h = h

    def on_resize(self, w, h):
        super().on_resize(w, h)
        self.set_viewport(0, self.unit_w, 0, self.unit_h)

    def on_draw(self):
        arcade.start_render()
        self.all_sprites.draw()
        self.score_text.draw()
        if self.show_help:
            self.help_text.draw()
        if self.game_over:
            if self.success:
                self.success_text.draw()
            else:
                self.game_over_text.draw()


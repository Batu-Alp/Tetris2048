
import time
import stddraw # the stddraw module is used as a basic graphics library
import random # used for creating tetrominoes with random types/shapes
from game_grid import GameGrid # class for modeling the game grid
from tetromino import Tetromino # class for modeling the tetrominoes
from picture import Picture # used representing images to displaya
import os # used for file and directory operations
from color import Color # used for coloring the game menu
import numpy as np
# MAIN FUNCTION OF THE PROGRAM
#-------------------------------------------------------------------------------
# Main function where this program starts execution

class Main():

   def start(self):
      
      # set the dimensions of the game grid
      
      grid_h, grid_w = 20, 20
      game_w = 12
      # set the size of the drawing canvas
      canvas_h, canvas_w = 40 * grid_h, 40 * grid_w
      stddraw.setCanvasSize(canvas_w, canvas_h) 
      # set the scale of the coordinate system
      stddraw.setXscale(-0.5, grid_w - 0.5)
      stddraw.setYscale(-0.5, grid_h - 0.5)
      
      self.tetrominos = list()
      self.tetrominos_copy = list()
      self.round_count = 0
      self.create_tetromino(grid_h, game_w)
      

      self.next_tetromino = self.tetrominos[self.round_count + 1]
      self.next_tetromino_copy = self.tetrominos[self.round_count + 1]
      
      self.next_tetromino_copy.move_pos(15, 10)

      self.is_tetromino_rotated = False
      
      
      
      # create the game grid
      grid = GameGrid(grid_h, game_w)
      # create the first tetromino to enter the game grid 
      # by using the create_tetromino function defined below
      grid.next_tetromino = self.next_tetromino
      self.current_tetromino = self.tetrominos[self.round_count]
     # Gives first tetromino to GameGrid class to draw it on the screen
      grid.current_tetromino = self.current_tetromino

      # display a simple menu before opening the game

      # self.display_game_menu(grid_h, grid_w)

      # main game loop (keyboard interaction for moving the tetromino) 
      while True:
         
         # check user interactions via the keyboard
         if stddraw.hasNextKeyTyped():
            key_typed = stddraw.nextKeyTyped()
            # if the left arrow key has been pressed
            if key_typed == "left": 
               # move the tetromino left by one
               self.current_tetromino.move(key_typed, grid) 
            # if the right arrow key has been pressed
            elif key_typed == "right":
               # move the tetromino right by one
               self.current_tetromino.move(key_typed, grid)
            # if the down arrow key has been pressed
            elif key_typed == "down":
               # move the tetromino down by one 
               # (causes the tetromino to fall down faster)
               self.current_tetromino.move(key_typed, grid)
            
            # rotate shape anticlockwise
            elif key_typed == "a":
               if self.current_tetromino.shape != "O":
                  self.is_tetromino_rotated = True
                  self.current_tetromino.get_tetromino_points(self.current_tetromino)
             
            # clear the queue that stores all the keys pressed/typed

            # rotate shape clockwise
            elif key_typed == "d":
               self.is_tetromino_rotated = True
               self.current_tetromino.get_tetromino_points(self.current_tetromino)
        

            elif key_typed == "b":
               time.sleep(5)

            stddraw.clearKeysTyped()
               
         # move (drop) the tetromino down by 1 at each iteration 
         success = self.current_tetromino.move("down", grid)

         # place the tetromino on the game grid when it cannot go down anymore
         if not success:
            # get the tile matrix of the tetromino
            tiles_to_place = self.current_tetromino.tile_matrix

            # update the game grid by adding the tiles of the tetromino
            game_over = grid.update_grid(tiles_to_place)
            # end the main game loop if the game is over
            if game_over:
               break
            # create the next tetromino to enter the game grid
            # by using the create_tetromino function defined below
            self.round_count += 1

            # Determines the current tetromino and gives it to GameGrid
            self.current_tetromino = self.tetrominos[self.round_count]
            # print("len", len(self.tetrominos))
            grid.current_tetromino = self.current_tetromino
            
            new_x, new_y = random.randint(2, 9), 21
            self.current_tetromino.move_pos(new_x, new_y)
            
            # Calculates a random position for following current tetromino
            row_count = self.is_full(grid_h, grid_w, grid)
            index = 0
            # Slides down the rows
            while index < grid_h:
               while row_count[index]:
                  self.slide_down(row_count, grid)
                  row_count = self.is_full(grid_h, grid_w, grid)
               index += 1

            if self.round_count == 8:
               self.tetrominos = []
               self.round_count = 0
               self.create_tetromino(grid_h, game_w)

            next_tetromino = self.tetrominos[self.round_count+1]
            grid.next_tetromino = next_tetromino
            self.next_tetromino_copy = self.tetrominos_copy[self.round_count + 1]
            # print("next shape", grid.next_tetromino.shape)
            # grid.next_tetromino.move_pos(15, 15)
            self.next_tetromino_copy.move_pos(15, 10)
            
            
            
         # display the game grid and as well the current tetromino      
      
         grid.display()

      print("Game over")

   # Function for creating random shaped tetrominoes to enter the game grid
   def create_tetromino(self, grid_height, grid_width):
      # type (shape) of the tetromino is determined randomly
      tetromino_types = ['I', 'O', 'Z', 'S', 'L', 'J', 'T']
      for i in range(10):
         random_index = random.randint(0, len(tetromino_types) - 1)
         random_type = tetromino_types[random_index]
         # create and return the tetromino
         tetromino = Tetromino(random_type, grid_height, grid_width)
         self.tetrominos.append(tetromino)

      self.tetrominos_copy = self.tetrominos.copy()
      return self.tetrominos

   # Function for displaying a simple menu before starting the game
   def display_game_menu(self, grid_height, grid_width):
      # colors used for the menu
      background_color = Color(42, 69, 99)
      button_color = Color(25, 255, 228)
      text_color = Color(31, 160, 239)
      # clear the background canvas to background_color
      stddraw.clear(background_color)
      # get the directory in which this python code file is placed
      current_dir = os.path.dirname(os.path.realpath(__file__))
      # path of the image file
      img_file = current_dir + "/menu_image.png"
      # center coordinates to display the image
      img_center_x, img_center_y = (grid_width - 1) / 2, grid_height - 7
      # image is represented using the Picture class
      image_to_display = Picture(img_file)
      # display the image
      stddraw.picture(image_to_display, img_center_x, img_center_y)
      # dimensions of the start game button
      button_w, button_h = grid_width - 1.5, 2
      # coordinates of the bottom left corner of the start game button 
      button_blc_x, button_blc_y = img_center_x - button_w / 2, 4
      # display the start game button as a filled rectangle
      stddraw.setPenColor(button_color)
      stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)
      # display the text on the start game button
      stddraw.setFontFamily("Arial")
      stddraw.setFontSize(25)
      stddraw.setPenColor(text_color)
      text_to_display = "Click Here to Start the Game"
      stddraw.text(img_center_x, 5, text_to_display)
      # menu interaction loop
      while True:
         # display the menu and wait for a short time (50 ms)
         stddraw.show(50)
         # check if the mouse has been left-clicked
         if stddraw.mousePressed():
            # get the x and y coordinates of the location at which the mouse has 
            # most recently been left-clicked  
            mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
            if mouse_x >= button_blc_x and mouse_x <= button_blc_x + button_w:
               if mouse_y >= button_blc_y and mouse_y <= button_blc_y + button_h: 
                  break # break the loop to end the method and start the game

   def slide_down(self, row_count, grid):
         for index, i in enumerate(row_count):
               if i:
                  for a in range(index, 19):
                     row = np.copy(grid.tile_matrix[a + 1])
                     grid.tile_matrix[a] = row
                     for b in range(12):
                           if grid.tile_matrix[a][b] is not None:
                              grid.tile_matrix[a][b].move(0, -1)
                  break

   def is_full(self, grid_h, grid_w, grid):
      # Creates an array with full of False, array size is equal to number of rows in the game grid
      row_count = [False for i in range(grid_h)]
      # if a row is full, this score variable keeps total score which will come from this full row
      score = 0
      for h in range(grid_h):
         # Keeps total number of tiles inside the same row, if counter == 12, row is full
         counter = 0
         for w in range(grid_w):
               if grid.is_occupied(h, w):
                  counter += 1
               # If row is full, calculates total score in this row
               if counter == 12:
                  score = 0
                  for a in range(12):
                     score += grid.tile_matrix[h][a].number
                  row_count[h] = True
        # Updating total score
      grid.score += score
        # Used for changing game speed by score
      grid.last_updated += score
      return row_count
   # start() function is specified as the entry point (main function) from which 
   # the program starts execution

main_game = Main()
main_game.start()


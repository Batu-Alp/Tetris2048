import lib.stddraw as stddraw  # stddraw is used as a basic graphics library
from lib.color import Color # used for coloring the game grid
from point import Point  # used for tile positions
import numpy as np  # fundamental Python module for scientific computing
from tile import Tile
from tetromino import Tetromino

# Class used for modelling the game grid
class GameGrid:
	# Constructor for creating the game grid based on the given arguments
   def __init__(self, grid_h, grid_w):
      # set the dimensions of the game grid as the given arguments
      self.grid_height = grid_h
      self.grid_width = grid_w
      # create a tile matrix to store the tiles landed onto the game grid
      self.tile_matrix = np.full((grid_h, grid_w), None)
      # create the tetromino that is currently being moved on the game grid
      self.current_tetromino = None
      self.next_tetromino = None
      # the game_over flag shows whether the game is over or not
      self.game_over = False
      # set the color used for the empty grid cells
      self.empty_cell_color = Color(42, 69, 99)
      # set the colors used for the grid lines and the grid boundaries
      self.line_color = Color(0, 100, 200) 
      self.boundary_color = Color(0, 100, 200)
      # thickness values used for the grid lines and the boundaries
      self.line_thickness = 0.002
      self.box_thickness = 10 * self.line_thickness
      self.normal_speed = 250

      self.paussed = False
      self.score = 0
      self.game_over = False
      self.restart = False

   # Method used for displaying the game grid
   def display(self, paussed):

      # clear the background to empty_cell_color
      stddraw.clear(self.empty_cell_color)
      # draw the game grid

      self.draw_grid(paussed)
      # draw the current/active tetromino if it is not None (the case when the 
      # game grid is updated)
      if self.current_tetromino is not None:
         self.current_tetromino.draw()
         #self.next_tetromino.draw()

      # draw a box around the game grid 
      self.draw_boundaries()
      # show the resulting drawing with a pause duration = 250 ms
      # stddraw.show(250)
      stddraw.show(self.normal_speed)  


   def merge(self):
        
        a , b = 0, 0
        while(a < self.grid_height):
            while(b < self.grid_width):

                if self.tile_matrix[a][b] != None and self.tile_matrix[a + 1][b] != None:
                    if self.tile_matrix[a][b].tile_number == self.tile_matrix[a + 1][b].tile_number:

                        # self.tile_matrix[a + 1][b].set_position(None)
                        self.tile_matrix[a + 1][b] = None
                        self.tile_matrix[a][b].tile_number += self.tile_matrix[a][b].tile_number
                        self.score += self.tile_matrix[a][b].tile_number
                        # self.last_updated += grid.tile_matrix[a][b].tile_number
                        self.tile_matrix[a][b].decide_color(self.tile_matrix[a][b].tile_number)
                        a = 0
                        b = 0
                b += 1
            a += 1
            b = 0



   # Delete full line
   def clearFullLine(self, grid_h, grid_w):

      for i in range(grid_w):
            for j in range(grid_w):
               if self.tile_matrix[i][j] is not None:  # To avoid AttributeError: 'NoneType' object has no attribute 'tile_number'
                  row_score = self.tile_matrix[i][j].tile_number
                  self.score += row_score

            self.tile_matrix = np.delete(self.tile_matrix, i , axis=0)
            self.tile_matrix = np.append(self.tile_matrix, np.full((1, grid_w), None), axis=0)

            for k in range(i, grid_h):
               for l in range(grid_w):
                  if self.tile_matrix[k][l] is not None:
                     self.tile_matrix[k][l].move(0, -1)


   def delete_tile(self):

      for i in range(1, self.grid_height - 1):
         for j in range(1, self.grid_width - 1):
            if self.tile_matrix[i][j] is not None:

               if self.tile_matrix[i + 1][j] is None and self.tile_matrix[i - 1][j] is None and self.tile_matrix[i][j + 1] is None and self.tile_matrix[i][j - 1] is None:
                  
                  tile_score = self.tile_matrix[i][j].tile_number
                  self.score += tile_score
                  self.tile_matrix[i][j] = None
                  self.delete_tile()


      
   # Method for drawing the cells and the lines of the game grid
   def draw_grid(self, paussed):
      # for each cell of the game grid
      for row in range(self.grid_height):
         for col in range(self.grid_width):
            # draw the tile if the grid cell is occupied by a tile
            if self.tile_matrix[row][col] is not None:
               self.tile_matrix[row][col].draw(Point(col, row))
               # self.tile_matrix[row][col].draw()



      # Draws the main score on the top right of the main game screen
      # self.showScore(self.score)

      # Displays total number of count how many times the speed increased
      self.showNextTetrominoAndScore(self.score, self.normal_speed, paussed)

      # draw the inner lines of the grid
      stddraw.setPenColor(self.line_color)
      stddraw.setPenRadius(self.line_thickness)
      # x and y ranges for the game grid
      start_x, end_x = -0.5, self.grid_width - 0.5
      start_y, end_y = -0.5, self.grid_height - 0.5
      for x in np.arange(start_x + 1, end_x, 1):  # vertical inner lines
         stddraw.line(x, start_y, x, end_y)
      for y in np.arange(start_y + 1, end_y, 1):  # horizontal inner lines
         stddraw.line(start_x, y, end_x, y)
      stddraw.setPenRadius()  # reset the pen radius to its default value  
  
   def set_next(self, next_tetromino):
        self.next_tetromino = next_tetromino

   def showNextTetrominoAndScore(self, score, speed, paussed):

        #stddraw.setPenRadius(200)
        stddraw.setFontSize(18)
        stddraw.setPenColor(Color(255, 255, 255))

        text_to_display = "Score: " + str(score)
        stddraw.text(14.4, 18.8, text_to_display) 
        
        text_to_display = "Press p to pauss the game"
        stddraw.text(14.4, 16.5, text_to_display)
        
        text_to_display = "Press r to restart the game"
        stddraw.text(14.4, 15.5, text_to_display)  
        
        text_to_display = "Game speed : " + str(speed)
        stddraw.text(14.4, 12.5, text_to_display)  
        
        text_to_display = "NEXT TETROMINO"
        stddraw.text(14.4, 10.5, text_to_display)

        if paussed is True:
           stddraw.setFontSize(30)
           stddraw.text(6, 18, "Paussed")


      
   # Method for drawing the boundaries around the game grid 
   def draw_boundaries(self):
      # draw a bounding box around the game grid as a rectangle
      stddraw.setPenColor(self.boundary_color)  # using boundary_color
      # set the pen radius as box_thickness (half of this thickness is visible 
      # for the bounding box as its lines lie on the boundaries of the canvas)
      stddraw.setPenRadius(self.box_thickness)
      # the coordinates of the bottom left corner of the game grid
      pos_x, pos_y = -0.5, -0.5
      stddraw.rectangle(pos_x, pos_y, self.grid_width, self.grid_height)
      stddraw.setPenRadius()  # reset the pen radius to its default value

   # Method used for checking whether the grid cell with given row and column 
   # indexes is occupied by a tile or empty
   def is_occupied(self, row, col):
      # considering newly entered tetrominoes to the game grid that may have 
      # tiles with position.y >= grid_height
      if not self.is_inside(row, col):
         return False
      # the cell is occupied by a tile if it is not None
      return self.tile_matrix[row][col] is not None
      
   # Method used for checking whether the cell with given row and column indexes 
   # is inside the game grid or not
   def is_inside(self, row, col):
      if row < 0 or row >= self.grid_height:
         return False
      if col < 0 or col >= self.grid_width:
         return False
      return True

   # Method that locks the tiles of the landed tetromino on the game grid while
   # checking if the game is over due to having tiles above the topmost grid row.
   # The method returns True when the game is over and False otherwise.
   def update_grid(self, tiles_to_lock, blc_position):
      # necessary for the display method to stop displaying the tetromino
      self.current_tetromino = None
      # lock the tiles of the current tetromino (tiles_to_lock) on the game grid 
      n_rows, n_cols = len(tiles_to_lock), len(tiles_to_lock[0])
      for col in range(n_cols):
         for row in range(n_rows):            
            # place each tile onto the game grid
            if tiles_to_lock[row][col] is not None:
               # compute the position of the tile on the game grid
               pos = Point()
               pos.x = blc_position.x + col
               pos.y = blc_position.y + (n_rows - 1) - row
               if self.is_inside(pos.y, pos.x):
                  self.tile_matrix[pos.y][pos.x] = tiles_to_lock[row][col]
               # the game is over if any placed tile is above the game grid
               else:
                  self.game_over = True

      # return the game_over flag
      self.clearFullLine(self.grid_height, self.grid_width)
      return self.game_over


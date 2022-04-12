import random
from turtle import pos, position

from pandas import pivot
from stddraw import point
# each tetromino is created with a random x value above the grid
from tile import Tile # used for representing each tile on the tetromino
from point import Point # used for tile positions
import numpy as np # fundamental Python module for scientific computing

# Class used for representing tetrominoes with 3 out of 7 different types/shapes 
# as (I, O and Z)
class Tetromino:
   # Constructor to create a tetromino with a given type (shape)
   def __init__(self, type, grid_height, grid_width):
      # set grid_height and grid_width from input parameters
      self.grid_height = grid_height
      self.grid_width = grid_width
      # set the shape of the tetromino based on the given type
      self.occupied_tiles = []
      self.shape = type
      self.rotate_center = []
      self.tile_n = 0
      

      if type == 'I':
         self.tile_n = 4  # n = number of rows = number of columns in the tile matrix
         # shape of the tetromino I in its initial orientation
         self.occupied_tiles.append((1, 0))  # (column_index, row_index)
         self.occupied_tiles.append((1, 1))
         self.occupied_tiles.append((1, 2))
         self.occupied_tiles.append((1, 3))
      elif type == 'O':
         self.tile_n = 2  # n = number of rows = number of columns in the tile matrix
         # shape of the tetromino O in its initial orientation
         self.occupied_tiles.append((0, 0))
         self.occupied_tiles.append((1, 0))
         self.occupied_tiles.append((0, 1))
         self.occupied_tiles.append((1, 1))
      elif type == 'Z':
         self.tile_n= 3  # n = number of rows = number of columns in the tile matrix
         # shape of the tetromino Z in its initial orientation
         self.occupied_tiles.append((0, 0))
         self.occupied_tiles.append((1, 0))
         self.occupied_tiles.append((1, 1))
         self.occupied_tiles.append((2, 1))
      elif type == 'J':
         self.tile_n= 3  # n = number of rows = number of columns in the tile matrix
         # shape of the tetromino Z in its initial orientation
         self.occupied_tiles.append((0, 2))
         self.occupied_tiles.append((1, 0))
         self.occupied_tiles.append((1, 1))
         self.occupied_tiles.append((1, 2))
      elif type == 'L':
         self.tile_n = 3  # n = number of rows = number of columns in the tile matrix
         # shape of the tetromino Z in its initial orientation
         self.occupied_tiles.append((1, 0))
         self.occupied_tiles.append((1, 1))
         self.occupied_tiles.append((1, 2))
         self.occupied_tiles.append((2, 2))
      elif type == 'T':
         self.tile_n = 3  # n = number of rows = number of columns in the tile matrix
         # shape of the tetromino Z in its initial orientation
         self.occupied_tiles.append((1, 0))
         self.occupied_tiles.append((1, 1))
         self.occupied_tiles.append((2, 1))
         self.occupied_tiles.append((1, 2))
      elif type == 'S':
         self.tile_n = 3  # n = number of rows = number of columns in the tile matrix
         # shape of the tetromino Z in its initial orientation
         self.occupied_tiles.append((0, 1))
         self.occupied_tiles.append((2, 0))
         self.occupied_tiles.append((1, 0))
         self.occupied_tiles.append((1, 1))
      
      # create a matrix of numbered tiles based on the shape of the tetromino
      self.tile_matrix = np.full((self.tile_n, self.tile_n), None)
      # initial position of the bottom-left tile in the tile matrix just before 
      # the tetromino enters the game grid
      self.bottom_left_corner = Point()
      # upper side of the game grid
      self.bottom_left_corner.y = grid_height
      # a random horizontal position 
      self.bottom_left_corner.x = random.randint(0, grid_width - self.tile_n)
      
      # create each tile by computing its position w.r.t. the game grid based on 
      # its bottom_left_corner
      for i in range(len(self.occupied_tiles)):
         col_index, row_index = self.occupied_tiles[i][0], self.occupied_tiles[i][1]
         position = Point()
         # horizontal position of the tile
         position.x = self.bottom_left_corner.x + col_index
         # vertical position of the tile
         position.y = self.bottom_left_corner.y + (self.tile_n - 1) - row_index
         # create the tile on the computed position 
         self.tile_matrix[row_index][col_index] = Tile(position)
      
   # Method for drawing the tetromino on the game grid
   def draw(self):
      n = len(self.tile_matrix)  # n = number of rows = number of columns
      for row in range(n):
         for col in range(n):
            # draw each occupied tile (not equal to None) on the game grid
            if self.tile_matrix[row][col] != None:
               # considering newly entered tetrominoes to the game grid that may 
               # have tiles with position.y >= grid_height
               position = self.tile_matrix[row][col].get_position()
               if position.y < self.grid_height:
                  self.tile_matrix[row][col].draw() 

   def down_tetromino_now(self, current_tetromino, grid, grid_h):
      for i in range(grid_h):
         current_tetromino.move("down",grid)
   # 90 degree rotation
   def rotate(self, current_tetromio):
      n = len(self.tile_matrix)      
      tile_dict = {}
      for row in range(n):
         for col in range(n):
            if self.tile_matrix[row, col] != None:
               pos_x = self.tile_matrix[row,col].position.x
               pos_y = self.tile_matrix[row,col].position.y
               tile_dict[self.tile_matrix[row, col]] = [pos_x, pos_y]
      
      if current_tetromio.shape == "T":
         x = self.tile_matrix[1,1].position.x
         y = self.tile_matrix[1,1].position.y
         self.pivot = [x, y]
      
      elif current_tetromio.shape == "O" :
         x = self.tile_matrix[0,0].position.x
         y = self.tile_matrix[0,0].position.y
         self.pivot = [x, y]
      
      elif current_tetromio.shape == "I" :
         self.pivot = list(tile_dict.values())[1]

      else:
         x = self.tile_matrix[1,1].position.x
         y = self.tile_matrix[1,1].position.y
         self.pivot = [x, y]
      
      rotate_left = True
      for tile in (tile_dict.keys()):

         x = tile_dict.get(tile)[1] - self.pivot[1]
         y = tile_dict.get(tile)[0] - self.pivot[0]

         rotated_x = self.pivot[0] - x  
         rotated_y = self.pivot[1] + y

         tile_dict[tile] = [rotated_x , rotated_y]

         if tile_dict.get(tile)[0] >= self.grid_width :
            rotate_left = False

         elif tile_dict.get(tile)[0] <= -1:
            rotate_left = False
      
      if rotate_left:
         np_arr = np.rot90(self.tile_matrix, 1)

         self.tile_matrix = np.full((self.tile_n, self.tile_n), None)
         for tile in tile_dict.keys():
            for i in range(len(np_arr)):
               for j in range(len(np_arr[i])):
                  if tile == np_arr[i, j]:  
                     point = Point()
                     point.x = tile_dict.get(tile)[0]
                     point.y = tile_dict.get(tile)[1]
                     self.tile_matrix[i, j] = Tile(point)
                
      


     
      

   def move(self, direction, game_grid):
      # check if the tetromino can be moved in the given direction by using the
      # can_be_moved method defined below
      if not(self.can_be_moved(direction, game_grid)):
         return False  # tetromino cannot be moved in the given direction
      # move the tetromino by first updating the position of the bottom left tile 
      if direction == "left":
         self.bottom_left_corner.x -= 1
      elif direction == "right":
         self.bottom_left_corner.x += 1
      else:  # direction == "down"
         self.bottom_left_corner.y -= 1
      # then moving each occupied tile in the given direction by 1
      n = len(self.tile_matrix)  # n = number of rows = number of columns
      for row in range(n):
         for col in range(n):
            if self.tile_matrix[row][col] != None:
               if direction == "left":
                  self.tile_matrix[row][col].move(-1, 0)
               elif direction == "right":
                  self.tile_matrix[row][col].move(1, 0)
               else: # direction == "down"
                  self.tile_matrix[row][col].move(0, -1)
                  
      return True  # successful move in the given direction
   
   # Method to check if the tetromino can be moved in the given direction or not
   def can_be_moved(self, dir, game_grid):
      n = len(self.tile_matrix)  # n = number of rows = number of columns
      if dir == "left" or dir == "right":
         for row in range(n):
            for col in range(n): 
               # direction = left --> check the leftmost tile of each row
               if dir == "left" and self.tile_matrix[row][col] != None:
                  leftmost = self.tile_matrix[row][col].get_position()
                  # tetromino cannot go left if any leftmost tile is at x = 0
                  if leftmost.x == 0:
                     return False
                  # skip each row whose leftmost tile is out of the game grid 
                  # (possible for newly entered tetrominoes to the game grid)
                  if leftmost.y >= self.grid_height:
                     break
                  # tetromino cannot go left if the grid cell on the left of any 
                  # of its leftmost tiles is occupied
                  if game_grid.is_occupied(leftmost.y, leftmost.x - 1):
                     return False
                  break  # end the inner for loop
               # direction = right --> check the rightmost tile of each row
               elif dir == "right" and self.tile_matrix[row][n - 1 - col] != None:
                  rightmost = self.tile_matrix[row][n - 1 - col].get_position()
                  # tetromino cannot go right if any of its rightmost tiles is 
                  # at x = grid_width - 1
                  if rightmost.x == self.grid_width - 1:
                     return False
                  # skip each row whose rightmost tile is out of the game grid 
                  # (possible for newly entered tetrominoes to the game grid)
                  if rightmost.y >= self.grid_height:
                     break
                  # tetromino cannot go right if the grid cell on the right of 
                  # any of its rightmost tiles is occupied
                  if game_grid.is_occupied(rightmost.y, rightmost.x + 1):
                     return False
                  break  # end the inner for loop
      # direction = down --> check the bottommost tile of each column
      else:
         for col in range(n):
            for row in range(n - 1, -1, -1):
               if self.tile_matrix[row][col] != None:
                  bottommost = self.tile_matrix[row][col].get_position()
                  # skip each column whose bottommost tile is out of the grid 
                  # (possible for newly entered tetrominoes to the game grid)
                  if bottommost.y > self.grid_height:
                     break
                  # tetromino cannot go down if any bottommost tile is at y = 0
                  if bottommost.y == 0:
                     return False 
                  # or the grid cell below any bottommost tile is occupied
                  if game_grid.is_occupied(bottommost.y - 1, bottommost.x):
                     return False
                  
                  break  # end the inner for loop
      return True  # tetromino can be moved in the given direction


   def move_pos(self, dx, dy):
      # Keeps the leftmost tile position
      pivot_point = Point()

      # Check if the leftmost object is None, looks one unit left and bottom, sets the pivot point relative them
      if self.tile_matrix[0][0] != None:
            pivot_point.x = self.tile_matrix[0][0].get_position().x
            pivot_point.y = self.tile_matrix[0][0].get_position().y
      # If the lestmost object None, looks one to the bottom tile
      elif self.tile_matrix[0][1] != None:
            pivot_point.x = self.tile_matrix[0][1].get_position().x
            pivot_point.y = self.tile_matrix[0][1].get_position().y
      # If the lestmost object None, looks one to the right tile
      else:
            pivot_point.x = self.tile_matrix[1][0].get_position().x
            pivot_point.y = self.tile_matrix[1][0].get_position().y
      
      for m in self.tile_matrix:
            for p in m:
                if p != None:
                    p.move(dx-pivot_point.x, dy-pivot_point.y)



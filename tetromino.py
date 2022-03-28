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

      if self.shape == 'I':
         n = 4  # n = number of rows = number of columns in the tile matrix
         # shape of the tetromino I in its initial orientation
         self.occupied_tiles.append((1, 0)) # (column_index, row_index)
         self.occupied_tiles.append((1, 1))
         self.occupied_tiles.append((1, 2))
         self.occupied_tiles.append((1, 3))   

      elif self.shape == 'O':
         n = 2  # n = number of rows = number of columns in the tile matrix
         # shape of the tetromino O in its initial orientation
         self.occupied_tiles.append((0, 0)) 
         self.occupied_tiles.append((1, 0))
         self.occupied_tiles.append((0, 1))
         self.occupied_tiles.append((1, 1))


      elif self.shape == 'S':
         n = 3
         self.occupied_tiles.append((0, 1)) 
         self.occupied_tiles.append((1,1))
         self.occupied_tiles.append((1, 0))
         self.occupied_tiles.append((2,0))
         

      elif self.shape == 'Z':
         n = 3  # n = number of rows = number of columns in the tile matrix
         # shape of the tetromino Z in its initial orientation
      
         self.occupied_tiles.append((0, 0)) 
         self.occupied_tiles.append((1, 0))
         self.occupied_tiles.append((1, 1))
         self.occupied_tiles.append((2, 1))  

      elif self.shape == 'L':
         n = 3

         self.occupied_tiles.append((1,0))
         self.occupied_tiles.append((1,1))
         self.occupied_tiles.append((1,2))
         self.occupied_tiles.append((2,2))
      elif self.shape == 'J':
         n = 3

         self.occupied_tiles.append((0,2))
         self.occupied_tiles.append((1,0))
         self.occupied_tiles.append((1,1))
         self.occupied_tiles.append((1,2))
      
      elif self.shape == 'T':
         n = 3

         self.occupied_tiles.append((0,1))
         self.occupied_tiles.append((1,1))
         self.occupied_tiles.append((2,1))
         self.occupied_tiles.append((1,2))
      
      # create a matrix of numbered tiles based on the shape of the tetromino
      self.tile_matrix = np.full((n, n), None)
      # initial position of the bottom-left tile in the tile matrix just before 
      # the tetromino enters the game grid
      self.bottom_left_corner = Point()
      # upper side of the game grid
      self.bottom_left_corner.y = grid_height
      # a random horizontal position 
      self.bottom_left_corner.x = random.randint(0, grid_width - n)
      # create each tile by computing its position w.r.t. the game grid based on 
      # its bottom_left_corner
      for i in range(len(self.occupied_tiles)):
         col_index, row_index = self.occupied_tiles[i][0], self.occupied_tiles[i][1]
         position = Point()
         # horizontal position of the tile
         position.x = self.bottom_left_corner.x + col_index
         # vertical position of the tile
         position.y = self.bottom_left_corner.y + (n - 1) - row_index
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

   """
   def rotate(self, grid):
        # First erase_shape
        self.erase_shape(grid)
        rotated_shape = []
        for x in range(len(self.shape[0])):
            new_row = []
            for y in range(len(self.shape)-1, -1, -1):
                new_row.append(self.shape[y][x])
            rotated_shape.append(new_row)
        
        right_side = self.x + len(rotated_shape[0])
        if right_side < len(grid[0]):     
            self.shape = rotated_shape
            # Update the height and width
            self.height = len(self.shape)
   """
   
   def rotate(self, game_grid, current_tetromino):
      pass
      """
      n = len(self.tile_matrix)
      copy_matrix = np.copy(self.tile_matrix)
      for r in range(n):
         for c in range(n):
               self.tile_matrix[c][n - 1 - r] = copy_matrix[r][c]
      for r in range(n):
         for c in range(n):
               # Check if there is a tile at self.tile_matrix[r][c]
               if self.tile_matrix[r][c] is not None:
                  # Moves tiles to their new position
                  self.tile_matrix[r][c].move(-r + c, -c + (n - r))
                  if self.tile_matrix[r][c].get_position().x < 0:
                     for i in range(0-self.tile_matrix[r][c].get_position().x):
                           current_tetromino.move("right", game_grid)
                  elif self.tile_matrix[r][c].get_position().x >= 12:
                     for i in range(self.tile_matrix[r][c].get_position().x-11):
                           current_tetromino.move("left", game_grid)
         """
      



      """
      if shape != 'O' and self.can_be_moved("left", game_grid):
         temp_list = []

         n = len(self.tile_matrix)
         pivot = Point(self.tile_matrix[1][0])
          

         indexes = []

         for row in range(n):
            for col in range(n):
               if self.tile_matrix[row,col] != None:
                  temp_list.append([self.tile_matrix[row,col].position.x, self.tile_matrix[row,col].position.y])
                  indexes.append((row,col))
         
         pivot = temp_list[1]
         for i in range(len(temp_list)):
            x = temp_list[i][1] - pivot[1]
            y = temp_list[i][0] - pivot[0]

            temp_list[i][0] = pivot[0] - x
            temp_list[i][1] = pivot[1] + y
         
         count = 0
         for ind in indexes:
            self.tile_matrix[ind[0]][ind[1]].position.x = temp_list[count][0]
            self.tile_matrix[ind[0]][ind[1]].position.y = temp_list[count][1]
            count +=1
            
         # self.tile_matrix = np.ndarray(temp_list)

         print(temp_list)
       """  

   # 90 degree rotation
   def get_tetromino_points(self, current_tetromino):
      print(current_tetromino.shape)
      n = len(self.tile_matrix)
      # pivot = Point(self.tile_matrix[1][0])
      temp_list = []
         

      indexes = []

      for row in range(n):
         for col in range(n):
            if self.tile_matrix[row, col] != None:
               temp_list.append([self.tile_matrix[row, col].position.x, self.tile_matrix[row, col].position.y])
               indexes.append((col,row))
      
      pivot = temp_list[1]

      rotate_left = True
      for i in range(len(temp_list)):
         x = temp_list[i][1] - pivot[1]
         y = temp_list[i][0] - pivot[0]

         temp_list[i][0] = pivot[0] - x
         temp_list[i][1] = pivot[1] + y

         if temp_list[i][0] > self.grid_width -1:
            rotate_left = False
            
      # indexes = self.get_indexs()

      
      if rotate_left:
         count = 0
         for ind in indexes:
            # if self.tile_matrix[ind[0]][ind[1]] == None:
            #    self.tile_matrix[ind[0]][ind[1]] = Tile()

            self.tile_matrix[ind[1]][ind[0]].position.x = temp_list[count][0]
            self.tile_matrix[ind[1]][ind[0]].position.y = temp_list[count][1]
            count +=1
               
         print(temp_list)

   def get_indexs(self):
      ind_list = []
      np_arr = np.rot90(self.occupied_tiles, 1)
      for row in range(np_arr.shape[1]):
         for col in range(np_arr.shape[0]):
            if np_arr[col, row] != None:
               ind_list.append((col, row))
      return ind_list


   # def can_rotate_left(self, temp_list):
   #    n = len(temp_list)
   #    for i in range(n):
   #       for j in range(n):
   #          if temp_list[i][j] != None and temp_list[i][j] > self.grid_width:
   #             return False
            
   #          elif temp_list[i][j] != None and temp_list[i][j] < 0:
   #             return False 
   #    return True


   # Method for moving the tetromino in a given direction by 1 on the game grid
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

   # def can_be_turned(self, dir, game_grid):
   #    n = len(self.tile_matrix)
   #    if dir == "clock":
   #       pass

   #    elif dir == "anticlock":
   #       pass

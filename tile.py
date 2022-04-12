from turtle import color
import lib.stddraw as stddraw  # stddraw is used as a basic graphics library
from lib.color import Color  # used for coloring the tile and the number on it
import copy as cp
import random
import numpy as np
from point import Point
import math


from lib.color import WHITE
from lib.color import BLACK
from lib.color import RED
from lib.color import GREEN
from lib.color import BLUE
from lib.color import CYAN
from lib.color import MAGENTA
from lib.color import YELLOW
from lib.color import DARK_BLUE
from lib.color import DARK_RED
from lib.color import ORANGE
from lib.color import VIOLET
from lib.color import PINK
from lib.color import BOOK_BLUE
from lib.color import BOOK_LIGHT_BLUE
from lib.color import BOOK_RED

colors = [Color(239, 230, 221), Color(239, 227, 205), Color(247,178,123), Color(247,150,99), Color(247,124,90),
                Color(247,93,59), Color(239,205,115), Color(239,206,99), Color(239,198,82), Color(238,198,66), Color(239,194,49), Color(60,58,51)]
# Class used for modeling numbered tiles as in 2048
class Tile: 
   # Class attributes shared among all Tile objects
   # ---------------------------------------------------------------------------
   # the value of the boundary thickness (for the boxes around the tiles)
   boundary_thickness = 0.004
   # font family and size used for displaying the tile number
   font_family, font_size = "Arial", 14

   # Constructor that creates a tile with 2 as the number on it
   def __init__(self,  position = Point(0, 0)):
      # set the number on the tile
      initial_numbers = [2,4]
      self.tile_number = random.choice(initial_numbers)
      # set the colors of the tile
      self.foreground_color = Color(0, 100, 200) # foreground (number) color
      self.box_color = Color(0, 100, 200) # box (boundary) color

      self.position = Point(position.x, position.y)
      self.tetromino_color = random.randint(1, len(colors) - 1)

   # Method for moving the tile by dx along the x axis and by dy along the y axis
   def move(self, dx, dy):
      self.position.translate(dx, dy)

   # Method for drawing the tile
   def draw(self, position, length = 1):
      # draw the tile as a filled square
      #stddraw.setPenColor(colors[self.tetromino_color])
      stddraw.setPenColor(self.decide_color(self.tile_number))
      stddraw.filledSquare(position.x, position.y, length/2)
      # draw the bounding box around the tile as a square
      stddraw.setPenColor(self.box_color)
      stddraw.setPenRadius(Tile.boundary_thickness)
      stddraw.square(position.x, position.y, length/2)
      stddraw.setPenRadius()  # reset the pen radius to its default value
      # draw the number on the tile
      stddraw.setPenColor(self.foreground_color)
      stddraw.setFontFamily(Tile.font_family)
      stddraw.setFontSize(Tile.font_size)
      stddraw.boldText(position.x, position.y, str(self.tile_number))

   def drawForNextTetromino(self, position, length = 1):
       # draw the tile as a filled square
      stddraw.setPenColor(self.decide_color(self.tile_number))
      stddraw.filledSquare(position.x + 13, position.y + 5, length/2)
      # draw the bounding box around the tile as a square
      stddraw.setPenColor(self.box_color)
      stddraw.setPenRadius(Tile.boundary_thickness)
      stddraw.square(position.x + 13, position.y + 5, length/2)
      stddraw.setPenRadius()  # reset the pen radius to its default value
      # draw the number on the tile
      stddraw.setPenColor(self.foreground_color)
      stddraw.setFontFamily(Tile.font_family)
      stddraw.setFontSize(Tile.font_size)
      stddraw.boldText(position.x + 13, position.y  + 5, str(self.tile_number))
      

   def decide_color(self, tile_number ):

      if tile_number == 2:
         return YELLOW
      elif tile_number == 4:
         return RED
      elif tile_number == 8:
         return GREEN
      elif tile_number == 16:
         return CYAN
      elif tile_number == 32:
         return PINK
      elif tile_number == 64:
         return BOOK_LIGHT_BLUE
      elif tile_number == 128:
         return VIOLET
      elif tile_number == 256:
         return BOOK_RED
      else:
         return Color(240,240,240)


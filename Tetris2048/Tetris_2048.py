import lib.stddraw as stddraw  # stddraw is used as a basic graphics library
from lib.picture import Picture  # used for displaying images
from lib.color import Color  # used for coloring the game menu
import os  # the os module is used for file and directory operations
from game_grid import GameGrid # the class for modeling the game grid
from tetromino import Tetromino # the class for modeling the tetrominoes
import random # used for creating tetrominoes with random types/shapes

# MAIN FUNCTION OF THE PROGRAM
#-------------------------------------------------------------------------------
# Main function where this program starts execution


def draw_canvas():
   
   # set the dimensions of the game grid
   global grid_h, grid_w, main_w
   grid_h, grid_w = 20, 12
   main_w = 18
   # set the size of the drawing canvas
   canvas_h, canvas_w = 40 * grid_h, 60 * grid_w
   stddraw.setCanvasSize(canvas_w, canvas_h)
   # set the scale of the coordinate system
   stddraw.setXscale(-0.5, grid_w + 4.5)
   stddraw.setYscale(-0.5, grid_h - 0.5)


   global  paused, game_over, restart

   paused = False
   game_over = False
   restart = False

   # display a simple menu before opening the game
   display_game_menu(grid_h, main_w,paused, game_over, restart)
   start(grid_h, grid_w, main_w, paused, game_over, restart)   

def start(grid_h, grid_w, main_w, paused, game_over, restart ):
   
 
   global grid
   grid = GameGrid(grid_h, grid_w)

   change_speed(grid_h, main_w) 

   current_tetromino = create_tetromino(grid_h, grid_w)
   grid.next_tetromino = create_tetromino(grid_h, grid_w)

   # create the game grid
   grid.current_tetromino = current_tetromino


   # the main game loop (keyboard interaction for moving the tetromino) 
   while True:
     
      # check user interactions via the keyboard
      
      if stddraw.hasNextKeyTyped():  # check if the user has pressed a key
         key_typed = stddraw.nextKeyTyped()  # the most recently pressed key

         if key_typed == "p":
      
            paused = not paused
               
         elif paused is False:
         # if the left arrow key has been pressed
            if key_typed == "left":
               # move the active tetromino left by one
               current_tetromino.move(key_typed, grid) 
            # if the right arrow key has been pressed
            elif key_typed == "right":
               # move the active tetromino right by one
               current_tetromino.move(key_typed, grid)
            # if the down arrow key has been pressed
            elif key_typed == "down":
               # move the active tetromino down by one 
               # (soft drop: causes the tetromino to fall down faster)
               current_tetromino.move(key_typed, grid)
            # clear the queue of the pressed keys for a smoother interaction
            elif key_typed == "up":
               current_tetromino.rotation(current_tetromino)

            elif key_typed == "space":# # Piece Drop
               for i in range(grid_h):
                  current_tetromino.move("down",grid)

                  
            elif key_typed=='r':
               start(grid_h, grid_w, main_w,paused, game_over, restart)
               


         stddraw.clearKeysTyped()

      # move the active tetromino down by one at each iteration (auto fall)
      if paused is False:
         success = current_tetromino.move("down", grid)

      # place the active tetromino on the grid when it cannot go down anymore
      if not success:
         # get the tile matrix of the tetromino without empty rows and columns
         # and the position of the bottom left cell in this matrix
         tiles, pos = grid.current_tetromino.get_min_bounded_tile_matrix(True)
         # update the game grid by locking the tiles of the landed tetromino
         game_over = grid.update_grid(tiles, pos)
         # end the main game loop if the game is over
         if game_over:
            gameOver(grid_h, main_w)
            start(grid_h, grid_w, main_w,paused, game_over, restart)


         # create the next tetromino to enter the game grid
         # by using the create_tetromino function defined below
         # current_tetromino = create_tetromino(grid_h, grid_w)
         index_arr, i = grid.checkFullRows(grid_h)
         grid.deleteRow_and_moveRowDown(grid_h, grid_w, index_arr, i)

         current_tetromino = grid.next_tetromino
         grid.current_tetromino = current_tetromino
         next_tetromino = create_tetromino(grid_h,grid_w)
         grid.next_tetromino = next_tetromino
         next_tetromino.draw_next_tetromino()

      if restart == True:
         start(grid_h, grid_w, main_w,paused, game_over, restart)


   
      # display the game grid and the current tetromino

      grid.merge(grid_h, grid_w)
      grid.delete_tile(grid_h, grid_w)
      grid.display(paused)

   print("Game over")
   restart = False
 

# Function for creating random shaped tetrominoes to enter the game grid
def create_tetromino(grid_height, grid_width):
   # type (shape) of the tetromino is determined randomly
   tetromino_types = [ 'I', 'O', 'Z', 'L', 'S', 'T', 'J' ]
   random_index = random.randint(0, len(tetromino_types) - 1)
   random_type = tetromino_types[random_index]
   # create and return the tetromino
   tetromino = Tetromino(random_type, grid_height, grid_width)
   
   return tetromino

# Function for displaying a simple menu before starting the game
def display_game_menu(grid_height, grid_width,paused, game_over, restart):
   # colors used for the menu
   background_color = Color(42, 69, 99)
   button_color = Color(25, 255, 228)
   text_color = Color(31, 160, 239)
   # clear the background canvas to background_color
   stddraw.clear(background_color)
   # get the directory in which this python code file is placed
   current_dir = os.path.dirname(os.path.realpath(__file__))
   # path of the image file
   img_file = current_dir + "/images/menu_image.png"
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
   stddraw.filledRectangle(button_blc_x, button_blc_y, button_w - 1, button_h)
   # display the text on the start game button
   stddraw.setFontFamily("Arial")
   stddraw.setFontSize(25)
   stddraw.setPenColor(text_color)


      
      
   text_to_display = "Click Here to Start the Game"
   stddraw.text(img_center_x, 5, text_to_display)
   while True:
           stddraw.show(50)
           if stddraw.mousePressed():
            # get the x and y coordinates of the location at which the mouse has 
            # most recently been left-clicked  
            mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
            # check if these coordinates are inside the button
            if mouse_x >= button_blc_x and mouse_x <= button_blc_x + button_w:
                  # change_speed(background_color, button_color, text_color, img_file, grid, grid_height, grid_width)
                  if mouse_y >= button_blc_y and mouse_y <= button_blc_y + button_h: 
                     break # break the loop to end the method and start the game
                  


def gameOver(grid_height, grid_width):


   stddraw.clear(Color(42, 69, 99))
   current_dir = os.path.dirname(os.path.realpath(__file__))
   # path of the image file
   img_file = current_dir + "/images/menu_image.png"
   img_center_x, img_center_y = (grid_width - 1) / 2, grid_height - 7
   image_to_display = Picture(img_file)
   stddraw.picture(image_to_display, img_center_x, img_center_y)
   button_w, button_h = grid_width - 1.5, 2
   button_blc_x, button_blc_y = img_center_x - button_w / 2, 4

   stddraw.setPenColor(Color(25, 255, 228))
   stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)

   stddraw.setFontFamily("Arial")
   stddraw.setFontSize(30)
   stddraw.setPenColor(Color(31, 160, 239))
   stddraw.text(img_center_x, 9, "Game Over")
   
   stddraw.setFontSize(25)
   stddraw.text(img_center_x, 3, "Score : " + str(grid.score))
   stddraw.text(img_center_x, 5, "Try Again")

   while True:
      stddraw.show(50)
      if stddraw.mousePressed():
         mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
         if mouse_x >= button_blc_x and mouse_x <= button_blc_x + button_w:
            if mouse_y >= button_blc_y and mouse_y <= button_blc_y + button_h:
               grid.game_over = False
               break

            
def change_speed(grid_height, grid_width):
   
   
        stddraw.clear(Color(42, 69, 99))
        current_dir = os.path.dirname(os.path.realpath(__file__))
        # path of the image file
        img_file = current_dir + "/images/menu_image.png"
        # center coordinates to display the image
        img_center_x, img_center_y = (grid_width - 1) / 2, grid_height - 7
        # image is represented using the Picture class
        image_to_display = Picture(img_file)
        # display the image
        stddraw.picture(image_to_display, img_center_x, img_center_y)
        # dimensions of the start game button
        button_w, button_h = grid_width - 13.5, 2
        stddraw.setPenColor(Color(25, 255, 228))
        # coordinates of the bottom left corner of the start game button
        button1_blc_x, button1_blc_y = img_center_x - button_w / 2, 4
        button2_blc_x, button2_blc_y = button1_blc_x - 5, 4
        button3_blc_x, button3_blc_y = button1_blc_x + 5, 4

        stddraw.filledRectangle(button1_blc_x, button1_blc_y, button_w, button_h)
        stddraw.filledRectangle(button2_blc_x, button2_blc_y, button_w, button_h)
        stddraw.filledRectangle(button3_blc_x, button3_blc_y, button_w, button_h)
        stddraw.setPenColor(Color(25, 255, 228))
        
        stddraw.setFontFamily("Arial")
        stddraw.setFontSize(25)
        stddraw.setPenColor(Color(31, 160, 239))

        stddraw.text(img_center_x - 5, 5, "I'm too young to die")
        stddraw.text(img_center_x, 5, "Hurt me plenty")
        stddraw.text(img_center_x + 5, 5, "Nightmare!")

        while True:
            # display the menu and wait for a short time (50 ms)
            stddraw.show(50)
            # check if the mouse has been left-clicked
            if stddraw.mousePressed():

                mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()

                if mouse_x >= button1_blc_x and mouse_x <= button1_blc_x + button_w:
                    if mouse_y >= button1_blc_y and mouse_y <= button1_blc_y + button_h:
                        grid.normal_speed = 150
                        break

                if mouse_x >= button2_blc_x and mouse_x <= button2_blc_x + button_w:
                    if mouse_y >= button2_blc_y and mouse_y <= button2_blc_y + button_h:
                        grid.normal_speed = 250
                        break
                    
                if mouse_x >= button3_blc_x and mouse_x <= button3_blc_x + button_w:
                    if mouse_y >= button3_blc_y and mouse_y <= button3_blc_y + button_h:
                        grid.normal_speed = 100 
                        break


# start() function is specified as the entry point (main function) from which 
# the program starts execution
if __name__== '__main__':
   draw_canvas()
   start(grid_h, grid_w, main_w, paused, game_over, restart)
import pygame, time
from pygame.locals import *
from pytmx.util_pygame import load_pygame

pygame.init() #starts the graphics system

#setting up starting game variables
    #starting position
x = 143 
y = 140 

    #integers
chips = 0 
health = 100
level = 1

    #lists
inventory = []
immunity = []

    #floats
health_water = 100.0
health_lava =  100.0

left = False
right = False

#imports the font used
helvetica = pygame.font.SysFont("Helvetica", 20) 

#contains the window's attributes
window = pygame.display.set_mode((700,700)) #sets the game window to 700 by 700 pixels
pygame.display.set_caption("CMSC 11 Machine Problem") #sets the name of the game window
clock = pygame.time.Clock() #variable that helps with setting up the frame rate 

#music and sfx
pygame.mixer.music.load("Bgmusic.mp3") #bg music
pygame.mixer.music.play(-1) #loops the music 
coin_sfx = pygame.mixer.Sound("Coins.wav") #chips sfx
key_sfx = pygame.mixer.Sound("Keys.wav") #keys sfx
gem_sfx = pygame.mixer.Sound("Gems.wav") #immunity item sfx
door_sfx = pygame.mixer.Sound("Locks.wav") #unlocking locks sfx

#character walking animation
walk_right = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png'), pygame.image.load('R10.png'), pygame.image.load('R11.png')]
walk_right = [pygame.transform.scale(image, (25, 35)) for image in walk_right]
walk_left = [ pygame.transform.flip(image, True, False) for image in walk_right ]
stand = pygame.image.load('standing.png')
stand = pygame.transform.scale(stand, (25, 35))

walk_count = 0 #counts the number of frames when character is walking

#description:
    #draws the images in walk_right, walk_left, and left to the character to make it look like an animation
    #there are 11 images per walk_right and walk_left, and we want to load each image for three frames each
#arguments:
    #walk_left: gets and draws the images of the character walking to the left
    #walk_right: gets and draws the images of the character walking to the right
    #stand: gets and draws the image of the character standing
#returns:
    #returns no value, but calling the function will draw the character to the game window
def redraw_game_window(walk_left, walk_right, stand):
    global walk_count
      
    if walk_count + 1 >= 33: #the upper limit of the walk_count variable
        walk_count = 0 
        
    if left:  
        window.blit(walk_left[walk_count//3], (x,y))
        walk_count += 1                          
    elif right:
        window.blit(walk_right[walk_count//3], (x,y))
        walk_count += 1
    else:
        window.blit(stand, (x, y))
        walk_count = 0


#definition of terms:
        #blit - draw images to the screen

#description:
    #loads the map from the tmx file by blitting each tile to the window
#arguments:
    #window: this is where the tiles will be blitted to/ this is where the map will load
    #tmxdata: contains the data needed to load the map
    #world_offset: this makes sure that tiles outside the window frame (since maps are bigger than the window) will still be blitted once the character steps into them
#returns:
    #returns no value, but calling the function will blit all tiles to the window
def blit_all_tiles(window, tmxdata, world_offset):
    for layer in tmxdata: #blit all layers
        for tile in layer.tiles(): #blit all tiles in all layers
            img = pygame.transform.scale(tile[2], (35,35)) #transforms the pixels of the tiles to 35, 35
            x_pixel = tile[0] * 35 + world_offset[0] #x axis
            y_pixel = tile[1] * 35 + world_offset[1] #y axis
            window.blit( img, (x_pixel, y_pixel)) #blits them to the window

#description:
    #gets the properties of each tile
#arguments:
    #tmxdata: to get the data from the .tmx file (map)
    #x and y: to get the current position of the character
    #world_offset: this makes sure that tiles outside the window frame (since maps are bigger than the window) will still have their properties taken once the character steps into them
#returns:
    #returns the properties of a specific tile
    #return type may differ depending on what kind ot tile it is
    #propeties may be an integer (chips, health, id), a float (health_lava, health_water), or a string (provides, requires)
def get_tile_properties(tmxdata, x , y, world_offset):
    world_x = x - world_offset[0]
    world_y = y - world_offset[1]
    tile_x = world_x // 35
    tile_y = world_y // 35
    layer = tmxdata.layers[1] 
    try:
        properties = tmxdata.get_tile_properties(tile_x, tile_y, 1)
    except ValueError:
        properties = {"id": -1, "chips":0, "health":0, "health_lava":0, "health_water":0, "provides":"", "requires":"", "walls":0}
    if properties is None:
        properties = {"id": -1, "chips":0, "health":0, "health_lava":0, "health_water":0, "provides":"", "requires":"", "walls":0}
    properties['x'] = tile_x #y coordinate of a particular tile (where the player is standing)
    properties['y'] = tile_y #y coordinate of a particular tile (where the player is standing)
    return properties

#loads the level 1 map
tmxdata = load_pygame("level1.tmx")
world_offset = [0, 0] #starts the map with 0,0 position

#The main loop
#This contains all conditions the character needs to meet when the game is running.
#Failure to meet these conditions would end the game.

running = True
while running:
    pygame.time.delay(50) #pauses every movement in the program for 50 milliseconds
    window.fill((0, 0, 0)) #fills the screen with the color black
    blit_all_tiles(window, tmxdata, world_offset)  

    #displays captions to the window
    display_chips_needed = helvetica.render("Collect 10 chips to pass the level!", 1, (255,255,255)) #writes caption in preferred font
    window.blit(display_chips_needed, (225, 10)) #blits caption to the window

    display_chips = helvetica.render(f"Chips collected: {chips}", 1, (255,255,255)) 
    window.blit(display_chips, (30, 30))  

    display_keys = helvetica.render(f"Keys Collected: {inventory}", 1, (255,255,255)) 
    window.blit(display_keys, (30, 50))
    
    display_immunity_item = helvetica.render(f"Immunity Item: {immunity}", 1, (255,255,255)) 
    window.blit(display_immunity_item, (30, 70))  

    #loop that ends the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #character movement by pressing WASD or arrow keys
    if pygame.key.get_pressed()[K_w] or pygame.key.get_pressed()[K_UP]: #if user presses W or up arrow key
        top_tile = get_tile_properties(tmxdata, x+17, y-10, world_offset) #get tile properties of the tile above the character

        #if top tile is not solid, the character can move upwards
        if top_tile['walls'] == 0: 
            y -=10

        #cannot press left and right simultaneously
        left = False 
        right = True
            

    elif pygame.key.get_pressed()[K_s] or pygame.key.get_pressed()[K_DOWN]: #S or down arrow key
        bottom_tile = get_tile_properties(tmxdata, x+12, y+45, world_offset)
        if bottom_tile['walls'] == 0:
            y +=10
        left = True
        right = False
    
                 
    elif pygame.key.get_pressed()[K_a] or pygame.key.get_pressed()[K_LEFT]: #A or left arrow key
        left_tile = get_tile_properties(tmxdata, x-10, y+17, world_offset)
        if left_tile['walls'] == 0:
            x -=10
        left = True
        right = False
        
            
    elif pygame.key.get_pressed()[K_d] or pygame.key.get_pressed()[K_RIGHT]: #D or right arrow key
        right_tile = get_tile_properties(tmxdata, x+25, y+17, world_offset)
        if right_tile['walls'] == 0:
            x +=10
        left = False
        right = True

    else: #if not pressing anything
        left = False
        right = False
        walkCount = 0

    #gets properties of collectibles when character approaches them
    touching = get_tile_properties(tmxdata, x+10, y+17, world_offset)

    #gets properties of locks when character approaches them 
    touching_lockleft = get_tile_properties(tmxdata, x-10, y+17, world_offset) #left
    touching_lockright = get_tile_properties(tmxdata, x+25, y+17, world_offset) #right
    touching_lockup = get_tile_properties(tmxdata, x+17, y-10, world_offset) #up
    touching_lockdown = get_tile_properties(tmxdata, x+12, y+45, world_offset) #down

    #chips
    chips += touching['chips'] #if character touches the chips, add 1 to chips variable
    if touching['id'] == 0: #id number of chips
        tile_x = touching['x']
        tile_y = touching['y']
        tmxdata.layers[1].data[tile_y][tile_x] = 0 #removes the chips when player collects it
        coin_sfx.play()
        
    #health for theif tile
    health += touching['health']
    if health < 0:
        running = False

    #health for lava
    health_lava += touching['health_lava']
    if health_lava < 0:
        running = False

    #health for water
    health_water += touching['health_water']
    if health_water < 0:
        running = False

    #sliding tile
    if touching['id'] == 26: #id number of left sliding tile
        x -=20 

    if touching['id'] == 27: #id number of right sliding tile
        x += 20

    #immunity items
        #if character attains water immunity item, set "health for water" to infinity
    if touching['provides'] == "Water": 
        health_water = float('inf')
        health_lava = 100.0
        tile_x = touching['x']
        tile_y = touching['y']
        gem_sfx.play()

        #if the character has an existing immunity item, remove the item from the inventory 
        if immunity != []:
            immunity.pop()

        #adds the water immunity item to the inventory
        immunity.append(touching['provides'])
        tmxdata.layers[1].data[tile_y][tile_x] = 0

    if touching['provides'] == "Lava":
        health_lava = float('inf')
        health_water = 100.0
        tile_x = touching['x']
        tile_y = touching['y']
        gem_sfx.play()

        if immunity != []:
            immunity.pop()

        immunity.append(touching['provides'])
        tmxdata.layers[1].data[tile_y][tile_x] = 0
    

    #keys
    if touching['provides'] == "Blue" or touching['provides'] == "Red" or touching['provides'] == "Yellow" or touching['provides'] == "Green": #if character touches the keys
        tile_x = touching['x']
        tile_y = touching['y']
        inventory.append(touching['provides']) #adds the keys to the inventory
        tmxdata.layers[1].data[tile_y][tile_x] = 0 #removes the keys when player collects it
        key_sfx.play()

    #locks
    if touching_lockleft['requires'] != "": #if the lock from the left of the character requires the keys
        tile_x = touching_lockleft['x']
        tile_y = touching_lockleft['y']
        if touching_lockleft['requires'] in inventory:
            if touching_lockleft['requires'] == "Red":
                tmxdata.layers[1].data[tile_y][tile_x] = 0 #the lock from the left requires the red key. given you have collected the red key, remove the red lock from the map
                door_sfx.play()
            if touching_lockleft['requires'] == "Blue":
                tmxdata.layers[1].data[tile_y][tile_x] = 0 #lock from the left requires blue key
                door_sfx.play()
            if touching_lockleft['requires'] == "Yellow":
                tmxdata.layers[1].data[tile_y][tile_x] = 0 #lock from the left requires yellow key
                door_sfx.play()
            if touching_lockleft['requires'] == "Green":
                tmxdata.layers[1].data[tile_y][tile_x] = 0 #lock from the left requires green key
                door_sfx.play()

    if touching_lockright['requires'] != "": #lock from the right of the character
        tile_x = touching_lockright['x']
        tile_y = touching_lockright['y']
        if touching_lockright['requires'] in inventory:
            if touching_lockright['requires'] == "Red":
                tmxdata.layers[1].data[tile_y][tile_x] = 0
                door_sfx.play()
            if touching_lockright['requires'] == "Blue":
                tmxdata.layers[1].data[tile_y][tile_x] = 0
                door_sfx.play()
            if touching_lockright['requires'] == "Yellow":
                tmxdata.layers[1].data[tile_y][tile_x] = 0
                door_sfx.play()
            if touching_lockright['requires'] == "Green":
                tmxdata.layers[1].data[tile_y][tile_x] = 0
                door_sfx.play()

    if touching_lockup['requires'] != "": #lock from above the character
        tile_x = touching_lockup['x']
        tile_y = touching_lockup['y']
        if touching_lockup['requires'] in inventory:
            if touching_lockup['requires'] == "Red":
                tmxdata.layers[1].data[tile_y][tile_x] = 0
                door_sfx.play()
            if touching_lockup['requires'] == "Blue":
                tmxdata.layers[1].data[tile_y][tile_x] = 0
                door_sfx.play()
            if touching_lockup['requires'] == "Yellow":
                tmxdata.layers[1].data[tile_y][tile_x] = 0
                door_sfx.play()
            if touching_lockup['requires'] == "Green":
                tmxdata.layers[1].data[tile_y][tile_x] = 0
                door_sfx.play()
                
    if touching_lockdown['requires'] != "": #lock from below the character
            tile_x = touching_lockdown['x']
            tile_y = touching_lockdown['y']
            if touching_lockdown['requires'] in inventory:
                if touching_lockdown['requires'] == "Red":
                    tmxdata.layers[1].data[tile_y][tile_x] = 0
                    door_sfx.play()
                if touching_lockdown['requires'] == "Blue":
                    tmxdata.layers[1].data[tile_y][tile_x] = 0
                    door_sfx.play()
                if touching_lockdown['requires'] == "Yellow":
                    tmxdata.layers[1].data[tile_y][tile_x] = 0
                    door_sfx.play()
                if touching_lockdown['requires'] == "Green":
                    tmxdata.layers[1].data[tile_y][tile_x] = 0
                    door_sfx.play()
                    
    #loads levels
    if touching['id'] == 1: #id number for the exit door
        if chips == 10: #only enter the exit door when all chips are collected
            level += 1 #when entering the exit door, add 1 to level
            if level == 2:
               tmxdata = load_pygame("level2.tmx")

               #sets variables to starting positions
               world_offset = [0, 0]
               chips = 0
               inventory =[]
               immunity = []
               provides = ""
               x = 143
               y = 143

            if level == 3:
               tmxdata = load_pygame("level3.tmx")
               world_offset = [0, 0]
               chips = 0
               inventory =[]
               immunity = []
               provides = ""
               x = 143
               y = 143

            if level == 4:
               tmxdata = load_pygame("level4.tmx")
               world_offset = [0, 0]
               chips = 0
               inventory =[]
               immunity = []
               provides = ""
               x = 143
               y = 143

            if level == 5:
               tmxdata = load_pygame("youwin.tmx")
               world_offset = [0, 0]
               chips = 0
               inventory =[]
               immunity = []
               provides = ""
               x = 0
               y = 0


    #lets the character move around the world (camera follows the character)
    if y < 100: #if character's y-position is less than 100
        y = 100 #set the character's y-position to 100
        world_offset[1] +=20 #y-value of the world offset will add 20 to itself in order for the world to keep up with the character

    if y > 600:
        y = 600
        world_offset[1] -=20

    if x < 100: 
        x = 100
        world_offset[0] +=20

    if x > 600:
        x = 600
        world_offset[0] -=20

    redraw_game_window(walk_left, walk_right, stand) 
    pygame.display.update() #updates the window
    clock.tick(33) #runs at 33 frames per second
    
pygame.quit()                              
    

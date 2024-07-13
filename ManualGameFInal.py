import pygame
import sys
import copy
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import os
import random

no_of_success = []
x_length_of_world = 60
y_length_of_world = 60
world = [[0 for _ in range(y_length_of_world)] for _ in range(x_length_of_world)]
for i in range(5):
    world[random.randint(0, 59)][random.randint(20, 40)] = 5
organisms = []
color_names = [(255, 255, 255), (255, 255, 0), (0, 255, 0), (0, 0, 255), (165, 42, 42), (0, 0, 0)]


def initial_body_positioner (position):
    #input: position in world (row,column)
    #process: creates inital body at position entered    
    x_posi = position[0]
    y_posi = position[1]
    world[x_posi][y_posi] = 1
    world[x_posi][y_posi+1] = 2
    world[x_posi][y_posi-1] = 3
    world[x_posi+1][y_posi] = 4
    world[x_posi-1][y_posi] = 4

def printworld():
    #process: prints current world
    # color_names = ['white', 'yellow', 'green', 'blue', 'brown', 'black'] #add 'red' at the end of array when 6 is used
    # cmap = colors.ListedColormap(color_names)
    # plt.imshow(world, cmap=cmap, interpolation='nearest')
    # plt.show()
    print("----------------------------------------------")
    for row in world:
        print(row)
    print('-----------------------------------------------')
         
def map_colors(array, color_names):
    color_array = []
    for row in array:
        color_row = []
        for number in row:
            if number < len(color_names):
                color_row.append(color_names[number])
            else:
                color_row.append((255, 0, 0))  # If the number is 6 or higher, map to 'red'
        color_array.append(color_row)
    return color_array

def add_arrays_1d(array1, array2):
    #input: two 1d array of same length
    #output: array made by adding corresponding elements of the two entered arrays
    length = len(array1)
    result = [0] * length   
    for i in range(length):
        result[i] = array1[i] + array2[i]
    return result

def max_position_finder_2d_matrix(matrix):
    max_value = float('-inf')
    max_position = [0, 0]
    for i, row in enumerate(matrix):
        for j, value in enumerate(row):            
            if value > max_value:
                max_value = value
                max_position = [i, j]
    return max_position

def body_positioner(old_position, new_position, old_body, new_body):
    #input: old position (row,column) and new position in world (row,column) and body of organism
    #process: removes original body and creates organism's body at position entered       
    for element in old_body:
        actual_element_position = add_arrays_1d(element[0], old_position)
        world[actual_element_position[0]][actual_element_position[1]] = 0
    for element in new_body:
        new_element_position = add_arrays_1d(element[0], new_position)
        world[new_element_position[0]][new_element_position[1]] = element[1]

def single_body_positioner(body):
    #input: body of organism
    #output: organism in middle of 9*9 array
    single_organism_world = [[0 for _ in range(9)] for _ in range(9)]
    for element in body:
        new_element_position = add_arrays_1d(element[0], [4,4])
        single_organism_world[new_element_position[0]][new_element_position[1]] = element[1]
    return single_organism_world

def rotate_90_clockwise(vector):
    return [vector[1], -vector[0]]

def rotate_90_anticlockwise(vector):
    return [-vector[1], vector[0]]

def find_num_of_legs(organism):
    no_of_legs = 0
    for element in organism.body:
        if element[1] == 3:
            no_of_legs += 1
    return no_of_legs

def list_to_evolution_caller(list):
    #input: list of numbers that are of form (displacement_of_x_from center, displacement_of_y_from_center, type_to_add, ..same_format_repetation... )
    #process: calls evolution method according to input
    for i in range(len(list)//3):
        matrix = [[0 for _ in range(7)] for _ in range(7)]
        matrix[3+list[1 + i*3]][3+list[0 + i*3]] = 1
        Ram.evolve(matrix, list[2+ i*3])

def list_to_evolution_caller2(list):
    #input: list of numbers that are of form (displacement_of_x_from center, displacement_of_y_from_center, type_to_add, ..same_format_repetation... )
    #process: calls evolution method according to input
    for i in range(len(list)//3):
        matrix = [[0 for _ in range(7)] for _ in range(7)]
        matrix[3+list[1 + i*3]][3+list[0 + i*3]] = 1
        Shyam.evolve(matrix, list[2+ i*3])

class Organism:
    def __init__(self, position):
        self.energy = 0        
        self.position = position
        x_posi = position[0]
        y_posi = position[1]
        self.body = [[[0, 0], 1],[[0, -1], 3],[[0, 1], 2],[[-1, 0], 4],[[1, 0], 4]]
        initial_body_positioner(position)   
        organisms.append(self)     
    
    def move(self, direction_and_turn_array):
        #input: 1d array of 12 length(make sure all positive), first 9 element for direction, last 3 for turn
        #process: dosent move if 0, moves the organism in direction entered starting from 12 o'clock clockwise form 1 to 8 and dont turn or else self.body change and if 0 turn anticlock if 1, clockwise if 2 
        
            max_value = max(direction_and_turn_array[:9])
            direction = direction_and_turn_array.index(max_value)
            if direction_and_turn_array[9]>=direction_and_turn_array[10] and direction_and_turn_array[9]>=direction_and_turn_array[11]:
                turn = 0
            elif direction_and_turn_array[10]>direction_and_turn_array[11]:
                turn = 1
            else:
                turn = 2
            
            old_position = self.position.copy()
            if direction == 0:
                pass
            elif direction == 1:            
                self.position = [self.position[0]-1, self.position[1]]
            elif direction == 2:            
                self.position = [self.position[0] - 1, self.position[1] + 1]
            elif direction == 3:            
                self.position = [self.position[0], self.position[1] + 1]
            elif direction == 4:            
                self.position = [self.position[0] + 1, self.position[1] + 1]
            elif direction == 5:            
                self.position = [self.position[0] + 1, self.position[1]]
            elif direction == 6:            
                self.position = [self.position[0] + 1, self.position[1] - 1]
            elif direction == 7:            
                self.position = [self.position[0], self.position[1] - 1]
            elif direction == 8:            
                self.position = [self.position[0] - 1, self.position[1] - 1]
            else:
                print("Invalid direction. Please enter a number from 1 to 8.")        
            
            old_body = copy.deepcopy(self.body)                       
            if turn == 0:
                pass
            elif turn == 2:                
                new_body_positions = []
                for element in self.body:
                    new_body_positions.append(rotate_90_clockwise(element[0]))
                for i in range(0,len(self.body)):
                    self.body[i][0] = new_body_positions[i]                             
            else:                
                new_body_positions = []
                for element in self.body:
                    new_body_positions.append(rotate_90_anticlockwise(element[0]))            
                for i in range(0,len(self.body)):
                    self.body[i][0] = new_body_positions[i]                
            
            invalid_move = False
            for element in old_body:
                actual_element_position = add_arrays_1d(element[0], old_position)
                world[actual_element_position[0]][actual_element_position[1]] = 0
            for element in self.body:    
                if add_arrays_1d(element[0], self.position)[0]<0 or add_arrays_1d(element[0], self.position)[1]<0 or add_arrays_1d(element[0], self.position)[0]>=x_length_of_world or add_arrays_1d(element[0], self.position)[1]>=y_length_of_world:   
                    invalid_move = True
                    break         
                if world[add_arrays_1d(element[0], self.position)[0]][add_arrays_1d(element[0], self.position)[1]]!=0:
                    invalid_move = True                    
                    if world[add_arrays_1d(element[0], self.position)[0]][add_arrays_1d(element[0], self.position)[1]]==5:
                        if element[1] == 2: 
                            muscle_count = 0
                            for element1 in  self.body:
                                if element1[1] == 4:
                                    muscle_count += 1
                            if self.energy < muscle_count:                                
                                self.energy += 1
                                world[add_arrays_1d(element[0], self.position)[0]][add_arrays_1d(element[0], self.position)[1]]=0
                    if element[1] == 6:
                        #still left to make death when hit brain and update accordingly in main function(pop the organism from organism list)
                        point_of_attack = [add_arrays_1d(element[0], self.position)[0],add_arrays_1d(element[0], self.position)[1]] 
                        if world[point_of_attack[0]][point_of_attack[1]] == 6:
                            break

                        
                        
                        for organism in organisms:
                            if organism != self:
                                for element in organism.body:
                                    if add_arrays_1d(element[0], organism.position) == point_of_attack: 
                                        if element[1] == 1:
                                            for element in organism.body:
                                                world[add_arrays_1d(element[0], organism.position)[0]][add_arrays_1d(element[0], organism.position)[1]] = 5
                                            organism.body.clear()                                      
                                        else:
                                            organism.body.remove(element)                                        
                        
                        world[point_of_attack[0]][point_of_attack[1]] =5
                                        

                                    


            if invalid_move:                           
                self.body = copy.deepcopy(old_body)
                self.position = old_position.copy()                
                  
            body_positioner(old_position, self.position, old_body, self.body)
    
    def evolve(self, list_of_position_value_in_single_organism_world, type):
        #input: position value (7*7 matrix) (make sure all positive), type to attach (0 to 6)
        #process: changes self.body and the way it looks in world  
        old_body = self.body      
        single_body_world = single_body_positioner(self.body)        
        for i in range(1,8):
            for j in range(1,8):
                if single_body_world[i][j] != 0:
                    list_of_position_value_in_single_organism_world[i-1][j-1] = 0
                if single_body_world[i+1][j] == 0 and single_body_world[i-1][j] == 0 and single_body_world[i][j+1] == 0 and single_body_world[i][j-1] == 0 and single_body_world[i+1][j+1] == 0 and single_body_world[i+1][j-1] == 0 and single_body_world[i-1][j+1] == 0 and single_body_world[i-1][j-1] == 0:
                    list_of_position_value_in_single_organism_world[i-1][j-1] = 0         
        position_to_add_type = add_arrays_1d(max_position_finder_2d_matrix(list_of_position_value_in_single_organism_world), [-3,-3])
        self.body.append([position_to_add_type, type])
        print(self.body)
        body_positioner(self.position, self.position, old_body, self.body)
    
    def scan(self):
        #output: array of type and distance starting from 12 oclock direction clockwise
        type_distance = []
        for direction in [[-1,0], [-1,1], [0,1],[1,1], [1,0], [1,-1],[0,-1],[-1,-1]]:  
            distance= 1
            while True:                
                inbody = False
                for element in self.body:
                    if element[0] == [distance*direction[0],distance*direction[1]]:
                        inbody = True
                x = add_arrays_1d(self.position, [distance*direction[0],distance*direction[1]])[0]
                y = add_arrays_1d(self.position, [distance*direction[0],distance*direction[1]])[1]
                if world[x][y] != 0 and (not inbody):
                    type_distance.append(world[x][y])
                    type_distance.append(distance)
                    break
                distance += 1
                x = add_arrays_1d(self.position, [distance*direction[0],distance*direction[1]])[0]
                y = add_arrays_1d(self.position, [distance*direction[0],distance*direction[1]])[1]
                if x<0 or y<0 or x>=x_length_of_world or y>=y_length_of_world:
                    type_distance.append(0)
                    type_distance.append(distance)
                    break
        return type_distance

Ram = Organism([30,8])
Shyam = Organism([30,52])


pygame.init()
width, height = 800, 650
SCREEN_WIDTH, SCREEN_HEIGHT = 800,650
screen = pygame.display.set_mode((width, height))
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_SIZE = 20
font = pygame.font.SysFont('Arial', FONT_SIZE)

# Function to display opening screen
def display_opening_screen(screen):
    screen.fill(WHITE)
    
    # Display title
    title_text = font.render('K_Up/W: up, K_Down/S: down, K_Left/A: left, K_Right/D: right', True, BLACK)
    screen.blit(title_text, ((SCREEN_WIDTH - title_text.get_width()) // 2, 50))
    title_text2 = font.render('up and down at once for clockwise rotation, right and left at once for anticlockwise rotation',True,BLACK)
    screen.blit(title_text2, ((SCREEN_WIDTH - title_text2.get_width()) // 2, 90))    
    
    # Display instructions
    instructions_text = font.render('Enter a list of numbers separated by spaces for evolution of left then right:', True, BLACK)
    screen.blit(instructions_text, ((SCREEN_WIDTH - instructions_text.get_width()) // 2, 200))
    
    pygame.display.flip()

# Function to get user input
def get_user_input(screen):
    input_box = pygame.Rect((SCREEN_WIDTH - 300) // 2, 250, 300, 40)
    input_text = ''
    input_active = True

    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    try:
                        numbers = list(map(int, input_text.split()))
                        return numbers
                    except ValueError:
                        print("Invalid input. Please enter numbers separated by spaces.")
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode        
        
        pygame.draw.rect(screen, BLACK, input_box, 2)
        text_surface = font.render(input_text, True, BLACK)
        screen.blit(text_surface, (input_box.x + 5, input_box.y + 10))    
        pygame.display.flip()   
   
# Function to start the game with user input
def start_game(numbers):
    global color_names
    global world
    global array
    array = map_colors(world, color_names)    
    screen.fill(BLACK)
    print("Starting game with numbers:", numbers)
    clock = pygame.time.Clock()

    # Function to draw the 2D array
    def draw_array():
        cell_size = 10
        for i, row in enumerate(array):
            for j, color in enumerate(row):
                pygame.draw.rect(screen, color, (j * cell_size, i * cell_size, cell_size, cell_size))

    # Function to change the array
    def go_up():
        global array        
        Ram.move([0,1,0,0,0,0,0,0,0,0,0,0])                
        array = map_colors(world, color_names)                   
    def go_down():
        global array
        Ram.move([0,0,0,0,0,1,0,0,0,0,0,0])
        array = map_colors(world, color_names)   
    def go_left():
        global array
        Ram.move([0,0,0,0,0,0,0,1,0,0,0,0])
        array = map_colors(world, color_names)   
    def go_right():
        global array
        Ram.move([0,0,0,1,0,0,0,0,0,0,0,0])
        array = map_colors(world, color_names)  
    def go_up_right():
        global array
        Ram.move([0,0,1,0,0,0,0,0,0,0,0,0])
        array = map_colors(world, color_names)  
    def go_right_down():
        global array
        Ram.move([0,0,0,0,1,0,0,0,0,0,0,0])
        array = map_colors(world, color_names)  
    def go_down_left():
        global array
        Ram.move([0,0,0,0,0,0,1,0,0,0,0,0])
        array = map_colors(world, color_names)  
    def go_left_up():
        global array
        Ram.move([0,0,0,0,0,0,0,0,1,0,0,0])
        array = map_colors(world, color_names)  
    def go_clockwise():
        global array
        Ram.move([0,0,0,0,0,0,0,0,0,0,1,0])
        array = map_colors(world, color_names) 
    def go_anticlockwise():
        global array
        Ram.move([0,0,0,0,0,0,0,0,0,0,0,1])
        array = map_colors(world, color_names) 

    def go_up2():
        global array
        Shyam.move([0,1,0,0,0,0,0,0,0,0,0,0])
        array = map_colors(world, color_names)    
    def go_down2():
        global array
        Shyam.move([0,0,0,0,0,1,0,0,0,0,0,0])
        array = map_colors(world, color_names)   
    def go_left2():
        global array
        Shyam.move([0,0,0,0,0,0,0,1,0,0,0,0])
        array = map_colors(world, color_names)   
    def go_right2():
        global array
        Shyam.move([0,0,0,1,0,0,0,0,0,0,0,0])
        array = map_colors(world, color_names)  
    def go_up_right2():
        global array
        Shyam.move([0,0,1,0,0,0,0,0,0,0,0,0])
        array = map_colors(world, color_names)  
    def go_right_down2():
        global array
        Shyam.move([0,0,0,0,1,0,0,0,0,0,0,0])
        array = map_colors(world, color_names)  
    def go_down_left2():
        global array
        Shyam.move([0,0,0,0,0,0,1,0,0,0,0,0])
        array = map_colors(world, color_names)  
    def go_left_up2():
        global array
        Shyam.move([0,0,0,0,0,0,0,0,1,0,0,0])
        array = map_colors(world, color_names)  
    def go_clockwise2():
        global array
        Shyam.move([0,0,0,0,0,0,0,0,0,0,1,0])
        array = map_colors(world, color_names) 
    def go_anticlockwise2():
        global array
        Shyam.move([0,0,0,0,0,0,0,0,0,0,0,1])
        array = map_colors(world, color_names) 
        
    def handle_events():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

    def handle_continuous_keys(keys):
        if keys[pygame.K_UP] and keys[pygame.K_RIGHT]:
            go_up_right()
        if keys[pygame.K_RIGHT] and keys[pygame.K_DOWN]:
            go_right_down()
        if keys[pygame.K_DOWN] and keys[pygame.K_LEFT]:
            go_down_left()
        if keys[pygame.K_LEFT] and keys[pygame.K_UP]:
            go_left_up()
        if keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]:
            go_anticlockwise()
        if keys[pygame.K_DOWN] and keys[pygame.K_UP]:
            go_clockwise()
        if keys[pygame.K_UP]:
            go_up()
        if keys[pygame.K_DOWN]:
            go_down()
        if keys[pygame.K_RIGHT]:
            go_right()
        if keys[pygame.K_LEFT]:
            go_left()

    def handle_continuous_keys2(keys):
        if keys[pygame.K_w] and keys[pygame.K_d]:
            go_up_right2()
        if keys[pygame.K_d] and keys[pygame.K_s]:
            go_right_down2()
        if keys[pygame.K_s] and keys[pygame.K_a]:
            go_down_left2()
        if keys[pygame.K_a] and keys[pygame.K_w]:
            go_left_up2()
        if keys[pygame.K_a] and keys[pygame.K_d]:
            go_anticlockwise2()
        if keys[pygame.K_s] and keys[pygame.K_w]:
            go_clockwise2()
        if keys[pygame.K_w]:
            go_up2()
        if keys[pygame.K_s]:
            go_down2()
        if keys[pygame.K_d]:
            go_right2()
        if keys[pygame.K_a]:
            go_left2()
                
    # Main game loop
    running = True
    while running:        
        running = handle_events()        
        keys = pygame.key.get_pressed()        
        handle_continuous_keys(keys)    
        handle_continuous_keys2(keys)  
        # Draw the 2D array
        draw_array()
        # Update the display
        pygame.display.flip()
        clock.tick(10)
    
    pygame.quit()
    sys.exit()


# Main function
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Opening Screen Example')
    
    display_opening_screen(screen)
    numbers = get_user_input(screen)
    list_to_evolution_caller(numbers)
    display_opening_screen(screen)
    numbers2 = get_user_input(screen)
    list_to_evolution_caller2(numbers2)
    start_game(numbers)
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()

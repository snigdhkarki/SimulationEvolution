import copy
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import os
import neat
import random
import pickle


no_of_success = []
no_of_success_eating = []
x_length_of_world = 60
y_length_of_world = 60
world = [[0 for _ in range(y_length_of_world)] for _ in range(x_length_of_world)]
for i in range(100):
    world[random.randint(0, 59)][random.randint(10, 59)] = 5
organisms = []

def distance_from_closest_deadcell(grid, position):
    #input: takes in a 2d matrix representing the world and tuple representing position of organism (x,y) 
    #output: the distance from closest 5(dead cell) to organism
    rows = len(grid)
    cols = len(grid[0])
    x, y = position   
    min_distance = float('inf') 
    
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 5:
                distance = (abs(x - i)*abs(x - i) + abs(y - j)*abs(y - j))**(1/2)
                if distance < min_distance:
                    min_distance = distance

    if min_distance != float('inf'):
        return min_distance 
    else:
        raise ValueError("trying to find closest distance to 5 when there is no 5 in world")

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

# def close_plot_after_delay(delay):
#     time.sleep(delay)
#     plt.close()

def printworld():
    #process: prints current world
    color_names = ['white', 'yellow', 'green', 'blue', 'brown', 'black'] #add 'red' at the end of array when 6 is used
    cmap = colors.ListedColormap(color_names)
    plt.imshow(world, cmap=cmap, interpolation='nearest')
    # thread = threading.Thread(target=close_plot_after_delay, args=(0.4,))
    # thread.start()
    plt.show()
    
    # for row in world:
    #     print(row)

def add_arrays_1d(array1, array2):
    #input: two 1d array of same length
    #output: array made by adding corresponding elements of the two entered arrays
    length = len(array1)
    result = [0] * length   
    for i in range(length):
        result[i] = array1[i] + array2[i]
    return result

def body_positioner(old_position, new_position, old_body, new_body):
    #input: old position (row,column) and new position in world (row,column) and body of organism
    #process: removes original body and creates organism's body at position entered       
    for element in old_body:
        actual_element_position = add_arrays_1d(element[0], old_position)
        world[actual_element_position[0]][actual_element_position[1]] = 0
    for element in new_body:
        new_element_position = add_arrays_1d(element[0], new_position)
        world[new_element_position[0]][new_element_position[1]] = element[1]
        
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

def scanned_array_to_dead_array(scanned_array):
    new_scanned_array = []
    for i,element in enumerate(scanned_array):
        if (i%4==0):
            if(element == 5):
                new_scanned_array.append(scanned_array[i+1])
            if(element != 5):
                new_scanned_array.append(100)
    
    
    # if(scanned_array[3] == 1):
    #     new_scanned_array[2] = 1
    # if(scanned_array[7] == 1):
    #     new_scanned_array[0] = 1

    if(scanned_array[3] == 1):
        new_scanned_array.append(100)
    else:
        new_scanned_array.append(0)
    if(scanned_array[7] == 1):
        new_scanned_array.append(100)
    else:
        new_scanned_array.append(0)

        
    return new_scanned_array

def new_move_to_old_move(new_direction_and_turn_array):   
    max_value = max(new_direction_and_turn_array)
    max_indexes = [i for i,element in enumerate(new_direction_and_turn_array) if element == max_value]
    random_max_index = random.choice(max_indexes)
    new_direction_and_turn_array[random_max_index] +=1
    direction_and_turn_array = [0 for _ in range(12)]
    i=1
    for element in new_direction_and_turn_array:        
        if element<0:
            direction_and_turn_array[i] = 0
        else:
            direction_and_turn_array[i] = element
        i += 2
    return direction_and_turn_array

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
                        if self.energy < 100:                                
                            self.energy += 1
                            world[add_arrays_1d(element[0], self.position)[0]][add_arrays_1d(element[0], self.position)[1]]=0
                if element[1] == 6:
                    #still left to make death when hit brain and update accordingly in main function(pop the organism from organism list)
                    point_of_attack = [add_arrays_1d(element[0], self.position)[0],add_arrays_1d(element[0], self.position)[1]] 
                    for organism in organisms:
                        for element in organism.body:
                            if add_arrays_1d(element[0], organism.position) == point_of_attack:
                                organism.body.remove(element)
                                world[add_arrays_1d(element[0], self.position)[0]][add_arrays_1d(element[0], self.position)[1]]=5
                                


        if invalid_move:                           
            self.body = copy.deepcopy(old_body)
            self.position = old_position.copy()                
                
        body_positioner(old_position, self.position, old_body, self.body)

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

GEN = 0
show = False
def main(genomes, config):
    print(len(genomes))
    global show
    global GEN
    global world
    global organisms    
    global no_of_success
    GEN += 1
    #the corresponding values in same address refer to same organism
    nets = []  
    ge = []
    organisms_list = []
    food_eaten = [0 for _ in range(10)]
    x = 2
    y = 2 
    
    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)       
        organisms_list.append(Organism([x,y]))        
        x += 6
        g.fitness = 0        #initial fitness to 0
        ge.append(g)
    
    
    
    for turn in range(150):
        if show: 
            printworld()             
        for x, single_organism in enumerate(organisms_list):              
            for _ in range(find_num_of_legs(single_organism)):
                if show == True:
                    print(single_organism.position)
                
                input = scanned_array_to_dead_array(single_organism.scan())  
                if show == True:
                    print(single_organism.scan())
                    print(input)                      
                output = nets[organisms_list.index(single_organism)].activate(tuple(input)) 
                if show == True:
                    print(output)
                new_move = new_move_to_old_move(list(output))
                if show == True:
                    print(new_move)                 
                single_organism.move(new_move)                
            ge[x].fitness += (single_organism.energy  * 10 )/150
            
            food_eaten[x] = single_organism.energy
            if show == True:
                print(ge[x].fitness)
                print('-----------------------')
            

    
    ge_list = []
    for i in range(10):
        ge_list.append(ge[i].fitness)                   
    if any(element >100 for element in ge_list):
        show = True
    # if(GEN>10):
    #     if (no_of_success_eating[-1]+no_of_success_eating[-2]+no_of_success_eating[-3]+no_of_success_eating[-4]+no_of_success_eating[-5])/5 >30:
    #         show = True
    no_of_success.append(sum(ge_list)/len(ge_list))
    no_of_success_eating.append(sum(food_eaten))
    arr = np.array(no_of_success)
    rounded_arr = np.array([round(num, 2) for num in arr])
    print(rounded_arr)  
    print(no_of_success_eating)
    food_eaten = [0 for _ in range(10)]
    
    
    

    
    x_length_of_world = 60
    y_length_of_world = 60
    world = [[0 for _ in range(y_length_of_world)] for _ in range(x_length_of_world)]
    for i in range(100):
        world[random.randint(0, 59)][random.randint(10, 59)] = 5
    organisms = []
    
def run(config_file):    
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)    
    p = neat.Population(config)

    # to show progress and graphs
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main, 1500)     #call main func 100 times
    with open('winner_genome.pkl', 'wb') as f:
        pickle.dump(winner, f)

if __name__ == '__main__':
    # Determine path to configuration file
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'new-minimized-config-feedforward.txt')
    run(config_path) 

print(no_of_success)
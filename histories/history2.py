import copy

world = [[0 for _ in range(20)] for _ in range(20)]
organisms = []

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
    for row in world:
        print(row)
        
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


Ram = Organism([2,2])
Shyam = Organism([2,5])
# printworld()
# print("--------------------------------------------------------------------")
# # Ram.evolve([
#     [0, 0, 0, 0, 0, 2, 0],
#     [0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 2, 0, 2, 0, 0],
#     [0, 0, 0, 3, 0, 0, 0],
#     [0, 0, 0, 0, 3, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0]
# ], 3)
# printworld()
# print("--------------------------------------------------------------------")
# Ram.evolve([
#     [0, 0, 0, 0, 0, 2, 0],
#     [0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 1, 0, 2, 0, 0],
#     [0, 0, 0, 3, 0, 0, 0],
#     [0, 0, 4, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0]
# ], 4)
# printworld()

# Ram.move([0,2,3,0,1,3,0,0,0,2,3,2])
# printworld()



Ram = Organism([2,2])
Shyam = Organism([2,5])
Hari = Organism([5,2])
Hari.body.append([[0,2],6])
body_positioner(Hari.position, Hari.position, Hari.body, Hari.body)
Krishna = Organism([5,7])
printworld()
print("--------------------------------------------------------------------")
Ram.move([0,0,0,3,1,2,0,1.5,0,2,0,2])
printworld()
print("--------------------------------------------------------------------")
Hari.move([0,0,0,2,0,0,0,0,0,2,0,0])
printworld()
print("--------------------------------------------------------------------")
Hari.move([0,0,0,2,0,0,0,0,0,2,0,0])
printworld()
print("--------------------------------------------------------------------")
Krishna.move([0,0,0,0,0,0,0,2,0,2,0,0])
printworld()
print("--------------------------------------------------------------------")
Krishna.move([0,0,0,2,0,0,0,0,0,2,0,0])
Krishna.move([0,0,0,2,0,0,0,0,0,2,0,0])
printworld()
print("--------------------------------------------------------------------")
print(Hari.energy)
Hari.move([0,0,0,0,0,2,0,0,0,2,0,0])
Hari.move([0,0,0,2,0,0,0,0,0,2,0,0])
Hari.move([0,0,0,2,0,0,0,0,0,2,0,0])
Hari.move([0,2,0,0,0,0,0,0,0,2,0,0])
printworld()
print("--------------------------------------------------------------------")
print(Hari.energy)



    
    # world[2][8] = 5
    # world[2][10] = 5
    # world[2][12] = 5
    # Shyam.move([0,0,0,2,0,0,0,0,0,2,0,0])
    # printworld()  
    # print("--------------------------------------------------------------------")
    # print(Shyam.energy)
    # Shyam.move([0,0,0,2,0,0,0,0,0,2,0,0])
    # printworld()  
    # print("--------------------------------------------------------------------")
    # print(Shyam.energy)
    # Shyam.move([0,0,0,2,0,0,0,0,0,2,0,0])
    # Shyam.move([0,0,0,2,0,0,0,0,0,2,0,0])
    # Shyam.move([0,0,0,2,0,0,0,0,0,2,0,0])
    # printworld()  
    # print("--------------------------------------------------------------------")
    # print(Shyam.energy)
    # Shyam.move([0,0,0,2,0,0,0,0,0,2,0,0])
    # Shyam.move([0,0,0,2,0,0,0,0,0,2,0,0])
    # Shyam.move([0,0,0,2,0,0,0,0,0,2,0,0])
    # printworld()  
    # print("--------------------------------------------------------------------")
    # print(Shyam.energy)




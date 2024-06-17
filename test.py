import random
def scanned_array_to_dead_array(scanned_array):
    new_scanned_array = []
    for i,element in enumerate(scanned_array):
        if (i%4==0):
            if(element == 5):
                new_scanned_array.append(scanned_array[i+1])
            if(element != 5):
                new_scanned_array.append(100)
    
    
    if(scanned_array[3] == 1):
        new_scanned_array[2] = 1
    if(scanned_array[7] == 1):
        new_scanned_array[0] = 1
        
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
            direction_and_turn_array[i] = (-1)*element
        else:
            direction_and_turn_array[i] = element
        i += 2
    return direction_and_turn_array

print(scanned_array_to_dead_array([0, 2, 0, 2, 5, 8, 5, 15, 4, 6, 0, 3, 0, 3, 0, 2]))
direction_and_turn_array = [0 for _ in range(12)]
print(direction_and_turn_array)
print(new_move_to_old_move([5,5,3,-1]))
print(scanned_array_to_dead_array([5,5,1,1,5,5,5,1,3,2,4,1,5,2,3,4]))
import random
import numpy as np

def get_move(data):
    # to be called by move function in server.py
    # whenever you  make a new move function, just replace the return statement with that function call
    # more convenient than always changing server.py
    # return greedy_eat(data)
    return hueristic_approach(data)

def hueristic_approach(data):
    # moves are L, R, U, D
    # need to generate list of legal moves 
    possible_moves = ["L", "R", "U", "D"]

    #im dum and have to do this 
    convert_move = dict()
    convert_move["L"] = "left"
    convert_move["R"] = "right"
    convert_move["U"] = "up"
    convert_move["D"] = "down"

    # Can't move back into itself
    head = data['you']['body'][0]
    neck = data['you']['body'][1]
    if head['x'] == neck['x']:
        # either can't move up or down
        if head['y'] > neck['y']: # can't move down
            possible_moves.remove("D")
        else: possible_moves.remove("U")
    
    else: # then y1 == y2, can't move left or right
        if head['x'] > neck['x']: # can't move left
            possible_moves.remove("L")
        else: possible_moves.remove("R")

    # Check out of the remaining 3 moves which ones are legal
    # i.e wont hit a wall or body of itself or other snake
    new_head = dict()
    for move in possible_moves:
        if move == "L":
            new_head['x'] = head['x']-1
            new_head['y'] = head['y'] 
        if move == "R":
            new_head['x'] = head['x'] + 1
            new_head['y'] = head['y']
        if move == "U":
            new_head['x'] = head['x']
            nead_head['y'] = head['y'] + 1
        if move == "D":
            new_head['x'] = head['x']
            new_head['y'] = head['y'] - 1

        # dont hit edges
        if new_head['x'] < 0: possible_moves.remove(move)
        if new_head['x'] > data['board']['width']: possible_moves.remove(move)
        if new_head['y'] < 0: possible_moves.remove(move)
        if new_head['y'] > data['board']['height']: possible_moves.remove(move)

        #don't hit other snake body or own body
        for snake_dict in data['board']['snakes']:
            if new_head in snake_dict['body']: possible_moves.remove(move)

    # Now choose possible move that gives the maximum heuristic value
    heuristic_values = dict()
    for move in possible_moves:
        if move == "L":
            new_head['x'] = head['x']-1
            new_head['y'] = head['y'] 
        if move == "R":
            new_head['x'] = head['x'] + 1
            new_head['y'] = head['y']
        if move == "U":
            new_head['x'] = head['x']
            nead_head['y'] = head['y'] + 1
        if move == "D":
            new_head['x'] = head['x']
            new_head['y'] = head['y'] - 1

        hueristic_values[move] = hueristic(data, new_head)
    
    best_move = max(heuristic_values, key=hueristic_values.get)
    
    return {'move': convert_move[best_move]}

def hueristic(data, head):
    # want to find an evaluiation of following values
    # MINIMIZE - Distance to food(s)
    # MAXIMIZE - Distance from nearest occupied square by other player
    # MAXIMIZE - Distance from own tail 
    tail = data['you']['body'][-1]

    # Want to maximize this value to keep the sneaky guy stretched out 
    distance_from_own_tail = abs(head['x'] - tail['x']) + abs(head['y'] - tail['y'])

    # Want to maximize this value 
    min_distance = min_distance_to_occupied(data)

    # Want to minimize this value
    nearest_food = distance_to_nearest_food(data, head)

    return distance_from_own_tail + min_distance - nearest_food

def min_distance_to_occupied(data):
    min_distance = 100
    head = data['you']['body'][0]
    for snake_dict in data['board']['snakes']:
        if snake_dict['name']==data['you']['name']: continue # skip ourselves
        snake_cords = snake_dict['body']
        distance = get_distances(head, snake_cords)
        if distance < min_distance: min_distance = distance
    return min_distance

def get_distances(head, snake_cords):
    distances = []
    for cord in snake_cords:
        distances.append(abs(head['x'] - cord['x']) + abs(head['y']- cord['y']))
    return min(distances)

 def distance_to_nearest_food(data, head):
    closest_distance = None
    for food_dict in data['board']['food']:
        distance = abs(head['x']-food_dict['x']) + abs(head['y']-food_dict['y'])
        if closest_distance == None or distance < closest_distance:
            closest_distance = distance 
    return closest_distance

def greedy_eat_helper(data,move_direction,closest_distance,closest_food_dict,greedy_moves,legal_moves):
    head = data['you']['body'][0]
    
    if move_direction == 'left':
        if head['x'] - 1 < 0: return
        new_coord = {'x':head['x']-1,'y':head['y']}
    elif move_direction == 'right':
        if head['x'] + 1 >= data['board']['width']: return
        new_coord = {'x':head['x']+1,'y':head['y']}
    elif move_direction == 'up':
        if head['y'] - 1 < 0: return
        new_coord = {'x':head['x'],'y':head['y']-1}
    else: # move_direction == 'down'
        if head['y'] + 1 >= data['board']['height']: return
        new_coord = {'x':head['x'],'y':head['y']+1}
    
    legal = True
    for snake_dict in data['board']['snakes']:
        if snake_dict['name']==data['you']['name']: continue # skip ourselves
        enemy_head = snake_dict['body'][0]
        if new_coord in snake_dict['body'] or \
           new_coord in [{'x':enemy_head['x']-1,'y':enemy_head['y']},{'x':enemy_head['x']+1,'y':enemy_head['y']},
                         {'x':enemy_head['x'],'y':enemy_head['y']-1},{'x':enemy_head['x'],'y':enemy_head['y']+1}]:
            legal = False
            break
    if legal and (new_coord not in data['you']['body']):
        if (abs(new_coord['x']-closest_food_dict['x']) + abs(new_coord['y']-closest_food_dict['y'])) < closest_distance: greedy_moves.append(move_direction)
        else: legal_moves.append(move_direction)
        
def greedy_eat(data):
    head = data['you']['body'][0]

    closest_distance = None
    closest_food_dict = None
    for food_dict in data['board']['food']:
        distance = abs(head['x']-food_dict['x']) + abs(head['y']-food_dict['y'])
        if closest_distance == None or distance < closest_distance:
            closest_distance = distance
            closest_food_dict = food_dict

    greedy_moves = [] # prioritize choosing one of these
    legal_moves = [] # if len(greedy_moves)==0, then choose on of these

    greedy_eat_helper(data,'left',closest_distance,closest_food_dict,greedy_moves,legal_moves)
    greedy_eat_helper(data,'right',closest_distance,closest_food_dict,greedy_moves,legal_moves)
    greedy_eat_helper(data,'up',closest_distance,closest_food_dict,greedy_moves,legal_moves)
    greedy_eat_helper(data,'down',closest_distance,closest_food_dict,greedy_moves,legal_moves)

    if len(greedy_moves) > 0: return {'move':random.choice(greedy_moves)}
    else: return {'move':random.choice(legal_moves)}


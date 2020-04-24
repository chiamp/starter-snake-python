import random

def get_move(data):
    # to be called by move function in server.py
    # whenever you  make a new move function, just replace the return statement with that function call
    # more convenient than always changing server.py
    return greedy_eat(data)


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


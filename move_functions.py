import random

def avoid_occupied_spaces(data):
    head = data['you']['body'][0]
    all_moves = []

    if head['x'] - 1 >= 0:
        new_coord = {'x':head['x']-1,'y':head['y']}
        legal = True
        for snake_dict in data['board']['snakes']:
            if new_coord in snake_dict['body']:
                legal = False
                break
        if legal and (new_coord not in data['you']['body']):
            all_moves.append('left')

    if head['x'] + 1 < data['board']['width']:
        new_coord = {'x':head['x']+1,'y':head['y']}
        legal = True
        for snake_dict in data['board']['snakes']:
            if new_coord in snake_dict['body']:
                legal = False
                break
        if legal and (new_coord not in data['you']['body']):
            all_moves.append('right')

    if head['y'] - 1 >= 0:
        new_coord = {'x':head['x'],'y':head['y']-1}
        legal = True
        for snake_dict in data['board']['snakes']:
            if new_coord in snake_dict['body']:
                legal = False
                break
        if legal and (new_coord not in data['you']['body']):
            all_moves.append('up')

    if head['y'] + 1 < data['board']['height']:
        new_coord = {'x':head['x'],'y':head['y']+1}
        legal = True
        for snake_dict in data['board']['snakes']:
            if new_coord in snake_dict['body']:
                legal = False
                break
        if legal and (new_coord not in data['you']['body']):
            all_moves.append('down')

    return {'move':random.choice(all_moves)}

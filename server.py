import os
import random

import cherrypy

"""
This is a simple Battlesnake server written in Python.
For instructions see https://github.com/BattlesnakeOfficial/starter-snake-python/README.md
"""


class Battlesnake(object):
    @cherrypy.expose
    def index(self):
        # If you open your snake URL in a browser you should see this message.
        return "Your Battlesnake is alive!"

    @cherrypy.expose
    def ping(self):
        # The Battlesnake engine calls this function to make sure your snake is working.
        return "pong"

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def start(self):
        # This function is called everytime your snake is entered into a game.
        # cherrypy.request.json contains information about the game that's about to be played.
        # TODO: Use this function to decide how your snake is going to look on the board.
        data = cherrypy.request.json
        print("START")
        return {"color": "#888888", "headType": "regular", "tailType": "regular"}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):
        # This function is called on every turn of a game. It's how your snake decides where to move.
        # Valid moves are "up", "down", "left", or "right".
        # TODO: Use the information in cherrypy.request.json to decide your next move.
        data = cherrypy.request.json
        return get_moves(data)
        
        # Choose a random direction to move in
        possible_moves = ["up", "down", "left", "right"]
        move = random.choice(possible_moves)

        print(f"MOVE: {move}")
        return {"move": move}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def end(self):
        # This function is called when a game your snake was in ends.
        # It's purely for informational purposes, you don't have to make any decisions here.
        data = cherrypy.request.json
        print("END")
        return "ok"

def get_moves(data):
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

    if head['x'] + 1 >= 0:
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

    if head['y'] + 1 >= 0:
        new_coord = {'x':head['x'],'y':head['y']+1}
        legal = True
        for snake_dict in data['board']['snakes']:
            if new_coord in snake_dict['body']:
                legal = False
                break
        if legal and (new_coord not in data['you']['body']):
            all_moves.append('down')

    return {'move':random.choice(all_moves)}



if __name__ == "__main__":
    server = Battlesnake()
    cherrypy.config.update({"server.socket_host": "0.0.0.0"})
    cherrypy.config.update(
        {"server.socket_port": int(os.environ.get("PORT", "8080")),}
    )
    print("Starting Battlesnake Server...")
    cherrypy.quickstart(server)

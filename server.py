import flask
from game import Game

app = flask.Flask(__name__)

games = {}
id_count = {}

@app.route("/get_game/<int:game_id>", methods=["GET"])
def get_game(game_id):
    game = games.get(game_id)
    if game:
        print(game.__dict__)
        return flask.jsonify(game.__dict__)
    else:
        return "Game not found", 404
    
@app.route("/create_game", methods=["POST"])
def create_game():
    global id_count
    
    if len(id_count) != 0:
        for id in id_count:
            if id_count[id] == False:
                id_count[id] = True
                game_id = id // 2
                player_id = id % 2
                game = games[game_id]
                
                if player_id % 2 == 0:
                    game.p1present = True
                else:
                    game.p2present = True
                    
                if game.p1present and game.p2present:
                    game.ready = True
                    
                ret = {"player_id": player_id} | game.__dict__
                
                return flask.jsonify(ret)
    
    if len(id_count) == 0:
        game_id = 0
        player_id = id = 0
        id_count[id] = True
        
        game = Game(game_id)
        game.p1present = True
        
        games[game_id] = game
        ret = {"player_id": player_id} | game.__dict__
        
        return flask.jsonify(ret)
    
    else:
        id = list(id_count.keys())[-1] + 1
        game_id = id // 2
        player_id = id % 2
        id_count[id] = True
        
        if not games.get(game_id):
            game = Game(game_id)
        else:
            game = games[game_id]
        
        if game.p1present:
            game.p2present = True
        else:
            game.p1present = True
            
        if game.p1present and game.p2present:
            game.ready = True
        
        games[game_id] = game
        ret = {"player_id": player_id} | game.__dict__
        
        return flask.jsonify(ret)
    
@app.route("/play/<int:game_id>/<int:player_id>", methods=["POST"])
def play_move(game_id, player_id):
    game = games.get(game_id)
    if game:
        data = flask.request.json
        move = data.get("move")
        game.play(player_id, move)
        return flask.jsonify({"p1Went": game.p1Went, "p2Went": game.p2Went, "move": game.moves})
    else:
        return "Game not found", 404
    
@app.route("/reset_game/<int:game_id>", methods=["POST"])
def reset_game(game_id):
    game = games.get(game_id)
    if game:
        game.resetWent()
        return flask.jsonify({"p1Went": game.p1Went, "p2Went": game.p2Went})
    else:
        return "Game Not Found", 404

@app.route("/disconnect/<int:game_id>/<int:player_id>", methods=["POST"])
def disconnect(game_id, player_id):
    global id_count
    id_count[game_id * 2 + player_id] = False
    
    game = games.get(game_id)
    if player_id == 1:
        game.p2present = False
        game.ready = False
    elif player_id == 0:
        game.p1present = False
        game.ready = False

    game.p1Went = False
    game.p2Went = False
    game.moves = [None, None]
    game.wins = [0,0]
    game.ties = 0
    
    games[game_id] = game
    return flask.jsonify(game.__dict__)
    
    
    
    

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5555)
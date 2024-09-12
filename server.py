from flask import Flask, request, jsonify
from game import Game

app = Flask(__name__)

games = {}
id_count = 0

@app.route("/get_game/<int:game_id>", method=["GET"])
def get_game(game_id):
    game = games.get(game_id)
    if game:
        return jsonify(game.__dict__)
    else:
        return "Game not found", 404
    
@app.route("/create_game", method=["POST"])
def create_game():
    global id_count
    game_id = id_count // 2
    games[game_id] = Game(game_id)
    id_count += 1
    
    return jsonify({"game_id": game_id, "player_id": 0})

@app.route("/join_game/<int:game_id>", method="POST")
def join_game(game_id):
    game = games.get(game_id)
    if game and not game.ready:
        game.ready = True
        return jsonify({"player_id": 1})
    else:
        return "Game full or not found", 400
    
@app.route("/play/<int:game_id>/<int:player_id>", method=["POST"])
def play_move(game_id, player_id):
    game = games.get(game_id)
    if game:
        data = request.json
        move = data.get("move")
        game.play(player_id, move)
        return jsonify(game.__dict__)
    else:
        return "Game not found", 404
    
@app.route("/reset_game/<int:game_id>", method=["POST"])
def reset_game(game_id):
    game = games.get(game_id)
    if game:
        game.resetWent()
        return jsonify(game.__dict__)
    else:
        return "Game Not Found", 404
    
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5555)
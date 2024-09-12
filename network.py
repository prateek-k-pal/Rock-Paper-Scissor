import requests

class Network:
    def __init__(self):
        self.server = "http://localhost"
        self.port = 5555
        self.game_id = None
        self.player_id = None
        
    def create_game(self):
        response = requests.get(f"{self.server}:{self.port}/create_game")
        data = response.json()
        self.game_id = data["game_id"]
        self.player_id = data["player_id"]
        
    def get_game(self):
        response = requests.get(f"{self.server}:{self.port}/get_game/{self.game_id}")
        return response.json()
    
    def send_move(self, move):
        response = requests.post(f"{self.server}:{self.port}/play/{self.game_id}/{self.player_id}", json={"move": move})
        return response.json()
    
    def reset_game(self):
        response = requests.post(f"{self.server}:{self.port}/reset_game/{self.game_id}")
        return requests.json()
import pygame
import requests
from game import Game
from os import getenv
from dotenv import load_dotenv

load_dotenv()
pygame.font.init()

server = getenv('SERVER')
try:
    port = getenv('PORT')
except:
    port = "5555"

width = 700
height = 700
clock = pygame.time.Clock()

win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Rock-Paper-Scissors Client")

class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 160
        self.height = 100

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(self.text, 1, (255, 255, 255))
        win.blit(text, (self.x + round(self.width / 2) - round(text.get_width() / 2), self.y + round(self.height / 2) - round(text.get_height() / 2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False

def redraw_window(win, game, p):
    win.fill((0, 0, 0))
    font = pygame.font.SysFont("comicsans", 70)
    if not game.ready:
        text = font.render("Waiting for Player...", 1, (255, 255, 255), True)
        win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
    else:
        font = pygame.font.SysFont("comicsans", 50)
        text = font.render("Your Move", 1, (255,255,255))
        win.blit(text, (60, 200))
        
        text = font.render("Opponent", 1, (255,255,255))
        win.blit(text, (400, 200))
        
        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)
        
        if game.bothWent():
            text1 = font.render(move1, 1, (255,255,255))
            text2 = font.render(move2, 1, (255,255,255))
            
        else:
            if game.p1Went and p == 0:
                text1 = font.render(move1, 1, (255, 255, 255))
            elif game.p1Went:
                text1 = font.render("Locked In", 1, (255, 255, 255))
            else:
                text1 = font.render("Waiting", 1, (255, 255, 255))
                
            if game.p2Went and p == 1:
                text2 = font.render(move2, 1, (255, 255, 255))
            elif game.p2Went:
                text2 = font.render("Locked In", 1, (255, 255, 255))
            else:
                text2 = font.render("Waiting", 1, (255, 255, 255))
                
        if p == 1:
            win.blit(text2, (80, 350))
            win.blit(text1, (420, 350))
        else:
            win.blit(text1, (80, 350))
            win.blit(text2, (420, 350))
                
        for btn in btns:
            btn.draw(win)

    pygame.display.update()

btns = [Button("Rock", 50, 500, (0, 255, 0)), Button("Scissors", 260, 500, (255, 0, 0)), Button("Paper", 475, 500, (0, 0, 255))]

def main():
    run = True

    # Create a new game
    try:
        response = requests.post(f"https://{server}/create_game")
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    except requests.exceptions.JSONDecodeError as e:
        print(f"JSON Decode failed: {e}")
    except requests.exceptions.SSLError as e:
        print(f"SSL Error: {e}")
    except requests.RequestException as e:
        print(f"Error: {e}")
        
    print(response)
    game_id = data["id"]
    player = data["player_id"]
    game = Game(game_id)
    game.p1Went = data["p1Went"]
    game.p2Went = data["p2Went"]
    game.ready = data["ready"]
    game.moves = data["moves"]
    game.wins = data["wins"]
    game.ties = data["ties"]
    game.p1present = data["p1present"]
    game.p2present = data["p2present"]
    
    try:
        if game.ready:
            print("Starting the game")
    except:
        print("Waiting for player 2....")

    while run:
        clock.tick(60)
        try:
            gameJS = requests.get(f"https://{server}/get_game/{game_id}").json()
                
        except:
            run = False
            print("Couldn't get game")
            break
        
        print(gameJS)
        if game.id == gameJS["id"]:
            game.p1Went = gameJS["p1Went"]
            game.p2Went = gameJS["p2Went"]
            game.ready = gameJS["ready"]
            game.moves = gameJS["moves"]
            game.wins = gameJS["wins"]
            game.ties = gameJS["ties"]
            game.p1present = gameJS["p1present"]
            game.p2present = gameJS["p2present"]
        
        if game.bothWent():
            redraw_window(win, game, player)
            pygame.time.delay(500)
            try:
                gameJS = requests.post(f"https://{server}/reset_game/{game_id}").json()
                
                game.p1Went = gameJS["p1Went"]
                game.p2Went = gameJS["p2Went"]
                
            except:
                run = False
                print("Couldn't get game")
                break
            
            font = pygame.font.SysFont("comicsans", 90)
            print(game.winner())
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render("You Won!", 1, (0, 255, 0))
            elif game.winner() == -1:
                text = font.render("Tie Game!", 1, (0, 0, 255))
            else:
                text = font.render("You Lost!", 1, (255, 0, 0))
                
            win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                requests.post(f"https://{server}/disconnect/{game_id}/{player}", json={"close": True})
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.ready:
                        move = btn.text
                        gameJS = requests.post(f"https://{server}/play/{game_id}/{player}", json={"move": move}).json()
                        
                        game.moves = gameJS["move"]
                        game.p1Went = gameJS["p1Went"]
                        game.p2Went = gameJS["p2Went"]
                        

        redraw_window(win, game, player)

def menu_screen():
    run = True
    while run:
        clock.tick(60)
        win.fill((0, 0, 0))
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Click to Play!", 1, (128, 128, 128))
        win.blit(text, (170, 200))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()

while True:
    menu_screen()

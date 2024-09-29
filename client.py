import pygame
import socket
import pickle
from vaisseau import Vaisseau
from ennemi import Ennemi
from bouclier import Bouclier
from vie import Vie

# Game related global variables
window_width = 700
window_height = 700
player1_start_x = 10
player1_start_y = 300
player2_start_x = 670
player2_start_y = 300

# Packet size for sending and receiving between server and clients
data_size = 4096

# FPS speed for the game clock
game_speed = 60


win = pygame.display.set_mode((window_width, window_height))
# Initiate the Bat objects
vaisseaux = [Vaisseau(), Vaisseau()]

class PongDTO:
    """This is a data transfer object containing the variables that\
        will be passed between server and clients."""

    # Initiate to default values
    def __init__(self):
        self.game_id = 0
        self.player_id = 0
        self.player_x = []
        self.player_y = []
        self.missiles = [[], []]
        self.start_play = False
        self.msg = ''
        self.end_play = False
        self.points = [0, 0]


class PickableSurface:
    def __init__(self, surface):
        self.surface = surface

    def __getstate__(self):
        state = self.__dict__.copy()
        surface = state.pop("surface")
        state["surface_string"] = (pygame.image.tostring(surface, "RGB"), surface.get_size())
        return state

    def __setstate__(self, state):
        surface_string, size = state.pop("surface_string")
        state["surface"] = pygame.image.fromstring(surface_string, size, "RGB")
        self.__dict__.update(state)



def update_bat_ball(dto):
    """This method takes PongDTO as input and updates the positions of the bats and the ball.
    This method also sets the colours of the player and opponent differently."""

    # Set the colors of bats
    

    # Set the initial coordinates of the bats and ball as received from server
    vaisseaux[0].rect.x = dto.player_x[0]
    vaisseaux[0].rect.y = dto.player_y[0]
    vaisseaux[1].rect.x = dto.player_x[1]
    vaisseaux[1].rect.y = dto.player_y[1]


# Create a socket for the server and client connection
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Server IP is where the server python file is running and listening for connections
server = "172.19.196.199"
port   = 5555
addr = (server, port)

# Initiate client and server connection
client.connect(addr)
# Receive the data transfer object from server for first time
receive_dto = pickle.loads(client.recv(data_size))
print("You are player ", receive_dto.player_id)

# Retrieve the player id from the DTO
player_id = receive_dto.player_id
# The opponent id is the other id from set {0,1}
opponent_id = list({0, 1} - {receive_dto.player_id})[0]



# Update the coordinates of the bats and ball with received DTO. This will get the initial positions from the server
update_bat_ball(receive_dto)
# Initiate font
pygame.font.init()


run = True
# Get the game clock
clock = pygame.time.Clock()
vaisseau_groupe = pygame.sprite.Group(vaisseaux[0], vaisseaux[1])
# Start the loop for the game
while run:
    # Set the game speed
    clock.tick(game_speed)
    # Fill the window color
    win.fill((255, 255, 255))
    # Draw the bats
    vaisseau_groupe.draw(win)
    vaisseaux[0].draw(win)
    vaisseaux[1].draw(win)

    # Render the window elements
    pygame.display.update()

    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    # Get the list of keys pressed
    keys = pygame.key.get_pressed()
    vaisseaux[0].handle_mouvement(keys, window_width, window_height)
    vaisseaux[1].handle_mouvement(keys, window_width, window_height )
    # Tirer un missile avec la touche Espace    
    if keys[pygame.K_SPACE]:
        vaisseaux[receive_dto.player_id].shoot_missile(window_width)
        
    # Set the DTO as per screen for both players. This is required for opponent because
    # client should reflect what is received
    receive_dto.player_x[0] = vaisseaux[0].rect.x
    receive_dto.player_x[1] = vaisseaux[1].rect.x
    receive_dto.player_y[0] = vaisseaux[0].rect.y
    receive_dto.player_y[1] = vaisseaux[1].rect.y

    missiles_pickable = []
    for m in vaisseaux[receive_dto.player_id].missiles:
        missiles_pickable.append(PickableSurface(m))
    setattr(receive_dto, 'missiles', missiles_pickable)


    try:
        # Send the DTO to server
        client.sendall(pickle.dumps(receive_dto))
        # Receive the DTO from server
        receive_dto = pickle.loads(client.recv(data_size))
    # Break loop for any exception
    except Exception as e:
        run = False
        print("Couldn't get game")
        print("An error occurred:", e)
        break
    
    # Update the coordinates of the bats and ball with received DTO.
    update_bat_ball(receive_dto)

    # Met à jour tous les sprites
    vaisseau_groupe.update()


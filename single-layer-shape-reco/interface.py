# WARNING:
#     This code was written for a specific task:
#     Recognise only rectangles and not circles
#     Expect bad and not reusable code
#     This program was ment to test the VNetwork library

import pygame
from vnetwork import Network

FPS = 30

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((1024, 512))
clock = pygame.time.Clock()

network: Network = None

def draw_neurons(surface) -> None:
    # Input neuron configuration
    neuron: dict = {
        "radius": 6,
        "margin-x": 8,
        "margin-y": 8,
        "offset-x": 40,
        "offset-y": 40
    }

    # Bias diagram configuration
    bias: dict = {
        "size": 6,
        "margin-x": 1,
        "margin-y": 1,
        "offset-x": 700,
        "offset-y": 40
    }

    # Nice frame for neuron grid
    pygame.draw.rect(surface, "#2D333B", (neuron["offset-x"]-20, neuron["offset-y"]-20, 650, 472), border_radius = 8)

    # Nice frame for bias grid
    pygame.draw.rect(surface, "#2D333B", (bias["offset-x"]-20, bias["offset-y"]-20, 320, 472), border_radius = 8)

    output_coords: tuple = (600, (512/2)-(20/2))
    
    # Draw connections
    for y in range(32):
        for x in range(32):
            color: int = network.layers[0][y*32+x].state * 255 # State is in range of 0.0 to 1.0

            pygame.draw.line(
                surface, "#454D57",
                (
                    x*(neuron["radius"]+neuron["margin-x"]) + neuron["offset-x"],
                    y*(neuron["radius"]+neuron["margin-y"]) + neuron["offset-y"]
                ), 
                output_coords
            )

    # Draw grid of 1024 neurons
    for y in range(32):
        for x in range(32):
            color: int = network.layers[0][y*32+x].state * 255 # State is in range of 0.0 to 1.0

            pygame.draw.circle(
                surface, [color]*3, 
                (
                    x*(neuron["radius"]+neuron["margin-x"]) + neuron["offset-x"],
                    y*(neuron["radius"]+neuron["margin-y"]) + neuron["offset-y"]
                ), 
                neuron["radius"]
            )

    # Draw grid legend
    font = pygame.font.SysFont("Monospace", 14)
    y: int = 0

    for value in range(-100, 110, 10):
        pygame.draw.rect(
            surface, ((value)+128, 100, 200), 
            (
                bias["offset-x"] + 35,
                y*(bias["size"]*3+bias["margin-y"]) + bias["offset-y"],
                bias["size"]*3, bias["size"]*3
            )
        )
        surface.blit(
            font.render(f"{value:>4}", True, (255, 255, 255)),
            (
                bias["offset-x"] - 10,
                y*(bias["size"]*3+bias["margin-y"]) + bias["offset-y"],
                bias["size"]*3, bias["size"]*3
            )
        )
        y += 1
    
    # Draw grid of 1024 biases
    for y in range(32):
        for x in range(32):
            color: int = network.layers[0][y*32+x].bias

            pygame.draw.rect(
                surface, (((color)+128) % 255, 100, 200), 
                (
                    x*(bias["size"]+bias["margin-x"]) + bias["offset-x"] + 65,
                    y*(bias["size"]+bias["margin-y"]) + bias["offset-y"],
                    bias["size"], bias["size"]
                )
            )
    
    # Draw output neuron
    if network.evaluate()[0].state > network.layers[1][0].bias:
        color: int = 255
    else:
        color: int = 0

    pygame.draw.circle(
        surface, [color]*3,
        output_coords,
        20
    )

def close() -> None:
    pygame.display.quit()

def update() -> bool:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    
    screen.fill("#22272E")

    draw_neurons(screen)

    pygame.display.update()

    return True
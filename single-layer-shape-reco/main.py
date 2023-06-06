# WARNING:
#     This code was written for a specific task:
#     Recognise only rectangles and not circles
#     Expect bad and not reusable code
#     This program was ment to test the VNetwork library

import pygame, os, random, time, vnetwork, interface
from vnetwork import Network
from random import randint as rint

def init_network() -> vnetwork.Network:
    network = vnetwork.Network(
        layerplan = [
            [[1, 1, 1] for _ in range(32 * 32)],
            [[0, 0, 25]]
        ]
    )

    return network

def init_shapes(shapes_dir: str) -> dict:
    # Shape file naming format:
    #     shape-n.txt
    #
    # Example:
    #     rect-1.txt
    #

    shapes_files: list = os.listdir(shapes_dir)
    shapes: dict = {}

    for file in shapes_files:
        shape = file.split("-")[0]

        if shape not in shapes:
            shapes[shape] = []

        shapes[shape].append(
            open(shapes_dir+file, "r").read().replace("\n", "")
        )

    return shapes

def random_shape(shapes: dict) -> str:
    return random.choice(shapes["rect"]+shapes["circle"])

def load_shape(inputs: list, shape: str) -> list:
    for index, character in enumerate(shape):
        if character == ".":
            inputs[index].state = 0
        else:
            inputs[index].state = 1
    
    return inputs

def adjust_bias(inputs: list, shape: str, power: float = 0.1) -> list:
    for index, character in enumerate(shape):
        if character != ".":
            inputs[index].bias += power
    
    return inputs

def next_shape(network: Network, shapes: dict) -> None:
    network.current_shape: str = random_shape(shapes)

    network.layers[0] = load_shape(
        network.layers[0],
        network.current_shape
    )

def adjust_network(network: Network, shapes: dict) -> None:
    if network.current_shape in shapes["rect"]:
        while network.evaluate()[0].state < network.layers[1][0].bias:
            network.layers[0] = adjust_bias(network.layers[0], network.current_shape, power = rint(1, 20))
    if network.current_shape in shapes["circle"]:
        while network.evaluate()[0].state > network.layers[1][0].bias:
            network.layers[0] = adjust_bias(network.layers[0], network.current_shape, power = -rint(1, 20))

def keybind(network: Network, shapes: dict) -> None:
    keys: pygame.key.ScancodeWrapper = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        next_shape(network, shapes)
        time.sleep(0.5)
    
    if keys[pygame.K_RETURN]:
        network.layers[0] = adjust_bias(network.layers[0], network.current_shape, power = 10)

    if keys[pygame.K_BACKSPACE]:
        network.layers[0] = adjust_bias(network.layers[0], network.current_shape, power = -10)
    
    if keys[pygame.K_t]:
        adjust_network(network, shapes)
        next_shape(network, shapes)

def main() -> None:
    network: Network = init_network()
    shapes: dict = init_shapes("./single-layer-shape-reco/shapes/")

    interface.network = network

    while interface.update():
        keybind(network, shapes)
    
    interface.close()

if __name__ == "__main__":
    main()
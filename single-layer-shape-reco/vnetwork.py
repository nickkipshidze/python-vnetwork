"""VNetwork

Made by Nick Kipshidze

I couldnt name it network (too simple) so I added V in front, VNetwork library (cool).
"""

import copy

class EVALFUNC:
    """Evaluation Functions
    
    Class of functions Node(s) use to evaluate their states
    """
    
    def SUM(inputs: list) -> float:
        """EVALFUN.SUM calculates sum of all parent node states

        Returns:
            float: sum
        """

        inputs_sum: int = 0

        for node in inputs:
            inputs_sum += (node.state + node.weight) * node.bias
        
        return inputs_sum

class CONFUNC:
    """Connection Functions
    
    Class of functions Network(s) use to connect nodes/neurons
    """
    
    def FULL(layers: list) -> list:
        """Connect every N layer's nodes with all of N+1 layer's nodes

        Args:
            layers (list): 2D array of all layers

        Returns:
            list: 2D array of all layers with connections setup
        """
        
        for layer in range(1, len(layers)):
            for node in layers[layer]:
                node.inputs = layers[layer-1]
        
        return layers

class Node:
    """Node class
    
    Node class to keep track of Node(s) state, weight, bias, etc.
    """
    
    def __init__(self, state: float = 0.0, weight: float = 0.0, bias: float = 1.0, inputs: list = [], evalfunc = EVALFUNC.SUM) -> None:
        self.state: float = state

        self.weight: float = weight
        self.bias: float = bias

        self.inputs: list = inputs

        self.evalfunc = evalfunc
    
    def evaluate(self) -> float:
        self.state = self.evalfunc(self.inputs)
        return self.state

    def __str__(self) -> str:
        return f"( {self.state} {self.weight} {self.bias} )"
    
    def __repr__(self):
        return self.__str__()
    
class Network:
    """Network
    
    Class to manage all nodes and layers
    """
    
    def __init__(self, layerplan: list = [], confunc = CONFUNC.FULL) -> None:
        """__init__

        Args:
            layerplan (list, optional): 2D array of pseudo neural network. Defaults to [].
            confunc (_type_, optional): connection function. Defaults to CONFUNC.FULL.
        """
        
        # Generate the network nodes / convert pseudo layers to actual layers with nodes
        # Connect the nodes with desired connection function
        
        self.layers = self.connect_network(
            self.build_network(layerplan),
            confunc
        )
    
    def build_network(self, layerplan: list) -> list:
        """Convert pseudo network to a neural network

        Args:
            layerplan (list): 2D array of pseudo neural network

        Returns:
            list: 2D array of layers and nodes
        """
        
        network: list = []

        default_properties: list = [0.0, 0.0, 1.0, [], EVALFUNC.SUM]

        for layer in layerplan:
            network.append([])

            for node in layer:
                # Take values from pseudo node
                properties = [prop for prop in node]

                # If value not provided add defaults
                properties += default_properties[
                    -(len(default_properties)-len(properties)):
                ]

                # Use the values from pseduo node for actual node
                network[-1].append(
                    Node(properties[0], properties[1], properties[2], properties[3], properties[4])
                )
        
        return network

    def connect_network(self, layers: list, confunc) -> list:
        """Connect network layer's nodes

        Args:
            layers (list): 2D array of layers and nodes
            confunc (_type_): connection function

        Returns:
            list: 2D array of layers and nodes with connections
        """
        
        return confunc(layers)

    def evaluate(self, mutate_network: bool = False) -> list:
        """Evaluate the network

        Args:
            mutate_network (bool, optional): make changes or not to network while evaluating. Defaults to False.

        Returns:
            list: list of output neurons with evaluated states
        """
        
        if mutate_network:
            layers = self.layers
        else:
            layers = copy.deepcopy(self.layers)

        # "Fire" every neuron layer by layer
        for layer in range(1, len(layers)):
            for node in layers[layer]:
                node.evaluate()
        
        return layers[-1]

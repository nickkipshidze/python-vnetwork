import vnetwork
from vnetwork import Node

def test_node_init() -> None:
    node: Node = Node(
        state = 1.0, 
        weight = 4.0,
        bias = 1.0,
        inputs = [],
        evalfunc = vnetwork.EVALFUNC.SUM
    )

    assert node.state == 1
    assert node.weight == 4.0
    assert node.bias == 1.0
    assert node.inputs == []
    assert node.evalfunc == vnetwork.EVALFUNC.SUM

def test_node_inputs() -> None:
    node_1: Node = Node(
        state = 1.0, 
        weight = 4.0,
        bias = 1.0,
        inputs = [],
        evalfunc = vnetwork.EVALFUNC.SUM
    )
    node_2: Node = Node(
        state = 2.0, 
        weight = 8.0,
        bias = 2.0,
        inputs = [node_1],
        evalfunc = vnetwork.EVALFUNC.SUM
    )

    assert node_2.inputs[0] == node_1
    assert node_2.inputs[0].state == node_1.state

    node_2.inputs[0].state = 0.0

    assert node_2.inputs[0].state == node_1.state

def test_node_eval() -> None:
    node_1: Node = Node(
        state = 1.0, 
        weight = 4.0,
        bias = 1.0,
        inputs = [],
        evalfunc = vnetwork.EVALFUNC.SUM
    )
    node_2: Node = Node(
        state = 2.0, 
        weight = 8.0,
        bias = 2.0,
        inputs = [node_1],
        evalfunc = vnetwork.EVALFUNC.SUM
    )
    node_3: Node = Node(
        state = 2.0, 
        weight = 8.0,
        bias = 2.0,
        inputs = [node_1, node_2],
        evalfunc = vnetwork.EVALFUNC.SUM
    )

    assert node_2.evaluate() == (node_1.state + node_1.weight) * node_1.bias
    assert node_3.evaluate() == (
            (node_1.state + node_1.weight) * node_1.bias
        ) + (
            (node_2.state + node_2.weight) * node_2.bias
        )

def test_network_init() -> None:
    network = vnetwork.Network(
        layerplan = [     # [( state weight bias )]
            [[], [], []], # [( 0.0 0.0 1.0 ), ( 0.0 0.0 1.0 ), ( 0.0 0.0 1.0 )]
            [[], []],     # [( 0.0 0.0 1.0 ), ( 0.0 0.0 1.0 )]
            [[]]          # [( 0.0 0.0 1.0 )]
        ]
    )

    assert network.layers.__repr__() == "[[( 0.0 0.0 1.0 ), ( 0.0 0.0 1.0 ), ( 0.0 0.0 1.0 )], [( 0.0 0.0 1.0 ), ( 0.0 0.0 1.0 )], [( 0.0 0.0 1.0 )]]"
    assert network.layers[1][0].inputs.__repr__() == "[( 0.0 0.0 1.0 ), ( 0.0 0.0 1.0 ), ( 0.0 0.0 1.0 )]"

def test_network_eval() -> None:
    network = vnetwork.Network(
        layerplan = [
            [[2], [2], [2]],
            [[0, 2], [0, 4]],
            [[]]
        ]
    )

    assert network.evaluate()[0].state == 18
    assert network.layers[2][0].state == 0

    assert network.evaluate(mutate_network = True)[0].state == 18
    assert network.layers[2][0].state == 18

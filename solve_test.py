from solve import *

def test_simple():
    gates = [
        Toffoli(0,1,2),
    ]
    circuit = Circuit(4, gates)
    output = circuit.evaluate([True, True, False, True])
    assert output == [True, True, True, True]
from solve import *

def test_simple():
    gates = [
        Input(),
        Input(),
        Input(),
        Toffoli(0,1,2),
    ]
    circuit = Circuit(gates)
    output = circuit.evaluate([True, True, False])
    assert output == [True, True, False, True]
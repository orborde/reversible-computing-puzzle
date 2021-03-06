#! /usr/bin/env python3

import itertools
from typing import *

class Gate:
    def evaluate(self, values: List[bool]) -> bool:
        raise NotImplementedError()

class Input(Gate):
    def __str__(self):
        return 'Input()'

    def __repr__(self):
        return self.__str__()

class Toffoli(Gate):
    def __init__(self, i1: int, i2: int, x: int) -> None:
        self._i1, self._i2, self._x = i1,i2,x

    def evaluate(self, values: List[bool]) -> bool:
        i1 = values[self._i1]
        i2 = values[self._i2]
        x  = values[self._x]

        if i1 and i2:
            return not x
        else:
            return x

    def __str__(self) -> str:
        return f'Toffoli(({self._i1}, {self._i2}) ! {self._x})'

    def __repr__(self):
        return self.__str__()

class Circuit:
    def __init__(self, gates: List[Gate]) -> None:
        self._gates = gates

    def __str__(self) -> str:
        return '\n'.join(f'{i}: {gate}' for i, gate in enumerate(self._gates))

    def __repr__(self) -> str:
        return self.__str__()

    def evaluate(self, inputs: List[bool]) -> List[bool]:
        input_gates = list(itertools.takewhile(
            lambda g: type(g) is Input, self._gates))
        assert len(inputs) == len(input_gates)

        values: List[bool] = []
        for i, gate in enumerate(self._gates):
            if type(gate) is Input:
                values.append(inputs[i])
            else:
                values.append(gate.evaluate(values))
        
        return values

def generate() -> Iterable[Circuit]:
    frontier: List[List[Gate]] = [[Input(), Input(), Input()]]

    while True:
        new_frontier: List[List[Gate]] = []

        for prefix in frontier:
            for i1,i2 in itertools.combinations(range(len(prefix)), r=2):
                for x in range(len(prefix)):
                    item = prefix + [Toffoli(i1,i2,x)]
                    new_frontier.append(item)
                    yield Circuit(item)

        frontier = new_frontier

def fredkin_oracle(switch: bool, x: bool, y: bool) -> Tuple[bool, bool]:
    if switch:
        return y,x
    else:
        return x,y

def check(circuit: Circuit) -> bool:
    for (switch, x, y) in itertools.product([True,False], repeat=3): # type: ignore - https://github.com/python/typeshed/issues/1850
        exp_x, exp_y = fredkin_oracle(switch, x, y)
        values = circuit.evaluate([switch, x, y])
        act_x, act_y = values[-2:]

        if (exp_x, exp_y) != (act_x, act_y):
            print(f'{switch, x, y}: {exp_x, exp_y} != {act_x, act_y}')
            return False
    return True

if __name__ == '__main__':
    for c in generate():
        print(c)
        v = check(c)
        print()

        if v: break

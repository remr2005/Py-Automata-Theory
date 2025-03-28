"""Import base modules"""
from automatas import BaseAutomata

class MealyAutomata(BaseAutomata):
    """Realisation of Mealy Automata"""
    def __init__(self, states: list[str],
                 initial_state: str,
                 alphabet: list[str],
                 table:dict[str, dict[str, list[str]]]) -> None:
        super().__init__(states, initial_state, alphabet)
        self.table = table
        self.state = initial_state

    def step(self, inp: str) -> str:
        """Machine step"""
        self.state, reaction = self.table[self.state][inp]
        return reaction

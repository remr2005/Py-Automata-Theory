"""Import base modules"""
from PyAutomataTheory.automatas import BaseAutomata

class MoorAutomata(BaseAutomata):
    """Realisation of Moor Automata"""
    def __init__(self, states: list[str],
                 initial_state: str,
                 alphabet: list[str],
                 table:dict[str, dict[str, str]],
                 table_reactions:dict[str, str]) -> None:
        super().__init__(states, initial_state, alphabet)
        self.table = table
        self.table_reactions = table_reactions

    def step(self, inp: str) -> None:
        """Machine step"""
        self.state = self.table[self.state][inp]

    def get_reaction(self) -> str:
        """Return reaction"""
        try:
            return self.table_reactions[self.state]
        except IndexError:
            return ""

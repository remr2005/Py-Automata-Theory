"""Modules"""

class BaseAutomata:
    """Class for Automata"""
    def __init__(self, states:list[str],
                 initial_state:str,
                 alphabet: list[str]) -> None:
        if initial_state not in states:
            raise ValueError("Initial state must be in states")
        self.states = states
        self.state = initial_state
        self.alphabet = alphabet

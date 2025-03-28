"""Modules"""
import xml.etree.ElementTree as ET
from copy import deepcopy
from PyAutomataTheory.automatas import MoorAutomata

def convert_moor_to_jflap(automata: MoorAutomata, filename: str) -> None:
    """Convert Moor automata to jflap file"""

    # Prepare data
    automata_ = deepcopy(automata)
    states = automata_.table_reactions
    transitions = automata_.table
    initial_state = automata.state

    # Create XML root and structure
    root = ET.Element("structure")
    ET.SubElement(root, "type").text = "moore"
    automaton = ET.SubElement(root, "automaton")

    # Map states to unique ids
    state_map = {state: str(i) for i, state in enumerate(states.keys())}

    # Add states to XML
    for state, output in states.items():
        state_elem = ET.SubElement(automaton, "state", id=state_map[state], name=state)
        ET.SubElement(state_elem, "output").text = output
        if state == initial_state:
            ET.SubElement(state_elem, "initial")

    # Add transitions to XML
    for from_state, paths in transitions.items():
        for symbol, to_state in paths.items():
            trans_elem = ET.SubElement(automaton, "transition")
            ET.SubElement(trans_elem, "from").text = state_map[from_state]
            ET.SubElement(trans_elem, "to").text = state_map[to_state]
            ET.SubElement(trans_elem, "read").text = symbol
            ET.SubElement(trans_elem, "transout").text = states[to_state]

    # Write the XML structure to a JFLAP file
    tree = ET.ElementTree(root)
    tree.write(f"{filename}.jff", encoding="utf-8", xml_declaration=True)

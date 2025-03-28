"""Convert Mealy automaton to JFLAP file"""
import xml.etree.ElementTree as ET
from copy import deepcopy
from automatas import MealyAutomata

def convert_mealy_to_jflap(automata: MealyAutomata, filename="mealy_machine.jff") -> None:
    """Convert Mealy automaton to JFLAP file"""
    automata_ = deepcopy(automata)
    table = automata_.table
    start_state = automata_.state
    structure = ET.Element("structure")
    etype = ET.SubElement(structure, "type")
    etype.text = "mealy"
    automaton = ET.SubElement(structure, "automaton")

    # Create states
    states = {}
    for state in table.keys():
        state_elem = ET.SubElement(automaton, "state", id=state, name=state)
        if state == start_state:
            ET.SubElement(state_elem, "initial")
        states[state] = state_elem

    # Create transitions
    for from_state, transitions in table.items():
        for symbol, (to_state, output) in transitions.items():
            transition = ET.SubElement(automaton, "transition")
            ET.SubElement(transition, "from").text = from_state
            ET.SubElement(transition, "to").text = to_state
            ET.SubElement(transition, "read").text = symbol
            ET.SubElement(transition, "transout").text = output

    tree = ET.ElementTree(structure)
    tree.write(f"{filename}.jff", encoding="utf-8", xml_declaration=True)

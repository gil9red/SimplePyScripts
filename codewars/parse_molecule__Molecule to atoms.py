#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
My solution from codewars.

"""

import re
from collections import defaultdict


def get_sub_formula(formula):
    """
    "(SO3)2" -> ("(SO3)2", "(SO3)", "2")
    "(SO3)" -> ("(SO3)", "(SO3)", "")

    """

    match = re.search(r"(\([a-zA-Z\d]+\))(\d*)", formula)
    if not match:
        return

    full_sub_formula = match.group(0)
    sub_formula = match.group(1)
    multiplier = match.group(2)

    return full_sub_formula, sub_formula, multiplier


def split_by_full_tokens(formula):
    """
    'Fe7S10FBO3' -> ['Fe7', 'S10', 'F', 'B', 'O3']

    """

    return re.findall(r"([A-Z][a-z]*\d*)", formula)


def split_by_tokens(formula):
    """
    'Fe7S10F1B1O3' -> ['Fe', '7', 'S', '10', 'F', '1', 'B', '1', 'O', '3']

    """

    return re.findall(r"([A-Z][a-z]*|\d+)", formula)


def complete_element_atom_number_with_one_atom(formula):
    """
    Append '1' for elements without atom number: 'FeK' -> 'Fe1K1'

    """

    tokens = split_by_full_tokens(formula)
    tokens = [token if token[-1] in "0123456789" else token + "1" for token in tokens]
    return "".join(tokens)


def parse_molecule(formula):
    formula = formula.replace("[", "(").replace("]", ")")
    formula = formula.replace("{", "(").replace("}", ")")

    while "(" in formula:
        match = get_sub_formula(formula)
        if not match:
            break

        full_sub_formula, sub_formula, multiplier = match
        new_sub_formula = complete_element_atom_number_with_one_atom(sub_formula)

        if multiplier:
            multiplier = int(multiplier)

            tokens = split_by_tokens(new_sub_formula)

            # ['K', '4', 'O', '2'] * 2 -> ['K', '8', 'O', '4']
            tokens = [
                str(int(token) * multiplier) if token.isdigit() else token
                for token in tokens
            ]
            new_sub_formula = "".join(tokens)

        formula = formula.replace(full_sub_formula, new_sub_formula)

    formula = complete_element_atom_number_with_one_atom(formula)
    tokens = split_by_tokens(formula)

    element_by_number_atom = defaultdict(int)
    for i in range(0, len(tokens), 2):
        element_by_number_atom[tokens[i]] += int(tokens[i + 1])

    return element_by_number_atom


if __name__ == "__main__":
    def equals_atomically(obj1, obj2):
        if len(obj1) != len(obj2):
            return False
        for k in obj1:
            if obj1[k] != obj2[k]:
                return False
        return True

    assert equals_atomically(
        parse_molecule("H2O"), {"H": 2, "O": 1}
    ), "Should parse water"
    assert equals_atomically(
        parse_molecule("Mg(OH)2"), {"Mg": 1, "O": 2, "H": 2}
    ), "Should parse magnesium hydroxide: Mg(OH)2"
    assert equals_atomically(
        parse_molecule("K4[ON(SO3)2]2"), {"K": 4, "O": 14, "N": 2, "S": 4}
    ), "Should parse Fremy's salt: K4[ON(SO3)2]2"

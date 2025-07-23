#! /usr/bin/env python3

import sys

from classes.enigma import Enigma
from data.reflecteurs import reflecteurB, reflecteurC

def main() -> int:
    reflecteur: str = input("Choisissez un réflecteur (B / C) : ")
    if reflecteur not in ["B", "C"]:
        sys.stderr.write("Nom du reflecteur invalide !\n")
        sys.stderr.flush()
        return 1
    rotors: str = input("Choisissez les rotors (I VI III) : ")
    positions: str = input("Choisissez les positions des rotors (T E M / 20 3 07) : ")
    permutations: str = input("Choisissez les permutations (AB CT GR): ")
    if reflecteur == "B":
        enigma = Enigma(reflecteurB, rotors, positions, permutations)
    else:
        enigma = Enigma(reflecteurC, rotors, positions, permutations)
    message: str = input("Entrez un message à chiffrer / déchiffrer : ")
    print(enigma.traduire_message(message))
    return 0

if __name__ == "__main__":
    sys.exit(main())

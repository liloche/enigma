import sys
import os

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from utils.convertions import nombre_en_lettre, lettre_en_nombre

class Rotor:
    def __init__(self, nom: str, permutations: list[int], encoches: list[int]) -> None:
        self.nom: str = nom
        self.permutations: list[int] = permutations
        self.encoches: list[int] = encoches
        self.position: int = 0
        return

    def tourner_rotor(self) -> bool:
        self.permutations.append(self.permutations.pop(0))
        tourner_suivant: bool = False
        if self.position in self.encoches: #Si il faut tourner le deuxième rotor
            tourner_suivant: bool = True
        self.position = (self.position + 1) % 26
        return tourner_suivant

    def permuter_lettre(self, lettre : str) -> str:
        return nombre_en_lettre(self.permutations[lettre_en_nombre(lettre)])

    def permuter_lettre_inverse(self, lettre : str) -> str:
        return nombre_en_lettre(self.permutations.index(lettre_en_nombre(lettre)))

    def appliquer_position(self, position : int) -> None:
        for i in range(position):
            self.permutations.append(self.permutations.pop(0))
        self.position: int = position
        return

import sys
import os

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from utils.convertions import lettre_en_nombre, nombre_en_lettre
from data.rotors import liste_rotor
from .rotor import Rotor

class Enigma:
    def __init__(self, reflecteur : list[int], rotors: str, positions: str, liste_permutations: str) -> None:
        self.rotors: list[Rotor] = []
        self.reflecteur: list[int] = reflecteur
        self.permutation: list[int] = [i for i in range (26)]
        liste_positions: list[str] = positions.split(" ")
        permutations: list[str] = liste_permutations.split(" ")
        for permutation in permutations:
            self.ajouter_permutation(permutation[0], permutation[1])
        self.choix_rotors(rotors)
        for i in range(3):
            if not liste_positions[0][0].isdigit():
                self.changer_position_rotor(i, lettre_en_nombre(liste_positions[i]))
            else:
                self.changer_position_rotor(i, int(liste_positions[i]))
        return

    def choix_rotors(self, alignements_rotors : str) -> list[Rotor]:
        rotors: list[str] = alignements_rotors.split(" ")
        if len(rotors) != 3:
            sys.stderr.write("Nombre de rotors invalide !\n")
            sys.stderr.flush()
            sys.exit(1)
        for rotor in rotors:
            for i in range(len(liste_rotor)):
                if liste_rotor[i].nom == rotor:
                    self.rotors.append(liste_rotor[i])
        return self.rotors

    def changer_position_rotor(self, rotor: int, position: int) -> None:
        assert rotor in [0, 1, 2], f"Le rotor n°{rotor} n'est pas installé dans Enigma" # vérifier que le rotor est bien installé dans la machine
        self.rotors[rotor].appliquer_position(position)
        return

    def permuter_lettre(self, lettre: str) -> str:
        return nombre_en_lettre(self.permutation[lettre_en_nombre(lettre)])

    def verifier_permutations(self) -> None:
        for i in range(26):
            if self.permutation[self.permutation[i]] != i:
                self.permutation[i] = i
        return

    def ajouter_permutation(self, lettre_a: str, lettre_b: str) -> None:
        a: int = lettre_en_nombre(lettre_a)
        b: int = lettre_en_nombre(lettre_b)
        self.permutation[a] = b
        self.permutation[b] = a
        self.verifier_permutations()
        return

    def traduire_lettre(self, lettre : str) -> str:
        if not ("A" <= lettre <= "Z"):
            return lettre
        i: int = 0
        while self.rotors[i].tourner_rotor() and i < 3:
            i += 1
        # La lettre pase dans les permutations
        lettre = self.permuter_lettre(lettre)
        # print("Première permutation :", lettre)
        # La lettre permutée passe dans les rotors
        lettre = self.rotors[0].permuter_lettre(lettre)
        # print("Premier rotor :", lettre)
        lettre = self.rotors[1].permuter_lettre(lettre)
        # print("Deuxième rotor :", lettre)
        lettre = self.rotors[2].permuter_lettre(lettre)
        # print("Troisième rotor :", lettre)
        # La lettre modifiée par les rotors passe dans le réflecteur
        lettre = nombre_en_lettre(self.reflecteur[lettre_en_nombre(lettre)])
        # print("Réflecteur :", lettre)
        # La lettre passe dans les rotors à l'envers
        lettre = self.rotors[2].permuter_lettre_inverse(lettre)
        # print("Troisième rotor inverse :", lettre)
        lettre = self.rotors[1].permuter_lettre_inverse(lettre)
        # print("Deuxième rotor inverse :", lettre)
        lettre = self.rotors[0].permuter_lettre_inverse(lettre)
        # print("Premier rotor inverse :", lettre)
        # La lettre repasse dans les permutations
        lettre = self.permuter_lettre(lettre)
        # print("Dernière permutation :", lettre)
        return lettre

    def traduire_message(self, message : str) -> str:
        traduit: str = ""
        for lettre in message:
            traduit += self.traduire_lettre(lettre)
        return traduit

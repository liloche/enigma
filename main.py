import sys

rotorI: list[int] = [4, 10, 12, 5, 11, 6, 3, 16, 21, 25, 13, 19, 14, 22, 24, 7, 23, 20, 18, 15, 0, 8, 1, 17, 2, 9]
rotorII: list[int] = [0, 9, 3, 10, 18, 8, 17, 20, 23, 1, 11, 7, 22, 19, 12, 2, 16, 6, 25, 13, 15, 24, 5, 21, 14, 4]
rotorIII: list[int] = [1, 3, 5, 7, 9, 11, 2, 15, 17, 19, 23, 21, 25, 13, 24, 4, 8, 22, 6, 0, 10, 12, 20, 18, 16, 14]
rotorIV: list[int] = [4, 18, 14, 21, 15, 25, 9, 0, 24, 16, 20, 8, 17, 7, 23, 11, 13, 5, 19, 6, 10, 3, 2, 12, 22, 1]
rotorV: list[int] = [21, 25, 1, 17, 6, 8, 19, 24, 20, 15, 18, 3, 13, 7, 11, 23, 0, 22, 12, 9, 16, 14, 5, 4, 2, 10]
rotorVI: list[int] = [9, 15, 6, 21, 14, 20, 12, 5, 24, 16, 1, 4, 13, 7, 25, 17, 3, 10, 0, 18, 23, 11, 8, 2, 19, 22]
rotorVII: list[int] = [13, 25, 9, 7, 6, 17, 2, 23, 12, 24, 18, 22, 1, 14, 20, 5, 0, 8, 21, 11, 15, 4, 10, 16, 3, 19]
rotorVIII: list[int] = [5, 10, 16, 7, 19, 11, 23, 14, 2, 1, 9, 18, 15, 3, 25, 17, 0, 12, 4, 22, 13, 8, 20, 24, 6, 21]

reflecteurB: list[int] = [24, 17, 20, 7, 16, 18, 11, 3, 15, 23, 13, 6, 14, 10, 12, 8, 4, 1, 5, 25, 2, 22, 21, 9, 0, 19]
reflecteurC: list[int] = [5, 21, 15, 9, 8, 0, 14, 24, 4, 3, 17, 25, 23, 22, 6, 2, 19, 10, 20, 16, 18, 1, 13, 12, 7, 11]

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

liste_rotor: list[Rotor] = [Rotor("I", rotorI, [16]), Rotor("II", rotorII, [4]), Rotor("III", rotorIII, [21]), Rotor("IV", rotorIV, [9]), Rotor("V", rotorV, [25]), Rotor("VI", rotorVI, [25, 12]), Rotor("VII", rotorVII, [25, 12]), Rotor("VIII", rotorVIII, [25, 12])]

class Enigma:
    def __init__(self, reflecteur : list[int]) -> None:
        self.rotors: list[Rotor] = []
        self.reflecteur: list[int] = reflecteur
        self.permutation: list[int] = [i for i in range (26)]
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


def lettre_en_nombre(lettre : str) -> int:
    assert "A" <= lettre <= "Z"
    return ord(lettre) - ord("A")

def nombre_en_lettre(nombre : int) -> str:
    assert 0 <= nombre <= 25
    return chr(nombre + ord("A"))

def traduire_lettre(enigma : Enigma, lettre : str) -> str:
    if not ("A" <= lettre <= "Z"):
        return lettre
    i: int = 0
    while enigma.rotors[i].tourner_rotor() and i < 3:
        i += 1
    # La lettre pase dans les permutations
    lettre = enigma.permuter_lettre(lettre)
    # print("Première permutation :", lettre)
    # La lettre permutée passe dans les rotors
    lettre = enigma.rotors[0].permuter_lettre(lettre)
    # print("Premier rotor :", lettre)
    lettre = enigma.rotors[1].permuter_lettre(lettre)
    # print("Deuxième rotor :", lettre)
    lettre = enigma.rotors[2].permuter_lettre(lettre)
    # print("Troisième rotor :", lettre)
    # La lettre modifiée par les rotors passe dans le réflecteur
    lettre = nombre_en_lettre(enigma.reflecteur[lettre_en_nombre(lettre)])
    # print("Réflecteur :", lettre)
    # La lettre passe dans les rotors à l'envers
    lettre = enigma.rotors[2].permuter_lettre_inverse(lettre)
    # print("Troisième rotor inverse :", lettre)
    lettre = enigma.rotors[1].permuter_lettre_inverse(lettre)
    # print("Deuxième rotor inverse :", lettre)
    lettre = enigma.rotors[0].permuter_lettre_inverse(lettre)
    # print("Premier rotor inverse :", lettre)
    # La lettre repasse dans les permutations
    lettre = enigma.permuter_lettre(lettre)
    # print("Dernière permutation :", lettre)
    return lettre

def traduire_message(enigma : Enigma, message : str) -> str:
    traduit: str = ""
    for lettre in message:
        traduit += traduire_lettre(enigma, lettre)
    return traduit

def initialiser_enigma(enigma : Enigma, rotors : str, positions : str, liste_permutations: str) -> None:
    liste_positions: list[str] = positions.split(" ")
    permutations: list[str] = liste_permutations.split(" ")
    for permutation in permutations:
        enigma.ajouter_permutation(permutation[0], permutation[1])
    enigma.choix_rotors(rotors)
    for i in range(3):
        if not liste_positions[0][0].isdigit():
            enigma.changer_position_rotor(i, lettre_en_nombre(liste_positions[i]))
        else:
            enigma.changer_position_rotor(i, int(liste_positions[i]))
    return

reflecteur: str = input("Choisissez un réflecteur (B / C) : ")
if reflecteur not in ["B", "C"]:
    sys.stderr.write("Nom du reflecteur invalide !\n")
    sys.stderr.flush()
    sys.exit(1)
if reflecteur == "B":
    enigma1 = Enigma(reflecteurB)
else:
    enigma1 = Enigma(reflecteurC)
rotors1: str = input("Choisissez les rotors (I VI III) : ")
positions1: str = input("Choisissez les positions des rotors (T E M / 20 3 07) : ")
permutations: str = input("Choisissez les permutations (AB CT GA): ")
initialiser_enigma(enigma1, rotors1, positions1, permutations)
message1: str = input("Entrez un message à chiffrer / déchiffrer : ")
print(traduire_message(enigma1, message1))

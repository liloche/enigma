def lettre_en_nombre(lettre : str) -> int:
    assert "A" <= lettre <= "Z"
    return ord(lettre) - ord("A")

def nombre_en_lettre(nombre : int) -> str:
    assert 0 <= nombre <= 25
    return chr(nombre + ord("A"))

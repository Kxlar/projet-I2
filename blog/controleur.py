from .models import Equipement, Character
import random
from django.shortcuts import get_object_or_404

lieux = [
    "Extérieur",
    "Accueil",
    "Vestiaires",
    "Restaurant",
    "Boutique",
    "Salle_Echauffement",
    "Bloc_jaune",
    "Bloc_vert",
    "Bloc_bleu",
    "Bloc_rouge",
    "Bloc_noir",
    "Bloc_volet",
]


def entrer(character_id):
    # Récupérer l'objet
    character = get_object_or_404(Character, id_character=character_id)
    # Effectuer les modifications nécessaires
    character.lieu = get_object_or_404(Equipement, id_equip="Accueil")
    character.save()
    return None


def echauffement(character_id):
    # Récupérer l'objet
    character = get_object_or_404(Character, id_character=character_id)
    # Effectuer les modifications nécessaires
    character.lieu = get_object_or_404(Equipement, id_equip="Salle_Echauffement")
    character.energie -= 1
    character.save()
    return None


def aller_vestiaires(character_id):
    # Récupérer l'objet
    character = get_object_or_404(Character, id_character=character_id)
    # Effectuer les modifications nécessaires
    character.lieu = get_object_or_404(Equipement, id_equip="Vestiaires")
    character.save()
    return None


def aller_bloc(character_id, equipement_id):
    # Récupérer l'objet
    character = get_object_or_404(Character, id_character=character_id)
    # Effectuer les modifications nécessaires
    character.lieu = get_object_or_404(Equipement, id_equip=equipement_id)
    character.save()
    return None


def grimper(character_id, equipement_id):
    # Récupérer l'objet
    character = get_object_or_404(Character, id_character=character_id)
    equipement = get_object_or_404(Equipement, id_equip=equipement_id)
    # Effectuer les modifications nécessaires
    if (
        character.force >= equipement.force_requise
        and character.technique >= equipement.technique_requise
    ):
        character.energie = max(
            0, character.energie - 1
        )  # Éviter des valeurs négatives
        character.magnesie = max(0, character.magnesie - 1)
    if random.random() < 0.3:  # Possibilité de rater le bloc
        character.reussite = False
    else:
        character.reussite = True
    character.save()
    return None


def bloc_suivant(character_id):
    liste_bloc = [
        "Bloc_jaune",
        "Bloc_vert",
        "Bloc_bleu",
        "Bloc_rouge",
        "Bloc_noir",
        "Bloc_volet",
    ]
    # Récupérer l'objet
    character = get_object_or_404(Character, id_character=character_id)
    # Effectuer les modifications nécessaires
    if character.reussite == True:
        if character.lieu.id_equip == "Bloc_violet":
            character.lieu = get_object_or_404(Equipement, id_equip="Vestiaires")
        else:
            character.lieu = get_object_or_404(
                Equipement,
                id_equip=liste_bloc[liste_bloc.index(character.lieu.id_equip) + 1],
            )
    character.save()
    return None


def aller_boutique(character_id):
    # Récupérer l'objet
    character = get_object_or_404(Character, id_character=character_id)
    # Effectuer les modifications nécessaires
    character.lieu = get_object_or_404(Equipement, id_equip="Boutique")
    character.magnesie = min(10, character.magnesie + 10)
    character.save()
    return None


def aller_restaurant(character_id):
    # Récupérer l'objet
    character = get_object_or_404(Character, id_character=character_id)
    # Effectuer les modifications nécessaires
    character.lieu = get_object_or_404(Equipement, id_equip="Restaurant")
    character.energie = min(10, character.energie + 10)
    character.save()
    return None


def sortir(character_id):
    # Récupérer l'objet
    character = get_object_or_404(Character, id_character=character_id)
    # Effectuer les modifications nécessaires
    character.lieu = get_object_or_404(Equipement, id_equip="Extérieur")
    character.energie = random.random() * 10
    if character.force < 10:
        character.force += 1
    if character.technique < 10:
        character.technique += 1
    character.save()
    return None


def deplacement_autorisé(character_id, ancien_lieu, nouveau_lieu):
    transitions_autorisées = {
        "Extérieur": ["Accueil", "Extérieur"],
        "Accueil": ["Vestiaires", "Restaurant", "Boutique", "Accueil", "Extérieur"],
        "Vestiaires": [
            "Accueil",
            "Restaurant",
            "Boutique",
            "Salle_Echauffement",
            "Vestiaires",
        ],
        "Salle_Echauffement": [
            "Bloc_jaune",
            "Bloc_vert",
            "Bloc_bleu",
            "Bloc_rouge",
            "Bloc_noir",
            "Bloc_violet",
            "Salle_Echauffement",
        ],
        "Bloc_jaune": [
            "Restaurant",
            "Boutique",
            "Vestiaires",
            "Bloc_jaune",
            "Bloc_vert",
            "Bloc_bleu",
            "Bloc_rouge",
            "Bloc_noir",
            "Bloc_violet",
        ],
        "Bloc_vert": [
            "Restaurant",
            "Boutique",
            "Vestiaires",
            "Bloc_jaune",
            "Bloc_vert",
            "Bloc_bleu",
            "Bloc_rouge",
            "Bloc_noir",
            "Bloc_violet",
        ],
        "Bloc_bleu": [
            "Restaurant",
            "Boutique",
            "Vestiaires",
            "Bloc_jaune",
            "Bloc_vert",
            "Bloc_bleu",
            "Bloc_rouge",
            "Bloc_noir",
            "Bloc_violet",
        ],
        "Bloc_rouge": [
            "Restaurant",
            "Boutique",
            "Vestiaires",
            "Bloc_jaune",
            "Bloc_vert",
            "Bloc_bleu",
            "Bloc_rouge",
            "Bloc_noir",
            "Bloc_violet",
        ],
        "Bloc_noir": [
            "Restaurant",
            "Boutique",
            "Vestiaires",
            "Bloc_jaune",
            "Bloc_vert",
            "Bloc_bleu",
            "Bloc_rouge",
            "Bloc_noir",
            "Bloc_violet",
        ],
        "Bloc_violet": [
            "Restaurant",
            "Boutique",
            "Vestiaires",
            "Bloc_jaune",
            "Bloc_vert",
            "Bloc_bleu",
            "Bloc_rouge",
            "Bloc_noir",
            "Bloc_violet",
        ],
        "Restaurant": [
            "Restaurant",
            "Boutique",
            "Accueil",
            "Bloc_jaune",
            "Bloc_vert",
            "Bloc_bleu",
            "Bloc_rouge",
            "Bloc_noir",
            "Bloc_violet",
        ],
        "Boutique": [
            "Restaurant",
            "Boutique",
            "Accueil",
            "Bloc_jaune",
            "Bloc_vert",
            "Bloc_bleu",
            "Bloc_rouge",
            "Bloc_noir",
            "Bloc_violet",
        ],
    }
    res = False
    if nouveau_lieu in transitions_autorisées.get(ancien_lieu, []):
        res = True
    return res

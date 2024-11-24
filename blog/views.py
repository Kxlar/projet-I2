from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages

from .forms import EquipForm
from .models import Equipement, Character
from .controleur import (
    entrer,
    aller_vestiaires,
    aller_restaurant,
    aller_bloc,
    aller_boutique,
    echauffement,
    grimper,
    sortir,
    deplacement_autorisé,
)


def accueil_site(request):
    equipements = Equipement.objects.all()  # Liste des équipements
    characters_by_equip = []
    # Liste des personnage présent pour chaque équipements
    for equipement in equipements:
        characters_in_equip = Character.objects.filter(lieu=equipement)
        characters_by_equip.append((equipement, characters_in_equip))
    # Reset du personnage selectionné
    characters = Character.objects.all()
    for character in characters:
        character.is_selected = False
        character.save()
    # Context à envoyer au template
    context = {
        "equipements": equipements,
        "characters_by_equip": characters_by_equip,
    }

    return render(request, "blog/accueil.html", context)


def accueil_detail(request, pk):
    equipements = Equipement.objects.all()  # Liste des équipements
    characters = Character.objects.all()  # Liste des personnages
    characters_by_equip = []
    # Liste des personnage présent pour chaque équipements
    for equipement in equipements:
        characters_in_equip = Character.objects.filter(lieu=equipement)
        characters_by_equip.append((equipement, characters_in_equip))
    # Reset du personnage selectionné
    for character in characters:
        character.is_selected = False
        character.save()
    # Permet de suivre le personnage dans la vue interactive
    character_suivi = get_object_or_404(Character, pk=pk)
    character_suivi.is_selected = True
    # Forms
    lieu_char = get_object_or_404(Equipement, id_equip=character_suivi.lieu.id_equip)
    ancien_lieu = lieu_char.id_equip
    print(ancien_lieu)
    if request.method == "POST":
        form = EquipForm(request.POST, instance=character_suivi)
        if form.is_valid:
            form.save(commit=False)
            nouveau_lieu = get_object_or_404(
                Equipement, id_equip=character_suivi.lieu.id_equip
            ).id_equip
            print(nouveau_lieu)
            # Logique de déplacement entre les equipements
            if deplacement_autorisé(
                character_suivi.id_character, ancien_lieu, nouveau_lieu
            ):
                if nouveau_lieu == "Accueil":
                    entrer(character_suivi.id_character)
                elif nouveau_lieu == "Vestiaires":
                    aller_vestiaires(character_suivi.id_character)
                elif nouveau_lieu == "Salle_Echauffement":
                    echauffement(character_suivi.id_character)
                elif nouveau_lieu in [
                    "Bloc_jaune",
                    "Bloc_vert",
                    "Bloc_bleu",
                    "Bloc_rouge",
                    "Bloc_noir",
                    "Bloc_violet",
                ]:
                    aller_bloc(character_suivi.id_character, nouveau_lieu)
                elif nouveau_lieu == "Boutique":
                    aller_boutique(character_suivi.id_character)
                elif nouveau_lieu == "Restaurant":
                    aller_restaurant(character_suivi.id_character)
                elif nouveau_lieu == "Extérieur":
                    sortir(character_suivi.id_character)

            return redirect("accueil_detail", pk=pk)
    else:
        form = EquipForm()
        # Context à envoyer au template
        context = {
            "characters": characters,
            "equip_form": form,
            "character_suivi": character_suivi,
            "equipements": equipements,
            "characters_by_equip": characters_by_equip,
        }

        return render(request, "blog/accueil_detail.html", context)


def vue_immersive(request, pk):
    character_suivi = get_object_or_404(Character, pk=pk)
    character_suivi.is_selected = True
    character_suivi.save()
    equipement = get_object_or_404(Equipement, id_equip=character_suivi.lieu.id_equip)
    liste_bloc = Equipement.objects.filter(id_equip__contains="Bloc")
    # form
    ancien_lieu = equipement.id_equip
    if request.method == "POST":
        form = EquipForm(request.POST, instance=character_suivi)
        if form.is_valid():
            form.save(commit=False)
            nouveau_lieu = get_object_or_404(
                Equipement, id_equip=character_suivi.lieu.id_equip
            ).id_equip
            # Logique de déplacement entre les équipements
            if deplacement_autorisé(
                character_suivi.id_character, ancien_lieu, nouveau_lieu
            ):
                if nouveau_lieu == "Accueil":
                    entrer(character_suivi.id_character)
                elif nouveau_lieu == "Vestiaires":
                    aller_vestiaires(character_suivi.id_character)
                elif nouveau_lieu == "Salle_Echauffement":
                    echauffement(character_suivi.id_character)
                elif nouveau_lieu in [
                    "Bloc_jaune",
                    "Bloc_vert",
                    "Bloc_bleu",
                    "Bloc_rouge",
                    "Bloc_noir",
                    "Bloc_violet",
                ]:
                    aller_bloc(character_suivi.id_character, nouveau_lieu)
                elif nouveau_lieu == "Boutique":
                    aller_boutique(character_suivi.id_character)
                elif nouveau_lieu == "Restaurant":
                    aller_restaurant(character_suivi.id_character)
                elif nouveau_lieu == "Extérieur":
                    sortir(character_suivi.id_character)
            return redirect("vue_immersive", pk=pk)
    else:
        form = EquipForm()
        context = {
            "equipement": equipement,
            "equip_form": form,
            "character_suivi": character_suivi,
            "liste_bloc": liste_bloc,
        }

        return render(request, "blog/vue_immersive.html", context)


def grimper_bloc(request):
    character_suivi = get_object_or_404(Character, is_selected=True)
    bloc = character_suivi.lieu.id_equip
    if not bloc in [
        "Bloc_jaune",
        "Bloc_vert",
        "Bloc_bleu",
        "Bloc_rouge",
        "Bloc_noir",
        "Bloc_volet",
    ]:
        return redirect(
            "accueil_site"
        )  # Redirige vers l'accueil si le personnage n'est pas sur un bloc
    grimper(character_suivi.id_character, bloc)
    if character_suivi.reussite == True:
        messages.success(request, "Félicitations ! Vous avez réussi le bloc.")
    else:
        messages.warning(
            request, "Vous avez échoué au bloc. Réessayez ou changez d'équipement."
        )
    context = {
        "character_suivi": character_suivi,
    }
    return render(request, "blog/grimper.html", context)

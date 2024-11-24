from django.conf import settings
from django.db import models


class Equipement(models.Model):
    id_equip = models.CharField(max_length=100, primary_key=True)
    force_requise = models.IntegerField()
    technique_requise = models.IntegerField()
    photo = models.CharField(max_length=200)

    def __str__(self):
        return self.id_equip


class Character(models.Model):
    id_character = models.CharField(max_length=100, primary_key=True)
    energie = models.IntegerField()  # max energie = 10
    magnesie = models.IntegerField()  # max magnésie = 10
    force = models.IntegerField()  # max force = 10
    technique = models.IntegerField()  # max technique = 10
    reussite = models.BooleanField()
    photo = models.CharField(max_length=200)
    is_selected = models.BooleanField(default=False)
    lieu = models.ForeignKey(Equipement, on_delete=models.CASCADE)

    def __str__(self):
        return self.id_character

    # Méthode pour régénérer l'énergie ou la magnésie
    def regenerer(self, type_attribut, valeur_max):
        if type_attribut == "energie":
            self.energie = min(valeur_max, self.energie + valeur_max)
        elif type_attribut == "magnesie":
            self.magnesie = min(valeur_max, self.magnesie + valeur_max)
        self.save()

from datetime import date
from django.db import models
from aemter.models import Funktion

class Kandidatur(models.Model):
    name = models.CharField(max_length=50, null=False)
    vorname = models.CharField(max_length=50, null=False)
    email = models.CharField(max_length=50, null=False)
    funktion = models.ForeignKey(Funktion, on_delete=models.CASCADE, null=False)
    wahldatum = models.DateField(null=True)
    beschlussnummer = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.vorname + " " + self.name

    class Meta:
        verbose_name = "Kandidatur"
        verbose_name_plural = "Kandidaturen"

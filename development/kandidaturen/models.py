from datetime import date
from django.db import models
from simple_history.models import HistoricalRecords
from aemter.models import Funktion

class Kandidatur(models.Model):
    name = models.CharField(max_length=50, null=False)
    vorname = models.CharField(max_length=50, null=False)
    spitzname = models.CharField(max_length=50, null=True)
    wahldatum = models.DateField(null=True)
    beschlussnummer = models.CharField(max_length=50, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.vorname + " " + self.name

    class Meta:
        verbose_name = "Kandidatur"
        verbose_name_plural = "Kandidaturen"


class KandidaturAmt(models.Model):
    kandidatur = models.ForeignKey(Kandidatur, on_delete=models.CASCADE, null=False)
    funktion = models.ForeignKey(Funktion, on_delete=models.CASCADE, null=False)
    history = HistoricalRecords()
    def __str__(self):
        return self.kandidatur.__str__() + ", " + self.funktion.__str__()
    class Meta:
        verbose_name = "Zuordnung Kandidatur-Amt"
        verbose_name_plural = "Zuordnungen Kandidatur-Amt"


class KandidaturMail(models.Model):
    kandidatur = models.ForeignKey(Kandidatur, on_delete=models.CASCADE, null=False)
    email = models.CharField(max_length=50, null=False)
    history = HistoricalRecords()
    def __str__(self):
        return self.email + " " + self.kandidatur.__str__()
    class Meta:
        verbose_name = "Zuordnung Kandidatur-Mail"
        verbose_name_plural = "Zuordnungen Kandidatur-Mail"

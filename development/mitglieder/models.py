from datetime import date
from django.db import models
from django.db.models import Q
from simple_history.models import HistoricalRecords
from aemter.models import Funktion

class Mitglied(models.Model):
    name = models.CharField(max_length=50, null=False)
    vorname = models.CharField(max_length=50, null=False)
    spitzname = models.CharField(max_length=50, null=True)
    strasse = models.CharField(max_length=50, null=True)
    hausnr = models.CharField(null=True, max_length=10)
    plz = models.CharField(max_length=5, null=True)
    ort = models.CharField(max_length=50, null=True)
    tel_mobil = models.CharField(max_length=15, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.vorname + " " + self.name

    def curr_funktion_count(self):
        """
        Funktion that returns the number of the current funktions of the member.
        """
        return self.mitgliedamt_set\
            .filter(Q(amtszeit_ende__isnull=True) | Q(amtszeit_ende__gte=date.today()))\
            .count()

    def curr_funktion_first(self):
        """
        Funktion that returns the first of the current funktions of the member
        or None if the member has no current funktion.
        """
        if self.mitgliedamt_set\
                .filter(Q(amtszeit_ende__isnull=True) | Q(amtszeit_ende__gte=date.today())):
            return self.mitgliedamt_set\
                .filter(Q(amtszeit_ende__isnull=True) | Q(amtszeit_ende__gte=date.today()))\
                .first()\
                .funktion
        else:
            return None

    class Meta:
        verbose_name = "Mitglied"
        verbose_name_plural = "Mitglieder"


class MitgliedAmt(models.Model):
    mitglied = models.ForeignKey(Mitglied, on_delete=models.CASCADE, null=False)
    funktion = models.ForeignKey(Funktion, on_delete=models.CASCADE, null=False)
    amtszeit_beginn = models.DateField(null=True)
    amtszeit_ende = models.DateField(null=True)
    history = HistoricalRecords()
    def __str__(self):
        return self.mitglied.__str__() + ", " + self.funktion.__str__()
    class Meta:
        verbose_name = "Zuordnung Mitglied-Amt"
        verbose_name_plural = "Zuordnungen Mitglied-Amt"

class MitgliedMail(models.Model):
    mitglied = models.ForeignKey(Mitglied, on_delete=models.CASCADE, null=False)
    email = models.CharField(max_length=50, null=False)
    history = HistoricalRecords()
    def __str__(self):
        return self.email + " " + self.mitglied.__str__()
    class Meta:
        verbose_name = "Zuordnung Mitglied-Mail"
        verbose_name_plural = "Zuordnungen Mitglied-Mail"

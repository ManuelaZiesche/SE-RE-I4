from django.db import models
from simple_history.models import HistoricalRecords

from mitglieder.models import Mitglied, MitgliedAmt
from aemter.models import Recht

class Checkliste(models.Model):
    """
    Represents a checklist.
    
    * mitglied: The Mitglied the checklist was created for. Must not be null.
    * amt: The Funktion the checklist was created for. Can be null.
    * history: Contains a log of all changes made to the model. Provided by django-simple-history.

    Note that the checklist will be deleted if the associated Mitglied or Funktion is deleted (cascade).
    """
    mitglied = models.ForeignKey(Mitglied, on_delete=models.CASCADE, null=False)
    amt = models.ForeignKey(MitgliedAmt, on_delete=models.CASCADE, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.amt.__str__()
    class Meta:
        verbose_name = "Checkliste"
        verbose_name_plural = "Checklisten"

class Aufgabe(models.Model):
    """
    Defines a general task that can be added to a checklist.

    * bezeichnung: The task's title that will be shown in the UI. May contain up to 50 characters and must not be null.
    * history: Contains a log of all changes made to the model. Provided by django-simple-history.
    """
    bezeichnung = models.CharField(max_length=50, null=False)
    history = HistoricalRecords()

    def __str__(self):
        return self.bezeichnung.__str__()
    class Meta:
        verbose_name = "Aufgabe"
        verbose_name_plural = "Aufgaben"

class ChecklisteAufgabe(models.Model):
    """
    Represents a general task inside of a specific checklist.

    * checkliste: The checklist that this task belongs to. Must not be null.
    * aufgabe: The task that was assigned to the checklist. Must not be null.
    * abgehakt: Whether or not the task has been completed for this specific checklist. Must not be null and is false by default.
    * history: Contains a log of all changes made to the model. Provided by django-simple-history.

    Please note that the entry is deleted if the associated Checkliste or Aufgabe is deleted (cascade).
    """
    checkliste = models.ForeignKey(Checkliste, on_delete=models.CASCADE, null=False)
    aufgabe = models.ForeignKey(Aufgabe, on_delete=models.CASCADE, null=False)
    abgehakt = models.BooleanField(default=False, null=False)
    history = HistoricalRecords()

    def __str__(self):
        return self.checkliste.__str__() + " - " + self.aufgabe.__str__()
    class Meta:
        verbose_name = "Zuordnung Checkliste-Aufgabe"
        verbose_name_plural = "Zuordnungen Checkliste-Aufgabe"

class ChecklisteRecht(models.Model):
    """
    Represents a Recht to be given inside of a specific checklist.

    * checkliste: The checklist that this Recht was assigned to. Must not be null.
    * recht: The Recht that was assigned to the checklist. Must not be null.
    * abgehakt: Whether or not the Recht has been given for this specific checklist. Must not be null and is false by default.
    * history: Contains a log of all changes made to the model. Provided by django-simple-history.

    Please note that the entry is deleted if the associated Checkliste or Recht is deleted (cascade).
    """
    checkliste = models.ForeignKey(Checkliste, on_delete=models.CASCADE, null=False)
    recht = models.ForeignKey(Recht, on_delete=models.CASCADE, null=False)
    abgehakt = models.BooleanField(default=False, null=False)
    history = HistoricalRecords()

    def __str__(self):
        return self.checkliste.__str__() + " - " + self.recht.__str__()
    class Meta:
        verbose_name = "Zuordnung Checkliste-Recht"
        verbose_name_plural = "Zuordnungen Checkliste-Recht"

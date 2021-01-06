# -*- coding: utf-8 -*-

import os, django, sys
sys.path.append('..')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bin.settings")
django.setup()

from aemter.models import Organisationseinheit, Funktion, Unterbereich
import csv


def importAemter(file):
    """
        **!WARNING!**
        This function clears following Tables in your Database:

        * Organisationseinheit
        * Unterbereich
        * Funktion

        To use this function you need to have a file.csv with following structure:

        * delimiter = ','
        * organisationseinheit,unterbereich,funktion,max_members
        * First line is a heading and will not be imported


        :param file: File containing the data to be imported
        :type file: TextIO
        :return: No return Value
    """

    # Delete existing Data
    Organisationseinheit.objects.all().delete()
    Unterbereich.objects.all().delete()
    Funktion.objects.all().delete()

    # read CSV
    reader = csv.reader(file, delimiter=',')
    for row in reader:
        organisationseinheit = row[0]
        unterbereich = row[1]
        funktion = row[2]
        max_members = row[3]

        # Print Current Line for Debug
        # print(organisationseinheit + " | " + unterbereich + " | " + funktion + " | " + max_members)

        if (organisationseinheit == 'Organisationseinheit'):
            continue

        # Erstelle das Organisationseinheit
        if not Organisationseinheit.objects.filter(bezeichnung=organisationseinheit).exists():
            # print(organisationseinheit + " wurde erstellt")
            new_referat = Organisationseinheit(
                bezeichnung = organisationseinheit
            )
            new_referat.save()
        else:
            new_referat = Organisationseinheit.objects.get(bezeichnung=organisationseinheit)

        # Erstelle den Unterbereich
        if not Unterbereich.objects.filter(bezeichnung=unterbereich, organisationseinheit=new_referat).exists():
            new_unterbereich = None
            if (unterbereich != 'None'):
                # print(unterbereich + " wurde erstellt")
                new_unterbereich = Unterbereich(
                    bezeichnung = unterbereich,
                    organisationseinheit = new_referat
                )
                new_unterbereich.save()
        else:
            new_unterbereich = Unterbereich.objects.get(bezeichnung=unterbereich, organisationseinheit=new_referat)

        # Erstelle das Funktion
        # print(funktion + " wurde erstellt")
        new_amt = Funktion(
            bezeichnung = funktion,
            workload = 5,
            max_members = max_members,
            organisationseinheit = new_referat,
            unterbereich = new_unterbereich
        )
        new_amt.save()
    pass

if __name__ == "__main__":
    file = open("ReferateUnterbereicheAemter.csv", encoding="utf-8")
    importAemter(file)

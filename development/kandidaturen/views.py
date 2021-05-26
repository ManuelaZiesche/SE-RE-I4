from django.shortcuts import render
from django.core.paginator import Paginator
from django.contrib.auth.decorators import user_passes_test
from django.db.models.functions import Lower
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Kandidatur, KandidaturAmt, KandidaturMail
from aemter.models import Funktion, Organisationseinheit, Unterbereich
from datetime import date
import simplejson, json
from django.db.models import Q

# Anzahl der Aemter bzw. E-Mails die gespeichert werden muessen
aemternum = 0
emailnum = 0

def main_screen(request):
    """
    Zeigt eine Tabelle mit Kandidaturen an und ermöglicht die Suche nach Kandidaturen mit bestimmten Namen.
    Admins wird zusätzlich das Löschen von einem oder mehreren Kandidaturen sowie das Wechseln zur View zum Erstellen oder zum Bearbeiten ermöglicht.

    Aufgaben:

    * Bereitstellung der Daten: Die View holt sämtliche Kandidaturen-Einträge aus der Datenbank und stellt diese als Kontext bereit.
    * Rendern des Templates
    * Rechteeinschränkung: Nur Admins können Kandidaturen erstellen, bearbeiten und löschen.

    :param request: Die HTML-Request, welche den Aufruf der View ausgelöst hat.
    :return: Die gerenderte View.
    """
    if not request.user.is_authenticated:
        messages.error(request, "Du musst angemeldet sein, um diese Seite sehen zu können.")
        return redirect("/")

    # Paginate data
    queryset = Kandidatur.objects.order_by(Lower('vorname'), Lower('name'))

    paginator = Paginator(queryset, 15) # Show 15 entries per page
    queryset_page = paginator.get_page(1) # Get entries for the first page

    return render(
        request=request,
        template_name="kandidaturen/kandidaturen.html",
        context={"data": queryset_page
                 })

@user_passes_test(lambda u: u.is_superuser)
def kandidaturErstellenView(request):
    """
    View zum Erstellen einer Kandidatur.

    Stellt Textfelder, Dropwdowns und Buttons zum Hinzufügen der Attribute bereit. Anfangs steht jeweils genau ein Eingabebereich für ein Amt und eine E-Mail-Adresse zur Verfügung. Über Buttons können weitere dieser hinzugefügt oder bereits bestehende entfernt werden.

    Mit Betätigung des Speichern-Buttons wird überprüft, ob Name, Vorname, Ämter und E-Mail-Adressen ausgefüllt wurden und ob alle E-Mail-Adressen gültig sind. 
    Bei erfolgreicher Prüfung wird die Kandidatur gespeichert und der Nutzer zu main_screen umgeleitet, ansonsten werden Felder mit fehlenden oder fehlerhaften Eingaben rot markiert.

    Aufgaben:

    * Zugriffsbeschränkung: Zugriff wird nur gewährt, wenn der Nutzer angemeldet UND Administrator ist.
    * Rendern des Templates
    * Speichern des Mitglieds in der Datenbank

    :param request: Die HTML-Request, welche den Aufruf der View ausgelöst hat.
    :return: Die gerenderte View.
    """
    if not request.user.is_authenticated:
        messages.error(request, "Du musst angemeldet sein, um diese Seite sehen zu können.")
        return redirect("/")
    # beim Erstellen existiert anfangs jeweils ein Feld fuer Funktion und E-Mail
    global aemternum, emailnum
    aemternum = emailnum = 1
    # Laden aller Referate
    referate = Organisationseinheit.objects.order_by('bezeichnung')
    # Anzahl von E-Mails, Aemtern sowie Referate werden an Frontend gesendet
    return render(
        request=request,
        template_name="kandidaturen/kandidatur_erstellen_bearbeiten.html",
        context={'referate':referate, 'amtid': aemternum, 'emailid': emailnum
                 })


# Kandidatur erstellen
def erstellen(request):

    """
    Speichert eine neue Kandidatur in der Datenbank.

    Aufgaben:

    * Speichern der Daten: Die Daten werden aus request gelesen und in die Datenbank eingefügt.
    * Weiterleitung zur Kandidaturenansicht.
    * Rechteeinschränkung: Nur Admins können die Funktion auslösen.

    :param request: Die POST-Request, welche den Aufruf der Funktion ausgelöst hat. Enthält alle Daten zu einer Kandidatur.
    :return: Weiterleitung zur Kandidaturenansicht.
    """
    if not request.user.is_authenticated:
        messages.error(request, "Du musst angemeldet sein, um diese Seite sehen zu können.")
        return redirect("/")
    if not request.user.is_superuser:
        return HttpResponse("Permission denied")

    global aemternum, emailnum
    if request.method == 'POST':
        # Kandidatur
        vorname = request.POST['vorname']
        nachname = request.POST['nachname']
        spitzname = request.POST['spitzname']
        wahldatum_str = request.POST['wahldatum']
        wahldatum = datetime.datetime.strptime(wahldatum_str, "%d.%m.%Y").date()
        beschlussnummer = request.POST['beschlussnummer']
        kandidatur = Kandidatur(name=nachname, vorname=vorname, spitzname=spitzname, wahldatum=wahldatum, beschlussnummer=beschlussnummer)
        kandidatur.save()

        # E-Mail
        for i in range(1, emailnum+1):
            email = request.POST['email'+str(i)]
            kandidaturmail = KandidaturMail(email=email, kandidatur=kandidatur)
            kandidaturmail.save()

        # Funktion
        for i in range(1, aemternum+1):
            amt_id = request.POST['selectamt'+str(i)]
            funktion = Funktion.objects.get(pk=amt_id)
            """
            amtszeit_beginn_str = request.POST['beginn_kandidatur'+str(i)]
            if amtszeit_beginn_str:
                amtszeit_beginn = datetime.datetime.strptime(amtszeit_beginn_str, "%d.%m.%Y").date()
            else:
                amtszeit_beginn = None
            amtszeit_ende_str = request.POST['ende_kandidatur'+str(i)]
            if amtszeit_ende_str:
                amtszeit_ende = datetime.datetime.strptime(amtszeit_ende_str, "%d.%m.%Y").date()
            else:
                amtszeit_ende = None
            
            kandidaturamt = KandidaturAmt(funktion=funktion, kandidatur=kandidatur, amtszeit_beginn=amtszeit_beginn, amtszeit_ende=amtszeit_ende)
            """
            kandidaturamt = KandidaturAmt(funktion=funktion, kandidatur=kandidatur)
            kandidaturamt.save()

        return HttpResponseRedirect(reverse('kandidaturen:homepage'))
    else:
        return HttpResponseRedirect('/kandidaturen/erstellen')



def kandidatur_laden(request):
    """
    Rendert ein Modal mit allen Daten einer aus der Tabelle gewählten Kandidatur.
    Aufgaben:
    * Bereitstellung der Daten: Die Mitglied-ID wird aus request gelesen und extrahieren aller Daten zur Kandidatur mit dieser ID
    * Rendern des Templates
    * Rechteeinschränkung: Nur angemeldete Nutzer können das gerenderte Template anfordern.
    :param request: Die Ajax-Request, welche den Aufruf der Funktion ausgelöst hat. Enthält die Id des Mitglieds, dessen Daten angezeigt werden sollen.
    :return: Das gerenderte Modal, das mit Daten des angeforderten Mitglieds ausgefüllt wurde
    """

    if not request.user.is_authenticated:
        return HttpResponse("Permission denied")
    # Extrahieren der Mitglied-Id aus der GET-Request
    kandidatur_id = simplejson.loads(request.GET.get('mitgliedid'))
    # Daten zur Kandidatur mit dieser Id an Frontend senden
    kandidatur = Kandidatur.objects.get(pk=kandidatur_id)
    curr_funktionen = kandidatur.kandidaturamt_set\
        .filter(Q(amtszeit_ende__isnull=True) | Q(amtszeit_ende__gte=date.today()))
    prev_funktionen = kandidatur.kandidaturamt_set\
        .filter(Q(amtszeit_ende__isnull=False) & Q(amtszeit_ende__lt=date.today()))
    return render(
        request=request,
        template_name='mitglieder/modal.html',
        context={
            'kandidatur': kandidatur,
            'curr_funktionen': curr_funktionen,
            'prev_funktionen': prev_funktionen
        })
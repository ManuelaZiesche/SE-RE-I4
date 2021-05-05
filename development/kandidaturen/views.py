from django.shortcuts import render
from django.core.paginator import Paginator
from django.contrib.auth.decorators import user_passes_test
from django.db.models.functions import Lower
from .models import Kandidatur
from aemter.models import Funktion, Organisationseinheit, Unterbereich

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
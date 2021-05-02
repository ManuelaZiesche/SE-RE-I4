from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models.functions import Lower
from .models import Kandidatur

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
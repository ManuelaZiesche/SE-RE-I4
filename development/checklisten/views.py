from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse

from .models import Checkliste, ChecklisteAufgabe, ChecklisteRecht, Aufgabe
from aemter.models import FunktionRecht
from mitglieder.models import Mitglied, MitgliedAmt

def main_screen(request):
    """
    This view renders all existing checklists. Furthermore, it provides the 20 latest Mitglieder to the modal used for creating a new checklist.
    If the user is not authenticated, an error message will be displayed and the user is redirected to the login page.

    :param request: The HTTP request that triggered the view.
    :return: The rendered main_screen view, or a redirect to the login page if the user is not authenticated.
    """
    if not request.user.is_authenticated:
        messages.error(request, "Du musst angemeldet sein, um diese Seite sehen zu können.")
        return redirect("/")

    checklisten = Checkliste.objects.all()
    mitglieder = Mitglied.objects.all().order_by('-id')[:20]

    return render(request=request, 
                  template_name='checklisten/main_screen.html', 
                  context = {"checklisten": checklisten, "mitglieder": mitglieder})

def erstellen(request):
    """
    This view is responsible for creating a new checklist.
    It first checks if the user is allowed to create a new checklist (i.e. is authenticated and superuser).
    Next, the Mitglied's and Funktion's IDs as well as whether general tasks shall be included are fetched from the request.
    The view then tries to find the Mitglied and Funktion with the specified ID, and returns an error message if at least one of them could not be found.
    After that, the view checks if a checklist for this Mitglied and Funktion already exists. If that is the case, an error message is shown to the user.
    Finally, the new checklist is created and all Aufgaben and Rechte are added to it according to the specified parameters in the request.

    :param request: The HTTP request that triggered the view, including parameters mitgliedSelect, funktionSelect and generalTasksCheckbox.
    :return: A HttpResponse, if an error has occured, indicating the error to the user.
    :return: A redirect to /checklisten if creating the checklist was successful or a checklist for the same Mitglied and Funktion already exists.
    """
    if not request.user.is_authenticated:
        return HttpResponse("Permission denied")
    if not request.user.is_superuser:
        return HttpResponse("Permission denied")

    # Get data from request
    mitglied_id = request.POST.get("mitgliedSelect")
    funktion_id = request.POST.get("funktionSelect")
    includeGeneralTasks = request.POST.get("generalTasksCheckbox")

    # Determine if general tasks shall be included
    if includeGeneralTasks == "on" or includeGeneralTasks is None and funktion_id == "-1":
        includeGeneralTasks = True
    else:
        includeGeneralTasks = False

    # Get foreign data
    mitglied = Mitglied.objects.get(id=mitglied_id)
    if not mitglied:
        return HttpResponse("Mitglied does not exist")
    
    # Get funktion if selected
    funktion = None
    if funktion_id != "-1":
        funktion = MitgliedAmt.objects.get(id=funktion_id)
        if not funktion:
            return HttpResponse("Funktion does not exist")

    existing = Checkliste.objects.filter(mitglied=mitglied, amt=funktion)
    if existing:
        messages.error(request, "Es existiert bereits eine Checkliste für dieses Mitglied und diese Funktion.")
        return redirect("/checklisten")

    # Create checkliste
    checkliste = Checkliste(mitglied=mitglied, amt=funktion)
    checkliste.save()

    # Add general tasks if selected
    if includeGeneralTasks == True:
        for task in Aufgabe.objects.all():
            aufgabe = ChecklisteAufgabe(checkliste=checkliste, aufgabe=task)
            aufgabe.save()
    
    # Add Rechte if Funktion was selected
    if funktion is not None:
        for funktion_recht in FunktionRecht.objects.filter(funktion__id=funktion.funktion.id):
            perm = funktion_recht.recht
            recht = ChecklisteRecht(checkliste=checkliste, recht=perm)
            recht.save()

    return redirect("/checklisten")

def abhaken(request):
    """
    This view is responsible for checking or unchecking a task from the checklist.
    It first checks if the user is allowed to check a task, i.e. is auhenticated and superuser.
    Next, the parameters task_type and task_id are fetched from the request. They are used to determine if an Aufgabe or a Recht was checked, and to get the correct task.
    Finally, the task is checked or unchecked depending on its current state and the changes are saved.

    :param request: The HTTP request that triggered the view, including parameters task_type and task_id.
    :return: An empty HttpResponse if the operation was successful.
    :return: An HttpResponse indicitang the error if an error has occured or if the user is not allowed to perform the operation.
    """
    if not request.user.is_authenticated:
        return HttpResponse("Nice try, FBI.")
    if not request.user.is_superuser:
        return HttpResponse("No way, CIA.")

    # Determine if an Aufgabe or a Recht was selected
    task_type = request.POST.get('task_type')
    if(task_type != "Aufgabe" and task_type != "Recht"):
        return HttpResponse("Invalid task_type")

    # Get the appropriate task from ChecklisteAufgabe or ChecklisteRecht, depending on task_type
    task_id = request.POST.get('task_id')
    if not task_id:
        return HttpResponse("No task_id provided")

    task = None
    if task_type == "Aufgabe":
        task = ChecklisteAufgabe.objects.get(id=task_id)
    if task_type == "Recht":
        task = ChecklisteRecht.objects.get(id=task_id)
    if not task:
        return HttpResponse("Invalid task_id")

    # Flip the (boolean) abgehakt property and save it
    task.abgehakt = not task.abgehakt
    task.save()

    return HttpResponse()

def loeschen(request):
    """
    This view is responsible for deleting an existing checklist.
    First, it checks whether the user is allowed to delete the checklist (i.e. is authenticated and superuser).
    Next, the checkliste specified in the request's parameter checkliste_id is deleted. 
    Since all ForeignKey relations in other models are set to cascade if the checklist is deleted (i.e. in ChecklisteRecht and AufgabeRecht), only the checklist itself needs to be deleted explicitly.

    :param request: The HTTP request that triggered the view, including parameter checkliste_id.
    :return: An empty HttpResponse if deleting the checklist was successful.
    :return: An HttpResponse indicating an error if one occured or a user is not allowed to to delete a checklist.
    """
    if not request.user.is_authenticated:
        return HttpResponse("Not today, NSA.")
    if not request.user.is_superuser:
        return HttpResponse("Good trick, MI6.")

    # Get Checkliste with specified ID
    checkliste_id = request.POST.get('checkliste_id')
    if not checkliste_id:
        return HttpResponse("No checkliste_id provided")
    checkliste = Checkliste.objects.get(id=checkliste_id)
    if not checkliste:
        return HttpResponse("Invalid checkliste_id")

    # Delete Checkliste
    checkliste.delete()

    return HttpResponse()

def get_funktionen(request):
    """
    This view is responsible for getting all Funktionen associated to a Mitglied that was selected in the create checklist modal.
    First, it checks if the user is allowed to get a list of Funktionen for a Mitglied in this context (i.e. the user is authenticated and superuser).
    Next, all Funktionen for the specified mitglied_id are determined and returned through a rendered template of select options to populate the dropdown in the create checklist modal.

    :param request: The HTTP request that triggered the view, including the mitglied_id to get the Funktionen for.
    :return: An HttpResponse indicating the error if an error occured.
    :return: The rendered select options to populate the dropdown with if everything was successful.
    """
    if not request.user.is_authenticated:
        return HttpResponse("Permission denied")
    if not request.user.is_superuser:
        return HttpResponse("Permission denied")

    mitglied_id = request.GET.get('mitglied_id')
    if not mitglied_id:
        return HttpResponse("No mitglied_id provided")
    funktionen = MitgliedAmt.objects.filter(mitglied__id=mitglied_id)

    return render(request=request, 
                  template_name='checklisten/_funktionSelectOptions.html', 
                  context = {"funktionen": funktionen})
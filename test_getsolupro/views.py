from django.shortcuts import render, redirect   # Les méthodes de rendu simple et redirection
from django.views.generic import TemplateView   # la classe de rendu de vues génériques 
from django.contrib import messages     # Module de gestion des messages contextuels
from django.http import JsonResponse
from urllib.request import urlopen
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

# Importation des modules de traitement d'image
import PIL.Image
import PIL.ImageDraw
import face_recognition
import base64
from io import BytesIO


# La vue traitant les requetes http au rendu de la page d'inscription
class page_inscription(TemplateView):
    template_name = "page_inscription.html"   # Le fichier html cerrespondant à générer à la demande
    
    # La vue retournée à la demande de la methode get d'une requete http 
    def get(self, request, *args, **kwargs):
        kwargs["formulaire"] = UserCreationForm()     # formulaire d'inscription
        return super().get(request, *args, **kwargs)
    
    # La vue retournée à la demande de la methode post d'une requete http 
    def post(self, request, *args, **kwargs):
        print(request.POST)
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect("page_accueil")
        else:
            kwargs["formulaire"] = UserCreationForm()     # formulaire d'inscription
            return super().get(request, *args, **kwargs)


# L'API traitant les requetes http au rendu de la page d'accueil
class page_accueil(TemplateView):
    template_name = "page_accueil.html"   # Le fichier html cerrespondant à générer à la demande
    
    # La vue retournée à la demande de la methode get d'une requete http
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    # La vue retournée à la demande de la methode post d'une requete http 
    def post(self, request, *args, **kwargs):
        url_image = request.POST.get("url_image")   # on recupere le contenu du champ url
        fichier_image = request.FILES.get("fichier_image")   # on recupere le contenu du champ fichier image
        
        # On verifie s'il y a une image imortée en fichier joint et une url saisie.
        # Si les deux existent, on choisit de traiter le fichier joint
        # sinon on traite ce qui existe seul (fichier ou url)
        if fichier_image and url_image:
            image_a_traiter = fichier_image
        elif fichier_image:
            image_a_traiter = fichier_image
        elif url_image:
            image_a_traiter = urlopen(url_image)
        else:
            return JsonResponse({
            "operation_status": "erreur",
            "message": "Désolé ! il n'y a aucune image à traiter."
        })

        # Chargement des données binaires de l'image
        given_image = face_recognition.load_image_file(image_a_traiter)

        # Detection des visages dans l'image
        face_locations = face_recognition.face_locations(given_image)
        nombre_de_visage = len(face_locations)  # Nombre de visage trouvé

        # Chargement des données binaires de l'image
        pil_image = PIL.Image.fromarray(given_image)

        for face_location in face_locations:
            # recuperation des cordonnees de la zone de visage
            top, left, bottom, right = face_location
            # Dessin du cadre sur la zone de detection du visage
            draw = PIL.ImageDraw.Draw(pil_image)
            draw.rectangle([left, top, right, bottom], outline="red", width=10)
        
        # Sauvegarde temporaire de l'image traitée
        buffered = BytesIO()
        pil_image.save(buffered, format="JPEG") # formattage en JPEG
        donnees_image = str(base64.b64encode(buffered.getvalue()))   # Encodage en binaire 64bits pour lecture dans une balise <img> 

        # Generation de la reponse en format JSON (API REST)
        return JsonResponse({
            "operation_status": "ok",
            "message": "{} visage(s) détecté(s) dans cette image.".format(nombre_de_visage),
            "donnees_image": donnees_image[2:-1]
        })





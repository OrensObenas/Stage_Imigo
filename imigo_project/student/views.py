from django.shortcuts import render, redirect
from .forms import EtudiantInfosForm, EtudiantInscriptionForm
from .models import Etudiant
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from .models import Document
from .forms import DocumentForm

def inscription_view(request):
    if request.method == 'POST':
        form = EtudiantInscriptionForm(request.POST)
        if form.is_valid():
            etudiant = form.save(commit=False)  # ne sauvegarde pas encore
            etudiant.password = make_password(etudiant.password)  # on chiffre ici
            etudiant.save()
            messages.success(request, "Inscription réussie ! Connectez-vous.")
            return redirect('connexion')
    else:
        form = EtudiantInscriptionForm()
    return render(request, 'student/inscription.html', {'form': form})


def connexion_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            etudiant = Etudiant.objects.get(email=email)
            if check_password(password, etudiant.password):
                request.session['etudiant_id'] = etudiant.id
                messages.success(request, "Connexion réussie !")
                return redirect('dashboard')
            else:
                messages.error(request, "Mot de passe incorrect.")
        except Etudiant.DoesNotExist:
            messages.error(request, "Email non trouvé.")
    
    return render(request, 'student/connexion.html')

def dashboard_view(request):
    etudiant_id = request.session.get('etudiant_id')

    if not etudiant_id:
        return redirect('connexion')  # l'utilisateur n'est pas connecté

    etudiant = Etudiant.objects.get(id=etudiant_id)
    return render(request, 'student/dashboard.html', {'etudiant': etudiant})

def deconnexion_view(request):
    request.session.flush()  # Efface la session
    return redirect('connexion')

def infos_personnelles_view(request):
    etudiant_id = request.session.get('etudiant_id')
    if not etudiant_id:
        return redirect('connexion')

    etudiant = Etudiant.objects.get(id=etudiant_id)

    if request.method == 'POST':
        form = EtudiantInfosForm(request.POST, instance=etudiant)
        if form.is_valid():
            form.save()
            messages.success(request, "Informations mises à jour avec succès.")
            return redirect('dashboard')
    else:
        form = EtudiantInfosForm(instance=etudiant)

    return render(request, 'student/infos_personnelles.html', {'form': form})

def documents_view(request):
    etudiant_id = request.session.get('etudiant_id')
    if not etudiant_id:
        return redirect('connexion')

    etudiant = Etudiant.objects.get(id=etudiant_id)
    documents = Document.objects.filter(etudiant=etudiant)

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.etudiant = etudiant
            doc.save()
            messages.success(request, "Document déposé avec succès.")
            return redirect('documents')
    else:
        form = DocumentForm()

    return render(request, 'student/documents.html', {
        'form': form,
        'documents': documents,
    })

def supprimer_document(request, document_id):
    etudiant_id = request.session.get('etudiant_id')
    if not etudiant_id:
        return redirect('connexion')

    document = Document.objects.get(id=document_id)

    # sécurité : l'étudiant ne peut supprimer QUE ses propres documents
    if document.etudiant.id != etudiant_id:
        return redirect('documents')  # tentative interdite

    document.delete()
    messages.success(request, "Document supprimé avec succès.")
    return redirect('documents')
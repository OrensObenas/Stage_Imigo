from django import forms
from .models import Document, Etudiant

class EtudiantInscriptionForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Etudiant
        fields = ['nom', 'prenoms', 'email', 'telephone', 'password']
        
class EtudiantInfosForm(forms.ModelForm):
    class Meta:
        model = Etudiant
        exclude = ['password', 'email']  # On ne modifie pas ces champs ici
        
class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['nom', 'fichier']
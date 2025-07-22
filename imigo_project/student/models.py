from django.db import models

class Etudiant(models.Model):
    nom = models.CharField(max_length=100)
    prenoms = models.CharField(max_length=100)
    date_naissance = models.DateField(null=True, blank=True)
    langue_principale = models.CharField(max_length=50, null=True, blank=True)
    nationalite = models.CharField(max_length=50, null=True, blank=True)
    numero_passeport = models.CharField(max_length=50, null=True, blank=True)
    date_expiration_passeport = models.DateField(null=True, blank=True)
    statut_marital = models.CharField(max_length=50, null=True, blank=True)
    sexe = models.CharField(max_length=10, null=True, blank=True)
    adresse = models.TextField(null=True, blank=True)
    ville_residence = models.CharField(max_length=100, null=True, blank=True)
    quartier_residence = models.CharField(max_length=100, null=True, blank=True)
    code_postal = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    pays_etudes = models.CharField(max_length=100, null=True, blank=True)
    ecole_provenance = models.CharField(max_length=100, null=True, blank=True)
    niveau_etude = models.CharField(max_length=50, null=True, blank=True)
    diplome_universite = models.CharField(max_length=100, null=True, blank=True)
    diplome_langue = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.nom} {self.prenoms}"

class Filiere(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    cout = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nom

class Ecole(models.Model):
    nom = models.CharField(max_length=100)
    ville = models.CharField(max_length=100)
    pays = models.CharField(max_length=100)
    description = models.TextField()
    localisation = models.CharField(max_length=255)
    filieres = models.ManyToManyField(Filiere, related_name='ecoles')

    def __str__(self):
        return self.nom

class Candidature(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE)
    statut = models.CharField(max_length=50, default='en attente')  # accepté, refusé, en cours, etc.

    def __str__(self):
        return f"{self.etudiant} postule à {self.filiere}"
    
class Document(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    fichier = models.FileField(upload_to='documents/')
    date_depot = models.DateTimeField(auto_now_add=True)
    valide = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nom} - {self.etudiant.nom}"
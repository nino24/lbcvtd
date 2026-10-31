"""Définition unique des colonnes du tableau d'annonces.

Partagée par le générateur de modèle (creer_modele.py) et par l'outil de
publication (publier.py) : si vous ajoutez une colonne, faites-le ici.
"""

# (clé interne, en-tête affiché, largeur Excel, aide affichée en commentaire)
COLONNES = [
    ("sku", "SKU", 12, "Référence unique de l'objet (ex. LBC-001). Obligatoire."),
    ("statut", "Statut", 13, "À publier = l'outil la poste. Brouillon = ignorée. Les autres statuts sont remplis par l'outil ou par vous."),
    ("titre", "Titre", 42, "Titre de l'annonce, 50 caractères max conseillés sur leboncoin."),
    ("nb_car", "Car.", 6, "Calculé automatiquement : longueur du titre (rouge si > 50)."),
    ("description", "Description", 60, "Texte de l'annonce. Retours à la ligne autorisés (Alt+Entrée dans Excel)."),
    ("categorie", "Catégorie", 22, "Catégorie leboncoin (liste déroulante, onglet Listes)."),
    ("prix", "Prix (€)", 10, "Prix de vente TTC en euros, nombre entier."),
    ("etat", "État", 18, "État de l'objet (liste déroulante)."),
    ("marque", "Marque", 16, "Facultatif."),
    ("photos", "Photos", 40, "Chemins de fichiers ou URL, séparés par ; ou retour à la ligne. Vide = l'outil cherche les images nommées SKU* dans le dossier photos."),
    ("code_postal", "Code postal", 11, "Lieu de l'annonce."),
    ("ville", "Ville", 16, "Facultatif si le code postal suffit."),
    ("livraison", "Livraison", 10, "Oui / Non : proposer l'envoi par colis."),
    ("poids_kg", "Poids colis (kg)", 12, "Obligatoire si Livraison = Oui."),
    ("main_propre", "Main propre", 11, "Oui / Non."),
    ("quantite", "Quantité", 9, "Stock disponible (compte pro)."),
    ("notes", "Notes internes", 24, "Jamais publiées : emplacement, prix d'achat, fournisseur…"),
    ("date_publication", "Publiée le", 17, "Rempli par l'outil."),
    ("lien", "Lien annonce", 34, "Rempli par l'outil."),
    ("message", "Message outil", 34, "Rempli par l'outil : erreurs de validation ou de publication."),
]

CLES = [c[0] for c in COLONNES]
ENTETES = {c[0]: c[1] for c in COLONNES}

STATUTS = ["À publier", "Brouillon", "En cours", "Publiée", "Erreur", "Vendue", "À retirer"]
ETATS = ["Neuf", "Très bon état", "Bon état", "État satisfaisant", "Pour pièces"]
OUI_NON = ["Oui", "Non"]
CATEGORIES = [
    "Électroménager", "Meubles", "Décoration", "Linge de maison", "Bricolage",
    "Jardinage", "Ordinateurs", "Accessoires informatique", "Téléphones & Objets connectés",
    "Tablettes & Liseuses", "Photo, audio & vidéo", "Consoles", "Jeux vidéo",
    "Vêtements", "Chaussures", "Accessoires & Bagagerie", "Montres & Bijoux",
    "Équipement bébé", "Vêtements bébé", "Jeux & Jouets", "Livres", "CD - Musique",
    "DVD - Films", "Instruments de musique", "Sport & Plein air", "Vélos",
    "Collection", "Antiquités", "Loisirs créatifs", "Matériel professionnel", "Autres",
]

ONGLET_ANNONCES = "Annonces"
LIGNE_ENTETE = 1
TITRE_MAX = 50

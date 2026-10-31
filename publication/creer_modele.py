"""Génère le modèle Excel `modele_annonces_leboncoin.xlsx`.

Usage : python creer_modele.py [chemin_sortie.xlsx]

Le fichier produit s'ouvre dans Excel, LibreOffice ou Google Sheets
(Fichier > Importer) : listes déroulantes, compteur de caractères du titre
et couleurs de statut sont conservés.
"""
import sys
from pathlib import Path

from openpyxl import Workbook
from openpyxl.comments import Comment
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

from colonnes import (CATEGORIES, CLES, COLONNES, ETATS, ONGLET_ANNONCES, OUI_NON,
                      STATUTS, TITRE_MAX)

NB_LIGNES = 500  # lignes préparées (validations, formules)
ORANGE = "FF6E14"  # couleur leboncoin

EXEMPLES = [
    {
        "sku": "LBC-001", "statut": "Brouillon",
        "titre": "Machine à café Nespresso Vertuo Next noire",
        "description": "Machine Nespresso Vertuo Next, coloris noir, utilisée quelques mois.\n"
                       "Fonctionne parfaitement, détartrée récemment.\n"
                       "Livrée avec le câble d'alimentation.\n\nRéf. : LBC-001",
        "categorie": "Électroménager", "prix": 55, "etat": "Très bon état", "marque": "Nespresso",
        "photos": "", "code_postal": "69003", "ville": "Lyon", "livraison": "Oui",
        "poids_kg": 5, "main_propre": "Oui", "quantite": 1, "notes": "Étagère B2 - acheté 20 €",
    },
    {
        "sku": "LBC-002", "statut": "Brouillon",
        "titre": "Lot de 3 livres Harry Potter grand format",
        "description": "Tomes 1, 2 et 3, éditions Gallimard grand format.\n"
                       "Couvertures légèrement frottées, intérieur impeccable.\n\nRéf. : LBC-002",
        "categorie": "Livres", "prix": 18, "etat": "Bon état", "marque": "Gallimard",
        "photos": "photos/LBC-002-1.jpg; photos/LBC-002-2.jpg", "code_postal": "69003", "ville": "Lyon",
        "livraison": "Oui", "poids_kg": 2, "main_propre": "Oui", "quantite": 1, "notes": "Carton 4",
    },
]


def col(cle):
    return get_column_letter(CLES.index(cle) + 1)


def onglet_annonces(wb):
    ws = wb.active
    ws.title = ONGLET_ANNONCES
    entete_fill = PatternFill("solid", fgColor=ORANGE)
    auto_fill = PatternFill("solid", fgColor="F2F2F2")
    fin = Side(style="thin", color="D9D9D9")

    for i, (cle, entete, largeur, aide) in enumerate(COLONNES, start=1):
        c = ws.cell(row=1, column=i, value=entete)
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = entete_fill if cle not in ("date_publication", "lien", "message", "nb_car") else PatternFill("solid", fgColor="7F7F7F")
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.comment = Comment(aide, "Modèle")
        ws.column_dimensions[get_column_letter(i)].width = largeur
    ws.row_dimensions[1].height = 32
    ws.freeze_panes = "C2"
    ws.auto_filter.ref = f"A1:{get_column_letter(len(COLONNES))}{NB_LIGNES + 1}"

    for r, ex in enumerate(EXEMPLES, start=2):
        for cle, val in ex.items():
            ws[f"{col(cle)}{r}"] = val

    for r in range(2, NB_LIGNES + 2):
        ws[f"{col('nb_car')}{r}"] = f'=IF({col("titre")}{r}="","",LEN({col("titre")}{r}))'
        for cle in CLES:
            c = ws[f"{col(cle)}{r}"]
            c.alignment = Alignment(vertical="top", wrap_text=cle in ("description", "photos", "message"))
            c.border = Border(bottom=fin)
            if cle in ("nb_car", "date_publication", "lien", "message"):
                c.fill = auto_fill
        ws[f"{col('prix')}{r}"].number_format = '# ##0 "€"'

    # Listes déroulantes (plages nommées sur l'onglet Listes)
    def liste(cle, plage, message):
        dv = DataValidation(type="list", formula1=plage, allow_blank=True,
                            showErrorMessage=True, errorTitle="Valeur non prévue", error=message)
        dv.add(f"{col(cle)}2:{col(cle)}{NB_LIGNES + 1}")
        ws.add_data_validation(dv)

    liste("statut", "=Listes!$A$2:$A$%d" % (len(STATUTS) + 1), "Choisissez un statut dans la liste.")
    liste("etat", "=Listes!$B$2:$B$%d" % (len(ETATS) + 1), "Choisissez un état dans la liste.")
    liste("categorie", "=Listes!$C$2:$C$%d" % (len(CATEGORIES) + 1), "Choisissez une catégorie (complétez l'onglet Listes si besoin).")
    for cle in ("livraison", "main_propre"):
        liste(cle, "=Listes!$D$2:$D$3", "Oui ou Non.")

    prix = DataValidation(type="whole", operator="between", formula1="1", formula2="999999",
                          showErrorMessage=True, error="Prix entier en euros.")
    prix.add(f"{col('prix')}2:{col('prix')}{NB_LIGNES + 1}")
    ws.add_data_validation(prix)

    # Mises en forme conditionnelles
    zone_nb = f"{col('nb_car')}2:{col('nb_car')}{NB_LIGNES + 1}"
    ws.conditional_formatting.add(zone_nb, CellIsRule(operator="greaterThan", formula=[str(TITRE_MAX)],
                                                      fill=PatternFill("solid", fgColor="F8CBAD"), font=Font(bold=True, color="C00000")))
    zone_statut = f"{col('statut')}2:{col('statut')}{NB_LIGNES + 1}"
    couleurs = {"À publier": "FFE699", "En cours": "BDD7EE", "Publiée": "C6EFCE",
                "Erreur": "FFC7CE", "Vendue": "D9D9D9", "À retirer": "F4B084"}
    s = col("statut")
    for statut, couleur in couleurs.items():
        ws.conditional_formatting.add(zone_statut, FormulaRule(formula=[f'${s}2="{statut}"'],
                                                               fill=PatternFill("solid", fgColor=couleur)))
    # Ligne entière grisée quand vendue
    ws.conditional_formatting.add(f"A2:{get_column_letter(len(COLONNES))}{NB_LIGNES + 1}",
                                  FormulaRule(formula=[f'${s}2="Vendue"'], font=Font(color="808080", italic=True)))


def onglet_listes(wb):
    ws = wb.create_sheet("Listes")
    for j, (titre, valeurs) in enumerate([("Statuts", STATUTS), ("États", ETATS),
                                         ("Catégories", CATEGORIES), ("Oui/Non", OUI_NON)], start=1):
        c = ws.cell(row=1, column=j, value=titre)
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor=ORANGE)
        for i, v in enumerate(valeurs, start=2):
            ws.cell(row=i, column=j, value=v)
        ws.column_dimensions[get_column_letter(j)].width = 30


def onglet_suivi(wb):
    ws = wb.create_sheet("Tableau de bord")
    ws["A1"] = "Tableau de bord des annonces"
    ws["A1"].font = Font(bold=True, size=14, color=ORANGE)
    s, p = col("statut"), col("prix")
    ws["A3"], ws["B3"], ws["C3"] = "Statut", "Nombre", "Valeur (€)"
    for c in ("A3", "B3", "C3"):
        ws[c].font = Font(bold=True)
    for i, statut in enumerate(STATUTS, start=4):
        ws[f"A{i}"] = statut
        ws[f"B{i}"] = f'=COUNTIF({ONGLET_ANNONCES}!{s}:{s},A{i})'
        ws[f"C{i}"] = f'=SUMIF({ONGLET_ANNONCES}!{s}:{s},A{i},{ONGLET_ANNONCES}!{p}:{p})'
        ws[f"C{i}"].number_format = '# ##0 "€"'
    fin = 4 + len(STATUTS)
    ws[f"A{fin}"] = "Total"
    ws[f"A{fin}"].font = Font(bold=True)
    ws[f"B{fin}"] = f"=SUM(B4:B{fin - 1})"
    ws[f"C{fin}"] = f"=SUM(C4:C{fin - 1})"
    ws[f"C{fin}"].number_format = '# ##0 "€"'
    ws.column_dimensions["A"].width = 18
    ws.column_dimensions["B"].width = 12
    ws.column_dimensions["C"].width = 14


def onglet_mode_emploi(wb):
    ws = wb.create_sheet("Mode d'emploi")
    lignes = [
        ("Mode d'emploi", True),
        ("", False),
        ("1. Une ligne = une annonce. Remplissez au minimum : SKU, Titre, Description, Catégorie, Prix, État, Code postal.", False),
        ("2. Photos : indiquez les chemins (ex. photos/LBC-003-1.jpg) séparés par « ; », ou laissez vide et nommez", False),
        ("    vos fichiers d'après le SKU (LBC-003-1.jpg, LBC-003-2.jpg…) dans le dossier photos : l'outil les trouve seul.", False),
        ("3. Passez le Statut à « À publier » pour les annonces prêtes. « Brouillon » = ignorée par l'outil.", False),
        ("4. Lancez : python publier.py verifier modele_annonces_leboncoin.xlsx  (contrôle sans rien publier)", False),
        ("5. Puis :   python publier.py publier modele_annonces_leboncoin.xlsx", False),
        ("6. L'outil remplit Statut, Publiée le, Lien annonce et Message outil. Fermez le fichier dans Excel pendant la publication.", False),
        ("", False),
        ("Colonnes grises = remplies automatiquement, ne pas saisir.", False),
        ("Car. passe en rouge si le titre dépasse 50 caractères.", False),
        ("Onglet Listes : ajoutez vos propres catégories en bas de la colonne C (puis élargissez la validation si besoin).", False),
        ("Google Sheets : Fichier > Importer ce fichier, ou utilisez directement la version Google Sheets (voir README).", False),
    ]
    for i, (texte, gras) in enumerate(lignes, start=1):
        ws[f"A{i}"] = texte
        if gras:
            ws[f"A{i}"].font = Font(bold=True, size=14, color=ORANGE)
    ws.column_dimensions["A"].width = 120


def main():
    sortie = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).with_name("modele_annonces_leboncoin.xlsx"))
    wb = Workbook()
    onglet_annonces(wb)
    onglet_listes(wb)
    onglet_suivi(wb)
    onglet_mode_emploi(wb)
    wb.save(sortie)
    print(f"Modèle créé : {sortie}")


if __name__ == "__main__":
    main()

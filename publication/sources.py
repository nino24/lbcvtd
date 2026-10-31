"""Lecture / écriture du tableau d'annonces : fichier Excel local ou Google Sheets.

Les deux sources exposent la même interface :
    annonces()                      -> liste de dicts (clé interne -> valeur), avec "_ligne"
    ecrire(ligne, {cle: valeur})    -> met à jour une ligne (mémorisé)
    enregistrer()                   -> écrit les modifications
"""
from pathlib import Path

from colonnes import CLES, ENTETES, LIGNE_ENTETE, ONGLET_ANNONCES

_ENTETE_VERS_CLE = {v.lower(): k for k, v in ENTETES.items()}


def _normaliser_entetes(entetes):
    """Associe chaque colonne du fichier à une clé interne (tolère l'ordre et la casse)."""
    index = {}
    for i, e in enumerate(entetes):
        cle = _ENTETE_VERS_CLE.get(str(e or "").strip().lower())
        if cle:
            index[cle] = i
    manquantes = [ENTETES[c] for c in ("sku", "statut", "titre") if c not in index]
    if manquantes:
        raise ValueError(f"Colonnes obligatoires absentes du tableau : {', '.join(manquantes)}")
    return index


class SourceExcel:
    def __init__(self, chemin):
        from openpyxl import load_workbook
        self.chemin = Path(chemin)
        self.dossier = self.chemin.parent
        self.wb = load_workbook(self.chemin)  # formules conservées
        self.ws = self.wb[ONGLET_ANNONCES] if ONGLET_ANNONCES in self.wb.sheetnames else self.wb.active
        entetes = [c.value for c in self.ws[LIGNE_ENTETE]]
        self.index = _normaliser_entetes(entetes)

    def annonces(self):
        res = []
        for n, row in enumerate(self.ws.iter_rows(min_row=LIGNE_ENTETE + 1, values_only=True), start=LIGNE_ENTETE + 1):
            a = {cle: row[i] if i < len(row) else None for cle, i in self.index.items()}
            if not any(a.get(c) for c in ("sku", "titre", "description")):
                continue
            a["_ligne"] = n
            res.append(a)
        return res

    def ecrire(self, ligne, valeurs):
        for cle, v in valeurs.items():
            if cle in self.index:
                self.ws.cell(row=ligne, column=self.index[cle] + 1, value=v)

    def enregistrer(self):
        try:
            self.wb.save(self.chemin)
            return self.chemin
        except PermissionError:
            # Fichier ouvert dans Excel : on ne perd rien, on écrit à côté.
            secours = self.chemin.with_name(self.chemin.stem + "_maj.xlsx")
            self.wb.save(secours)
            return secours


class SourceGoogleSheets:
    """Google Sheets via un compte de service (voir README, section Google Sheets).

    Le classeur doit être partagé en « Éditeur » avec l'adresse e-mail du compte de service.
    """

    def __init__(self, id_ou_url, fichier_identifiants, dossier_photos="."):
        import gspread
        self.dossier = Path(dossier_photos)
        gc = gspread.service_account(filename=fichier_identifiants)
        sh = gc.open_by_url(id_ou_url) if id_ou_url.startswith("http") else gc.open_by_key(id_ou_url)
        try:
            self.ws = sh.worksheet(ONGLET_ANNONCES)
        except gspread.WorksheetNotFound:
            self.ws = sh.sheet1
        self.valeurs = self.ws.get_all_values(value_render_option="UNFORMATTED_VALUE")
        self.index = _normaliser_entetes(self.valeurs[LIGNE_ENTETE - 1])
        self._maj = []

    def annonces(self):
        res = []
        for n, row in enumerate(self.valeurs[LIGNE_ENTETE:], start=LIGNE_ENTETE + 1):
            a = {cle: (row[i] if i < len(row) else "") if (row[i] if i < len(row) else "") != "" else None for cle, i in self.index.items()}
            if not any(a.get(c) for c in ("sku", "titre", "description")):
                continue
            a["_ligne"] = n
            res.append(a)
        return res

    def ecrire(self, ligne, valeurs):
        from gspread.utils import rowcol_to_a1
        for cle, v in valeurs.items():
            if cle in self.index:
                self._maj.append({"range": rowcol_to_a1(ligne, self.index[cle] + 1), "values": [[v]]})

    def enregistrer(self):
        if self._maj:
            self.ws.batch_update(self._maj, value_input_option="USER_ENTERED")
            self._maj = []
        return "Google Sheets"


def ouvrir(source, identifiants=None, dossier_photos=None):
    if "docs.google.com" in source or (not Path(source).exists() and len(source) > 30 and "." not in source):
        if not identifiants:
            raise ValueError("Pour Google Sheets, indiquez --identifiants chemin/compte_service.json")
        return SourceGoogleSheets(source, identifiants, dossier_photos or ".")
    s = SourceExcel(source)
    if dossier_photos:
        s.dossier = Path(dossier_photos)
    return s


__all__ = ["ouvrir", "CLES"]

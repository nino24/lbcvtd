"""Publication des annonces du tableau (Excel ou Google Sheets) sur leboncoin.

Commandes :
    python publier.py verifier  annonces.xlsx      Contrôle le tableau, ne publie rien
    python publier.py connexion                    Ouvre le navigateur pour vous connecter (une seule fois)
    python publier.py calibrer                     Ouvre le formulaire + l'inspecteur Playwright pour ajuster parcours_leboncoin.json
    python publier.py publier   annonces.xlsx      Publie les lignes au statut « À publier »

Options utiles (publier) :
    --auto              clique lui-même sur le bouton final (sinon : mode assisté, vous validez chaque annonce)
    --limite N          nombre maximum d'annonces par lancement (défaut 20)
    --pause 45-120      attente aléatoire en secondes entre deux annonces
    --sku LBC-004       ne traiter que ce(s) SKU (option répétable)
    --photos DOSSIER    dossier où chercher les photos (défaut : dossier du tableau, puis son sous-dossier photos/)
    --identifiants F    fichier JSON du compte de service Google (source Google Sheets)

Le navigateur utilise un profil dédié (~/.lbc-publication/profil) : votre session leboncoin y reste
ouverte d'un lancement à l'autre. Les captchas et validations éventuelles sont faits par vous, à l'écran.
"""
import argparse
import json
import os
import random
import re
import sys
import time
import urllib.request
from datetime import datetime
from pathlib import Path

import sources
from colonnes import ENTETES, TITRE_MAX

ICI = Path(__file__).resolve().parent
PROFIL = Path.home() / ".lbc-publication" / "profil"
CACHE = Path.home() / ".lbc-publication" / "cache_photos"
JOURNAUX = ICI / "journaux"
PARCOURS = ICI / "parcours_leboncoin.json"
EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp")


# --------------------------------------------------------------------------- validation

def _texte(v):
    if v is None:
        return ""
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    return str(v).strip()


def _oui(v):
    return _texte(v).lower() in ("oui", "o", "yes", "y", "1", "true", "vrai", "x")


def prix_net(v):
    """« 55 € », « 1 200,00 » ou 55.0 -> « 55 » / « 1200 » (chiffres seuls pour le champ prix)."""
    t = re.sub(r"[^\d,.]", "", _texte(v)).replace(",", ".")
    try:
        f = float(t)
    except ValueError:
        return t
    return str(int(f)) if f.is_integer() else f"{f:.2f}"


def photos_de(annonce, dossier, max_photos):
    """Retourne la liste des fichiers photo (chemins locaux ; les URL sont téléchargées)."""
    brut = _texte(annonce.get("photos"))
    res = []
    if brut:
        for morceau in re.split(r"[;\n|]+", brut):
            m = morceau.strip()
            if not m:
                continue
            if m.lower().startswith(("http://", "https://")):
                res.append(("url", m))
            else:
                p = Path(m).expanduser()
                if not p.is_absolute():
                    p = (dossier / p)
                res.append(("fichier", p))
    else:
        sku = _texte(annonce.get("sku"))
        trouves = []
        for d in (dossier / "photos", dossier):
            if d.is_dir():
                trouves += [p for p in d.iterdir() if p.suffix.lower() in EXTENSIONS and p.stem.upper().startswith(sku.upper())]
        # LBC-001-1 / LBC-0010 : on exige un séparateur ou la fin juste après le SKU
        trouves = [p for p in trouves if len(p.stem) == len(sku) or not p.stem[len(sku)].isalnum()]
        res = [("fichier", p) for p in sorted(set(trouves), key=lambda p: p.name)]
    return res[:max_photos]


def verifier_annonce(a, dossier, max_photos, skus_vus):
    erreurs, alertes = [], []
    sku = _texte(a.get("sku"))
    titre = _texte(a.get("titre"))
    if not sku:
        erreurs.append("SKU manquant")
    elif sku in skus_vus:
        erreurs.append(f"SKU en double (déjà ligne {skus_vus[sku]})")
    skus_vus.setdefault(sku, a["_ligne"])
    if not titre:
        erreurs.append("titre manquant")
    elif len(titre) > 100:
        erreurs.append(f"titre trop long ({len(titre)} car.)")
    elif len(titre) > TITRE_MAX:
        alertes.append(f"titre de {len(titre)} car. (> {TITRE_MAX}, risque d'être coupé)")
    if len(_texte(a.get("description"))) < 15:
        erreurs.append("description absente ou trop courte")
    prix = prix_net(a.get("prix"))
    try:
        if float(prix) <= 0:
            raise ValueError
    except ValueError:
        erreurs.append("prix invalide")
    for cle in ("categorie", "etat"):
        if not _texte(a.get(cle)):
            erreurs.append(f"{ENTETES[cle].lower()} manquant(e)")
    cp = _texte(a.get("code_postal"))
    if not re.fullmatch(r"\d{5}", cp.zfill(5) if cp.isdigit() else cp):
        erreurs.append("code postal invalide (5 chiffres)")
    if _oui(a.get("livraison")) and not _texte(a.get("poids_kg")):
        erreurs.append("livraison = Oui mais poids du colis manquant")
    photos = photos_de(a, dossier, max_photos)
    if not photos:
        erreurs.append("aucune photo trouvée")
    for genre, p in photos:
        if genre == "fichier" and not p.exists():
            erreurs.append(f"photo introuvable : {p}")
    return erreurs, alertes, photos


def a_publier(a):
    return _texte(a.get("statut")).lower() in ("à publier", "a publier")


def selection(src, args):
    lignes = src.annonces()
    if args.sku:
        voulus = {s.upper() for s in args.sku}
        return [a for a in lignes if _texte(a.get("sku")).upper() in voulus]
    return [a for a in lignes if a_publier(a)]


def cmd_verifier(args):
    src = sources.ouvrir(args.source, args.identifiants, args.photos)
    lignes = selection(src, args)
    if not lignes:
        print("Aucune ligne au statut « À publier ». (Les brouillons sont ignorés.)")
        return 0
    skus, ok = {}, 0
    for a in lignes:
        erreurs, alertes, photos = verifier_annonce(a, src.dossier, args.max_photos, skus)
        etiquette = f"Ligne {a['_ligne']:>4}  {_texte(a.get('sku')):<12} {_texte(a.get('titre'))[:45]:<45}"
        if erreurs:
            print(f"✗ {etiquette}  → {' ; '.join(erreurs)}")
        else:
            ok += 1
            print(f"✓ {etiquette}  {len(photos)} photo(s)" + (f"  ⚠ {' ; '.join(alertes)}" if alertes else ""))
    print(f"\n{ok}/{len(lignes)} annonce(s) prête(s) à publier.")
    return 0 if ok == len(lignes) else 1


# --------------------------------------------------------------------------- navigateur

def navigateur(p, args):
    Path(args.profil).mkdir(parents=True, exist_ok=True)
    # LBC_NAVIGATEUR=/chemin/vers/chromium pour forcer un exécutable précis
    options_exec = {"executable_path": os.environ["LBC_NAVIGATEUR"]} if os.environ.get("LBC_NAVIGATEUR") else {}
    options = dict(user_data_dir=str(args.profil), headless=args.invisible, locale="fr-FR",
                   viewport={"width": 1280, "height": 900}, slow_mo=args.lenteur)
    if args.chrome:
        options["channel"] = "chrome"  # utilise Google Chrome installé plutôt que Chromium
    ctx = p.chromium.launch_persistent_context(**options, **options_exec)
    page = ctx.pages[0] if ctx.pages else ctx.new_page()
    page.set_default_timeout(args.delai * 1000)
    return ctx, page


def cmd_connexion(args):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        ctx, page = navigateur(p, args)
        page.goto("https://www.leboncoin.fr/")
        input("Connectez-vous à votre compte pro dans la fenêtre ouverte, puis appuyez sur Entrée ici… ")
        ctx.close()
    print("Session enregistrée dans", PROFIL)


def cmd_calibrer(args):
    from playwright.sync_api import sync_playwright
    parcours = charger_parcours(args.parcours)
    with sync_playwright() as p:
        ctx, page = navigateur(p, args)
        page.goto(parcours["url_depot"])
        print("L'inspecteur Playwright est ouvert : bouton « Pick locator » pour obtenir le sélecteur d'un champ,\n"
              "puis reportez-le dans parcours_leboncoin.json. Fermez l'inspecteur (Resume) pour quitter.")
        page.pause()
        ctx.close()


def charger_parcours(chemin=PARCOURS):
    with open(chemin, encoding="utf-8") as f:
        return json.load(f)


def localiser(page, cible):
    """Transforme une description JSON en locator Playwright. `cible` peut être une liste d'alternatives."""
    alternatives = cible if isinstance(cible, list) else [cible]
    for alt in alternatives:
        if "css" in alt:
            loc = page.locator(alt["css"])
        elif "label" in alt:
            loc = page.get_by_label(alt["label"], exact=alt.get("exact", False))
        elif "placeholder" in alt:
            loc = page.get_by_placeholder(alt["placeholder"], exact=alt.get("exact", False))
        elif "role" in alt:
            loc = page.get_by_role(alt["role"], name=alt.get("name"), exact=alt.get("exact", False))
        elif "texte" in alt:
            loc = page.get_by_text(alt["texte"], exact=alt.get("exact", False))
        elif "testid" in alt:
            loc = page.get_by_test_id(alt["testid"])
        else:
            raise ValueError(f"Cible inconnue dans le parcours : {alt}")
        loc = loc.first
        try:
            loc.wait_for(state="visible", timeout=alt.get("attente_ms", 4000))
            return loc
        except Exception:
            continue
    return None


def gabarit(valeur, annonce):
    """Remplace {titre}, {prix}… par les valeurs de l'annonce."""
    def val(m):
        cle = m.group(1)
        return prix_net(annonce.get(cle)) if cle == "prix" else _texte(annonce.get(cle))
    return re.sub(r"\{(\w+)\}", val, valeur)


def telecharger(photos):
    CACHE.mkdir(parents=True, exist_ok=True)
    fichiers = []
    for genre, p in photos:
        if genre == "url":
            nom = re.sub(r"[^\w.-]", "_", p.split("?")[0].rsplit("/", 1)[-1]) or "photo.jpg"
            dest = CACHE / f"{abs(hash(p))}_{nom}"
            if not dest.exists():
                urllib.request.urlretrieve(p, dest)
            fichiers.append(str(dest))
        else:
            fichiers.append(str(p))
    return fichiers


def executer_parcours(page, parcours, annonce, fichiers_photos, auto):
    """Déroule les étapes du parcours. Retourne le lien de l'annonce (ou l'URL finale)."""
    page.goto(parcours["url_depot"])
    for n, etape in enumerate(parcours["etapes"], start=1):
        if etape.get("commentaire_seul"):
            continue
        cond = etape.get("si_oui")
        if cond and not _oui(annonce.get(cond)):
            continue
        cond = etape.get("si_rempli")
        if cond and not _texte(annonce.get(cond)):
            continue
        action = etape["action"]
        nom = etape.get("nom", f"étape {n}")

        if action == "attendre":
            page.wait_for_timeout(etape.get("ms", 1000))
            continue
        if action == "valider":
            if auto:
                action = "cliquer"
            else:
                return None  # mode assisté : la main passe à l'utilisateur

        cible = json.loads(gabarit(json.dumps(etape["cible"], ensure_ascii=False), annonce)) if "cible" in etape else None
        loc = localiser(page, cible) if cible else None
        if loc is None:
            if etape.get("optionnel"):
                continue
            raise RuntimeError(f"{nom} : élément introuvable (à recalibrer dans parcours_leboncoin.json)")

        if action == "remplir":
            loc.fill(gabarit(etape["valeur"], annonce))
        elif action == "taper":  # saisie touche par touche, pour les champs à autocomplétion
            loc.click()
            loc.press_sequentially(gabarit(etape["valeur"], annonce), delay=60)
        elif action == "cliquer":
            loc.click()
        elif action == "choisir":  # ouvre une liste puis clique l'option portant la valeur
            loc.click()
            option = localiser(page, [{"role": "option", "name": gabarit(etape["valeur"], annonce)},
                                      {"texte": gabarit(etape["valeur"], annonce), "exact": True}])
            if option is None:
                raise RuntimeError(f"{nom} : option « {gabarit(etape['valeur'], annonce)} » introuvable")
            option.click()
        elif action == "photos":
            loc.set_input_files(fichiers_photos)
            page.wait_for_timeout(etape.get("attente_ms", 1500) * max(1, len(fichiers_photos)))
        else:
            raise ValueError(f"Action inconnue : {action}")
        if etape.get("pause_ms"):
            page.wait_for_timeout(etape["pause_ms"])

    fin = parcours.get("confirmation", {})
    if fin.get("url_contient"):
        page.wait_for_url(re.compile(fin["url_contient"]), timeout=60000)
    return page.url


def cmd_publier(args):
    from playwright.sync_api import sync_playwright
    src = sources.ouvrir(args.source, args.identifiants, args.photos)
    parcours = charger_parcours(args.parcours)
    lignes = selection(src, args)[: args.limite]
    if not lignes:
        print("Aucune ligne au statut « À publier ».")
        return 0
    JOURNAUX.mkdir(exist_ok=True)
    pmin, pmax = (int(x) for x in args.pause.split("-"))
    print(f"{len(lignes)} annonce(s) à traiter — mode {'automatique' if args.auto else 'assisté'}.")

    publiees = erreurs = 0
    skus = {}
    with sync_playwright() as p:
        ctx, page = navigateur(p, args)
        for i, a in enumerate(lignes):
            sku = _texte(a.get("sku"))
            errs, _, photos = verifier_annonce(a, src.dossier, args.max_photos, skus)
            if errs:
                src.ecrire(a["_ligne"], {"statut": "Erreur", "message": "Validation : " + " ; ".join(errs)})
                src.enregistrer()
                erreurs += 1
                print(f"✗ {sku} : {' ; '.join(errs)}")
                continue

            print(f"→ {sku} ({i + 1}/{len(lignes)}) : {_texte(a.get('titre'))}")
            src.ecrire(a["_ligne"], {"statut": "En cours", "message": ""})
            src.enregistrer()
            try:
                lien = executer_parcours(page, parcours, a, telecharger(photos), args.auto)
                if lien is None:  # mode assisté
                    rep = input("   Vérifiez l'annonce à l'écran et cliquez vous-même sur Publier.\n"
                                "   Entrée = publiée · s = sauter (reste « À publier ») · q = quitter : ").strip().lower()
                    if rep == "q":
                        src.ecrire(a["_ligne"], {"statut": "À publier"})
                        src.enregistrer()
                        break
                    if rep == "s":
                        src.ecrire(a["_ligne"], {"statut": "À publier", "message": "Sautée manuellement"})
                        src.enregistrer()
                        continue
                    lien = page.url
                src.ecrire(a["_ligne"], {"statut": "Publiée", "lien": lien,
                                         "date_publication": datetime.now().strftime("%d/%m/%Y %H:%M"), "message": ""})
                publiees += 1
                print(f"   ✓ publiée")
            except Exception as e:  # une annonce en échec n'arrête pas les autres
                capture = JOURNAUX / f"{sku}_{datetime.now():%Y%m%d_%H%M%S}.png"
                try:
                    page.screenshot(path=str(capture), full_page=True)
                except Exception:
                    capture = None
                msg = str(e).splitlines()[0][:300]
                src.ecrire(a["_ligne"], {"statut": "Erreur", "message": msg + (f" (capture : {capture.name})" if capture else "")})
                erreurs += 1
                print(f"   ✗ {msg}")
            finally:
                print("   tableau mis à jour :", src.enregistrer())
            if i < len(lignes) - 1:
                attente = random.randint(pmin, pmax)
                print(f"   pause {attente} s avant l'annonce suivante…")
                time.sleep(attente)
        ctx.close()
    print(f"\nTerminé : {publiees} publiée(s), {erreurs} en erreur.")
    return 0 if erreurs == 0 else 1


# --------------------------------------------------------------------------- CLI

def main(argv=None):
    ap = argparse.ArgumentParser(description="Publie sur leboncoin les annonces d'un tableau Excel / Google Sheets.")
    sous = ap.add_subparsers(dest="commande", required=True)

    def communs(sp, source=True):
        if source:
            sp.add_argument("source", help="fichier .xlsx, ou URL / identifiant d'une Google Sheet")
            sp.add_argument("--identifiants", help="JSON du compte de service Google (Google Sheets)")
            sp.add_argument("--photos", help="dossier des photos")
            sp.add_argument("--sku", action="append", help="ne traiter que ce SKU (répétable)")
            sp.add_argument("--max-photos", type=int, default=10)
        sp.add_argument("--chrome", action="store_true", help="utiliser Google Chrome installé")
        sp.add_argument("--lenteur", type=int, default=150, help="ralentissement entre actions, en ms")
        sp.add_argument("--delai", type=int, default=20, help="délai d'attente max d'un élément, en s")
        sp.add_argument("--parcours", default=PARCOURS, help="fichier de parcours (défaut : parcours_leboncoin.json)")
        sp.add_argument("--profil", default=PROFIL, help="dossier du profil navigateur")
        sp.add_argument("--invisible", action="store_true", help=argparse.SUPPRESS)

    communs(sous.add_parser("verifier", help="contrôler le tableau sans rien publier"))
    communs(sous.add_parser("connexion", help="se connecter une fois à leboncoin"), source=False)
    communs(sous.add_parser("calibrer", help="ouvrir le formulaire avec l'inspecteur Playwright"), source=False)
    sp = sous.add_parser("publier", help="publier les lignes « À publier »")
    communs(sp)
    sp.add_argument("--auto", action="store_true", help="cliquer soi-même sur le bouton final")
    sp.add_argument("--limite", type=int, default=20)
    sp.add_argument("--pause", default="45-120", help="pause aléatoire min-max entre annonces, en s")

    args = ap.parse_args(argv)
    return {"verifier": cmd_verifier, "connexion": cmd_connexion,
            "calibrer": cmd_calibrer, "publier": cmd_publier}[args.commande](args)


if __name__ == "__main__":
    sys.exit(main())

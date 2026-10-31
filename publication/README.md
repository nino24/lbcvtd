# Publication automatique sur leboncoin (compte pro)

Un tableau (Excel **ou** Google Sheets) → un outil qui dépose les annonces sur votre compte leboncoin, puis réécrit dans le tableau le statut, la date et le lien de chaque annonce.

```
 Tableau (1 ligne = 1 annonce)  ──►  publier.py  ──►  navigateur (votre session leboncoin)
        ▲                                                   │
        └──────── Statut / Publiée le / Lien / Message ◄────┘
```

## 1. Le tableau

- **Excel** : `modele_annonces_leboncoin.xlsx` (régénérable avec `python creer_modele.py`).
- **Google Sheets** : même structure, importée dans votre Drive (« Annonces leboncoin – tableau de publication »).

Onglets : **Annonces** (la saisie), **Listes** (valeurs des menus déroulants), **Tableau de bord** (nombre et valeur des annonces par statut), **Mode d'emploi**.

| Colonne | Rôle |
|---|---|
| SKU | Référence unique (ex. `LBC-001`) — la même que celle du générateur d'annonces `index.html` |
| Statut | `À publier` → l'outil la poste · `Brouillon` → ignorée · `En cours` / `Publiée` / `Erreur` → remplis par l'outil · `Vendue` / `À retirer` → pour votre suivi |
| Titre, Car. | Titre + compteur (rouge au-delà de 50 caractères) |
| Description, Catégorie, Prix, État, Marque | Contenu de l'annonce |
| Photos | Chemins ou URL séparés par `;` — **ou vide** : l'outil prend les fichiers `SKU*.jpg/png/webp` du dossier `photos/` (ex. `LBC-003-1.jpg`, `LBC-003-2.jpg`) |
| Code postal, Ville | Localisation |
| Livraison, Poids colis, Main propre, Quantité | Options de vente |
| Notes internes | Jamais publiées (emplacement, prix d'achat…) |
| Publiée le, Lien annonce, Message outil | Remplis par l'outil (colonnes grises) |

## 2. Installation (une fois, sur votre ordinateur)

```bash
cd publication
pip install -r requirements.txt
python -m playwright install chromium     # ou utilisez votre Chrome avec l'option --chrome
python publier.py connexion               # connectez-vous à votre compte pro dans la fenêtre
```

La session est conservée dans `~/.lbc-publication/profil` : pas besoin de se reconnecter à chaque fois.

## 3. Utilisation

```bash
python publier.py verifier annonces.xlsx            # contrôle tout, ne publie rien
python publier.py publier  annonces.xlsx            # mode assisté (recommandé)
python publier.py publier  annonces.xlsx --auto     # clique lui-même sur « Publier »
python publier.py publier  annonces.xlsx --sku LBC-004 --sku LBC-005
```

- **Mode assisté (par défaut)** : l'outil remplit tout le formulaire (titre, catégorie, description, prix, photos, localisation…), puis vous rend la main. Vous vérifiez, cliquez sur *Publier*, appuyez sur Entrée : le tableau est mis à jour et l'annonce suivante démarre.
- **Mode `--auto`** : à utiliser une fois le parcours bien calibré (voir § 4).
- Une annonce en erreur n'arrête pas la série : elle passe en `Erreur` avec le motif dans *Message outil* et une capture d'écran dans `journaux/`.
- Garde-fous : 20 annonces max par lancement (`--limite`), pause aléatoire de 45 à 120 s entre deux annonces (`--pause`). Le tableau est enregistré après **chaque** annonce ; s'il est ouvert dans Excel, la mise à jour est écrite dans `…_maj.xlsx`.

### Depuis Google Sheets

1. Créez un compte de service sur [console.cloud.google.com](https://console.cloud.google.com) (API *Google Sheets* activée) et téléchargez sa clé JSON.
2. Partagez votre Google Sheet en **Éditeur** avec l'adresse e-mail du compte de service.
3. Lancez :
   ```bash
   python publier.py publier "https://docs.google.com/spreadsheets/d/…/edit" --identifiants cle.json --photos ~/Photos/annonces
   ```
   Les photos doivent être des fichiers de votre ordinateur (`--photos`) ou des URL publiques d'images.

## 4. Calibrage du parcours leboncoin (important)

leboncoin ne propose pas d'API publique de dépôt pour les annonces de biens : l'outil pilote donc le **formulaire web**, décrit étape par étape dans `parcours_leboncoin.json` (champ visé, valeur à saisir, conditions comme « seulement si Livraison = Oui »).

Les intitulés fournis sont un point de départ et **doivent être vérifiés sur votre compte pro** (le formulaire varie selon la catégorie et évolue régulièrement) :

```bash
python publier.py calibrer
```

ouvre la page de dépôt avec l'inspecteur Playwright : le bouton *Pick locator* donne l'identifiant exact de chaque champ, à reporter dans le JSON. Faites un premier essai en mode assisté sur une annonce (`--sku`) : si une étape échoue, le message indique laquelle.

Types d'étapes : `remplir`, `taper` (champs à autocomplétion), `cliquer`, `choisir` (liste déroulante), `photos`, `attendre`, `valider` (bouton final). Une `cible` peut lister plusieurs alternatives (`label`, `placeholder`, `role`+`name`, `texte`, `css`, `testid`) essayées dans l'ordre ; `optionnel: true` saute l'étape si l'élément est absent ; `{colonne}` insère la valeur de la ligne.

## 5. À savoir

- Les conditions d'utilisation de leboncoin encadrent l'usage de robots. Le mode assisté, le rythme limité et la connexion manuelle (captchas faits par vous) restent proches d'un usage humain, mais l'automatisation se fait **sous votre responsabilité**. Pour de gros volumes, demandez à votre interlocuteur leboncoin Pro s'il existe un **import par flux ou une API partenaire** pour votre activité : `publier.py` est conçu pour qu'un tel connecteur remplace simplement le navigateur, le tableau restant identique.
- Rien n'est envoyé ailleurs que sur leboncoin : le tableau reste sur votre ordinateur ou votre Drive.

# Générateur d'annonces — Le Bon Coin & Vinted

Un outil tout simple : vous déposez une ou plusieurs **photos** d'un objet, et il génère une annonce prête à coller :

- **Titre** (avec compteur de caractères : 50 max pour leboncoin, 100 pour Vinted)
- **Description** rédigée en français, honnête et structurée
- **URL de la fiche produit** sur le web, le cas échéant (site du fabricant en priorité)
- Catégorie suggérée, prix conseillé et état estimé

L'analyse des photos et la recherche web sont faites par l'API Claude (modèle `claude-opus-5`, avec l'outil de recherche web d'Anthropic). Deux plateformes : **Le Bon Coin** (par défaut) et **Vinted** (titre plus court, description avec hashtags).

## Mode « En série + SKU »

Pour vider une armoire ou un garage d'un coup :

1. **Réglez les SKU en début de session** : un préfixe (ex. `LBC-`) et un premier numéro (ex. `001`). Ces réglages sont mémorisés dans le navigateur, et le compteur avance automatiquement après chaque série — la session suivante repart au bon numéro.
2. **Ajoutez un article par objet** (photos + infos/prix facultatifs). Chaque carte affiche son SKU en direct.
3. **Générez la série** : les annonces sont produites l'une après l'autre (une erreur sur un article n'arrête pas les autres). Chaque description se termine par `Réf. : SKU` (désactivable) pour retrouver l'objet quand il se vend.
4. **Exportez** :
   - **🖨 Imprimer les étiquettes** / **⬇️ Fichier étiquettes** : une planche imprimable (3 colonnes, étiquettes ≈ 63 × 38 mm, compatible Avery L7160 ou papier libre à découper) avec SKU, titre et prix — à coller sur chaque objet ou sac.
   - **⬇️ Export CSV** : le récapitulatif complet (SKU, plateforme, titre, prix, catégorie, état, URL, description), séparateur `;`, ouvrable directement dans Excel/LibreOffice pour suivre vos ventes.

## Utilisation

1. **Obtenez une clé API Anthropic** : créez un compte sur [console.anthropic.com](https://console.anthropic.com), ajoutez un peu de crédit, puis créez une clé dans *Settings → API Keys*.
2. **Ouvrez `index.html`** dans votre navigateur (double-clic suffit — aucune installation, aucun serveur).
3. Collez votre clé API dans la section *Réglages* (elle est mémorisée uniquement dans votre navigateur, via `localStorage`).
4. Ajoutez vos photos, choisissez la plateforme, cliquez sur **Générer l'annonce**.
5. Relisez, ajustez si besoin (les champs sont modifiables), puis copiez chaque élément avec les boutons **Copier**.

### Sur téléphone

Hébergez le fichier avec **GitHub Pages** pour y accéder depuis n'importe quel appareil :
*Settings → Pages → Source : « Deploy from a branch » → branche principale, dossier `/` (root)*.
L'outil sera alors disponible à l'adresse `https://<votre-compte>.github.io/lbcvtd/`, et le bouton photo ouvrira directement l'appareil photo.

## Coût

Chaque génération consomme quelques milliers de tokens (photos + recherche web) : comptez environ **0,05 à 0,15 $ par annonce**. Le coût estimé s'affiche sous chaque résultat.

## Confidentialité et notes techniques

- Les photos sont redimensionnées dans le navigateur puis envoyées **directement à l'API Anthropic** — aucun autre serveur n'intervient, rien n'est stocké en ligne.
- Les photos au format HEIC (iPhone) sont converties automatiquement sur Safari ; sur les autres navigateurs, exportez-les d'abord en JPEG.
- Les *refusal fallbacks* de l'API sont activés (`fallbacks: "default"`) : si les filtres de sécurité déclinent une requête, elle est automatiquement relancée sur un modèle de repli au lieu d'échouer.

## Pistes d'évolution

- Publication directe via l'API leboncoin / Vinted (nécessite un compte pro ou partenaire)
- Génération multi-annonces en série (un dossier de photos → plusieurs annonces)
- Estimation de prix affinée à partir des annonces similaires en cours

# Process de montage

> Le *quoi* (style) est dans `DA.md`. Ici c'est le *comment* : formats, structures, export, contrôle qualité.

## 1. Formats

| Format | Ratio | Résolution | Durée cible | Plateformes |
|---|---|---|---|---|
| Short produit | 9:16 | 1080×1920 | 15–35 s | TikTok, Reels, Shorts |
| Extrait de live (« best-of ») | 9:16 | 1080×1920 | 20–60 s | TikTok, Reels, Shorts |
| Teaser de live | 9:16 | 1080×1920 | 8–15 s | Stories, TikTok, Reels |
| Story | 9:16 | 1080×1920 | ≤ 15 s par slide | Instagram / Facebook |
| Vidéo fiche produit | 1:1 ou 4:5 | 1080×1080 / 1080×1350 | 10–30 s | Site, marketplace, pub |
| Format long / replay | 16:9 | 1920×1080 | libre | YouTube |

## 2. Zones de sécurité (vertical 1080×1920)

Rien d'important (texte, prix, visage, logo) dans ces zones, recouvertes par l'interface :

- **Haut :** 220 px (pseudo, onglets)
- **Bas :** 420 px (légende, musique, boutons)
- **Droite :** 140 px (likes, commentaires, partage)
- **Gauche :** 60 px

→ Zone utile ≈ **880 × 1280 px** centrée légèrement vers le haut. Garder un calque guide « safe zone » dans le projet modèle.

## 3. Structures types

### Short produit (15–35 s)
1. **0–1,5 s — Hook** : le produit en action / le résultat / une phrase choc à l'écran
2. **1,5–5 s — Problème ou désir** : pourquoi on en a besoin
3. **5–20 s — Preuve** : détails en gros plan, démonstration, avant/après, essayé
4. **20–28 s — Prix / offre** : prix bien visible, rareté si vraie
5. **Fin — CTA unique** : « Dispo au live de jeudi 20h » / « Lien en bio »

### Extrait de live
1. **Hook** : le meilleur moment (réaction, prix annoncé, « rupture en 2 min »)
2. **Contexte** en 1 sous-titre (« En live hier soir… »)
3. **Le moment** monté serré (couper les temps morts, garder l'énergie)
4. **Preuve sociale** : commentaires à l'écran, compteur de ventes, « vendu ! »
5. **CTA** : prochain live, date et heure

### Teaser de live
1. Hook visuel (les produits qui seront présentés, en rafale)
2. Date + heure **en gros**
3. Une raison de venir (exclu, prix live, nouveauté)
4. CTA : « Active la notif » / « Mets un rappel »

## 4. Pipeline de montage

1. **Brief** : dupliquer `briefs/_MODELE-BRIEF.md` → `briefs/AAAA-MM-JJ_nom-video.md`
2. **Dérushage** : repérer les meilleurs moments (marqueurs), écarter le flou / mal éclairé
3. **Ours (bout à bout)** : structure seule, sans habillage — valider que l'histoire tient
4. **Montage serré** : jump cuts, rythme 2–3 s, hook retravaillé
5. **Habillage** : sous-titres, textes, prix, logo, CTA (presets du projet modèle uniquement)
6. **Son** : voix nettoyée, musique, sound design, normalisation −14 LUFS
7. **Étalonnage** : preset DA, vérifier la fidélité des couleurs produit
8. **Contrôle qualité** (checklist ci-dessous) **sur un téléphone**
9. **Export & publication**
10. **48 h après** : noter les chiffres et l'enseignement dans `JOURNAL-DA.md`

## 5. Réglages d'export

| Paramètre | Valeur |
|---|---|
| Conteneur / codec | MP4 — H.264 (High) |
| Résolution | selon format (voir tableau §1) |
| Images / seconde | ⟨25 ou 30⟩ — **toujours la même** que celle du tournage |
| Débit vidéo | 15–20 Mb/s (VBR 2 passes si dispo) |
| Audio | AAC, 48 kHz, 320 kb/s, stéréo |
| Loudness | −14 LUFS intégré, −1 dBTP max |
| Couleur | Rec.709, plage complète désactivée (vidéo standard) |

**Nommage des fichiers :** `AAAA-MM-JJ_format_produit_v1.mp4`
ex. `2026-11-17_short_jean-brut-501_v2.mp4`

**Rangement :** ⟨chemin Drive/Dropbox⟩ → `/Rushes`, `/Projets`, `/Exports`, `/Assets DA` (polices, logo, LUT, sons, templates).

## 6. Checklist avant publication

- [ ] Le produit est visible dans les **2 premières secondes**
- [ ] Hook compréhensible **sans le son**
- [ ] Sous-titres relus, zéro faute, style DA
- [ ] Aucun texte dans les zones de sécurité
- [ ] Prix lisible et **juste**
- [ ] Couleurs du produit fidèles à la réalité
- [ ] Voix audible au-dessus de la musique, niveau −14 LUFS
- [ ] Un seul CTA, clair
- [ ] Polices / couleurs / sons = ceux de `DA.md`
- [ ] Musique et images : droits OK
- [ ] Visionnée en entier **sur téléphone**, son coupé puis son activé
- [ ] Nom de fichier conforme, brief mis à jour

## 7. Outils & presets

| Outil | Usage | Preset / template |
|---|---|---|
| ⟨ex. CapCut / Premiere / DaVinci⟩ | Montage | ⟨lien projet modèle⟩ |
| ⟨ex. Canva⟩ | Miniatures, écrans de fin | ⟨lien template⟩ |
| ⟨outil sous-titres⟩ | Sous-titres auto | ⟨preset style DA⟩ |

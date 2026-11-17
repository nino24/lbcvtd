# Process de montage

> Ici uniquement la **technique** (contraintes des plateformes, export, organisation). Tout ce qui relève du style se décide au fil de l'eau dans `JOURNAL-DA.md` puis `DA.md`.

## 1. Formats

| Ratio | Résolution | Où |
|---|---|---|
| 9:16 (vertical) | 1080×1920 | TikTok, Reels, Shorts, Stories |
| 4:5 | 1080×1350 | Fil Instagram / Facebook, pubs |
| 1:1 | 1080×1080 | Site, marketplace, pubs |
| 16:9 | 1920×1080 | YouTube, replays |

*Les types de vidéos et leurs durées seront définis ensemble (`DA.md` §8).*

## 2. Zones de sécurité (vertical 1080×1920)

Rien d'important (texte, prix, visage, logo) dans ces zones, recouvertes par l'interface :

- **Haut :** 220 px (pseudo, onglets)
- **Bas :** 420 px (légende, musique, boutons)
- **Droite :** 140 px (likes, commentaires, partage)
- **Gauche :** 60 px

→ Zone utile ≈ **880 × 1280 px** centrée légèrement vers le haut. Garder un calque guide « safe zone » dans le projet modèle.

## 3. Pipeline de montage

1. **Brief** : dupliquer `briefs/_MODELE-BRIEF.md` → `briefs/AAAA-MM-JJ_nom-video.md`
2. **Dérushage** : repérer les meilleurs moments (marqueurs), écarter le flou / mal éclairé
3. **Ours (bout à bout)** : structure seule, sans habillage — valider que l'histoire tient
4. **Montage** : selon le rythme défini dans `DA.md`
5. **Habillage** : sous-titres, textes, éléments récurrents définis dans `DA.md`
6. **Son** : voix nettoyée, musique, sound design, normalisation −14 LUFS
7. **Étalonnage** : vérifier la fidélité des couleurs produit
8. **Contrôle qualité** (checklist ci-dessous) **sur un téléphone**
9. **Export & publication**
10. **48 h après** : on en parle, et ce qu'on en retient devient un point dans `JOURNAL-DA.md`

## 4. Réglages d'export

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

## 5. Checklist avant publication

- [ ] Sous-titres / textes relus, zéro faute
- [ ] Aucun texte ni élément important dans les zones de sécurité
- [ ] Prix (s'il est affiché) lisible et **juste**
- [ ] Couleurs du produit fidèles à la réalité
- [ ] Voix audible, niveau −14 LUFS
- [ ] Conforme aux règles validées dans `DA.md`
- [ ] Musique et images : droits OK
- [ ] Visionnée en entier **sur téléphone**, son coupé puis son activé
- [ ] Nom de fichier conforme, brief mis à jour

*Cette liste s'enrichira avec les règles DA qu'on validera.*

## 6. Outils & presets

| Outil | Usage | Preset / template |
|---|---|---|
| — | — | à définir ensemble |

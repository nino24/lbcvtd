# Outils de montage

| Script | Rôle |
|---|---|
| `transcription.py` | Transcription mot à mot (faster-whisper, modèle « small ») → `transcript.json`. Entrée : audio mono 16 kHz float32 (`ffmpeg -i video.mp4 -ac 1 -ar 16000 -f f32le audio.f32`) |
| `sous_titres.py` | `transcript.json` → sous-titres animés `.ass` (incrustés) + `.srt` (à importer sur les plateformes). Contient la liste des corrections (Whatnot, TikTok…) et des mots-clés colorés |
| `animation_palette.py` | Intro « palette + carton » et écran de fin ShopTonStock (images PNG transparentes 1080×1920, 30 i/s) |
| `carte_whatnot.py` | Carton qui s'ouvre → logo Whatnot + « 25€ à l'inscription » + pastille « Lien en bio 🚀 ». `WHATNOT_LOGO=chemin.png` pour utiliser le logo officiel |
| `assemblage_exemple.sh` | Commande ffmpeg d'assemblage de la vidéo du 17/11 (zoom-punch + flash + whoosh sur « Whatnot », calques, sous-titres, −14 LUFS) — les horaires sont à adapter pour chaque vidéo |

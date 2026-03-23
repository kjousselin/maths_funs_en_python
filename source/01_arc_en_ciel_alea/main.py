#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
main.py
Script pour générer une animation GIF d'arc-en-ciel avec des tentatives de mélange aléatoire.
"""


import pathlib

#from funcs import draw_a_rainbow, generate_a_random_rainbow, export_gif

# matplotlib plus efficace que plotly
from funcs_matplotlib_version import draw_a_rainbow, generate_a_random_rainbow, export_gif, generate_some_random_rainbows, export_mp4_from_gif, export_mp4_from_frames

################################# PARAMÈTRES #################################


# Dimensions de la figure
WIDTH        = 400
HEIGHT       = 190

verbose      = True
max_attempts = None   # 4500 en plotly 350x250 pour 30.6 Mo
nb_essais    = 3     # int >0
fps          = 30    # nb de frames par secondes


# Couleurs réelles de l’arc-en-ciel
RAINBOW_COLORS_OK = [
    "#FF0000",  # Rouge
    "#FF7F00",  # Orange
    "#FFFF00",  # Jaune
    "#00FF00",  # Vert
    "#0000FF",  # Bleu
    "#4B0082",  # Indigo
    "#8B00FF"   # Violet
]

# Répertoire de sortie
OUTPUT_DIR = pathlib.Path('./output/')




################################# MAIN #################################

if __name__ == "__main__":
    
    #frames, attempts = generate_a_random_rainbow(RAINBOW_COLORS_OK, max_attempts=max_attempts, verbose=verbose, width=WIDTH, height=HEIGHT )

    frames, attempts = generate_some_random_rainbows(RAINBOW_COLORS_OK, max_attempts=max_attempts, nb_essais=nb_essais, verbose=verbose, width=WIDTH, height=HEIGHT, fps=fps )
    
    gif_file         = export_gif(frames, OUTPUT_DIR, verbose=verbose, duration=1/fps, attempts=attempts)
    
    mp4_file         = export_mp4_from_gif(gif_file, verbose=verbose,  fps=fps)

    # Ou export en mp4 directement depuis les frames
    export_mp4_from_frames(frames, str(gif_file)+"_plus_net.mp4", fps=fps)

    if verbose: print(f"Terminé.")

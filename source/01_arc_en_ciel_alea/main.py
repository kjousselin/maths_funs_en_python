#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
main.py
Script pour générer une animation GIF d'arc-en-ciel avec des tentatives de mélange aléatoire.
"""


import pathlib

#from funcs import draw_a_rainbow, generate_a_random_rainbow, export_gif

# matplotlib plus efficace que plotly
from funcs_matplotlib_version import draw_a_rainbow, generate_a_random_rainbow, export_gif, generate_some_random_rainbows

################################# PARAMÈTRES #################################


# Dimensions de la figure
WIDTH        = 550
HEIGHT       = 200

verbose      = True
max_attempts = None   # 4500 en plotly 350x250 pour 30.6 Mo
nb_essais    = 5      # int >0


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

    frames, attempts = generate_some_random_rainbows(RAINBOW_COLORS_OK, max_attempts=max_attempts, nb_essais=nb_essais, verbose=verbose, width=WIDTH, height=HEIGHT )
    
    gif_file         = export_gif(frames, OUTPUT_DIR, verbose=verbose, duration=0.1, attempts=attempts)
    
    if verbose: print(f"Terminé.")

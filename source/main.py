#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
main.py
Script pour générer une animation GIF d'arc-en-ciel avec des tentatives de mélange aléatoire.
"""


import pathlib

from funcs import draw_a_rainbow, generate_a_random_rainbow, export_gif


################################# PARAMÈTRES #################################


# Dimensions de la figure
WIDTH        = 800
HEIGHT       = 500

verbose      = True
max_attempts = None

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
    
    frames, attempts = generate_a_random_rainbow(RAINBOW_COLORS_OK, max_attempts=max_attempts, verbose=verbose)
    
    gif_file         = export_gif(frames, OUTPUT_DIR, verbose=verbose, duration=0.02)
    
    if verbose: print(f"\nGIF exported to {gif_file} ({attempts} attempts)")

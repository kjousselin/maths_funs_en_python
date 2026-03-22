import numpy as np
import matplotlib
matplotlib.use("Agg")  # backend purement raster, pas GUI
import matplotlib.pyplot as plt
import imageio.v2 as imageio
import random
import datetime



# NUAGES
def add_cloud(ax, x_center, y_center, scale=1):
    """
    Ajout de nuages à la figure fig, autour des positions (x_center, y_center)
    
    Returns
    -------
    fig      la figure matplolib complétée
    """

    t       = np.linspace(0, 2*np.pi, 100)
    offsets = [(-1, 0), (0, 0.5), (1, 0), (0.5, -0.5), (-0.5, -0.5)]

    for dx, dy in offsets:
        x = x_center + scale*(dx + 0.8*np.cos(t))
        y = y_center + scale*(dy + 0.6*np.sin(t))
        ax.fill(x, y, color="#cfd8dc", edgecolor="black")



# Dessine un arc en ciel
def draw_a_rainbow(rainbow_colors, thickness=1, width=400, height=300):
    """
    Renvoie une figure matplolib
    
    rainbow_colors   list         liste des couleurs 
    thickness        float|int    épaisseur des bandes (1 = elles se touchent)
    width            int          dimension de l'image (largeur) en pixel
    height           int          dimension de l'image (hauteur) en pixel
    
    Returns
    -------
    fig              figure matplolib
    """

    dpi          = 100
    width_pouce  = width/dpi
    height_pouce = height/dpi

    fig, ax      = plt.subplots(figsize=(width_pouce, height_pouce), dpi=dpi)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

    theta        = np.linspace(0, np.pi, 300)

    for i, color in enumerate(rainbow_colors):
        r_outer = 10 - i * thickness
        r_inner = r_outer - thickness

        x_outer = r_outer * np.cos(theta)
        y_outer = r_outer * np.sin(theta)

        x_inner = r_inner * np.cos(theta[::-1])
        y_inner = r_inner * np.sin(theta[::-1])

        x = np.concatenate([x_outer, x_inner])
        y = np.concatenate([y_outer, y_inner])

        ax.fill(x, y, color=color)

    # nuages
    add_cloud(ax, -6.5, 0, scale=2)
    add_cloud(ax, 6.5, 0, scale=2)


    # dessin bien à droite, pour laisser de la place au text (autre solution plt.subplot(1,2))
    ax.set_xlim([-10.5,30])
    ax.set_aspect('equal')
    ax.axis('off')

    return fig, ax



# Dessine un arc en ciel aléatoire
def generate_a_random_rainbow(target_colors, max_attempts=None, verbose=False, width=800, height=500):
    """
    Génère des arcs-en-ciel aléatoires jusqu'à obtenir l'ordre cible ou atteindre max_attempts.
    
    Parameters
    ----------
    target_colors  list           Liste des couleurs dans l'ordre cible.
    max_attempts   int or None    Nombre maximum de tentatives. Si None, tente indéfiniment jusqu'à réussite.
    
    Returns
    -------
    frames         list           Liste des images (frames) de chaque tentative.
    attempts       int            Nombre de tentatives effectuées.
    """

    frames         = []
    attempt        = 0
    rainbow_colors = []

    while rainbow_colors != target_colors and (max_attempts is None or attempt < max_attempts):

        attempt += 1
        if verbose:
            print('.', end='', flush=True)

        rainbow_colors = target_colors.copy()
        random.shuffle(rainbow_colors)

        fig, ax = draw_a_rainbow(rainbow_colors, width=width, height=height)

        ax.text(
            0, 11,
            f"tentative n° {attempt}",
            ha       = 'center',
            fontsize = 14,
            color    = 'blue',
            fontname = 'Patrick Hand'
        )

        # conversion en image numpy
        fig.canvas.draw()
        image = np.asarray(fig.canvas.buffer_rgba())

        frames.append(image)

        plt.tight_layout()

        plt.close(fig)  # évite fuite mémoire


    return frames, attempt



# Dessine plusieurs arc en ciel aléatoire à suivre (nb_essais)
def generate_some_random_rainbows(target_colors, max_attempts=None, nb_essais=1, verbose=False, width=800, height=500):
    """
    Génère des arcs-en-ciel aléatoires jusqu'à obtenir l'ordre cible ou atteindre max_attempts.
    Répète l'opération nb_essais fois !
    
    Parameters
    ----------
    target_colors  list           Liste des couleurs dans l'ordre cible.
    max_attempts   int or None    Nombre maximum de tentatives. Si None, tente indéfiniment jusqu'à réussite.
    
    Returns
    -------
    frames         list           Liste des images (frames) de chaque tentative.
    attempts       int            Nombre de tentatives effectuées.
    """
    attempts = []
    frames   = []


    for essai in range(1, nb_essais+1):

        print(f'\nEssai numéro {essai} :')

        attempt        = 0
        rainbow_colors = []

        while rainbow_colors != target_colors and (max_attempts is None or attempt < max_attempts):

            attempt += 1
            if verbose:
                print('.', end='', flush=True)

            rainbow_colors = target_colors.copy()
            random.shuffle(rainbow_colors)

            fig, ax = draw_a_rainbow(rainbow_colors, width=width, height=height)

            # Ecrire les anciens essais
            for essai_old in range(1, essai):
                ax.text(
                    12, 10-essai_old*2,
                    f"Expérience n° {essai_old} : tentative n° {int(attempts[-essai_old])+1}",
                    ha       = 'left',
                    fontsize = 14,
                    color    = 'blue',
                    fontname = 'Patrick Hand'
                )

            # ecrire l'essai en cours, et les anciens
            ax.text(
                12, 10-essai*2,
                f"Expérience n° {essai} : tentative n° {attempt}",
                ha       = 'left',
                fontsize = 14,
                color    = 'blue',
                fontname = 'Patrick Hand'
            )

            # conversion en image numpy
            fig.canvas.draw()
            image = np.asarray(fig.canvas.buffer_rgba())

            frames.append(image)

            plt.close(fig)  # évite fuite mémoire

        print(f"\n{attempt} tentatives !")

        attempts.append(str(attempt))
    
    attempts = '_'.join(attempts)


    return frames, attempts



# EXPORT GIF
def export_gif(frames, OUTPUT_DIR, verbose=False, duration=0.1, attempts=""):
    """
    Exporte les frames en GIF animé dans le répertoire de sortie.
    """

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    prefix    = "animation_rainbow"
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M')
    file_path = OUTPUT_DIR / f"{timestamp}_{prefix}_{attempts}_attempts.gif"

    imageio.mimwrite(file_path, frames, duration=duration*1000, loop=None)

    if verbose: print(f"\nGIF exported to {file_path} ({attempts} attempts)")

    return file_path


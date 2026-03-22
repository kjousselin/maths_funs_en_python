import plotly.graph_objects as go
import numpy as np
import imageio.v2 as imageio
from io import BytesIO
import random
import datetime
#from tqdm import tqdm




# NUAGES
def add_cloud(fig, x_center, y_center, scale=1):
    """
    Ajout de nuages à la figure fig, autour des positions (x_center, y_center)
    
    Returns
    -------
    fig      la figure plotly complétée
    """
    t = np.linspace(0, 2*np.pi, 100)
    
    # plusieurs cercles pour effet nuage
    offsets = [(-1, 0), (0, 0.5), (1, 0), (0.5, -0.5), (-0.5, -0.5)]
    
    for dx, dy in offsets:
        x = x_center + scale*(dx + 0.8*np.cos(t))
        y = y_center + scale*(dy + 0.6*np.sin(t))
        
        fig.add_trace(go.Scatter(
            x=x,
            y=y,
            fill="toself",
            fillcolor="#cfd8dc",  # gris bleu clair
            line=dict(color="black", width=2),
            showlegend=False
        ))
        
    return(fig)



def draw_a_rainbow(rainbow_colors, thickness = 1, width = 800, height = 500):
    """
    Renvoie une figure plotly
    
    rainbow_colors   list         liste des couleurs 
    thickness        float|int    épaisseur des bandes (1 = elles se touchent)
    width            int          dimension de l'image (largeur)
    height           int          dimension de l'image (hauteur)
    
    Returns
    -------
    fig              figure plotly
    """

    fig = go.Figure()

    theta = np.linspace(0, np.pi, 300)
    
    
    # ajout d'une courbe (arc de cercle) par couleur de la liste
    for i, color in enumerate(rainbow_colors):
        r_outer = 10 - i * thickness
        r_inner = r_outer - thickness

        x_outer = r_outer * np.cos(theta)
        y_outer = r_outer * np.sin(theta)

        x_inner = r_inner * np.cos(theta[::-1])
        y_inner = r_inner * np.sin(theta[::-1])

        x = np.concatenate([x_outer, x_inner])
        y = np.concatenate([y_outer, y_inner])

        fig.add_trace(go.Scatter(
                                    x          = x,
                                    y          = y,
                                    fill       = "toself",
                                    fillcolor  = color,
                                    line       = dict(color=color),
                                    showlegend = False
                                ))

    # Ajout des nuages à gauche et à droite
    fig = add_cloud(fig, -6.5, 0, scale=2)
    fig = add_cloud(fig, 6.5, 0, scale=2)

    # layout
    fig.update_layout(
                        width        = width,
                        height       = height,
                        xaxis        = dict(visible=False, scaleanchor="y"),  # orthonormé
                        yaxis        = dict(visible=False),
                        plot_bgcolor = "white",
                        margin       = dict(l=0, r=0, t=0, b=0),
                    )

    #fig.show()    

    return(fig)



def generate_a_random_rainbow(target_colors, max_attempts=None, verbose=False):
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
    frames = []
    attempt = 0
    rainbow_colors = []

    while rainbow_colors != target_colors and (max_attempts is None or attempt < max_attempts):

        # N° de tentative
        attempt += 1
        if verbose: print('.', end='')


        rainbow_colors = target_colors.copy()
        random.shuffle(rainbow_colors)

        # Dessiner l'arc-en-ciel
        fig = draw_a_rainbow(rainbow_colors, thickness=1, width=550, height=300)

        # Ajouter annotation du numéro de tentative
        fig.add_annotation(
                            x         = 0.02,
                            y         = 0.98,
                            xref      = "paper",
                            yref      = "paper",
                            text      = f"tentative n° {attempt}",
                            showarrow = False,
                            font      = dict(size=20, color="blue", family="Patrick Hand"),
                            align     = "left",
                        )

    
        # Convertir la figure en image et ajouter aux frames
        buf = BytesIO()
        fig.write_image(buf, format="png", scale=1)
        buf.seek(0)
        frames.append(imageio.imread(buf))


    return frames, attempt



def export_gif(frames, output_dir, prefix="animation_rainbow", duration=0.1, verbose=False):
    """
    Exporte les frames en GIF animé dans le répertoire de sortie.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    # supprimer les frames vides 
    frames = [frame for frame in frames if frame is not None]
    
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M')
    file_path = output_dir / f"{timestamp}_{prefix}.gif"
    
    imageio.mimwrite(file_path, frames, duration=duration, loop=None)
    
    return file_path



from tqdm import tqdm
import datetime
import plotly.graph_objects as go
import numpy as np
import random
import time
from IPython.display import clear_output
import pathlib

from funcs import draw_a_rainbow

################################# PARAMÈTRES #################################

width = 800
height = 500

# Couleurs réelles de l’arc-en-ciel
rainbow_colors_ok = [
    "#FF0000",  # Rouge
    "#FF7F00",  # Orange
    "#FFFF00",  # Jaune
    "#00FF00",  # Vert
    "#0000FF",  # Bleu
    "#4B0082",  # Indigo
    "#8B00FF"   # Violet
]

output_dir = './output/'



################################# Exécution du script #################################

if __name__=='__main__':

    from tqdm import tqdm
    
    import plotly.graph_objects as go
    import numpy as np
    import imageio.v2 as imageio
    from io import BytesIO

    import datetime

    now_str = datetime.datetime.today().strftime('%Y%m%d_%H%M')

    output_dir = pathlib.Path(output_dir)
    
    

    frames = []

    k = 0

    rainbow_colors = []

    while rainbow_colors != rainbow_colors_ok:

        k+=1
        
        if k==10: break
        
        rainbow_colors = rainbow_colors_ok.copy()
        
        # mélange aléatoirement les couleurs de la liste
        random.shuffle(rainbow_colors)

        # fonction qui dessine l'arc en ciel, selon la liste de couleurs
        fig = draw_a_rainbow(rainbow_colors, thickness=1, width=550, height=300)

        # ajouter la numérotation de la tentative
        fig.add_annotation(     x=0.02,                 # position horizontale (0=à gauche, 1=à droite)
                                y=0.98,                 # position verticale (0=bas, 1=haut)
                                xref="paper",           # x est fixé par rapport à la figure, pas aux données
                                yref="paper",           # idem, y
                                text=f"k = {k}",        # texte
                                showarrow=False,        # supprime la flèche (True par défaut !)
                                font=dict(size=20, color="blue", family="Patrick Hand"),  # police
                                align="left",
                            )

        # Crée un "buffer" en mémoire pour stocker l'image temporairement, l'ajouter dans la liste 'frames'
        buf = BytesIO()
        fig.write_image(buf, format="png", scale=1)
        buf.seek(0)
        frames.append(imageio.imread(buf))


    # Export du GIF
    file = output_dir / f"{now_str}_animation_rainbow.gif"
    imageio.mimsave(file, frames, duration=0.1, loop=None )
    print(f"GIF exported to {str(file)}")

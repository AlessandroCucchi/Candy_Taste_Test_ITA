"""Stile grafico condiviso dai notebook: palette fissa, assi sobri, linee sottili."""
import matplotlib.pyplot as plt
import matplotlib as mpl

# Palette categoriale (ordine fisso: il colore segue l'entità, mai il rango)
BLU, ARANCIO, ACQUA, GIALLO, MAGENTA = "#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"
GRIGIO, GRIGIO_CHIARO = "#8a8984", "#d9d8d4"
TESTO, TESTO_2 = "#0b0b0b", "#52514e"
CATEGORIALE = [BLU, ARANCIO, ACQUA, GIALLO, MAGENTA]


def applica_stile():
    mpl.rcParams.update({
        "figure.dpi": 110,
        "savefig.dpi": 200,
        "savefig.bbox": "tight",
        "figure.facecolor": "#fcfcfb",
        "axes.facecolor": "#fcfcfb",
        "axes.edgecolor": GRIGIO_CHIARO,
        "axes.labelcolor": TESTO_2,
        "axes.titlecolor": TESTO,
        "axes.titlesize": 12,
        "axes.titleweight": "bold",
        "axes.titlelocation": "left",
        "axes.labelsize": 10,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "axes.grid.axis": "y",
        "axes.axisbelow": True,
        "grid.color": "#ecebe8",
        "grid.linewidth": 0.8,
        "xtick.color": TESTO_2,
        "ytick.color": TESTO_2,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "legend.frameon": False,
        "legend.fontsize": 9,
        "lines.linewidth": 2,
        "font.family": "DejaVu Sans",
    })


def salva(fig, nome):
    """Salva la figura nella cartella figures/ del progetto."""
    fig.savefig(f"../figures/{nome}.png")

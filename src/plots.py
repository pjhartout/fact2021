import re
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors

try:
    import dataloaders
    import utils
except ModuleNotFoundError:
    import src.dataloaders as dataloaders
    import src.utils as utils

from dotenv import dotenv_values, find_dotenv
from pathlib import Path

DOTENV = dotenv_values(find_dotenv())
PLOTS_DIR = Path(DOTENV["PROJECT_DIR"]) / "plots"
PLOTS_DIR.mkdir(exist_ok=True)

colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
colorlist = ["deepskyblue", "orangered", "yellowgreen", "slateblue", "m"]


def plot_yaleb_lighting_positions(fname="yaleb_lighting_positions"):
    plt.clf()
    plt.figure(figsize=(10, 9))
    for i, pos in enumerate(dataloaders.YalebDataset.train_positions):
        label = "train position" if i == 0 else None
        s = plt.rcParams["lines.markersize"] ** 2 * 2
        plt.scatter(
            *pos,
            edgecolors=(0, 0, 0),
            s=s,
            c="white",
            linewidths=1,
            label=label
        )
    for i, (name, groups) in enumerate(utils.cluster_yaleb_poses().items()):
        for j, group in enumerate(groups):
            label = name if j == 0 else None
            plt.scatter(
                int(group[0]), int(group[1]), c=colorlist[i], label=label
            )
    plt.legend()
    plt.title("clustering of YaleB lighting positions")
    plt.xlabel("azimuth")
    plt.ylabel("elevation")

    pos2n_bad = {
        ("-010", "+00"): 3,
        ("+095", "+00"): 4,
        ("-050", "-40"): 3,
        ("+050", "-40"): 3,
        ("-110", "+15"): 3,
        ("-110", "-20"): 1,
        ("-035", "+40"): 1,
    }
    for pos, n_bad in pos2n_bad.items():
        label2coord = lambda l: int(l.replace("+", ""))
        plt.text(label2coord(pos[0]), label2coord(pos[1]), str(n_bad))

    plt.savefig(PLOTS_DIR / (fname + ".png"), bbox_inches="tight")

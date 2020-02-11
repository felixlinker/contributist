import numpy as np
import matplotlib.pyplot as plt


def plt_heatmap(heatmap, xlabels, ylabels):
    fig, ax = plt.subplots()
    ax.imshow(heatmap, cmap='YlGn')
    ax.set_xticks(np.arange(len(xlabels)))
    ax.set_yticks(np.arange(len(ylabels)))
    ax.set_xticklabels(xlabels)
    ax.set_yticklabels(ylabels)

    # x labels on top
    ax.tick_params(top=True, bottom=False,
                   labeltop=True, labelbottom=False)

     # Turn spines off and create white grid.
    for _, spine in ax.spines.items():
        spine.set_visible(False)

    ax.set_xticks(np.arange(heatmap.shape[1]+1)-.5, minor=True)
    ax.set_yticks(np.arange(heatmap.shape[0]+1)-.5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)

    fig.tight_layout()
    plt.show()

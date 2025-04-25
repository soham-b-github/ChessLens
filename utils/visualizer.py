import matplotlib.pyplot as plt


# visualizer.py

import matplotlib.pyplot as plt
import numpy as np

def display_board_state(board_state):
    import matplotlib.pyplot as plt
    import numpy as np

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xticks(np.arange(8))
    ax.set_yticks(np.arange(8))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 8)
    ax.grid(True)

    # Draw pieces
    for y in range(8):
        for x in range(8):
            piece = board_state[y][x]
            if isinstance(piece, str) and piece.strip():
                ax.text(x + 0.5, 7.5 - y, piece, ha='center', va='center', fontsize=16)

    plt.gca().invert_yaxis()
    plt.show()


# ~ def display_board_state(board_state):
    # ~ """
    # ~ Visualizes an 8x8 board with text labels.
    # ~ Each tile in `board_state` should be a string or symbol.
    # ~ """
    # ~ fig, ax = plt.subplots(figsize=(6, 6))
    # ~ ax.set_xticks(np.arange(8))
    # ~ ax.set_yticks(np.arange(8))
    # ~ ax.set_xticklabels([])
    # ~ ax.set_yticklabels([])
    # ~ ax.set_xlim(0, 8)
    # ~ ax.set_ylim(0, 8)
    # ~ ax.grid(True)

    # ~ # Draw pieces
    # ~ for y in range(8):
        # ~ for x in range(8):
            # ~ piece = board_state[y][x]
            # ~ if piece:
                # ~ ax.text(x + 0.5, 7.5 - y, piece, ha='center', va='center', fontsize=16)

    # ~ plt.gca().invert_yaxis()
    # ~ plt.show()

# Author: Linda Mazzone
# Bachelor Thesis – Computational Linguistics: A Large-Scale, Cross-Linguistic Investigation of Vowel Dispersion
# University of Zurich
# Spring Semester 2025
# Description: Script to get a visual representation of the expectation of vowel dispersion based
# on the Vowel Dispersion Theory.
# Note: This script was written as part of my Bachelor's thesis in Computational Linguistics.

import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse



# Updated vowel list and positions based on the new image layout
vowels = ['i', 'ɪ', 'ʊ', 'o', 'u', 'e', 'ə', 'ɔ', 'ɛ', 'æ', 'a', 'ɑ']
positions = {
    'i': (300, 300),
    'ɪ': (500, 350),
    'ʊ': (800, 350),
    'o': (1000, 475),
    'u': (1100, 300),
    'e': (350, 420),
    'ə': (700, 480),
    'ɔ': (950, 600),
    'ɛ': (420, 550),
    'æ': (480, 660),
    'a': (600, 750),
    'ɑ': (850, 750)
}
fig, ax = plt.subplots(figsize=(8, 6))

# Plot ellipses and vowel labels
for v in vowels:
    x, y = positions[v]
    ellipse = Ellipse((x, y), 150, 100, color='blue', alpha=0.3)
    ax.add_patch(ellipse)
    ax.text(x, y, v, ha='center', va='center', fontsize=25, color='black')

# Set limits
ax.set_xlim(200, 1200)
ax.set_ylim(800, 200)

# Position axes
ax.xaxis.set_label_position('top')
ax.xaxis.tick_top()
ax.yaxis.set_label_position('right')
ax.yaxis.tick_right()

# Add black lines for F1 and F2 axes
ax.axhline(y=200, color='black', linewidth=1.5)  # Top (F2)
ax.axvline(x=1200, color='black', linewidth=1.5)  # Right (F1)
# Hide left and bottom spines
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)

# Remove tick marks and numbers
ax.set_xticks([])
ax.set_yticks([])


# Axis labels and grid
ax.set_xlabel('F2 (Hz)', fontsize=12)
ax.set_ylabel('F1 (Hz)', fontsize=12)
# ax.grid(True)

plt.tight_layout()
plt.savefig('vowel_inventory_ellipses_12.png', dpi=300)
plt.show()



# Define the minimal vowel set and positions for the new layout
vowels3 = ['i', 'u', 'a']
positions3 = {
    'i': (300, 300),
    'u': (1000, 300),
    'a': (600, 650)
}

# Plot with F2 on top, F1 on right, and larger ellipses
fig, ax = plt.subplots(figsize=(8, 6))

# Plot each vowel with a larger ellipse
for v in vowels3:
    x, y = positions3[v]
    ellipse = Ellipse((x, y), 500, 300, color='blue', alpha=0.3)
    ax.add_patch(ellipse)
    ax.text(x, y, v, ha='center', va='center', fontsize=30, color='black')

# Set limits and invert y-axis
ax.set_xlim(0, 1300)
ax.set_ylim(850, 100)


# Position axes
ax.xaxis.set_label_position('top')
ax.xaxis.tick_top()
ax.yaxis.set_label_position('right')
ax.yaxis.tick_right()

# Remove tick marks and numbers
ax.set_xticks([])
ax.set_yticks([])


# Add bold black lines for F2 (top) and F1 (right)
ax.axhline(y=0, color='black', linewidth=1.5)  # Top line (F2)
ax.axvline(x=1300, color='black', linewidth=1.5)  # Right line (F1)
# Hide left and bottom spines
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)




# Labels
ax.set_xlabel('F2 (Hz)', fontsize=12)
ax.set_ylabel('F1 (Hz)', fontsize=12)

# Grid
# ax.grid(True)

plt.tight_layout()
plt.savefig('vowel_inventory_ellipses_3.png', dpi=300)
plt.show()

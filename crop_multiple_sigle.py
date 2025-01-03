# -*- coding: utf-8 -*-
"""Crop_multiple_sigle.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1hIsEfXDRd6K-wnQxRh36FVGb2EiNOhU1
"""

# Commented out IPython magic to ensure Python compatibility.
import cv2
import os
import matplotlib.pyplot as plt
import sys

#!git clone https://github.com/MASSIMOQSELLA/MyAKarpathyMicrogradTest.git
#!git config --global user.name "MASSIMOQSELLA"
#!git config --global user.email "massimo_qsella@yahoo.it"
#!git remote set-url origin https://<TOKEN>@github.com/MASSIMOQSELLA/MyAKarpathyMicrogradTest.git
# %cd /content/MyAKarpathyMicrogradTest/crop_images/
#!git pull

def img_show(img, title):
# Visualizzare l'immagine
  plt.imshow(img, cmap='gray')
  plt.title(title)
  plt.axis("off")  # Nascondi gli assi
  plt.show()

# Percorso all'immagine
image_path = "/content/MyAKarpathyMicrogradTest/crop_images/sigla_false4.png"

ck = os.path.exists(image_path)
print (ck)
# Leggi l'immagine
image = cv2.imread(image_path)

# Specifica il numero di righe e colonne della griglia
rows, cols = 5, 4  # Adatta al tuo layout (7x7 è un esempio)

# Ottieni le dimensioni dell'immagine
height, width, _ = image.shape

# Calcola l'altezza e la larghezza di ogni cella
cell_height = ((height // rows))
cell_width = ((width // cols))
#cell_height = round(0.9 * cell_width) + 2
#print(f"cell_height: {cell_height}, cell_width: {cell_width}")

# Cartella per salvare i ritagli
output_dir = "/content/MyAKarpathyMicrogradTest/signatures_false/"
#os.makedirs(output_dir, exist_ok=True)

# Itera su ogni cella della griglia
initial_count = 69
count = initial_count
for r in range(rows):
    for c in range(cols):
        # Calcola le coordinate di ogni cella
        x_start = (c * cell_width)
        y_start = (r * cell_height)
        x_end = (x_start + cell_width)
        y_end = (y_start + cell_height)
        cropped = image[y_start:y_end, x_start:x_end]
        img_show(cropped, f"Image_num_{count} tuned")
        dest_image_path = f"{output_dir}/sigla_false_{count}.png"
        print(f"writing: {dest_image_path}")
        #cv2.imwrite(dest_image_path, cropped)
        count += 1

print(f"{(count-initial_count+1)}Firme estratte salvate in: {output_dir}")

# %cd /content/MyAKarpathyMicrogradTest/signatures_false/
#!git add .
#!git commit -m "Aggiornamento file"
#!git push origin main
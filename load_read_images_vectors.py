# -*- coding: utf-8 -*-
"""load_read_images_vectors.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Rc12Dy5JeTJ7ed3q9EkXrUiYoWVHMfiQ
"""

import cv2
import os
import matplotlib.pyplot as plt
import numpy as np

#!git clone https://github.com/MASSIMOQSELLA/MyAKarpathyMicrogradTest.git
#!git config --global user.name "USER"
#!git config --global user.email "email"
#!git remote set-url origin https://<TOKEN>@github.com/MASSIMOQSELLA/MyAKarpathyMicrogradTest.git

# Percorso all'immagine

def img_show(img, title):
# Visualizzare l'immagine
  plt.imshow(img, cmap='gray')
  plt.title(title)
  plt.axis("off")  # Nascondi gli assi
  plt.show()

dataset_path = "/content/MyAKarpathyMicrogradTest/signatures_real/dataset_sigle_real_vectors.npy"
originals_dir_path="/content/MyAKarpathyMicrogradTest/signatures_real/"

os.chdir(originals_dir_path)
count_files = 0
for image_file in os.listdir(originals_dir_path):
  if(image_file.startswith("sigla_false_")):
    count_files += 1
print('count files', count_files)

#verifica l'esistenza
answ = os.path.exists(dataset_path)
print(answ)

# Carica il dataset
dataset = np.load(dataset_path)

# Verifica la forma
img_num, _ = dataset.shape
print("Numero di immagini nel dataset:", img_num)
#print(dataset.shape)  # Output: (numero_di_immagini, numero_di_pixel)

# Accedi a un'immagine

for i in range(img_num):
  if i % 100 == 0:
    image_vector = dataset[i]  #  vettore 1D
    image_2d = image_vector.reshape(56, 56)  # Ricostruzione in 2D
    img_show(image_2d, f"Immagine numero {i} ricostuita")
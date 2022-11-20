from utils import *
import numpy as np
import matplotlib.pyplot as plt

#On va travailler avec les images prise a la longueur d'onde 530. On en a pris que 30
imgs  = load_images("TPCO/data/530")

flatten_mean_imgs = np.mean(imgs, axis =0).flatten()

"""
Tracé des graphs
"""
# On regarde au pixel 4,5
plt.figure()
plt.plot(imgs[:,4,5])
plt.title("Variation de la valeur du pixel en fonction du temps à 530nm")
plt.xlabel("numéro de l'image")
plt.ylabel("valeur du pixel")
plt.show()

plt.figure()
plt.plot(flatten_mean_imgs)
plt.title("Bruit spatial Fixe (FPN) à 530nm")
plt.xlabel("pixel")
plt.ylabel("valeur du pixel")
plt.show()


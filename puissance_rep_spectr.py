from utils import * 
import numpy as np 
import os
import matplotlib.pyplot as plt


if os.path.isdir("mean_images"):
    mean_images = load_mean_images(folder_path="mean_images")
else:
    mean_images = mean_image_value()

if os.path.isfile("mean_detector_value.txt"):
    mean_det_values = load_detector_values(as_dictionnary=False)
else:
    mean_det_values = mean_detector_value(is_dictionnary=False)

ResSpectral = load_data_file("RepspectraleDSS.txt")


max_l = len(mean_det_values)
wave_l = mean_det_values[:,0]
puissances = mean_det_values[:,1] / ResSpectral[:max_l, 1]



with open("puissances.txt", "w") as f:
    f.write("Wavelength(nm)\tPuissances(W)\n")
    for i in range(len(wave_l)):
        f.write(f"{wave_l[i]}\t{puissances[i]}\n")


def compute_tab_rs(img_window = None):
    tab_rs = []
    for i in range(len(wave_l)):
        rs = compute_rs(mean_images[wave_l[i]], puissances[i], (img_window))
        tab_rs.append(rs)
    return tab_rs



plt.figure()
plt.plot(wave_l, puissances)

plt.title("Puissance lumineuse a la sorite de la sphère en fonction de la longueur d'onde")
plt.ylabel("Puissance (W)")
plt.xlabel("Wavelength (nm)")
plt.show()

def draw_rs(RS, title = "Reponse spectral en fonction de la longueur d'onde"):
    plt.figure()
    plt.plot(wave_l, RS)

    plt.title(title)
    plt.ylabel("Reposne spectral (Vn/W)")
    plt.xlabel("Wavelength (nm)")
    plt.show()


rs_full_img= compute_tab_rs(None)
rs_window = compute_tab_rs(img_window=(20,20,30,30))
rs_pixel= compute_tab_rs(img_window=(50,50,51,51))

with open("reponse_spectral.txt", "w") as f:
    f.write("Wavelength(nm)\tReponseSpectral(Vn/W)\n")
    for i in range(len(wave_l)):
        f.write(f"{wave_l[i]}\t{rs_full_img[i]}\n")

draw_rs(rs_full_img, "Reponse spectral de toute l'image en fonction de la longueur d'onde")
draw_rs(rs_window, "Reponse spectral d'une fenetre de l'image en fonction de la longueur d'onde")
draw_rs(rs_pixel, "Reponse spectral d'un pixel de l'image en fonction de la longueur d'onde")





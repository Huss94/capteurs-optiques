from utils import * 
import numpy as np
import glob
import os 


def mean_detector_value(folder_path = "TPCO/data"):
    """
    compute the mean detector value for each wavelength in the folder_path, write them in a txt file and return a numpy array containing the information 
    """
    wave_lengths = glob.glob(folder_path + '/*')

    with open("mean_detector_value.txt", 'w') as f:
        f.write("longueDonde(nm)"+'\t' + "ValeurMoyenne(V)" + '\n')
    
    mean_values = {}
    for l in wave_lengths:
        lbda = l[len(folder_path) + 1:]
        mean_value = compute_mean_detector_values(l + '/' + lbda + '.dat')
        mean_values[int(lbda)] = mean_value
        with open("mean_detector_value.txt", 'a') as f:
            f.write(lbda +'\t' + str(mean_value) + '\n')
        
    return mean_values


def mean_image_value(folder_path = "TPCO/data"):
    """
    compute the mean image value for each wavelength in the folder_path, save them in mean_images folder and return a numpy array containing the information 
    """
    wave_lengths = glob.glob(folder_path + '/*')


    if not os.path.isdir("mean_images"):
        os.mkdir("mean_images")

    mean_images = {} 
    for l in wave_lengths:
        lbda = l[len(folder_path) + 1:]
        mean_image = np.uint8(compute_mean_image(l))
        mean_images[int(lbda)] = mean_image
        cv.imwrite(f"mean_images/{lbda}.bmp", mean_image)

        # with open("mean_image_value.txt", 'a') as f:
        #     f.write(l[len(folder_path) + 1:] +'\t' + str(mean_image))
        

    return mean_images



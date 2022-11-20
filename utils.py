import glob
import numpy as np
import shutil
import cv2 as cv
import os 

def move_ini_file(path = "TP_capt", dest_folder = "TPCO/data"): 
    paths = glob.glob(path+'/*')
    for p in  paths:
        dest = dest_folder + p[len(path) + 1:-4]
        shutil.copy(p, dest)

def load_data_file(path):
    data = np.genfromtxt(path,delimiter='\t', skip_header=1)
    return data

def compute_mean_detector_values(path_dat_file):
    data= load_data_file(path_dat_file)
    return np.mean(data[:,1])

def compute_mean_image(folder_path):
    imgs = load_images(folder_path)
    return np.mean(imgs, axis = 0)

def load_images(folder_path):
    paths = glob.glob(folder_path + '/*.bmp')
    imgs = []
    for p in paths:
        im = cv.imread(p,0)
        imgs.append(im)

    imgs = np.array(imgs) 
    return imgs


def load_mean_images(folder_path = "mean_images", ext = "bmp"):
    print("Loading images")
    paths = glob.glob(folder_path + f'/*.{ext}')
    mean_images  = {}
    for p in paths:
        wavelength = int(p[len(folder_path) + 1: - len(ext) - 1])
        im = cv.imread(p,0)
        mean_images[wavelength] = im
    return mean_images

def load_detector_values(path = "mean_detector_value.txt", as_dictionnary = False):
    print("Loading detector value")
    data = load_data_file(path)
    if as_dictionnary:
        mean_values = {}
        for i in range(data.shape[0]):
            mean_values[data[i,0]] = data[i,1]
    else:
        mean_values = data

    return mean_values
    
def mean_detector_value(folder_path = "TPCO/data", is_dictionnary = True):
    """
    compute the mean detector value for each wavelength in the folder_path, write them in a txt file and return a numpy array containing the information 
    """
    wave_lengths = glob.glob(folder_path + '/*')

    with open("mean_detector_value.txt", 'w') as f:
        f.write("longueDonde(nm)"+'\t' + "ValeurMoyenne(V)" + '\n')
    
    mean_values = {} if is_dictionnary else []
    for l in wave_lengths:
        lbda = l[len(folder_path) + 1:]
        mean_value = compute_mean_detector_values(l + '/' + lbda + '.dat')
        if is_dictionnary:
            mean_values[int(lbda)] = mean_value
        else:
            mean_values.append([int(lbda), mean_value])

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

def compute_rs(img, puissance, img_window):
    """Compute the spectral response given an image, the power, and an img window

    Args:
        img (numpy.ndarray): image representant l'intensité ou la tension
        puissance (float): puissance lumineuse a une certaine longueur d'onde
        img_window (tuple): (xmin, ymin, xmax, ymax)

    Returns:
        float: réponse spectral pour une valeur de lambda 
    """
    if img_window is not None:
        xmin, ymin, xmax, ymax = img_window
        assert xmin <= xmax
        assert ymin <= ymax
        intensity = np.mean(img[xmin:xmax, ymin:ymax])
    else:
        intensity = np.mean(img)
    

    rs = intensity/puissance
    return rs


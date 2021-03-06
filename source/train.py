import os
import time
import glob
import cv2
import numpy as np

from sklearn.svm import LinearSVC
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from scipy.ndimage.measurements import label

from external import extract_features

############
# Hyper #
############
color_space = "YCrCb" #"RGB"
orient = 9
pix_per_cell = 8
cell_per_block = 2
hog_channel = "ALL" #0
spatial_size = (32,32) #(16,16)
hist_bins = 32 #16
spatial_feat = True
hist_feat = True
hog_feat = True

def train():
    ########################################################################################################################
    print("Starting training...")
    basedir = "../data/vehicles/"
    image_types = os.listdir(basedir)
    cars = []
    for imtype in image_types:
        cars.extend(glob.glob(basedir+imtype+'/*'))
    print("Training: Number of vehicle images found", len(cars))

    basedir = "../data/non-vehicles/"
    image_types = os.listdir(basedir)
    notcars = []
    for imtype in image_types:
        notcars.extend(glob.glob(basedir+imtype+'/*'))
    print("Training: Number of notvehicle images found", len(notcars))
    ########################################################################################################################
    t = time.time()
    n_samples = 1000
    random_idxs = np.random.randint(0,len(cars),n_samples)
    test_cars = cars
    test_notcars = notcars
    print("Training: Extracting Features - Round 1...")
    car_features = extract_features(test_cars, 
        color_space=color_space, 
        spatial_size=spatial_size,
        hist_bins=hist_bins,
        orient=orient,
        pix_per_cell=pix_per_cell,
        cell_per_block=cell_per_block,
        hog_channel=hog_channel, spatial_feat=spatial_feat,
        hist_feat=hist_feat,hog_feat=hog_feat)
    print("Training: Extracting Features - Round 2...")
    notcar_features = extract_features(test_notcars, 
        color_space=color_space, 
        spatial_size=spatial_size,
        hist_bins=hist_bins,
        orient=orient,
        pix_per_cell=pix_per_cell,
        cell_per_block=cell_per_block,
        hog_channel=hog_channel, spatial_feat=spatial_feat,
        hist_feat=hist_feat,hog_feat=hog_feat)
    print("Training:", time.time()-t, "total seconds to compute the features...")
    ########################################################################################################################
    X = np.vstack((car_features, notcar_features)).astype(np.float64)
    X_scalar = StandardScaler().fit(X)
    scaled_X = X_scalar.transform(X)

    y = np.hstack((np.ones(len(car_features)), np.zeros(len(notcar_features))))

    rand_state = np.random.randint(0,100)
    X_train, X_test, y_train, y_test = train_test_split( scaled_X, y, test_size=0.1, random_state=rand_state)

    print("Training: feature vector length", len(X_train[0]))
    svc = LinearSVC()
    t = time.time()
    svc.fit(X_train, y_train)
    print("Training:", time.time()-t, "seconds to train SVM")
    print("Training: test accuracy is ", svc.score(X_test, y_test))
    return X_scalar, svc
    ########################################################################################################################

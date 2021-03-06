##Writeup
---

**Vehicle Detection Project**

The goals / steps of this project are the following:

* Perform a Histogram of Oriented Gradients (HOG) feature extraction on a labeled training set of images and train a classifier Linear SVM classifier
* Optionally, you can also apply a color transform and append binned color features, as well as histograms of color, to your HOG feature vector. 
* Note: for those first two steps don't forget to normalize your features and randomize a selection for training and testing.
* Implement a sliding-window technique and use your trained classifier to search for vehicles in images.
* Run your pipeline on a video stream (start with the test_video.mp4 and later implement on full project_video.mp4) and create a heat map of recurring detections frame by frame to reject outliers and follow detected vehicles.
* Estimate a bounding box for vehicles detected.

[//]: # (Image References)
[image1i]: ./writeup_images/image1.png
[image2i]: ./writeup_images/image2.png
[image3i]: ./writeup_images/image3.png
[image4i]: ./writeup_images/image4.png
[image5i]: ./writeup_images/image5.png
[image6i]: ./writeup_images/image6.png
[image7i]: ./writeup_images/image7.png
[image8i]: ./writeup_images/image8.png

## [Rubric](https://review.udacity.com/#!/rubrics/513/view) Points
###Here I will consider the rubric points individually and describe how I addressed each point in my implementation.  

---
###Writeup / README

####1. Provide a Writeup / README that includes all the rubric points and how you addressed each one.  You can submit your writeup as markdown or pdf.

This is my writeup, you're reading it!

###Histogram of Oriented Gradients (HOG)

####1. Explain how (and identify where in your code) you extracted HOG features from the training images.
In the pipeline, the hog features are extracted in the `generate_image.py` file around lines 84-87. This section of the code points to a function named `get_hog_features()`. This method was discussed thouroughly in the lectures. Calculating the hog for the region of entire region of interest is useful because we can then step through the resulting array, and use the HOG features as part of the inputs to a trained model. This eliminates the need to repetitivly call the hog function on sub-regions of the input. HOG features can be a robust technique for capturing the gradients of an object. In lines 15-25 of the `external.py` file, we can see the implementation of the aforementioned `get_hog_features()`. It relies on the `skimage.feature` library and a few parameters like the number of orientations to use, pixels per cell, cells per block, etc. After some experimentation, the best results came from using the `YCrCb` color space along with these parameters: `orient = 9`, `pix_per_cell = 8`, `cell_per_block = 2`. 

Here is an example of this function on one each of the `vehicle` and `non-vehicle` classes:

![alt text][image1i]
![alt text][image2i]
![alt text][image3i]

####2. Explain how you settled on your final choice of HOG parameters.
Settling on the paramters came through trial and error. I experimented with some of the combinations that were seen in the lectures, with a few different color spaces, and I visualized the results as I tried different combinations. I also used the forums and other Udacity resources to see what results were working well for others.


####3. Describe how (and identify where in your code) you trained a classifier using your selected HOG features (and color features if you used them).
I trained a linear SVM using the provided dataset and the sklearn library. In the pipeline, before the first image is processed, I generate a model using the `train()` function around lines 51-56 in the `find_cars()` function. This is imported from the `train.py` file. In it, we see that the classifier is trained (using `extract_features()` on an image) with hog features, spatial features, and histogram features. All of these features are stacked and then the SVM is used to fit the data into a model classifier. This entire process is around lines 30-87 of the `train.py` file. This model is later used in the pipeline to determine if sub-regions of an input image match to a car image.


###Sliding Window Search

####1. Describe how (and identify where in your code) you implemented a sliding window search.  How did you decide what scales to search and how much to overlap windows?
I begin to set-up the parameters of my sliding-window search in lines 73-82 of the `generate_image.py` file. The windows overlap by about 75% (6cells/8cells). Searching begins at the top left of the cropped image and continues through the end of the cropped image. The windows are approximatly 64x64px. By calculating the number of windows that can fit in the area of interest, along with overlaps, it is possible to step through each of them from within a for-loop (see begining around line 90 of that same file). I used the scales and overlap that were tested in the lectures. 

Region of Interest

![alt text][image4i]

The windows overlap by about 75%. Highlighted are 4 overlapping windows.

![alt text][image5i]

####2. Show some examples of test images to demonstrate how your pipeline is working.  What did you do to optimize the performance of your classifier?

Ultimately I searched on one scale using YCrCb 3-channel HOG features plus spatially binning and color histograms in the feature vector, which provided a nice result. For performance, I am only searching a specific area of interest, and ignoring other parts of the image that would not have cars (for example, the sky). Here are some example images:

![alt text][image6i]
---

### Video Implementation

####1. Provide a link to your final video output.  Your pipeline should perform reasonably well on the entire project video (somewhat wobbly or unstable bounding boxes are ok as long as you are identifying the vehicles most of the time with minimal false positives.)
Here's a [link to my video result](./output_images/test-l0.mp4)


####2. Describe how (and identify where in your code) you implemented some kind of filter for false positives and some method for combining overlapping bounding boxes.

I recorded the positions of positive detections in each frame of the video. For each positive detection, I created a heatmap that would aggregate clusters of overlapping detections as they occured. I used this in hopes of being able to detect false positives using the heatmap. I then used `scipy.ndimage.measurements.label()` to identify clusters in the heatmap. I proceed under the assumption that each cluster on the heatmap represents a vehicle and place bounding boxes around the clusters.

Here's an example result showing the heatmap from a series of frames of video, the result of `scipy.ndimage.measurements.label()` and the bounding boxes then overlaid on the last frame of video:

### Here are six frames and their corresponding heatmaps:
![alt text][image7i]

### Here the resulting bounding boxes are drawn onto the last frame in the series:
![alt text][image8i]



---

###Discussion

####1. Briefly discuss any problems / issues you faced in your implementation of this project.  Where will your pipeline likely fail?  What could you do to make it more robust?

I ran into quite a few issues while working on this project. I am currently only using the heatmap to try detechting false positives, but I would like to investigate a more robust technique that can augment this. I still have false positives in the pipeline results . I would also like to implement a tracker class that could be used to track vehicles across images, and to help track vehicles as they disappear behind obstacles. I would also really like to reduce the jitter effect that occurs when the car-detections are not averaged across frames. My pipeline would likely somewhat fail with multiple vehicles at different distances. This is because I am currently only using one scale instead of a few.  

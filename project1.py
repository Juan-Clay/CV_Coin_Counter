import cv2
import numpy as np


 


def main(fileName):
    #Reads the image and loads into program. 
    image = cv2.imread(fileName)

    #Makes the image gray to make it easier to read
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    #Blur the image to reduce noise and make it easier to process
    blurred = cv2.GaussianBlur(gray, (15, 15), 0)
   

    #Make the image binary, specifically use OTSU to make it easier to filter out background from different photo conditions
    _, binary = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
   
    #this kernel will be used to apply a morphological operation on the binary image
    kernel = np.ones((8, 8), np.uint8)
    #apply morphological transformations to an image.
    morphed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=3)
    
    #calculates the minimum distance of each pixel in the foreground to the nearest background pixel
    dist_transform = cv2.distanceTransform(morphed, cv2.DIST_L2, 3)
    
    #apply threshold to the transformed 
    _, sure_fg = cv2.threshold(dist_transform, 0.5 * dist_transform.max(), 255, 0)
  
    #Increase size of foreground elements
    sure_bg = cv2.dilate(morphed, kernel, iterations=3)

    #Turn into int8 binary image, almost no change. 
    sure_fg = np.uint8(sure_fg)

    #Subtract sure_bg and sure_fg to find centers
    unknown = cv2.subtract(sure_bg, sure_fg)

    #Locate the centers of the coins 
    _, markers = cv2.connectedComponents(sure_fg)
    markers = markers + 1
    markers[unknown == 255] = 0

    #watershed to find the borders of all the coins to get their areas and xy coords
    markers = cv2.watershed(image, markers)

    #make color boundaries red
    image[markers == -1] = [0, 0, 255]  


    #setup to find areas of each coin from watershed
    unique_labels = np.unique(markers)
    areas = []

    #goes through all existing labels
    for label in unique_labels:
        #skip boundaries and background
        if label == -1 or label == 1:  
            continue
        #calculate area
        area = np.sum(markers == label)
        #Set to list
        areas.append(area)

    #all labels and their xy coords
    _, labels, stats, centroids = cv2.connectedComponentsWithStats(sure_fg)


    #different coins area thresholds, found through analyzing areas of test cases. 
    dimePenny_threshold = 25750
    pennyNickle_threshold = 30750
    nickleQuarter_threshold = 38050




    for i, centroid in enumerate(centroids):
        #skip the background
        if i == 0:  
            continue
        
        #get x and y of the coin
        x, y = int(centroid[0]), int(centroid[1])
        
        #draw dot of the circle
        cv2.circle(image, (x, y), 10, (0, 255, 0), -1)
        # Optionally classify based on the area (stats[i, cv2.CC_STAT_AREA])
        
        #get area of current coin
        area = areas[i-1]


        # Classify the coin based on its area
        if area < 20000:
            continue
        elif area < dimePenny_threshold:
            coin_type = "10"
            print(f"{x} {y} {coin_type}")
        elif dimePenny_threshold <= area < pennyNickle_threshold:
            coin_type = "1"
            print(f"{x} {y} {coin_type}")
        elif pennyNickle_threshold <= area < nickleQuarter_threshold:
            coin_type = "5"
            print(f"{x} {y} {coin_type}")
        elif area <= 52000:
            coin_type = "25"
            print(f"{x} {y} {coin_type}")
        else:
            continue
        #write on image what value the coin is
        cv2.putText(image, coin_type, (x - 20, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 4)
        

    
name = input()
main(name)
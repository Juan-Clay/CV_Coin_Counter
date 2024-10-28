import cv2
import numpy as np




def check_for_coin(x, y):
    clickrange = 50
    for c in range(0, len(centers)):
        #check if current mouse click is within range of a center
        if (x >= centers[c][0] - clickrange and x <= centers[c][0] + clickrange) and ((y >= centers[c][1] - clickrange and y <= centers[c][1] + clickrange)):
            return c
    return -1


def mouse_callback(event, x, y, flags, param):
    # Check if the event is moving the mouse
    if event == cv2.EVENT_MOUSEMOVE:
        # Update the window title with the current mouse coordinates
        cv2.setWindowTitle('Win', f'Coordinates: ({x}, {y})')
    if event == cv2.EVENT_LBUTTONDOWN:
        check = check_for_coin(x, y)
        if check != -1:
            cv2.setWindowTitle('Win', f'Coin: ({centers[check][2]}) coords: ({x}, {y}) Area: ({centers[check][3]}) NEW AREA: ({areas[check]})')


def showimage(image):
    cv2.namedWindow("Win", cv2.WINDOW_NORMAL)
    cv2.setMouseCallback('Win', mouse_callback)
    cv2.imshow("Win", image)
    cv2.waitKey(0)


def test2OLD(fileName):
    #Reads the image and loads into program. 
    image = cv2.imread(fileName + '.png')


    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    blurred = cv2.GaussianBlur(gray, (15, 15), 0)

    _, binary = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    #binary = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                               #cv2.THRESH_BINARY_INV, 11, 2)

    # kernel = np.ones((3, 3), np.uint8)
    # morphed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=2)
    kernel = np.ones((15, 15), np.uint8)
    morphed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=3)


    dist_transform = cv2.distanceTransform(morphed, cv2.DIST_L2, 5)


    #_, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)
    _, sure_fg = cv2.threshold(dist_transform, 0.5 * dist_transform.max(), 255, 0)

    sure_bg = cv2.dilate(morphed, kernel, iterations=3)

    sure_fg = np.uint8(sure_fg)

    unknown = cv2.subtract(sure_bg, sure_fg)


    _, markers = cv2.connectedComponents(sure_fg)
    markers = markers + 1

    markers[unknown == 255] = 0

    markers = cv2.watershed(image, markers)


    image[markers == -1] = [0, 0, 255]  # Mark boundaries in red

    _, labels, stats, centroids = cv2.connectedComponentsWithStats(sure_fg)


    # dimePenny_threshold = 5700
    # pennyNickle_threshold = 9400
    # nickleQuarter_threshold = 11800

    dimePenny_threshold = 5882
    pennyNickle_threshold = 9718
    nickleQuarter_threshold = 11312




    centers = []
    for i, centroid in enumerate(centroids):
        if i == 0:  # Skip the background
            continue

        x, y = int(centroid[0]), int(centroid[1])
        cv2.circle(image, (x, y), 10, (0, 255, 0), -1)
        # Optionally classify based on the area (stats[i, cv2.CC_STAT_AREA])
        area = stats[i, cv2.CC_STAT_AREA]

        #centers.append([centroid[0], centroid[1], i, stats[i, cv2.CC_STAT_AREA]])

        # Classify the coin based on its area
        if area < dimePenny_threshold:
            coin_type = "10"
        elif dimePenny_threshold <= area < pennyNickle_threshold:
            coin_type = "1"
        elif pennyNickle_threshold <= area < nickleQuarter_threshold:
            coin_type = "5"
        else:
            coin_type = "25"
        cv2.putText(image, coin_type, (x - 20, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 4)
        #print(f"Coin {i}: Centroid = {centroid}, Area = {stats[i, cv2.CC_STAT_AREA]}, Type = {coin_type}")
        #[x, y, coin#, area, coin type]
        centers.append([centroid[0], centroid[1], i, stats[i, cv2.CC_STAT_AREA], coin_type])


    #print(centroids)

    return centers, image








def test2(fileName):
    #Reads the image and loads into program. 
    image = cv2.imread(fileName + '.png')

    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
   
    blurred = cv2.GaussianBlur(gray, (15, 15), 0)
    #showimage(blurredOG)
    #showimage(blurred)


    _, binary = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    #_, binary = cv2.threshold(gray, 160, 255, cv2.THRESH_BINARY_INV)
    #howimage(binary)
    #binary = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                               #cv2.THRESH_BINARY_INV, 11, 2)

    #kernel = np.ones((3, 3), np.uint8)
    #morphed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=2)
    kernel = np.ones((8, 8), np.uint8)
    morphed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=3)
    #showimage(morphed)
    


    dist_transform = cv2.distanceTransform(morphed, cv2.DIST_L2, 3)
    




    #_, sure_fg = cv2.threshold(dist_transform, 0.5 * dist_transform.max(), 255, 0)
    _, sure_fg = cv2.threshold(dist_transform, 0.5 * dist_transform.max(), 255, 0)
    #showimage(sure_fg)

    #sure_bg = cv2.dilate(morphed, kernel, iterations=3)
    sure_bg = cv2.dilate(morphed, kernel, iterations=3)
    #showimage(sure_bg)
    sure_fg = np.uint8(sure_fg)
    #showimage(sure_fg)

    unknown = cv2.subtract(sure_bg, sure_fg)
    #showimage(unknown)

    _, markers = cv2.connectedComponents(sure_fg)
    markers = markers + 1
    markers[unknown == 255] = 0

    markers = cv2.watershed(image, markers)
    #print(markers)
    image[markers == -1] = [0, 0, 255]  # Mark boundaries in red




    unique_labels = np.unique(markers)
    areas = []

    for label in unique_labels:
        if label == -1 or label == 1:  # Skip boundaries and background
            continue
        #print(markers, "   ", label)
        area = np.sum(markers == label)
        areas.append(area)

    _, labels, stats, centroids = cv2.connectedComponentsWithStats(sure_fg)
    #print(stats[6][cv2.CC_STAT_LEFT  ], "  ", stats[2][cv2.CC_STAT_AREA])


    # dimePenny_threshold = 5700
    # pennyNickle_threshold = 9400
    # nickleQuarter_threshold = 11800

    dimePenny_threshold = 25750
    pennyNickle_threshold = 30750
    nickleQuarter_threshold = 38050




    centers = []
    for i, centroid in enumerate(centroids):
        if i == 0:  # Skip the background
            continue

        x, y = int(centroid[0]), int(centroid[1])
        cv2.circle(image, (x, y), 10, (0, 255, 0), -1)
        # Optionally classify based on the area (stats[i, cv2.CC_STAT_AREA])
        
        area = areas[i-1]

        #centers.append([centroid[0], centroid[1], i, stats[i, cv2.CC_STAT_AREA]])

        # Classify the coin based on its area
        if area < 20000:
            continue
        elif area < dimePenny_threshold:
            coin_type = "10"
        elif dimePenny_threshold <= area < pennyNickle_threshold:
            coin_type = "1"
        elif pennyNickle_threshold <= area < nickleQuarter_threshold:
            coin_type = "5"
        elif area <= 52000:
            coin_type = "25"
        else:
            continue
        cv2.putText(image, coin_type, (x - 20, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 4)
        #print(f"Coin {i}: Centroid = {centroid}, Area = {stats[i, cv2.CC_STAT_AREA]}, Type = {coin_type}")
        #[x, y, coin#, area, coin type]
        centers.append([centroid[0], centroid[1], i, stats[i, cv2.CC_STAT_AREA], coin_type])



    return centers, image, areas














def get_radius(area):
    return np.sqrt(area/np.pi)


def compare_coords_and_type(line, single_output):
    threshold = get_radius(single_output[3])//2
    #check if center is within half the radius of the correct center
    #print(line, "           ",single_output)
    if ((single_output[0] >= (line[0] - threshold)) and (single_output[0] <= (line[0] + threshold))) and ((single_output[1] >= (line[1] - threshold)) and (single_output[1] <= (line[1] + threshold))):
        #check if coin type matches
        #print("ya")
        if line[2] == int(single_output[4]):
            return True
    return False

#finds the closest coin in the testcaes that matches the single output. returns the line where the coin is in the file, -1 if there is no coin
def find_closest_case(testcases, single_output):
    for line in range(1, len(testcases)):
        
        if compare_coords_and_type(testcases[line], single_output):
            return line
    return -1


def compare_outputs(testcases, output, case):
    #To calculate the accuracy of classificaton
    total = testcases[0][0]
    running = 0
   
    #for every output made in my program, compare it to its respective output in the testcase
    for o in output:
        #Gives me the line in the testcase that contains the supposed coin it is refering to, based off the coordinate search that gradescope is doing.
        line = find_closest_case(testcases, o)
        
        #Once it finds the correct testcase, compare the testcases coin to the actual
        if line != -1:
            #If the coins match
            if testcases[line][2] == int(o[4]):
                running += 1

    if total == 0:
        rate = "NO COINS IN IMAGE"
    else:
        rate = running/total
    print("For ", case, " There was a ", rate, " percent classification rate, it was ", running, "/", total)
            

def tester():
    tests = ["1", "6", "11", "16", "21", "26", "31", "36", "41"]
    

    for t in tests:
        file = open(t+".txt", "r")
        data = [[int(n) for n in line.split()] for line in file]
        centers, image, areas = test2(t)
        compare_outputs(data, centers, t)
        #showimage(image)
        


#centers, image, areas = DEBUG("41")
centers, image, areas = test2("26")
print(centers)
showimage(image)
#tester()
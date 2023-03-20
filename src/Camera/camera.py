import cv2
import numpy as np
from ..util import createDataMap

class Camera:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
         # check/change parameter before testing

    def capture(self):
        _, src = self.cap.read()

        hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)

        # Define the range of red color in HSV
        lower1 = np.array([0, 160, 100])  # S = 155, V = 84
        upper1 = np.array([5, 255, 255])  # 10

        # upper boundary RED color range values; Hue (160 - 180)
        lower2 = np.array([175, 160, 100])  # 160
        upper2 = np.array([179, 255, 255])

        lower_mask = cv2.inRange(hsv, lower1, upper1)
        upper_mask = cv2.inRange(hsv, lower2, upper2)

        full_mask = lower_mask + upper_mask

        # Threshold the HSV image to get only red colors
        color = cv2.bitwise_and(src, src, mask=full_mask)
        val = np.nonzero(color)
        copy = np.copy(color)
        avg_x = 0
        avg_y = 0

        x_axis = list(val[1])
        y_axis = list(val[0])
        data = [x_axis,y_axis]
        
        if len(x_axis) > 0:

            # Remove Outliers
            #outliers = createDataMap(data)
            createDataMap(data)

            #if outliers is not None:
                #for i in range(len(outliers)):
                #    data[0].remove(outliers[i][0])
                #    data[1].remove(outliers[i][1])

                #for i in range(len(outliers)):
                    #copy[outliers[i][1],outliers[i][0],0] = 0
                    #copy[outliers[i][1],outliers[i][0],1] = 0
                    #copy[outliers[i][1],outliers[i][0],2] = 0
            
             # Calculate centroids
            if len(data[0]) > 0:
                avg_x = int(round(np.average(data[0])))
                avg_y = int(round(np.average(data[1])))
                copy = cv2.circle(copy, (avg_x, avg_y),
                                radius=10, color=(0, 255, 0), thickness=-1)
                
        return avg_x, copy
    
if __name__== "__main__":
    pass
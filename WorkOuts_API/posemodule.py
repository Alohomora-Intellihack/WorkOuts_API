import cv2
import mediapipe as mp
import os
import time


class poseDetector():
    def __init__(self,mode= False, upBody =False,smooth = True,detectionCon = 0.5,trackCon=0.5):
            

                self.mode = mode
                self.upBody = upBody
                self.smooth = smooth
                self.detectionCon = detectionCon
                self.trackCon = trackCon

                self.mpDraw = mp.solutions.drawing_utils

                self.mpPose = mp.solutions.pose
                self.pose = self.mpPose.Pose(static_image_mode=False,  min_detection_confidence=0.5)
                


    def findPose(self,img,draw = True):
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        #print(results.pose_landmarks)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img,self.results.pose_landmarks,self.mpPose.POSE_CONNECTIONS)

        return img
        

    def getPosition(self,img,draw =True):
        lmlist = []
        if self.results.pose_landmarks:

            for id,lm in enumerate(self.results.pose_landmarks.landmark):
                h, w ,c = img.shape
                cx,cy = int(lm.x*w) ,int(lm.y*h)
                lmlist.append([id,cx,cy])
                if draw:
                    cv2.circle(img,(cx,cy),10,(255,0,0),cv2.FILLED)
            

        return lmlist

    def findAngle(self, img, p1, p2, p3, draw=True):
        # Get the landmarks
        x1, y1 = self.getPosition(img, draw=False)[p1][1:]
        x2, y2 = self.getPosition(img, draw=False)[p2][1:]
        x3, y3 = self.getPosition(img, draw=False)[p3][1:]

        # Calculate the angle
        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
        if angle < 0:
            angle += 360

        # Draw the angle
        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
            cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)
            cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x1, y1), 15, (0, 0, 255), 2)
            cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (0, 0, 255), 2)
            cv2.circle(img, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x3, y3), 15, (0, 0, 255), 2)
            cv2.putText(img, str(int(angle)), (x2 - 50, y2 + 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

        return angle


    

def main():
    pTime = 0
    path = os.path.dirname(os.path.realpath(__file__))+'/videos/'+'squats1.mp4'
    cap = cv2.VideoCapture(path)
    detector = poseDetector()
    
    

    while True:
        success, img = cap.read()
        img = detector.findPose(img)
        lmlist = detector.getPosition(img,draw=False)
        if(len(lmlist)!=0):
            print(lmlist[14])
            cv2.circle(img,(lmlist[14][1],lmlist[14][2]),10,(0,0,255),cv2.FILLED)
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv2.putText(img,str(int(fps)),(70,50),cv2.FONT_HERSHEY_PLAIN,3,
        (255,0,0),3)
        img = cv2.resize(img, (1100,1100))
        cv2.imshow("Image",img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()

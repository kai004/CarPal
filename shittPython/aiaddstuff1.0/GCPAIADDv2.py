#uses google ML vision, get license plate from cars.


#NO RESIZE
#image_0002.jpg
#image_000.6jpg
#image_0007.jpg
#image_0009.jpg
#image_0010.jpg
#image_0011.jpg
#image_0012.jpg

#badDriving400.mp4
#badDriving432.mp4
#badDriving625.mp4

import io
import os
from google.cloud import vision_v1p3beta1 as vision
from datetime import datetime
import cv2


# Setup google authen client key
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:/Users/ebona/Downloads/AIADD-6d5644ba369b.json'
# Source path content all images
SOURCE_PATH_I= "C:/Users/ebona/Desktop/aiadd/"
SOURCE_PATH_V= "badDriving432.mp4"
v_v="vid-frame.jpg"
# Recognizes license plates from images, and hopefully video



def main():

    
    cap = cv2.VideoCapture(SOURCE_PATH_V)
    count=0
    miin=0
    while(cap.isOpened()):
        count+=1
        miin+=1
        #get one frame
        ret, frame= cap.read()
        if ret==True and count >5 and miin>= 120:
            #color scaled image

            #gray scaled image
            gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            cv2.imwrite( SOURCE_PATH_I+ v_v, gray)
            path=SOURCE_PATH_I +v_v
            detect_licPlate(path)
            
            #display the frame
            #cv2.imshow('frame', gray)
            count=0
            
        if cv2.waitKey(1) & 0xFF== ord('q'):
            break
        


        
    cap.release()
    cv2.destroyAllWindows()




def detect_licPlate(iPath):
    start = datetime.now()

    # Read image with opencv
    img = cv2.imread(iPath)
  
   # Get image size
    h, w= img.shape[:2]

    #if image size is reeealy big and high quality, make it smaller

    # Scale the image size for viewing
    imgS = cv2.resize(img, (800, int((h * 800) / w)))

    #Show the origin image in better sized scale
    cv2.imshow('Origin image', imgS)
    
    # Save the image to temp file
    cv2.imwrite(SOURCE_PATH_I + "output.jpg", img)

    # Create new img path for google vision
    iPath = SOURCE_PATH_I+ "output.jpg"

    # Create google vision client
    client = vision.ImageAnnotatorClient()

    # Read image file
    with io.open(iPath, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    # Recognize text
    response = client.text_detection(image=image)
    texts = response.text_annotations
    
      
    l=[]
    w=[]
    numbs=['1','2','3','4','5','6','7','8','9','0']

    for text in texts:
        l.append(text.description)
        #print(l)
        break
    for k in l:
        l=str(l[0])
        l=l.replace("\n", " ")
        w=l.split()
        
    for m in w:
        if len(str(m)) ==7 :
            for p in m:
                if p in numbs:
                    print (m)
                    break
                
                
                    
                


if __name__ =="__main__":
    print("Begin detection initiation-in 3-2-1-now")
    main()
    print("WOOOWWWEEE A LICENCE PLATE!")



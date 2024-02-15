from sense_hat import SenseHat
from time import sleep
from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder
from picamera2.outputs import CircularOutput
from libcamera import controls
import cv2


sense=SenseHat()
picam2 = Picamera2()

sense.clear() ## to clear the LED matrix

dispW=1280
dispH=720
## Next, we configure the preview window size that determines how big should the image be from the camera, the bigger the image the more the details you capture but the slower it runs
## the smaller the size, the faster it can run and get more frames per second but the resolution will be lower. We keep 
picam2.preview_configuration.main.size= (dispW,dispH)  ## 1280 cols, 720 rows. Can also try smaller size of frame as (640,360) and the largest (1920,1080)
## with size (1280,720) you can get 30 frames per second

## since OpenCV requires RGB configuration we set the same format for picam2. The 888 implies # of bits on Red, Green and Blue
picam2.preview_configuration.main.format= "RGB888"
picam2.preview_configuration.align() ## aligns the size to the closest standard format
picam2.preview_configuration.controls.FrameRate=30 ## set the number of frames per second, this is set as a request, the actual time it takes for processing each frame and rendering a frame can be different

picam2.configure("preview")


blue= (0,0,255)
yellow= (255,255,0)
red=(255,0,0)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video = cv2.VideoWriter('video.mp4', fourcc, 1, (dispW, dispH))

pressure=sense.get_pressure()

temperature=sense.get_temperature()
temperature=round(temperature,1)  ## round temperature to 1 decimal place

humidity=sense.get_humidity()
print("Start blowing")

out = []

should_run = True
count = 0

while should_run:

    new_temp = sense.get_temperature()
    new_temp = round(new_temp, 1)
    new_humidity= sense.get_humidity()

    print(f"Old: {temperature} New: {new_temp}")
    print(f"Old: {humidity} New: {new_humidity}")

    if abs(new_temp - temperature) > 0:
        # make it blink
        
        faceCascade=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        
        picam2.start()        
        
        while True:
            frame=picam2.capture_array() ## frame is a large 2D array of rows and cols and at intersection of each point there is an array of three numbers for RGB i.e. [R,G,B] where RGB value ranges from 0 to 255
    
            ## frame[rows,columns] --> is the pixel of each frame
            
            ## the above command will only grab the frame
            frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(frameGray, 1.3, 5)
            
            for face in faces:
                x,y,w,h = face
                cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0),3)
    
            
            cv2.imshow("piCamera2", frame) ## show the frame
            out.append(frame)
            count+=1

            
            key=cv2.waitKey(1) & 0xFF
            
            if key == ord("q"): ## stops for 1 ms to check if key Q is pressed
                should_run = False
                break


print("The air pressure is",pressure, "millibars")

print("The air temperature is", temperature, "celcius")

print("The humidity is", humidity, "%")

cv2.destroyAllWindows()
    
for i in range(0,len(out)):
    video.write(out[i])
video.release()
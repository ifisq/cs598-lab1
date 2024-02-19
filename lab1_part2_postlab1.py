from sense_hat import SenseHat
from time import sleep

sense=SenseHat()
sense.clear()
x = 3
y = 5
blue= (0,0,255)
#sense.set_pixel(x,y, blue)

run = True
while run:
    #sense.clear()
    sense.set_pixel(x,y, blue)
    for event in sense.stick.get_events():
        
        print(event.direction,event.action)
        
        if event.action =="pressed":  ## check if the joystick was pressed
            if event.direction=="middle":   ## to check for other directions use "up", "down", "left", "right"
                run = False
                break
            elif event.direction == "left":
                x-=1
            elif event.direction == "right":
                x+=1
            elif event.direction == "up":
                y-=1
            elif event.direction == "down":
                y+=1
            
            sleep(0.5) ## wait a while and then clear the screen
            sense.clear()
            
sense.clear()
            
            
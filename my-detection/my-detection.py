import jetson.inference
import jetson.utils
import sys
from twenty_four_game import Solution2

print("Print system arguments...")
for a in sys.argv:
    print(a)

# load the detection network
net = jetson.inference.detectNet(argv = sys.argv)

# create video sources and outputs
camera = jetson.utils.videoSource("/dev/video0")
display = jetson.utils.videoOutput()
font1 = jetson.utils.cudaFont()
font2 = jetson.utils.cudaFont()

s = Solution2()

res = "No solution"
curr_det = []

while True:
    img = camera.Capture()
    detections = net.Detect(img)

    if len(detections) > 0:
        temp_det = [int(item.ClassID) for item in detections] 
        temp_det.sort()
    else:
        temp_det = []
    
    font1.OverlayText(img, img.width, img.height, "Detected: " + str(temp_det), 5, 5, font1.White, font1.Gray40)
    if temp_det != curr_det:
        print("Detected:", temp_det)
    
    if len(temp_det) == 4:
        #if temp_det != curr_det:
            #res = s.judgePoint24(temp_det)
            #if res == False:
                #print("No solution exists.")
        if temp_det != curr_det:
            res = s.judgePoint24(temp_det)
            print(res)
    else:
        res = "No solution"
                
    font2.OverlayText(img, img.width, img.height, res, 5, 40, font2.White, font2.Gray40)
    
    curr_det = temp_det
    
    # render the image
    display.Render(img)
    
    # update the title bar
    display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))
    


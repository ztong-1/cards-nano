import jetson.inference
import jetson.utils
import sys
from twenty_four_game import Solution

print("Print system arguments...")
for a in sys.argv:
    print(a)

net = jetson.inference.detectNet(argv = sys.argv)
camera = jetson.utils.videoSource("/dev/video0")
display = jetson.utils.videoOutput()

s = Solution()

curr_sum = -1
curr_det = []

while True:
    img = camera.Capture()
    detections = net.Detect(img)

    if len(detections) > 0:
        temp_det = [int(item.ClassID) for item in detections] 
        temp_det.sort()
    else:
        temp_det = []

    if temp_det != curr_det:
        print("Detected:", temp_det)

    if len(temp_det) == 4:
        #temp_sum = sum(temp_det)
        #if temp_det != curr_det:
            #print("temp_sum", temp_sum)
        #curr_sum = temp_sum
        if temp_det != curr_det:
            res = s.judgePoint24(temp_det)
            if res == False:
                print("No solution exists.")

    curr_det = temp_det

    display.Render(img)
    display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))
    


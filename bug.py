# Bug- 1 vehicle_count = 15 
# green_time = 10 + vehiclecount * 2
# print('Green time:', green_time) 
# vehicle_count = 15 
# green_time = 10 + vehicle_count * 2
# print('Green time:', green_time) 



# Condition check karo — kya sahi hai?
# signal_state = 'GREEN' 
# if signal_state == 'GREEN':   
#     print('Gaadiyaan chal sakti hain!')
# else:   
#     print('Ruko!')


#     Bug 3 —
#     List aur Loop Yeh code 4 lanes print karna chahta hai — kya hoga actually?
# lanes = ['North', 'South', 'East', 'West'] 
# for lane in lanes:
#   print('Lane:', lane)


#   Bug 4 — 
#   OpenCV Image load hogi ya nahi? Kya missing hai?
import cv2 
img = cv2.imread('traffic.jpg') 
cv2.imshow('Traffic', img) 
cv2.waitkey(0)
cv2.destroyAllWindows()

# Bug 5 — 
# YOLO Detection Yeh code YOLO detection chalata hai — kya galat hai?
from ultralytics import YOLO
import cv2
model = YOLO('yolov8n.pt') 
img   = cv2.imread('traffic.jpg')
results = model(img)
for box in results[0].boxes: 
        class_id = int(box.cls[0])    
        print(model.names[class_id])
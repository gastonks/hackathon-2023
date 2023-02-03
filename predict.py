from ultralytics import YOLO
from PIL import Image, ImageDraw, ImageFont
import os, random

model = YOLO("runs/detect/final4/weights/best.pt")

dir_save = "Predict/"

image_test_path = "datasets/CYTECH_DATA/test/images/"
random_image_test = random.choice(os.listdir(image_test_path))
image_path = image_test_path + random_image_test
print(image_path)
image_name = image_path.split("/")[-1]
names = ['Bouteille',"Plastique","goblet plastique","goblet en papier","metal","carton"]

result = model(image_path)

print(result[0])

img = Image.open(image_path)
cimg = img.copy()
img_draw = ImageDraw.Draw(cimg)
for i in range(len(result[0])):
    boxe = [float(x) for x in result[0].boxes[i].xyxy[0]]
    conf = round(float(result[0].boxes[i].conf), 3)
    id_class = int(result[0].boxes[i].cls)
    img_draw.rectangle(boxe, outline="black", width=3)
    img_draw.text((boxe[0]+4,boxe[1]+3), names[id_class]+" "+str(conf), fill="black")
cimg.show()
cimg.save(dir_save+image_name)
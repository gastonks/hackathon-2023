import tensorflow as tf
import os
import numpy as np
import matplotlib.pyplot as plt

def getLabelData(filePath):
    labelData = []
    linesArray = []
    file = open(filePath, "r")
    # we only use the 1st line, because it took  too much time with readlines()
    lines = file.readline()
    labelData = lines.split()
    return labelData

dataDir = "../CYTECH_DATA"
imagesTrainDir = dataDir+"/train/images"
labelsTrainDir = dataDir+"/train/labels"
imagesValidationDir = dataDir+"/valid/images"
labelsValidationDir = dataDir+"/valid/labels"

height = 300
width = 300
class_names = ["Bouteille","Plastique","goblet plastique","goblet en papier","metal","carton"]

nbFilesT = len(os.listdir(imagesTrainDir))
nbFilesV = len(os.listdir(imagesValidationDir))

imagesT = [] # images
targetsT = [] # box coord
labelsT = [] # labels
i = 0

# get training data
for filename in os.listdir(imagesTrainDir):
    fullPathFileImage = os.path.join(imagesTrainDir, filename)
    # check if it's a file
    if(os.path.exists(fullPathFileImage)):
        # get corresponding label
        labelFileName = os.path.splitext(filename)[0]+".txt"
        fullPathFileLabel = os.path.join(labelsTrainDir, labelFileName)
        if(os.path.exists(fullPathFileLabel)):
            labelData = getLabelData(fullPathFileLabel)
            if i % 100 == 0 :
                print(i," / ",nbFilesT)

            # if the format is valid
            if(len(labelData) == 5):
                img = tf.keras.preprocessing.image.img_to_array(tf.keras.preprocessing.image.load_img(fullPathFileImage, target_size=(height, width)))
                imagesT.append(img)
                label = int(labelData[0])
                targetTuple = (float(labelData[1]), float(labelData[2]), float(labelData[3]), float(labelData[4]))
                targetsT.append(targetTuple)
                labelsT.append(label)
                i += 1

imagesT = np.array(imagesT)
labelsT = np.array(labelsT)
targetsT = np.array(targetsT)

trainTargets = {
    "cl_head": labelsT,
    "bb_head": targetsT
}

imagesV = [] # images
targetsV = [] # box coord
labelsV = [] # labels
i = 0



for filename in os.listdir(imagesValidationDir):
    fullPathFileImage = os.path.join(imagesValidationDir, filename)
    # check if it's a file
    if(os.path.exists(fullPathFileImage)):
        # get corresponding label
        labelFileName = os.path.splitext(filename)[0]+".txt"
        fullPathFileLabel = os.path.join(labelsValidationDir, labelFileName)
        if(os.path.exists(fullPathFileLabel)):
            labelData = getLabelData(fullPathFileLabel)
            if i % 100 == 0 :
                print(i," / ",nbFilesV)

            # if the format is valid
            if(len(labelData) == 5):
                img = tf.keras.preprocessing.image.img_to_array(tf.keras.preprocessing.image.load_img(fullPathFileImage, target_size=(height, width)))
                imagesV.append(img)
                label = int(labelData[0])
                targetTuple = (float(labelData[1]), float(labelData[2]), float(labelData[3]), float(labelData[4]))
                targetsV.append(targetTuple)
                labelsV.append(label)
                i += 1


imagesV = np.array(imagesV)
labelsV = np.array(labelsV)
targetsV = np.array(targetsV)

validationTargets = {
    "cl_head": labelsV,
    "bb_head": targetsV
}

input_shape = (height, width, 3)
input_layer = tf.keras.layers.Input(input_shape)

#create the base layers
base_layers = tf.keras.layers.experimental.preprocessing.Rescaling(1./255, name='bl_1')(input_layer)
base_layers = tf.keras.layers.Conv2D(16, 3, padding='same', activation='relu', name='bl_2')(base_layers)
base_layers = tf.keras.layers.MaxPooling2D(name='bl_3')(base_layers)
base_layers = tf.keras.layers.Conv2D(32, 3, padding='same', activation='relu', name='bl_4')(base_layers)
base_layers = tf.keras.layers.MaxPooling2D(name='bl_5')(base_layers)
base_layers = tf.keras.layers.Conv2D(64, 3, padding='same', activation='relu', name='bl_6')(base_layers)
base_layers = tf.keras.layers.MaxPooling2D(name='bl_7')(base_layers)
base_layers = tf.keras.layers.Flatten(name='bl_8')(base_layers)

classifier_branch = tf.keras.layers.Dense(512, activation='relu', name='cl_1')(base_layers)
classifier_branch = tf.keras.layers.Dense(len(class_names), name='cl_head')(classifier_branch)  

locator_branch = tf.keras.layers.Dense(512, activation='relu', name='bb_1')(base_layers)
locator_branch = tf.keras.layers.Dense(128, activation='relu', name='bb_1')(base_layers)
locator_branch = tf.keras.layers.Dense(64, activation='relu', name='bb_2')(locator_branch)
locator_branch = tf.keras.layers.Dense(32, activation='relu', name='bb_3')(locator_branch)
locator_branch = tf.keras.layers.Dense(len(class_names), activation='sigmoid', name='bb_head')(locator_branch)


model = tf.keras.Model(input_layer, outputs=[classifier_branch,locator_branch])

losses = {"cl_head":tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True), "bb_head":tf.keras.losses.MSE}

model.compile(loss=losses, optimizer='Adam', metrics=['accuracy'])

model.summary()

history = model.fit(imagesT, trainTargets,
             validation_data=(imagesV, validationTargets),
             batch_size=32,
             epochs=50,
             steps_per_epoch=25,
             shuffle=True,
             verbose=1)

model.save("rps.h5")

#print(history.history.keys())


acc = history.history['bb_head_accuracy']
val_acc = history.history['val_bb_head_accuracy']
loss = history.history['bb_head_loss']
val_loss = history.history['val_bb_head_loss']

epochs = range(len(acc))

plt.plot(epochs, acc, 'r', label='Training accuracy')
plt.plot(epochs, val_acc, 'b', label='Validation accuracy')
plt.title('Training and validation accuracy')
plt.legend(loc=0)
plt.figure()

plt.show()

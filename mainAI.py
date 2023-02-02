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
class_names = ["Bouteille","Plastique","goblet plastique","goblet en papier","metal","carton"]

images = np.array([]) # images
targets = np.array([]) # box coord
labels = np.array([]) # labels
progress = 0

for filename in os.listdir(imagesTrainDir):
    fullPathFileImage = os.path.join(imagesTrainDir, filename)
    # check if it's a file
    if(os.path.exists(fullPathFileImage)):
        # get corresponding label
        labelFileName = os.path.splitext(filename)[0]+".txt"
        fullPathFileLabel = os.path.join(labelsTrainDir, labelFileName)
        if(os.path.exists(fullPathFileLabel)):
            labelData = getLabelData(fullPathFileLabel)
            if progress % 100 == 0 :
                print(progress," / ",5568)

            # if the format is valid
            if(len(labelData) == 5):
                img = tf.keras.preprocessing.image.img_to_array(tf.keras.preprocessing.image.load_img(fullPathFileImage))
                np.append(images, img)
                label = labelData[0]
                targetTuple = (labelData[1], labelData[2], labelData[3], labelData[4])
                np.append(targets, targetTuple)
                np.append(labels, class_names[int(label)])
            progress += 1

y = (targets, labels)

model = tf.keras.models.Sequential([
    # Note the input shape is the desired size of the image 150x150 with 3 bytes color
    # This is the first convolution
    tf.keras.layers.Conv2D(64, (3,3), activation='relu', input_shape=(150, 150, 3)),
    tf.keras.layers.MaxPooling2D(2, 2),
    # The second convolution
    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    # The third convolution
    tf.keras.layers.Conv2D(128, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    # The fourth convolution
    tf.keras.layers.Conv2D(128, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    # Flatten the results to feed into a DNN
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dropout(0.5),
    # 512 neuron hidden layer
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(6, activation='softmax')
])

model.compile(loss = 'categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

model.summary()

history = model.fit(images, y, epochs=25, steps_per_epoch=20, verbose = 1, validation_steps=3)

model.save("rps.h5")

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
loss = history.history['loss']
val_loss = history.history['val_loss']

epochs = range(len(acc))

plt.plot(epochs, acc, 'r', label='Training accuracy')
plt.plot(epochs, val_acc, 'b', label='Validation accuracy')
plt.title('Training and validation accuracy')
plt.legend(loc=0)
plt.figure()


plt.show()

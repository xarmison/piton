from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Dropout, Flatten, Dense, BatchNormalization
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import Adam

import matplotlib.pyplot as plt

import numpy as np

import time

class CNN():
    def __init__(self):
        # Debug Mode
        self.debug = 0

        # Input shape
        self.img_rows = 300
        self.img_cols = 300
        self.channels = 3
        self.input_shape = (self.img_rows, self.img_cols, self.channels)
        self.num_classes = 8

        optimizer = Adam(0.0002, 0.5)
        loss = ['categorical_crossentropy']

        # Defining the activation functions
        self.convActivation = 'relu'
        self.denseActivation = 'relu'

        # Build and compile the NN
        self.cnn = self.build_cnn()
        self.cnn.compile(
            loss = loss,
            optimizer = optimizer,
            metrics = ['acc']
        )
    
    def build_cnn(self):
        # CNN model
        model = Sequential()
        
        model.add(Conv2D(32, (3, 3), padding='same', activation=self.convActivation, input_shape=self.input_shape))
        model.add(Conv2D(32, (3, 3), activation=self.convActivation))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))

        model.add(Conv2D(64, (3, 3), padding='same', activation=self.convActivation))
        model.add(Conv2D(64, (3, 3), activation=self.convActivation))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))

        model.add(Conv2D(64, (3, 3), padding='same', activation=self.convActivation))
        model.add(Conv2D(64, (3, 3), activation=self.convActivation))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))

        model.add(Flatten())
        model.add(Dense(512, activation=self.denseActivation))
        model.add(Dropout(0.5))
        model.add(Dense(512, activation=self.denseActivation))
        model.add(Dropout(0.5))
        model.add(Dense(512, activation=self.denseActivation))
        model.add(Dropout(0.5))

        # Normalizes the network input weights between 0 and 1
        model.add(BatchNormalization())

        model.add(Dense(8, activation='softmax'))

        if(self.debug):
            model.summary()

        return model

    def train(self, epochs=1, batch_size=1):
        self.epochs = epochs
        
        training_set = ImageDataGenerator().flow_from_directory(
            'dataset/training_set',
            target_size = (self.img_rows, self.img_cols),
            batch_size = batch_size,
            class_mode = 'categorical'
        )

        test_set = ImageDataGenerator().flow_from_directory(
            'dataset/test_set',
            target_size = (self.img_rows, self.img_cols),
            batch_size = batch_size,
            class_mode = 'categorical'
        )

        start = time.time()
        # Fit the model on the batches generated by datagen.flow().
        history = self.cnn.fit_generator(
            training_set,
            steps_per_epoch = len(training_set),
            epochs = epochs,
            validation_data = test_set,
            validation_steps = len(test_set)
        )

        self.history = history

        end = time.time()

        print("Model took %0.2f seconds to train"%(end - start))

    def save_plots(self):
        # Plot the curves
        plt.figure(figsize=[8,6])
        plt.plot(self.history.history['loss'],'r',linewidth=3.0)
        plt.plot(self.history.history['val_loss'],'b',linewidth=3.0)
        plt.legend(['Training loss', 'Validation Loss'],fontsize=18)
        plt.xlabel('Epochs ',fontsize=16)
        plt.ylabel('Loss',fontsize=16)
        plt.title('Loss Curves',fontsize=16)

        plt.savefig('results/img/cnn_loss_{}e.png'.format(self.epochs))

        plt.figure(figsize=[8,6])
        plt.plot(self.history.history['acc'],'r',linewidth=3.0)
        plt.plot(self.history.history['val_acc'],'b',linewidth=3.0)
        plt.legend(['Training Accuracy', 'Validation Accuracy'],fontsize=18)
        plt.xlabel('Epochs ',fontsize=16)
        plt.ylabel('Accuracy',fontsize=16)
        plt.title('Accuracy Curves',fontsize=16)

        plt.savefig('results/img/cnn_acc_{}e.png'.format(self.epochs))

        plt.show()

    def save_logs(self):
        loss_history = np.array(self.history.history['loss'])
        np.savetxt(
            'results/logs/log_loss_{}e.txt'.format(self.epochs), 
            loss_history, 
            fmt='%d'
        )

        acc_history = np.array(self.history.history['acc'])
        np.savetxt(
            'results/logs/log_acc_{}e.txt'.format(self.epochs),
            acc_history,
            fmt='%d'
        )

    def save_model(self):
        self.cnn.save('results/models/cnn_{}e.h5'.format(self.epochs))

if __name__ == '__main__':
    cnn = CNN()
    cnn.train(epochs=10, batch_size=1)
    cnn.save_model()
    cnn.save_plots()
    cnn.save_logs()
    

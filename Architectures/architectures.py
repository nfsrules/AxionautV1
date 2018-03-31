from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout, Flatten
from keras.utils import np_utils
from keras.optimizers import SGD, Adam
from keras.layers import Conv2D, MaxPooling2D
from keras import callbacks


model_path = 'Models/'

class ConvNets(Sequential):
    def __init__(self,input_shape = (70, 250, 3), learning_rate=0.5, optimizers='sgd'):
        super(ConvNets, self).__init__()

        # Conv1 1 (conv + non-linearity + pooling)
        self.add(Conv2D(1,kernel_size=(3, 3),
                         activation='sigmoid',
                         input_shape=(70, 250, 3),
                         padding='same',
                         name='conv1'))

        self.add(MaxPooling2D(pool_size=(2, 2)))

        self.add(Dropout(0.1))

        # Conv 2 (conv, non-linearity + pooling)
        self.add(Conv2D(2,kernel_size=(3, 3),
                        activation='sigmoid',
                        input_shape=(35, 125, 1),
                        padding='same',
                        name='conv2'))

        self.add(MaxPooling2D(pool_size=(2, 2)))

        self.add(Dropout(0.1))

        # Conv 3 (conv, non-linearity + pooling)
        self.add(Conv2D(4,kernel_size=(3, 3),
                         activation='sigmoid',
                         input_shape=(17, 62, 1),
                         padding='same',
                         name='conv3'))

        self.add(MaxPooling2D(pool_size=(2, 2)))

        self.add(Dropout(0.1))


        # Conv 4 (conv, non-linearity + pooling)
        self.add(Conv2D(4,kernel_size=(3, 3),
                         activation='sigmoid',
                         input_shape=(8, 31, 1),
                         padding='same',
                         name='conv4'))

        self.add(MaxPooling2D(pool_size=(2, 2)))

        self.add(Dropout(0.1))

        self.add(Flatten())  # flatten output as vector

        # Fully connected layer 1
        self.add(Dense(20, name='fc1')) 

        self.add(Activation('sigmoid'))  

        # Fully connected layer 2
        self.add(Dense(5, name='fc2')) 
        self.add(Activation('softmax'))   

        # Setting optimizer
        if optimizers == 'sgd':
          opt = SGD(learning_rate)
        else:
          opt = Adam()

        # Compile model
        self.compile(loss='categorical_crossentropy',
              optimizer=opt, metrics=['accuracy'])

        # Print model summary
        self.summary()

    def train(self, train_X, train_Y, batch_size=300,nb_epoch=100,validation_split=0.1):
        """Training method with built-in early stopping. Return plot history
        Save the model after each epoch if the validation loss improved. """

        save_best = callbacks.ModelCheckpoint(model_path, monitor='val_loss', 
                                              verbose=1, save_best_only=True, mode='min')

        #stop training if the validation loss doesn't improve for 5 consecutive epochs.
        early_stop = callbacks.EarlyStopping(monitor='val_loss', min_delta=0,patience=5, verbose=0, mode='auto')

        callbacks_list = [save_best, early_stop]

        history = self.fit([train_X], train_Y,
                  batch_size=100,
                  nb_epoch=50,
                  validation_split=0.1,
                  callbacks=callbacks_list,
                  verbose=1)

        return history


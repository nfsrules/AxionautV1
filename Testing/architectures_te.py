from keras.models import Sequential
from keras.layers import Input, Dense, Activation, Dropout
from keras.layers import Convolution2D, MaxPooling2D, Flatten, LSTM, BatchNormalization
from keras.optimizers import SGD
from keras.models import load_model, Model
from keras.optimizers import Adam
from keras import callbacks


model_path = 'Models/'


class ConvNets():

  def __init__(self):

    self.dropout_value = 0
    self.input_shape = (70, 250, 3)

    img_in = Input(shape=self.input_shape, name='img_in')
    self.x = img_in

    self.x = Convolution2D(1, 3, 3, activation='relu', border_mode='same')(self.x)
    self.x = MaxPooling2D(pool_size=(2, 2), strides=(2,2))(self.x)
    self.x = Dropout(self.dropout_value)(self.x)
    self.x = BatchNormalization()(self.x)

    self.x = Convolution2D(2, 3, 3, activation='relu', border_mode='same')(self.x)
    self.x = MaxPooling2D(pool_size=(2, 2), strides=(2,2))(self.x)
    self.x = Dropout(self.dropout_value)(self.x)
    self.x = BatchNormalization()(x)

    self.x = Convolution2D(2, 3, 3, activation='relu', border_mode='same')(self.x)
    self.x = MaxPooling2D(pool_size=(2, 2), strides=(2,2))(self.x)
    self.x = Dropout(self.dropout_value)(self.x)
    self.x = BatchNormalization()(self.x)

    self.x = Convolution2D(4, 3, 3, activation='relu', border_mode='same')(self.x)
    self.x = MaxPooling2D(pool_size=(2, 2), strides=(2,2))(self.x)
    self.x = Dropout(self.dropout_value)(self.x)
    self.x = BatchNormalization()(self.x)

    self.flat = Flatten()(self.x)

    self.x = Dense(20)(self.flat)
    self.x = Activation('relu')(self.x)

    self.x = Dense(3)(self.x)
    self.angle_out = Activation('softmax')(self.x)

    self.summary()


  def optimizer(self):
    """Create default Adam optimizer"""
    adam = Adam()
    model = Model(input=[self.img_in], output=[self.angle_out])
    self.compile(optimizer=adam, loss='categorical_crossentropy', metrics=['accuracy'])



  def train(self):
    #Save the model after each epoch if the validation loss improved.
    save_best = callbacks.ModelCheckpoint(model_path,
                                          monitor='val_loss',
                                          verbose=1,
                                          save_best_only=True,
                                          mode='min')
    #stop training if the validation loss doesn't improve for 5 consecutive epochs.
    early_stop = callbacks.EarlyStopping(monitor='val_loss',
                                          min_delta=0,
                                          patience=5,
                                          verbose=0,
                                          mode='auto')
    callbacks_list = [save_best, early_stop]


    history = model.fit([train_X], train_Y,
                       batch_size=100,
                       nb_epoch=50,
                       validation_split=0.1,
                       callbacks=callbacks_list,
                      verbose=1)
    return history

  def save(self):

    self.save('last_model_test.hdf5')
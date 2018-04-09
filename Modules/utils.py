# coding=utf-8
import sys
import os
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import tensorflow as tf
from keras.models import load_model
import json
import picamera
import picamera.array


models_path = 'models/'

def plot_train_loss(history):
  
  plt.plot(history.history['acc'])
  plt.plot(history.history['val_acc'])
  plt.title('model accuracy')
  plt.ylabel('accuracy')
  plt.xlabel('epoch')
  plt.legend(['train', 'test'], loc='upper left')
  plt.show()
  # summarize history for loss
  plt.plot(history.history['loss'])
  plt.plot(history.history['val_loss'])
  plt.title('model loss')
  plt.ylabel('loss')
  plt.xlabel('epoch')
  plt.legend(['train', 'test'], loc='upper left')
  plt.show()


def predict_from_img(img):
  """
  Given the 250x150 image from Camera
  Returns prediction.
  """
  global graph, model

  try:
    img = np.array([img[80:, :, :]])

    with graph.as_default():
      pred = model.predict(img)
      print('pred : ', pred)
    prediction = list(pred[0])
  except:
    prediction = [0, 0, 1, 0, 0]

  return prediction


def autopilot_loop(car):
  """Main loop camera fuction to capture images and
  get predictions from autopilot function. This function
  is being running in a Thread.
  """
  global model, graph, commands, max_speed, state, running

  if (car.model_loaded == True):
    commands = car.commands 
    model = car.model
    graph = car.graph
    max_speed = car.max_speed
    state = car.state
    stream = car.cam.capture_continuous(car.cam_output, 
                      format="rgb", 
                      use_video_port=True)
    for frames in stream:
      img_arr = frames.array
      if (state == 'stopped'):
        break
      # Call autopilot function
      autopilot(img_arr)
      # Reset camera output
      car.cam_output.truncate(0)
  else:
    print('Error. Driving model not loaded')


def freeze(model):
  """ Set all layers in a model to non-trainable.
  The weights for these layers will not be updated during training.
  This function modifies the given model in-place,
  but it also returns the modified model to allow easy chaining with other functions.
  """
  for layer in model.layers:
    layer.trainable = False
  return model

# Import GPIO Libraries
import math
import RPi.GPIO as GPIO
import time

# Configure pins and starting the hardware
GPIO.setmode(GPIO.BMC)
TRIG = 23
ECHO = 24

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

GPIO.output(TRIG, False)
print("Waiting For Sensor Start")
time.sleep(2)


def distance_measure():
"""Estimate distance to any object in front of the vehicle.
The result is given in centimeters.
"""
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO)==0:
      pulse_start = time.time()

    while GPIO.input(ECHO)==1:
      pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 17150

    distance = round(distance, 2)

return distance

GPIO.cleanup()


def speed_control(local_angle, max_speed, curve_factor):
  """Function to control speed in curves.
  local_angle: model steering angle prediction
  curve factor: 
  Return:
  Fixed max speed in curves.
  """
    # Check distance to closest object (Based on HC-SR04)
    if distance_measure() < 5:
        local_gas = 0
    else:
        # Calcule k_factor
        global k_factor
        k_factor = (-1) * math.log(curve_factor)

        # Correcting throttle 
        if local_angle < 0:
            max_speed = math.exp(k_factor * local_angle)
        else:
            max_speed = math.exp((-1) * k_factor * local_angle) 

  return local_gas


def autopilot(img):
  """Steering angle prediction function"""
  global model, graph, state, max_speed
  img = np.array([img[80:, :, :]])
  
  with graph.as_default():
    pred = model.predict(img)
    prediction = list(pred[0])
  index_class = prediction.index(max(prediction))

  local_angle = -1 + 2 * float(index_class)/float(len(prediction)-1)

  # To be later changed by some speed control
  local_gas =  speed_control(local_angle)

  pwm.set_pwm(commands['direction'], 0, 
        int(local_angle * (commands['right'] 
        - commands['left']) / 2. 
        + commands['straight']))

  if state == "started":

    pwm.set_pwm(commands['gas'], 0, 
        int(local_gas * (commands['drive_max'] 
        - commands['drive']) 
        + commands['drive']))

  else:

    pwm.set_pwm(commands['gas'], 0, commands['neutral'])


def load_autopilot(model_name):
  """Function to load Keras autopilot model"""
  new_model_path = models_path + model_name
  #print(new_model_path)
  model = load_model(new_model_path)
  graph = tf.get_default_graph()
  return model, graph


def get_commands(path=None, default=True):
  """Get PWD commands, uses Axionaut optimized by default.
  If settings are not default takes as input:
  path : path to commands.json file
  Returns dictionary with commands
  """
  if default == True:
    commands = {
          "direction_pin": 1, "gas_pin": 2,
          "left": 270, "straight": 400, "right": 530,
          "stop": 210, "neutral": 385, "drive": 400, "drive_max": 420,
          "rev_stop": 400, "rev_neutral": 370, "rev_drive": 360, "rev_drive_max": 350, 
          "go_t": 0.25, "stop_t": -0.25, "left_t": 0.5, "right_t": -0.5, "invert_dir": -1
        }
  else:
    commands_json_file = path + "commands.json"
    with open(commands_json_file) as json_file:
      commands = json.load(json_file)

  return commands



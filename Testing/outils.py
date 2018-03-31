import matplotlib.pyplot as plt
plt.style.use('ggplot')
import tensorflow as tf
from keras.models import load_model
import json
import picamera
import picamera.array



model_path = './autopilots/'

# config to save images
ct = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
save_folder = os.path.join('datasets/', str(ct))

if not os.path.exists(save_folder):
    os.makedirs(save_folder)


def plot_losses(history):
	"""Function to plot Training history"""
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


def autopilot_loop(car):
	"""Main loop camera fuction to capture images and
	get predictions from autopilot function. This function
	is being running in a Thread.
	"""
	global model, graph, commands, max_speed, state

	if car.model_loaded == True:
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
        	if not running:
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


def speed_control(local_angle, max_speed, curve_factor):
	"""Function to control speed in curves.
	local_angle: model steering angle prediction
	curve factor: 
	Return:
	Fixed max speed in curves.
	"""
	return max_speed * (1 - local_angle * np.exp(-curve_factor))


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


def load_model(model_name):
	"""Function to load Keras autopilot model"""
    new_model_path = models_path + model_name
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



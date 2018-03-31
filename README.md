## Axionaut
Mini autonomous RC vehicle for AI enthusiasts.

## Introduction
Axionaut provides a straightforward approach to prototype mini RC autonomous vehicles. 

The complete bill of materials is avaliable here:
https://www.axionable.com/axionaut-termine-1er-de-la-deuxieme-course-iron-car/

Axionaut is intended to rapid experimentation, use the built-in Deep Learning architectures and start driving!.

Axionaut is totally free and open for everyone to use and contribute.

## Code style
PEP 8 -- Style Guide for Python Code.


## Screenshot
![alt text](https://www.axionable.com/wp-content/uploads/2018/02/axionautV1.png)


## Tech/framework used

<b>Built using:</b>
- [TensorFlow](https://www.tensorflow.org)
- [Keras](https://keras.io)


## Features

1. <strong>Autonomous drive mode:</strong> Real-time autopilot using Deep Learning models.
2. <strong>Data recording:</strong> Live data recording from the car.
3. <strong>Training mode:</strong> Build and train your own driving models from scratch or using Transfer Learning.
4. <strong>Free ride:</strong> Enjoy driving your RC car on the free ride mode.


## Code Example

Create a new vehicle and set it to self-driving mode is extreamely easy:

	#Load self-driving pre trained model
    model, graph = load_autopilot('autopilot.hdf5')

    # Create Axionaut car with default settings
    axionaut = vehicles.Axionaut()

    # Configure PDW control commands as default
    axionaut.commands = get_commands(path=None, default=True)

    # Test camera position
    axionaut.camera_test()

    # Set vehicle to auto pilot mode 
    axionaut.autopilot(model, graph)

    # Start car   
    axionaut.start()


Also, the following commands are avaliable:

To start self-driving mode:
`python main.py mode self_driving`

To start recording mode:
`python main.py mode record`

To start on free ride mode:
`python main.py mode free`

To train your own model:
`python main.py mode train architecture ConvNets epochs 100 batch size 300 optimizer Adam`

Feel free to explore and set your prefered training hyperparameters!


## Installation
### Raspberry side:
Clone repository to your Raspberry Pi:
`git clone https://github.com/Axionable/AxionautV1`

Install packages:
`pip install -r requirements.txt`

### Computer side:
Clone repository to your laptop:
`git clone https://github.com/Axionable/AxionautV1`

Install packages:
`pip install -r laptop_requirements.txt`


## Status


## How to use?
If people like your project they’ll want to learn how they can use it. To do so include step by step guide to use your project.

## Contribute

Axionaut is currently under developement. Please feel free to contribute!


## Credits
IronCar France 2018

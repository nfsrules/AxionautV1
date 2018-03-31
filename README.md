## Axionaut
Mini autonomous RC vehicle for AI enthusiasts.

## Introduction
Axionaut provides a straightforward approach to prototype mini RC autonomous vehicles. 

The complete bill of materials can be found here:
https://www.axionable.com/axionaut-termine-1er-de-la-deuxieme-course-iron-car/

Axionaut is intended to rapid experimentation, use the built-in Deep Learning architectures and start driving!.

Totally free and open for everyone to use and contribute.

## Code style
PEP 8 -- Style Guide for Python Code.
 

## Screenshot
![alt text](https://www.axionable.com/wp-content/uploads/2018/02/axionautV1.png)


## Tech/framework used

<b>Built using:</b>
- [TensorFlow](https://www.tensorflow.org)
- [Keras](https://keras.io)


## Features

1. Autonomous drive mode: Real-time autopilot using Deep Learning models.
2. Data recording: Live data recording from the car.
3. Training mode: Build and train your own driving models from scratch or using Transfer Learning.
4. Free ride: Enjoy driving your RC car on the free ride mode.


## Code Example

Create a new vehicle and set it to self-driving mode is extreamely easy:

	#Load self-driving pre-train model
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

Feel free to set your prefered training hyperparameters!


## Installation
### On the Raspberry:
Clone repository to your Raspberry Pi:
`git clone https://github.com/Axionable/AxionautV1`

Install packages:
`pip install -r requirements.txt`

### On the computer side:
Clone repository to your laptop:
`git clone https://github.com/Axionable/AxionautV1`

Install packages:
`pip install -r laptop_requirements.txt`


## API Reference

Depending on the size of the project, if it is small and simple enough the reference docs can be added to the README. For medium size to larger projects it is important to at least provide a link to where the API reference docs live.

## Tests
Describe and show how to run the tests with code examples.

## How to use?
If people like your project they’ll want to learn how they can use it. To do so include step by step guide to use your project.

## Contribute

Let people know how they can contribute into your project. A [contributing guideline](https://github.com/zulip/zulip-electron/blob/master/CONTRIBUTING.md) will be a big plus.

## Credits
Give proper credits. This could be a link to any repo which inspired you to build this project, any blogposts or links to people who contrbuted in this project. 

#### Anything else that seems useful

## License
A short snippet describing the license (MIT, Apache etc)

MIT © [Yourname]()
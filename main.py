# coding=utf-8
import os
import sys
sys.path.append('Modules/')
sys.path.append('Databases/')
sys.path.append('Architectures/')
sys.path.append('Models/')


from utils import load_autopilot, get_commands
import architectures
import vehicles 
import argparse
import warnings
warnings.filterwarnings("ignore")

models_path = '/Models'

parser = argparse.ArgumentParser(description='Axionaut')
parser.add_argument('--mode', default='self_driving', help='self_driving, records or training') # PoSelf driving, Record, Training
parser.add_argument('--architecture', default='ConvNets', help='ConvNets or ConvLSTM')
parser.add_argument('--tl', default='transfer_learning', help='Weights initialization - Random or Transfer Learning')
parser.add_argument('-e', '--epochs', default=150, type=int)
parser.add_argument('-b', '--batch_size', default=64, type=int)
parser.add_argument('-op', '--optimizer', default='Adam')


args = parser.parse_args()


if (args.mode == 'self_driving'):
    print('Vehicle started in self driving mode.')

    # Load self-driving pre-train model
    model, graph = load_autopilot('autopilot.hdf5')

    print('Model loaded...')

    # Create Axionaut car with default settings
    axionaut = vehicles.Axionaut()

    # Configure PDW control commands as default
    axionaut.commands = get_commands(path=None, default=True)

    # Test camera position
    axionaut.camera_test()

    print('Hardware configured...')

    # Set Axionaut to auto pilot mode / Wrap driving model to vehicle
    axionaut.autopilot(model, graph)

    # Start Axtionaut :)
    raw_input('Self self_driving started. Pres any key to start driving. Press Crtl + C to exit.')
    
    axionaut.start()

elif(args.mode == 'training'):

    print('Vehicle started in training mode.')

    # Create Axionaut car with default settings
    axionaut = Axionaut()

    # Configure PDW control commands as default
    axionaut.commands = get_commands(path=None, default=True)

    # Training mode started with Transfer Learning
    if (args.tl == True):

        # Load self-driving pre-trained model
        model, graph = load_model('autopilot.hdf5')

        # Freeze all convolutional layers
        for layer in model.layers:
          layer.trainable = False

        # Training routine
        print('Training routine started with transfer learning. Press Crtl + C to exit.')

        history = axionaut.train(model, graph, transfer_learning=True, 
                                 epochs=args.epochs, 
                                 batch_size=args.batch_size,
                                 optimizer=args.optimizer)

        utils.plot_train_loss(history)

        print('trained finished. Best model saved')

    else:
        if args.arch == 'ConvNets':

            # Create a new ConvNet model from library
            model =  architectures.ConvNets()

            # Train model
            history = model.train(model, graph, transfer_learning=True, 
                                  epochs=args.epochs, 
                                  batch_size=args.batch_size,
                                  optimizer=args.optimizer)

            utils.plot_train_loss(history)

            print('trained finished. Best model saved')

        else:

            # Create a new ConvNet model from library
            model =  architectures.ConvNets()

            # Train model
            history = model.train(model, graph, transfer_learning=True, 
                                  epochs=args.epochs, 
                                  batch_size=args.batch_size,
                                  optimizer=args.optimizer)

            print('Architecture ConvLSTM')

else:
    print('Vehicle started in Record model')

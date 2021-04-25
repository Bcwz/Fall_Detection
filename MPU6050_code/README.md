## Requirements
main.py has a few dependencies such as Tensorflow, Keras, smbus and ThingsBoard. Recommend looking up installation guides on those. You may need to use an older version of Keras due to some compatibility issues with the latest version.

## Running the program
Run main.py to start the program. Ensure that RPi is connected to same network as ThingsBoard and buzzer RPi. Else there might be error.

## Generating a C library for register reads
The library has already been generated and placed within the folder, but in the instance where it gets misplaced or corrupted, just run a make command while in this folder.
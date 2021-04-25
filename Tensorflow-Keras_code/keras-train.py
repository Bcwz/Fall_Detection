import pandas as pd
import tensorflow as tf

""" Directory for training and output data"""
Input_CSV_Dir = "dataset.csv"      # Points to location of CSV Data
Output_Model_Dir = "testmodel.h5"   # Points to location of trained Output Model

""" Load Dataset """
csvfile = pd.read_csv(Input_CSV_Dir)    # Load csv data using panda dataframe
target = csvfile.pop("target")          # Extract 'target' column in the CSV File. It contains expected answer, used in training.

""" Link expected result in training with the target, then shuffle them """
dataset = tf.data.Dataset.from_tensor_slices((csvfile.values, target.values))
train_dataset = dataset.shuffle(len(csvfile)).batch(1)

""" The diffferent setup_FCN() will setup the Fully Connected Layer """
""" setup_FCN_24x24() will be used in the project. The others are for accuracy testing & comparison purpose only """
""" Each methods will setup the layers differently more information will be commented in the methods """

def setup_FCN_12x12():

    # Swquential Model is used.
    model = tf.keras.Sequential()

    # Consist of 4 Layers of nodes.
    # First layer consist of 6 nodes, to receive 6 inputs
    # Second layer consist of 12 nodes.
    # Third layer consist of  12 nodes.
    # Last Layer consist of 1 node, to output either 0 or 1
    # We are using binary_crossentropy as the loss function, hence the last layer is setup that way.

    model.add(tf.keras.layers.Dense(6, input_shape=(None, 6), activation='relu'))
    model.add(tf.keras.layers.Dense(12, activation='relu'))
    model.add(tf.keras.layers.Dense(12, activation='relu'))
    model.add(tf.keras.layers.Dense(1, activation='sigmoid'))

    # Compile the model using binary_crossentropy.
    model.compile(optimizer='adam',
                 loss='binary_crossentropy',
                 metrics=['accuracy'])

    # return the model after compilation
    return model

def setup_FCN_12():

    # Swquential Model is used.
    model = tf.keras.Sequential()

    # Consist of 4 Layers of nodes.
    # First layer consist of 6 nodes, to receive 6 inputs
    # Second layer consist of 12 nodes.
    # Last Layer consist of 1 node, to output either 0 or 1
    # We are using binary_crossentropy as the loss function, hence the last layer is setup that way.

    model.add(tf.keras.layers.Dense(6, input_shape=(None, 6), activation='relu'))
    model.add(tf.keras.layers.Dense(12, activation='relu'))
    model.add(tf.keras.layers.Dense(1, activation='sigmoid'))

    # Compile the model using binary_crossentropy.
    model.compile(optimizer='adam',
                 loss='binary_crossentropy',
                 metrics=['accuracy'])

    # return the model after compilation
    return model

def setup_FCN_24():

    # Swquential Model is used.
    model = tf.keras.Sequential()

    # Consist of 4 Layers of nodes.
    # First layer consist of 6 nodes, to receive 6 inputs
    # Second layer consist of 12 nodes.
    # Last Layer consist of 1 node, to output either 0 or 1
    # We are using binary_crossentropy as the loss function, hence the last layer is setup that way.

    model.add(tf.keras.layers.Dense(6, input_shape=(None, 6), activation='relu'))
    model.add(tf.keras.layers.Dense(24, activation='relu'))
    model.add(tf.keras.layers.Dense(1, activation='sigmoid'))

    # Compile the model using binary_crossentropy.
    model.compile(optimizer='adam',
                 loss='binary_crossentropy',
                 metrics=['accuracy'])

    # return the model after compilation
    return model

def setup_FCN_24x24():

    # Swquential Model is used.
    model = tf.keras.Sequential()

    # Consist of 4 Layers of nodes.
    # First layer consist of 6 nodes, to receive 6 inputs
    # Second layer consist of 12 nodes.
    # Last Layer consist of 1 node, to output either 0 or 1
    # We are using binary_crossentropy as the loss function, hence the last layer is setup that way.

    model.add(tf.keras.layers.Dense(6, input_shape=(None, 6), activation='relu'))
    model.add(tf.keras.layers.Dense(24, activation='relu'))
    model.add(tf.keras.layers.Dense(24, activation='relu'))
    model.add(tf.keras.layers.Dense(1, activation='sigmoid'))

    # Compile the model using binary_crossentropy.
    model.compile(optimizer='adam',
                 loss='binary_crossentropy',
                 metrics=['accuracy'])

    # return the model after compilation
    return model

""" Creating, training, and saving the model"""

# Create and setting up the model using setup_FCN_24x24()
model = setup_FCN_24x24()

# Use model.fit to train it. As we have a very large dataset, we do not have to train it multiple times.
model.fit(train_dataset, epochs=3)

# After training is completed, save the model in h5 format.
model.save(Output_Model_Dir, save_format='h5')

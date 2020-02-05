import csv
import tensorflow as tf
import numpy as np
from ai.utils import read_csv

labelCount = 3

class NeuralNetwork:
    def __init__(self, featureCount, labelCount = 3):
        self.model = tf.keras.Sequential([
            tf.keras.layers.Dense(64, activation='relu', input_shape=(featureCount,)),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(labelCount, activation='softmax')]
        )

        self.model.compile(optimizer='sgd',
                    loss='categorical_crossentropy',
                    metrics=['accuracy'])


    def fitToCsv(self, filePath, epochs):
        matrix, columns = read_csv(filePath)

        labels = matrix[:, -labelCount:]
        features = matrix[:, :-labelCount]

        self.model.fit(features, labels, epochs=epochs, batch_size=32)

    def evaluate(self, features):
        predictions = self.model.predict([features])

        value = predictions[0, 0] + predictions[0, 2]/2
        valueNormalized = value*2 - 1.0 # converts from [0.0, 1.0] to [-1.0, 1.0]

        return valueNormalized

    @staticmethod
    def load():
        pass
from ai.neural_network import NeuralNetwork
from ai.feature_extractor import FeatureExtractor
import os

class SmartEvaluator:
    predictionMemory = dict()

    def __init__(self, epochs):
        self.filePath = os.getcwd() + "/ai/games.csv"
        self.neuralNetwork = NeuralNetwork(8)
        self.neuralNetwork.fitToCsv(self.filePath, epochs)

    def evaluateBoard(self, gameManager):
        featureExtractor = FeatureExtractor(gameManager)
        features = featureExtractor.getFeatures()
        
        if str(features) in SmartEvaluator.predictionMemory:
            value = SmartEvaluator.predictionMemory[str(features)]
        else:
            value = self.neuralNetwork.evaluate(features)
            SmartEvaluator.predictionMemory[str(features)] = value

        return value
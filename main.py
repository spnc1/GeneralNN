import csv, random, time, os, math
from itertools import starmap
from operator import mul

# if os.name == 'nt': os.system('cls')
# elif os.name == 'posix': os.system('clear')

data = []
answers = []

def readCsv(filepath: str, targetArray: list, answersTargetArray: list):
    """
    Takes a file path of training data and saves it to 2 arrays, a data and an answers array.
    IGNORES HEADERS AND MUST BE FLOATS

    Paramaters
    ----------
    filepath            : File path of training/testing data to be read
    targetArray         : Name of arrray for training/testing data
    answersTargetArray  : Name of array for training/testing data answers
    """

    with open(filepath, mode="r") as csv_file:
        reader = csv.reader(csv_file)

        # skips header
        next(reader)

        # QUOTE_NONNUMERIC converts all non-quoted elements to floats
        reader = csv.reader(csv_file, quoting=csv.QUOTE_NONNUMERIC)

        for item in reader:
            targetArray.append(item[1:])
            answersTargetArray.append(item[0])

def oneHot(number, listLength): return [0 if i != number else 1 for i in range(listLength)]

def dotProduct(arrayA, arrayB): return sum(starmap(mul,zip(arrayA,arrayB)))

class Layer():
    """
    A class to represent a hidden or output layer of a neural network

    Attributes
    ----------
    nInputs             : The amount of neurons in the previous layer (Size of input layer)
    nNeurons            : The amount of Neurons in the current layer (Size of this layer)
    weights             : The weight matrix
    biases              : The bias vector
    output              : The layer output

    Methods
    -------
    forwardPropagation  : Takes an input layer and an activation function choice and saves the output to self.output
    """

    def __init__(self, nInputs: int, nNeurons: int):

        # Generate a matrix of weights with nInputs width and nNeurons height
        weights = [[0.025*random.uniform(-0.5,0.5) for x in range(nInputs)] for y in range(nNeurons)]
        
        # Generate a vector of biases with length nNeurons
        biases = [random.uniform(-0.5,0.5) for i in range(nNeurons)]

        # Make them accessible by the class object
        self.nInputs = nInputs
        self.nNeurons = nNeurons
        self.weights = weights
        self.biases = biases
    
    def forwardPropagation(self, inputs: list[float]):
        """
        Method for forward propagation of the neural network at the current layer

        Parameters
        ----------
        inputs              : The input layer

        Outputs
        --------
        self.output         : The vector output of the layer, accessible with self.output
        """
        
        # Must test if list comprehension is faster
        
        output = []
        for n in range(self.nNeurons):
            outputBatch = 0
            for value, weight in zip(inputs, self.weights[n]): outputBatch += value * weight
            output.append(outputBatch + self.biases[n])
        
        self.output = output

class activationLayer():
    def __init__(self, inputArray: list[float], activationFunction: str = ''):
        activationFunction = activationFunction.lower()
        
        if activationFunction == '':
            self.output = inputArray
            return

        if activationFunction == 'relu':
            self.output = [i if i > 0 else 0 for i in inputArray]
            return

        elif activationFunction == 'leaky relu':
            self.output = [i if i > 0 else 0.01*i for i in inputArray]
            return

        elif activationFunction == 'logistic sigmoid':
            self.output = [1/(1+math.exp(i)) for i in inputArray]
            return

        elif activationFunction == 'softmax':
            allSummed = sum(inputArray)
            self.output = [i/allSummed for i in inputArray]
            return

# XOR gate truth table
truthTable = [
    [0,0,0],
    [0,1,1],
    [1,0,1],
    [1,1,0]
]

data = [scenario[0:2] for scenario in truthTable]
answers = [scenario[2] for scenario in truthTable]

print('Truth Table')
for scenario in truthTable: print(scenario)
print()

# For understanding back propagation
for i in range(1):

    # 1 pass through
    inputLayer = data[i]
    expectedOutputLayer = answers[i]

    h1 = Layer(len(inputLayer), 2)
    h1.forwardPropagation(inputLayer)
    z1 = activationLayer(h1.output, 'ReLU')

    outputLayer = Layer(len(z1.output), 2)
    outputLayer.forwardPropagation(z1.output)
    output = activationLayer(outputLayer.output, 'Softmax')

    answer = oneHot(expectedOutputLayer, 2)

    print(f'Output: {output.output}, Expected Answer: {answer}\n')

    # Calculate Cost
    cost = 0
    for n, output in enumerate(output.output):
        cost += (output - answer[n]) ** 2
    
    print(f'Cost: {cost}')

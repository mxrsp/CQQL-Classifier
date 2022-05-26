import itertools
import util as ut

class CQQL_Classifier:

    @staticmethod
    def classify(data, minterms, activeMinterms, threshold):
        # number of correctly classified classes
        correctlyPredictedClasses = 0
        predictedClasses = 0

        # object is evaluated over all minterms
        for i in range(len(data) - 1):
            objectClass = 0
            sumDisjunctions = 0
            for index, activeMinterm in enumerate(activeMinterms):
                if activeMinterm == 1:
                    minterm = minterms[index]
                else:
                    continue
                prod = 1
                for j in range(len(data[i]) - 1):
                    if minterm[j] == 1:
                        prod *= data[i][j]
                    elif minterm[j] == 0:
                        prod *= 1 - data[i][j]
                    else:
                        continue
                sumDisjunctions += prod

            predictedClasses += 1
            if sumDisjunctions > threshold:
                objectClass = 1
            if data[i][len(data[i]) - 1] == objectClass:
                correctlyPredictedClasses += 1

        accuracy = correctlyPredictedClasses / predictedClasses
        return accuracy

    @staticmethod
    def findThreshold(self, validationData, minterms, activeMinterms):

        # split data for calculations
        splitData = ut.Util.splitClasses(validationData)
        positiveData = splitData[0]
        negativeData = splitData[1]

        threshold = 0

        # find max value of negative training data und min value of positive training data
        maxNegative = 0
        minPositive = 1

        for i in range(len(positiveData) - 1):
            sumOfDNF = 0
            for index, activeMinterm in enumerate(activeMinterms):
                if activeMinterm == 1:
                    minterm = minterms[index]
                else:
                    continue
                prodOfMinterm = 1
                for j in range(len(positiveData[i]) - 1):
                    prodOfMinterm *= positiveData[i][j] if minterm[j] == 1 else (1 - positiveData[i][j])
                sumOfDNF += prodOfMinterm
            minPositive = sumOfDNF if sumOfDNF < minPositive else minPositive

        for i in range(len(negativeData) - 1):
            sumOfDNF = 0
            for index, activeMinterm in enumerate(activeMinterms):
                if activeMinterm == 1:
                    minterm = minterms[index]
                else:
                    continue
                prodOfMinterm = 1
                for j in range(len(negativeData[i]) - 1):
                    prodOfMinterm *= negativeData[i][j] if minterm[j] == 1 else (1 - negativeData[i][j])
                sumOfDNF += prodOfMinterm
            maxNegative = sumOfDNF if sumOfDNF > maxNegative else maxNegative

        # check if maximum value < minimum value(happens if objects are well seperated)
        if maxNegative < minPositive:
            threshold = (maxNegative + minPositive) / 2
        # else we need to maximize the discrete accuracy
        # we have to find the threshold value from the interval [minPositive, maxNegative]
        # this can be evaluated against a validation set
        else:
            # set initial values
            diff = 1

            lowerBoundary = min(minPositive, maxNegative)
            upperBoundary = max(minPositive, maxNegative)
            middlePoint = (lowerBoundary + upperBoundary) / 2

            lower = middlePoint - 0.00000001
            upper = middlePoint + 0.00000001

            # stop loop as soon as the accuracy doesn't fluctuate more than 0.01 anymore
            while diff > 0.01:
                accLower = CQQL_Classifier.classify(validationData, minterms, activeMinterms, lower)
                accUpper = CQQL_Classifier.classify(validationData, minterms, activeMinterms, upper)

                # calculate difference between both accuracies
                diff = abs(accLower - accUpper)

                # set the better threshold
                # create the new intervals
                if accLower > accUpper:

                    threshold = lower

                    # set new upper limit as the other one isn't needed anymore
                    # also set new lower and upper
                    middlePoint = (lower + middlePoint) / 2
                    lower = middlePoint - 0.001
                    upper = middlePoint + 0.001

                elif accUpper > accLower:
                    threshold = upper

                    # set new upper limit as the other one isn't needed anymore
                    # also set new lower and upper
                    middlePoint = (middlePoint + upper) / 2
                    lower = middlePoint - 0.001
                    upper = middlePoint + 0.001
                elif diff < 0.01:
                    threshold = max(lower, upper)
            return threshold
        return threshold

    # create all minterms
    @staticmethod
    def createMinterms(size: int):
        minterms = list(itertools.product([0, 1], repeat=size - 1))
        return minterms

    # extract all minterms that fullfill the condition that leads to class 1
    def extractMinterms(self, trainingData, minterms, theta_p_threshold):

        # split data for calculations
        splitData = ut.Util.splitClasses(trainingData)
        positiveData = splitData[0]
        negativeData = splitData[1]

        numberOfClassOne = len(positiveData)
        numberOfClassZero = len(negativeData)

        # active/inactive minterm list
        activeList = []

        # iterate over every minterm to decide if it should be removed
        for minterm in minterms:

            sumPos = 0
            sumNeg = 0

            # sum all products of each object where class is 1
            for i in range(len(positiveData) - 1):
                prod = 1
                for j in range(len(positiveData[i]) - 1):
                    prod *= positiveData[i][j] if minterm[j] == 1 else (1 - positiveData[i][j])
                sumPos += prod

            # sum all products of each object where class is 0
            for i in range(len(negativeData) - 1):
                prod = 1
                for j in range(len(negativeData[i - 1]) - 1):
                    prod *= negativeData[i][j] if minterm[j] == 1 else (1 - negativeData[i][j])
                sumNeg += prod

            gamma = numberOfClassZero / (numberOfClassOne + numberOfClassZero)
            lambdA = 0.5

            # check if the classes are evenly distributed
            if gamma == 1 / 2:
                # if the sum of positive training data is greater than negative training data:
                # remove the minterm from the list as it is unneeded
                if sumPos > sumNeg:
                    activeList.append(1)
                else:
                    activeList.append(0)
            # if unevenly distributed, chose this
            else:
                # lambda value chosen arbitrarly
                stability_threshold = (gamma * lambdA * sumPos) / (
                        gamma * lambdA * sumPos + (1 - gamma) * (1 - lambdA) * sumNeg)
                if stability_threshold > theta_p_threshold:
                    activeList.append(1)
                else:
                    activeList.append(0)
        return activeList
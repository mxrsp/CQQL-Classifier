import util as ut
import cqqlCFL
# example usage
class main:

    # loading data
         # data, col_names = loadDataset()
         # data = ut.normalizeDataset(data)
         # data = shuffle(data)

     # prepare testdata, trainingdata and validation data
         # splitIndex = int((len(data) * 0.70))
         # trainingData = data[:splitIndex]
         # testData = data[splitIndex:]
         # restData = data[splitIndex:]
         # splitIndex = int((len(restData) * 2 / 3))
         # testData = restData[splitIndex:]
         # validationData = restData[:splitIndex]

    # CQQL Classifier
         # cqqlCFL = cqqlCFL.CQQL_Classifier()

    # create all possibile minterms
        # minterms = cqqlCFL.createMinterms(data[0].shape[0])

    # bestActive = []
    # bestAcc = 0
    # theta_p
    # extract minterms
    # try each theta value
        # for theta_p_threshold in np.arange(0, 1, 0.05):

            # activeMinterms = cqqlCFL.extractMinterms(trainingData, minterms, theta_p_threshold)
            # acc = cqqlCFL.classify(trainingData,
            #                      minterms, activeMinterms, cqqlCFL.findThreshold(trainingData, minterms, activeMinterms)
            # if acc > bestAcc:
            #   bestActive = activeMinterms
            #   theta_p = theta_p_threshold

    # classify
    # cqqlCFL.classify(testData, minterms, bestActive, theta_p)
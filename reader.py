import pickle

data = pickle.load(open("rex-reed.pickle", "rb"))
data2 = pickle.load(open("anthony-lane.pickle", "rb"))
dataSet = set(data)
data2Set = set(data2)

for item in dataSet.intersection(data2Set):
    score1 = data[item].split("/")
    score1 = float(score1[0]) / float(score1[1])

    score2 = data2[item].split("/")
    score2 = float(score2[0]) / float(score2[1])
    print(item + ": " + str(100*round(score1+score2, 2)) + "%")

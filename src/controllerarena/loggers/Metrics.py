class Metrics(object):
    def __init__(self):
        fid = open('log.csv', 'r')
        lines = fid.readlines()
        self.data = map(lambda x: map(lambda y: float(y), x[:-1].split(',')), lines)
        fid.close()

    def totalTime(self):
        return self.data[len(self.data)-1][0]

m = Metrics()
print m.totalTime()

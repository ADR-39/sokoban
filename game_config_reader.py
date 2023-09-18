
class GameConfigReader:

    def __init__(self, instream):
        self.instream = instream

    def normal_read(self):
        inlist = self.instream.readlines()
        self.data = {
            'size': self.make_complex_from_str(inlist[0], singular=True),
            'blocks': self.make_complex_from_str(inlist[1]),
            'boxes': self.make_complex_from_str(inlist[2]),
            'targets': self.make_complex_from_str(inlist[3]),
             'weights': self.make_weights(inlist[5]),
            'figure': self.make_complex_from_str(inlist[4], singular=True),
        }

    @staticmethod
    def make_complex_from_str(instr, singular=False):
        tokens = instr.split()
        res = []

        for first, sec in zip(tokens[::2], tokens[1::2]):
            pair = int(first), int(sec)
            res.append(pair)

        return res if not singular else res[0]

    @staticmethod
    def make_weights(instr):
        tokens = instr.split()
        res = []

        for first, sec, trd in zip(tokens[::3], tokens[1::3], tokens[2::3]):
            pair = int(first), int(sec)
            weight = int(trd)
            res.append((pair, weight))

        return res


    def tolist(self):
        return list(self.data.values())

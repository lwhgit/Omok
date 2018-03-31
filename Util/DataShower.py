
class DataShower:

    @staticmethod
    def showArray(arr):
        s = ""
        for y in range(0, len(arr[0])):
            for x in range(0, len(arr)):
                s += str("{0:>4d}".format(arr[x][y]))
            s += "\n\n"
        print(s)
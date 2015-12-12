__author__ = 'ava-katushka'

class ImageMetrics:
    big_size = 30
    small_size = 5
    num = big_size / small_size

    @classmethod
    def normalization_func(cls, a, b):
        prop = float(a) / (a + b)
        return 4 * (prop**2) - 4 * prop + 1


    @classmethod
    def construct_description(cl, vector):
        result = [0] * (cl.num ** 2)
        for x,y in vector:
            col = (x - 1) / cl.small_size
            str = (y - 1) / cl.small_size
            i = str * cl.num + col
            result[i] += 1
        return result

    @classmethod
    def count_dist(cl, v1, v2):
        dist = 0
        for x, y in zip(v1, v2):
            dist += cl.normalization_func(x, y) ** 2
        return dist ** (0.5)






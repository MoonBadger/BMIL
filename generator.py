import random as rnd


class Generator:
    __LAT_DOWN_LEFT = 97
    __LAT_DOWN_RIGHT = 123
    __LAT_UP_LEFT = 65
    __LAT_UP_RIGHT = 91
    __NUM_LEFT = 48
    __NUM_RIGHT = 58
    __SYMB_LEFT_1 = 33
    __SYMB_RIGHT_1 = 48
    __SYMB_LEFT_2 = 58
    __SYMB_RIGHT_2 = 65
    __SYMB_LEFT_3 = 91
    __SYMB_RIGHT_3 = 97

    __LIMIT = 100

    def __init__(self):
        self.__s_arr = list(range(self.__LAT_DOWN_LEFT, self.__LAT_DOWN_RIGHT))
        self.__s_arr += range(self.__LAT_UP_LEFT, self.__LAT_UP_RIGHT)
        self.__s_arr += range(self.__NUM_LEFT, self.__NUM_RIGHT)
        self.__s_arr += range(self.__SYMB_LEFT_1, self.__SYMB_RIGHT_1)
        self.__s_arr += range(self.__SYMB_LEFT_2, self.__SYMB_RIGHT_2)
        self.__s_arr += range(self.__SYMB_LEFT_3, self.__SYMB_RIGHT_3)
        self.__max_len = len(self.__s_arr)

    def max_len(self):
        return self.__max_len

    def limit(self):
        return self.__LIMIT

    def __generate_symb(self, alph_len):
        x = rnd.randint(0, alph_len)
        return chr(self.__s_arr[x])

    def generate_pass(self, pass_len, alph_len):
        password = ''
        for i in range(pass_len):
            password += self.__generate_symb(alph_len)
        return password



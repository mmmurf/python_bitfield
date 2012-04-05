import array

class BitField(object):
    
    def __init__(self):
        
        self.array = array.array('I')
        self.initializer = 0
        self.shift = 3
        self.mask = 0x7
 

    def __count_bits(self, n):
        count = 0
        while n:
            count += 1
            n &= (n - 1)
        return count

    def count(self):
        count = 0
        for x in range(0, len(self.array)):
            count += self.__count_bits(self.array[x])
        return count

    def hb(self, n):
        return self.__highest_bit(n)

    def __highest_bit(self, n):
        count = 0
        while n != 1:
            n = n>>1
            count += 1
            
        return count
        

    def max(self):
        x = len(self.array) -1
        while x >= 0:
            val = self.array[x]
            if val != 0:
                return self.__highest_bit(val) + (x * 2**self.shift)
            x -= 1
        return 0
            

    def __array(self):
        return self.array

    def __reverse(self):
        self.initializer = 7

    def __get_index(self, i):
        return (i>>self.shift)

    def set(self, i):
        self.__prefill(self.__get_index(i))
        self.array[self.__get_index(i)] |= (1 << (i&self.mask))

    def unset(self, i):
        if len(self.array) == 0:
            pass
        elif len(self.array) <= (self.__get_index(i)):
            pass
        else:
            self.array[self.__get_index(i)] ^= (1 << (i&self.mask)) # uses xor=

    def get(self, i):
        if len(self.array) == 0:
            return False
        elif len(self.array)-1 < (self.__get_index(i)):
            return False
        else:
            return (self.array[self.__get_index(i)] & (1 << (i&self.mask))) != 0
        
    def __prefill(self, i):
        while len(self.array) <= i:
            self.array.fromlist([self.initializer] * 10)

    
    # returns a paginated list of bits that are set
    def indexes_by_page(self, page=1, per_page=10, starting_index=0):

        def items_in_array_index(k):
            items = []
            for i in range(0,8):
                if (k & (1 << (i&self.mask))) != 0:
                    items.append(i)
            return items

        items = []
        for x in range(self.__get_index(starting_index), len(self.array)):
            if self.array[x] != 0:
                indexes = items_in_array_index(self.array[x])
                positioned = [(x * 8) + i for i in indexes]
                positioned = filter(lambda x: x > starting_index, positioned)
                items.extend(positioned)
        #OPTIMIZE: this will keep searching after enough have been found
        return items[(page * per_page)-per_page:page * per_page]
        
      

    def fromstring(self, value):
        self.array.fromstring(value)

    def __str__(self):
        return self.tostring()

    def tostring(self):
        return self.array.tostring()


    #FIXME:  this is not really done properly... should be false if one is bigger, for example
    def __eq__(self, other):
        smaller = min(len(self.__array()), len(other.__array())) 
        for i in range(0, smaller):
            if self.__array()[i] !=  other.__array()[i]:
                return False
        return True

    def __compareeacharray(self, other, fcompare, fminmax):
        b = BitField()
        # deepcopy is used here to prevent unnecessarily growing arrays... in some cases the growth
        # is just for a comparison and can be discarded after the comparison returns

        s = copy.deepcopy(self)
        o = copy.deepcopy(other)

        while len(s.__array()) < len(o.__array()):
            s.__array().fromlist([self.initializer] * 100)

        while len(o.__array()) < len(s.__array()):
            o.__array().fromlist([self.initializer] * 100)


        
        for i in range(0, len(s.__array())):
            b.__array().append( fcompare(s.__array()[i], o.__array()[i]))
        return b


    def __xor__(self, other):
        return self.__compareeacharray(other, long.__xor__, max)

    def __or__(self, other):
        return self.__compareeacharray(other, long.__or__, max)
    
    def __and__(self, other):
        return self.__compareeacharray(other, long.__and__, max)

    def __compareeach(self, other, fcompare, fminmax):
        b = BitField()
        dominant = fminmax(self.max(), other.max()) 
        for i in range(0, dominant+1):
            s = self.get(i)
            o = other.get(i)
            fcompare(s, o, b, i)
        return b

   


 
    # item by item invert, ... tbd what to do... probably a custom method that takes two args... the
    # bitfield and the size to invert it for ?
    def __invert__(self):
        b = BitField()
        for i in range(0, self.max()):
            if not self.get(i): b.set(i)

        return b

    def __iadd__(self, other):
        b = (self | other)
        
        self.array = b.__array()
        return self

    def __isub__(self, other):
        b = (self ^ other) & self 
        
        self.array = b.__array()
        return self

    def tobitstring(self, length=20):
        out = ""
        for x in range(0, length):
            if self.get(x):
                out += "1"
            else:
                out += "0"
        return out

    def copy(self):
        c = BitField()
        c += self
        return c

        




def test():
    b1 = BitField()

    assert b1.get(33) == False
    assert b1.get(523424) == False

    print "tests finished"


if __name__ == "__main__":    
    test()
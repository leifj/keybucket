__author__ = 'leifj'

class BaseConverter(object):
    decimal_digits = "0123456789"

    def __init__(self, digits):
        self.digits = digits

    def from_decimal(self, i):
        return self.convert(i, self.decimal_digits, self.digits)

    def to_decimal(self, s):
        return int(self.convert(s, self.digits, self.decimal_digits))

    def convert(number, fromdigits, todigits):
        # Based on http://code.activestate.com/recipes/111286/
        if str(number)[0] == '-':
            number = str(number)[1:]
            neg = 1
        else:
            neg = 0

        # make an integer out of the number
        x = 0
        for digit in str(number):
           x = x * len(fromdigits) + fromdigits.index(digit)

        # create the result in base 'len(todigits)'
        if x == 0:
            res = todigits[0]
        else:
            res = ""
            while x > 0:
                digit = x % len(todigits)
                res = todigits[digit] + res
                x = int(x / len(todigits))
            if neg:
                res = '-' + res
        return res
    convert = staticmethod(convert)

id_encoder = BaseConverter("23456789abcdefghijkmnprstuvwABCDEFGHIJKMNOPRSTUVW")

consonant = 'bdfghjklmnprstvz'
vowel = 'aiou'
MASK_FIRST4 = 0xF0000000
MASK_FIRST2 = 0xC0000000

def uint2quint(i):
    """
    convert an unsigned int to a proquint
    """
    q = ''

    j = i & MASK_FIRST4
    i <<= 4
    j >>= 28
    q += consonant[j]
    j = i & MASK_FIRST2
    i <<= 2
    j >>= 30
    q += vowel[j]
    j = i & MASK_FIRST4
    i <<= 4
    j >>= 28
    q += consonant[j]
    j = i & MASK_FIRST2
    i <<= 2
    j >>= 30
    q += vowel[j]
    j = i & MASK_FIRST4
    i <<= 4
    j >>= 28
    q += consonant[j]

    q += '-'

    j = i & MASK_FIRST4
    i <<= 4
    j >>= 28
    q += consonant[j]
    j = i & MASK_FIRST2
    i <<= 2
    j >>= 30
    q += vowel[j]
    j = i & MASK_FIRST4
    i <<= 4
    j >>= 28
    q += consonant[j]
    j = i & MASK_FIRST2
    i <<= 2
    j >>= 30
    q += vowel[j]
    j = i & MASK_FIRST4
    i <<= 4
    j >>= 28
    q += consonant[j]

    return q
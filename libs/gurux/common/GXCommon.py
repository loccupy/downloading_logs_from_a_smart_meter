import sys

###Python 2 requires this
#pylint: disable=bad-option-value,old-style-class
class GXCommon:
    #pylint: disable=too-few-public-methods
    """General methods for communication."""

    __NIBBLE = 4
    __HEX_ARRAY = "0123456789ABCDEFGH"
    __LOW_BYTE_PART = 0x0F

    def __init__(self, data=None, senderInfo=None):
        """
        Constructor.
        """

    @classmethod
    def getVersion(cls):
        """Get version."""
        return sys.version_info

    @classmethod
    def toHex(cls, value):
        """Convert data to hex."""
        #Return empty string if array is empty.
        if not value:
            return ""
        hexChars = ""
        #Python 2.7 handles bytes as a string array. It's changed to bytearray.
        if sys.version_info < (3, 0) and not isinstance(value, bytearray):
            value = bytearray(value)
        for it in value:
            hexChars += GXCommon.__HEX_ARRAY[it >> GXCommon.__NIBBLE]
            hexChars += GXCommon.__HEX_ARRAY[it & GXCommon.__LOW_BYTE_PART]
            hexChars += ' '
        return hexChars

    #Convert char hex value to byte value.
    @classmethod
    def ___getValue(cls, c):
        #Id char.
        if c.islower():
            c = c.upper()
        pos = GXCommon.__HEX_ARRAY.find(c)
        if pos == -1:
            raise Exception("Invalid hex string")
        return pos

    @classmethod
    def hexToBytes(cls, value):
        """Convert string to byte array."""
        buff = bytearray()
        lastValue = -1
        for ch in value:
            if ch != ' ':
                if lastValue == -1:
                    lastValue = cls.___getValue(ch)
                elif lastValue != -1:
                    buff.append(lastValue << GXCommon.__NIBBLE | cls.___getValue(ch))
                    lastValue = -1
            elif lastValue != -1:
                buff.append(cls.___getValue(ch))
                lastValue = -1
        return buff

import ctypes

def main():
     string_lib = ctypes.cdll.LoadLibrary('/home/pi/Desktop/pioneer600/getTime.so')
     string_lib.get_string.restype = ctypes.c_char_p
     myString = string_lib.get_string()
     print(myString)

main()

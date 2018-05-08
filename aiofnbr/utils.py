from urllib.parse import quote_plus

def bounds(value,min,max):
    if value < min:
        value = min
    elif value > max:
        value = max
    return value

def uriencode(string):
    if type(string) is int:
        string = str(string)
    return quote_plus(bytes(string,"utf-8"))

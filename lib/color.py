class Color:

    def __init__(self, red, green, blue):
        self.red   = red if 0 <= red < 256 else 0 if red < 0 else 255
        self.green = green if 0 <= green < 256 else 0 if green < 0 else 255
        self.blue  = blue if 0 <= blue < 256 else 0 if blue < 0 else 255

    def __getitem__(self, arg):
        if (arg == 'red' or arg == 0):
            return self.red 
        if (arg == 'green' or arg == 1):
            return self.green 
        if (arg == 'blue' or arg == 2):
            return self.blue
        raise IndexError

import math

# Self-made 2d vector class
class Vec:
    def __init__(self, x, y):
        #Ensure that x and y are both integers. If not, set this to the zero vector and print an error
        if isinstance(x, (int, float)) and isinstance(y, (int, float)):
            self.x = x
            self.y = y
        else:
            print("Vector given non-number values")
            self.x = 0
            self.y = 0

        

    # Operator overload for +. This also overloads +=
    def __add__(self, other):
        return Vec(self.x + other.x, self.y + other.y)

    # Operator overload for -. This also overloads -=
    def __sub__(self, other):
        return Vec(self.x - other.x, self.y - other.y)

    # Operator overload for *
    def __mul__(self, scale):
        return Vec(self.x*scale, self.y*scale)

    # Operator overload for /
    def __truediv__(self, scale):
        return Vec(self.x/scale, self.y/scale)

    # Method to divide x and y of this vec by x and y of the other vec
    def divide_by_vec(self, other):
        return Vec(self.x/other.x, self.y/other.y)

    def multiply_vec(self, other):
        return Vec(self.x*other.x, self.y*other.y)
    
    # Returns magnitude of self
    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)

    # Calling this is faster than vec.magnitude()**2, because there is no wasted call to sqrt
    def magnitude2(self):
        return self.x**2 + self.y**2

    # Prints out x and y values
    def write(self):
        print(self.x, self.y)

    # Turns the vec into a tuple (useful for pygame)
    def to_tuple(self):
       return (self.x, self.y)

    def from_tuple(tup):
        if isinstance(tup, tuple) and len(tup) == 2:
            return Vec(tup[0], tup[1])

        else:
            print("Input not a tuple or invalid length")
            return Vec(0,0)

    # Converts each coordinate into an int
    def int_cast(self):
        return Vec(int(self.x), int(self.y))

    #Return a copy of self
    def copy(self):
        return Vec(self.x, self.y)


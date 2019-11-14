
from math import sin, cos, sqrt, atan2, radians


class Point(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __sub__(self, other):
        R = 6373.0
        lat1 = radians(self.x)
        lat2 = radians(other.x)
        lon1 = radians(self.y)
        lon2 = radians(other.y)
        dlat = abs(lat2 - lat1)
        dlon = abs(lon2 - lon1)
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c
        print("Result:", round(distance * 1000), " metr")
        print("Should be:", 278.546, "km")
        return distance*1000


def user_location(lat,lng):
    user_loc = Point(lat,lng)
    return user_loc

def meal_location(lat,lng):
    meal_loc = Point(lat, lng)
    return meal_loc

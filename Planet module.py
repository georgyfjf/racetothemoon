import math

# Constants
G = 6.67408 * 10 ** (-11)


def vect_sum(r1, ang1, r2, ang2):
    x1 = r1 * math.cos(ang1)
    y1 = r1 * math.sin(ang1)
    x2 = r2 * math.cos(ang2)
    y2 = r2 * math.sin(ang2)
    x, y = x1 + x2, y1 + y2
    r = math.sqrt(x ** 2 + y ** 2)
    if x > 0:
        if y >= 0:
            ang = math.atan(y / x)
        if y < 0:
            ang = math.atan(y / x) + 2 * math.pi
    if x < 0:
        ang = math.atan(y / x) + math.pi
    if x == 0:
        if y > 0:
            ang = math.pi / 2
        if y < 0:
            ang = 3 / 2 * math.pi
        if y == 0:
            ang = None
    return tuple([r, ang])


class Planet:

    def __init__(self, r, ang, m, R, v):
        '''
        :param r: first coordinate
        :param ang: second coordinate
        :param m: mass
        :param R: radius
        :param v: angular velocity
        '''
        self.m = m
        self.r0 = (r, ang)
        self.radius = R
        self.v = v

    def coord(self, t):  # Returns current coordinate
        if self.r0[1] is not None:
            return tuple([self.r0[0], self.r0[1] + (t * self.v) % (2 * math.pi)])
        else:
            return self.r0

    def dist_surf(self, r, ang, t):  # Returns distance to the surface
        r1 = self.coord(t)
        if self.r0[1] is not None:
            print(vect_sum(r, ang, r1[0], (r1[1] + math.pi) % (2 * math.pi)))
            return vect_sum(r, ang, r1[0], (r1[1] + math.pi) % (2 * math.pi))[0] - self.radius
        else:
            return r - self.radius

    def gravity(self, r, ang, t):  # Returns g, angle to the center of the planet
        a, b = self.coord(t)
        R = self.dist_surf(r, ang, t) + self.radius
        if self.r0[1] is not None:
            return tuple([(G * self.m) / R ** 2, vect_sum(r, (ang + math.pi) % (2 * math.pi), a, b)[1]])
        else:
            return tuple([(G * self.m) / R ** 2, (ang + math.pi) % (2 * math.pi)])

    def atm_pres(self):  # coming soon
        pass


Earth = Planet(0, None, 5.9726 * 10 ** 24, 6371000, 0)
Moon = Planet(384467000, 0, 7.3477 * 10 ** 22, 1737100, 2 * math.pi / (27 * 24 * 60 * 60))






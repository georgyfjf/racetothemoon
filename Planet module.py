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

    def __init__(self, r, ang, m, R, v, w, atm):
        '''
        :param r: first coordinate
        :param ang: second coordinate
        :param m: mass
        :param R: radius
        :param v: angular orbital velocity
        :param w: angular velocity
        :param atm: existence of atmosphere
        '''
        self.m = m
        self.r0 = (r, ang)
        self.radius = R
        self.v = v
        self.w = w
        self.atm = atm

    def coord(self, t):  # Returns current coordinate
        if self.r0[1] is not None:
            return tuple([self.r0[0], self.r0[1] + (t * self.v) % (2 * math.pi)])
        else:
            return self.r0

    def dist_surf(self, r, ang, t):  # Returns distance to the surface
        r1 = self.coord(t)
        if self.r0[1] is not None:
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

    def atm_pres(self, V, r, ang):
        if self.atm:
            h = self.dist_surf(r, ang, 0)
            if 0 < h <= 11000:
                Ps = 101325 * (1 - h / 44331)**5.255876
                D = 1.225 * (1 - h / 44331)**4.255876
            elif 11000 < h <= 20000:
                Ps = 101325 * 0.223361 * 10**(-(h-11000)/6375000)
                D = 1.225 * 0.297076 * 10**(-(h-11000)/6375000)
            elif 20000 < h <= 32000:
                Ps = 101325 * (0.988626 + h / 198912)**(-34.16320)
                D = 1.225 * (0.978261 + h / 201020)**(-35.16320)
            elif 32000 < h <= 47000:
                Ps = 101325 * (0.898309 + h / 55282)**(-12.20114)
                D = 1.225 * (0.857003 + h / 57947)**(-13.20114)
            elif 47000 < h <= 51000:
                Ps = 101325 * 0.00109456 * 10**(-(h-47000)/7922)
                D = 1.225 * 0.00116533 * 10**(-(h-47000)/7922)
            elif 51000 < h <= 71000:
                Ps = 101325 * (0.838263 - h / 176150)**12.20114
                D = 1.225 * (0.798990 - h / 184809)**11.20114
            elif h > 71000:
                Ps = 0
                D = 0
            Pd = D * V**2
            P = Ps + Pd
            return (P)
        else:
            return 0


Earth = Planet(0, None, 5.9726 * 10 ** 24, 6371000, 0, 7.292 * 10**(-5), True)
Moon = Planet(384467000, 0, 7.3477 * 10 ** 22, 1737100, 2 * math.pi / (27 * 24 * 60 * 60), 0, False)





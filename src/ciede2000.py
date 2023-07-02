import math
import numpy as np

def rgb_to_ciede2000(rgb1, rgb2):
    def _convert_rgb_to_lab(rgb):
        # sRGBをXYZに変換
        r = rgb[0] / 255.0
        g = rgb[1] / 255.0
        b = rgb[2] / 255.0

        r = _rgb_to_xyz_helper(r)
        g = _rgb_to_xyz_helper(g)
        b = _rgb_to_xyz_helper(b)

        # XYZをLabに変換
        x = r * 0.4124564 + g * 0.3575761 + b * 0.1804375
        y = r * 0.2126729 + g * 0.7151522 + b * 0.0721750
        z = r * 0.0193339 + g * 0.1191920 + b * 0.9503041

        x /= 0.95047
        y /= 1.0
        z /= 1.08883

        x = _lab_helper(x)
        y = _lab_helper(y)
        z = _lab_helper(z)

        l = max(0.0, min(100.0, y * 116.0 - 16.0))
        a = max(-128.0, min(127.0, (x - y) * 500.0))
        b = max(-128.0, min(127.0, (y - z) * 200.0))

        return l, a, b

    def _rgb_to_xyz_helper(value):
        if value > 0.04045:
            value = math.pow((value + 0.055) / 1.055, 2.4)
        else:
            value /= 12.92
        return value

    def _lab_helper(value):
        if value > 0.008856:
            value = math.pow(value, 1.0 / 3.0)
        else:
            value = (value * 903.3 + 16.0) / 116.0
        return value

    def _delta_e_ciede2000(lab1, lab2):
        l1, a1, b1 = lab1
        l2, a2, b2 = lab2

        c1 = math.sqrt(a1 * a1 + b1 * b1)
        c2 = math.sqrt(a2 * a2 + b2 * b2)
        cm = (c1 + c2) / 2.0

        g = 0.5 * (1 - math.sqrt(math.pow(cm, 7) / (math.pow(cm, 7) + math.pow(25.0, 7))))

        a1p = a1 * (1 + g)
        a2p = a2 * (1 + g)

        c1p = math.sqrt(a1p * a1p + b1 * b1)
        c2p = math.sqrt(a2p * a2p + b2 * b2)

        h1p = math.atan2(b1, a1p) % (2.0 * math.pi)
        h2p = math.atan2(b2, a2p) % (2.0 * math.pi)

        if math.fabs(h1p - h2p) > math.pi:
            h2p += 2.0 * math.pi

        hp = (h1p + h2p) / 2.0

        if c1 * c2 == 0:
            dp = 0
        else:
            dp = (h2p - h1p + 2.0 * math.pi) % (2.0 * math.pi) - math.pi

        dl = l2 - l1
        dc = c2p - c1p
        dh = 2.0 * math.sqrt(c1p * c2p) * math.sin(dp / 2.0)

        lpm = (l1 + l2) / 2.0
        cpm = (c1p + c2p) / 2.0

        if c1p * c2p == 0:
            dhp = 0
        elif math.fabs(h1p - h2p) <= math.pi:
            dhp = h2p - h1p
        else:
            dhp = (h2p - h1p + 2.0 * math.pi) % (2.0 * math.pi) - math.pi

        dhp = 2.0 * math.sqrt(c1p * c2p) * math.sin(dhp / 2.0)

        t = 1.0 - 0.17 * math.cos(hp - math.pi / 6.0) + 0.24 * math.cos(2.0 * hp) + 0.32 * math.cos(3.0 * hp + math.pi / 30.0) - 0.20 * math.cos(4.0 * hp - 21.0 * math.pi / 60.0)

        sl = 1.0 + (0.015 * math.pow(lpm - 50.0, 2.0)) / math.sqrt(20.0 + math.pow(lpm - 50.0, 2.0))
        sc = 1.0 + 0.045 * cpm
        sh = 1.0 + 0.015 * cpm * t

        dt = 30.0 * math.exp(-math.pow((hp - 275.0) / 25.0, 2.0))
        rc = 2.0 * math.sqrt(math.pow(cpm, 7) / (math.pow(cpm, 7) + math.pow(25.0, 7)))
        rt = -rc * math.sin(2.0 * dt * math.pi / 180.0)

        de = math.sqrt(math.pow(dl / (sl * 1.0), 2.0) + math.pow(dc / (sc * 1.0), 2.0) + math.pow(dh / (sh * 1.0), 2.0) + rt * (dc / (sc * 1.0)) * (dh / (sh * 1.0)))

        return de

    lab1 = _convert_rgb_to_lab(rgb1)
    lab2 = _convert_rgb_to_lab(rgb2)
    delta_e = _delta_e_ciede2000(lab1, lab2)

    return delta_e

def np_rgb_ciede2000(rgb1, rgb2):
        rgb1 = rgb1.tolist()
        rgb2 = rgb2.tolist()
        delta_e = rgb_to_ciede2000(rgb1, rgb2)
        delta_e_array = np.array(delta_e)
        return delta_e_array

def load_array(array, i, j):
    return_array = array[i, j, :]
    return return_array

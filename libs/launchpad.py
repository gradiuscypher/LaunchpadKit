import pypm


def find_launchpads():
    ins = []
    outs = []

    for loop in range(pypm.CountDevices()):
        interf, name, inp, outp, opened = pypm.GetDeviceInfo(loop)

        if name.startswith('Launchpad'):
            if inp:
                ins.append(loop)
            else:
                outs.append(loop)

    return zip(ins, outs)


class LaunchPadError(Exception):
        def __init__(self, value):
                self.value = value

        def __str__(self):
                return repr(self.value)


class Launchpad():

    def __init__(self, id_in, id_out):
        self.midi_in = pypm.Input(id_in)
        self.midi_out = pypm.Output(id_out, 0)
        self.drumrack = False

    def reset(self):
        self.midi_out.WriteShort(0xb0, 0, 0)
        self.drumrack = False

    def test(self, brightness):
        if 1 <= brightness <= 3:
            self.midi_out.WriteShort(0xb0, 0, 124 + brightness)
            self.drumrack = False

    def setDrumRackMode(self, drumrack=True):
        self.drumrack = drumrack
        self.midi_out.WriteShort(0xb0, 0, drumrack and 2 or 1)

    def set_light(self, x, y, red, green):
        if not 0 <= x <= 8:
            raise LaunchPadError("Bad x value %s" % x)
        if not 0 <= y <= 8:
            raise LaunchPadError("Bad y value %s" % y)
        if not 0 <= red <= 3:
            raise LaunchPadError("Bad red value %s" % red)
        if not 0 <= green <= 3:
            raise LaunchPadError("Bad green value %s" % green)

        velocity = 16 * green + red + 8 + 4

        if y == 8:
            if x != 8:
                note = 104 + x
                self.midi_out.WriteShort(0xb0, note, velocity)
            return

        if self.drumrack:
            if x == 8:
                note = 107 - y
            elif x < 4:
                note = 36 + x + 4 * y
            else:
                note = 64 + x + 4 * y
        else:
            note = x + 16 * (7 - y)

        self.midi_out.WriteShort(0x90, note, velocity)

    def set_all(self, levels):
        velocity = 0
        for level in self.order_all(levels):
            red = level[0]
            green = level[1]
            if velocity:
                velocity2 = 16*green + red + 8 + 4
                self.midi_out.WriteShort(0x92, velocity, velocity2)
                velocity = 0
            else:
                velocity = 16*green + red + 8 + 4
        self.set_light(0, 0, levels[0][0][0], levels[0][0][1])

    def order_all(self, levels):
        for y in range(8):
            for x in range(8):
                yield levels[x][7-y]
        x = 8
        for y in range(8):
            yield levels[x][7-y]

        y = 8
        for x in range(8):
            yield levels[x][y]


    def single_light_test(self):
        for x in range(8):
            for y in range(8):
                self.set_light(x, y, x % 4, y % 4)

    def all_light_test(self, r=None, g=None):
        grid = []
        for x in range(9):
            grid.append([])
            for y in range(9):
                if r is None:
                    grid[x].append((x % 4, y % 4))
                else:
                    grid[x].append((r % 4, g % 4))
        self.set_all(grid)
        return grid

    def poll(self):
        if self.midi_in.Poll():
            data = self.midi_in.Read(1)
            [status, note, velocity, extraData] = data[0][0]

            if status == 176:
                y = 8
                x = note - 104

                print x, y

            elif self.drumrack:
                if note > 99:
                    x = 8
                    y = 107 - note
                else:
                    x = note % 4
                    y = (note / 4) - 9

                    if y > 7:
                        x += 4
                        y -= 8

            else:
                x = note % 16
                y = 7 - (note / 16)

                print x, y, velocity == 127
                return x, y, velocity == 127

        return None

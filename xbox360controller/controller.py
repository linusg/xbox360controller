"""A pythonic Xbox 360 controller library for Linux.

Partly inspired by the following libraries/codes:
- https://www.freebasic.net/forum/viewtopic.php?t=18068 (libjoyrumble)
- https://gist.github.com/rdb/8864666
"""

import os
import select
import struct
import sys
import time
from array import array
from collections import namedtuple
from fcntl import ioctl
from glob import glob
from threading import Thread, Event

from xbox360controller.linux.input import *
from xbox360controller.linux.input_event_codes import *
from xbox360controller.linux.joystick import *

LED_PERMISSION_WARNING = """Warning: Permission to the LED sysfs file was denied.
You may run this script as user root or try creating a udev rule containing:

  SUBSYSTEM=="leds", RUN+="/bin/chmod 666 /sys/class/leds/%k/brightness"

E.g. in a file /etc/udev/rules.d/xpad.rules
"""

LED_SUPPORT_WARNING = """Warning: Setting the LED status is not supported for
this gamepad or its driver.
"""

BUTTON_NAMES = {
    BTN_A: "BTN_A",
    BTN_B: "BTN_B",
    BTN_X: "BTN_X",
    BTN_Y: "BTN_Y",
    BTN_TL: "BTN_TL",
    BTN_TR: "BTN_TR",
    BTN_SELECT: "BTN_SELECT",
    BTN_START: "BTN_START",
    BTN_MODE: "BTN_MODE",
    BTN_THUMBL: "BTN_THUMBL",
    BTN_THUMBR: "BTN_THUMBR",
}

AXIS_NAMES = {
    ABS_X: "ABS_X",
    ABS_Y: "ABS_Y",
    ABS_Z: "ABS_Z",
    ABS_RX: "ABS_RX",
    ABS_RY: "ABS_RY",
    ABS_RZ: "ABS_RZ",
    ABS_HAT0X: "ABS_HAT0X",
    ABS_HAT0Y: "ABS_HAT0Y",
}

ControllerEvent = namedtuple("Event", ["time", "type", "number", "value", "is_init"])


def _get_uptime():
    with open("/proc/uptime", "r") as f:
        uptime_seconds = float(f.readline().split()[0])
        return uptime_seconds


BOOT_TIME = time.time() - _get_uptime()


class RawAxis:
    def __init__(self, name):
        self.name = name
        self._value = 0
        self.when_moved = None

    def __repr__(self):
        return "<xbox360controller.{cls} ({name})>".format(
            cls=self.__class__.__name__, name=self.name
        )

    @property
    def value(self):
        return self._value

    def run_callback(self):
        if self.when_moved is not None and callable(self.when_moved):
            self.when_moved(self)


class Axis:
    def __init__(self, name):
        self.name = name
        self._value_x = 0
        self._value_y = 0
        self.when_moved = None

    def __repr__(self):
        return "<xbox360controller.{cls} ({name})>".format(
            cls=self.__class__.__name__, name=self.name
        )

    @property
    def x(self):
        return self._value_x

    @property
    def y(self):
        return self._value_y

    def run_callback(self):
        if self.when_moved is not None and callable(self.when_moved):
            self.when_moved(self)


class Button:
    def __init__(self, name):
        self.name = name
        self._value = False
        self.when_pressed = None
        self.when_released = None

    def __repr__(self):
        return "<xbox360controller.{cls} ({name})>".format(
            cls=self.__class__.__name__, name=self.name
        )

    @property
    def is_pressed(self):
        return bool(self._value)


class Xbox360Controller:
    # https://github.com/paroj/xpad/blob/a6790a42800661d6bd658e9ba2215c0dc9bb2a44/xpad.c#L1355
    LED_OFF = 0
    LED_BLINK = 1
    LED_TOP_LEFT_BLINK_ON = 2
    LED_TOP_RIGHT_BLINK_ON = 3
    LED_BOTTOM_LEFT_BLINK_ON = 4
    LED_BOTTOM_RIGHT_BLINK_ON = 5
    LED_TOP_LEFT_ON = 6
    LED_TOP_RIGHT_ON = 7
    LED_BOTTOM_LEFT_ON = 8
    LED_BOTTOM_RIGHT_ON = 9
    LED_ROTATE = 10
    LED_BLINK_PREV = 11
    LED_BLINK_SLOW_PREV = 12
    LED_ROTATE_TWO = 13
    LED_BLINK_SLOW = 14
    LED_BLINK_ONCE_PREV = 15

    @classmethod
    def get_available(cls):
        return [cls(index) for index in range(len(glob("/dev/input/js*")))]

    def __init__(self, index=0, axis_threshold=0.2, raw_mode=False):
        self.index = index
        self.axis_threshold = axis_threshold
        self.raw_mode = raw_mode
        self._ff_id = -1

        try:
            self._dev_file = open(self._get_dev_file(), "rb")
        except FileNotFoundError:
            raise Exception(
                "controller device with index {index} "
                "was not found!".format(index=index)
            )

        self._event_file = open(self._get_event_file(), "wb")

        def _led_error(msg):
            sys.stderr.write(msg)
            sys.stderr.flush()
            time.sleep(0.1)
            self._led_file = None

        try:
            self._led_file = open(self._get_led_file(), "w")
        except PermissionError:
            _led_error(LED_PERMISSION_WARNING)
        except FileNotFoundError:
            _led_error(LED_SUPPORT_WARNING)

        if raw_mode:
            self.axes = self._get_axes()
            self.buttons = self._get_buttons()
        else:
            self.axis_l = Axis("axis_l")
            self.axis_r = Axis("axis_r")
            self.hat = Axis("hat")
            self.trigger_l = RawAxis("trigger_l")
            self.trigger_r = RawAxis("trigger_r")
            self.axes = [
                self.axis_l,
                self.axis_r,
                self.hat,
                self.trigger_l,
                self.trigger_r,
            ]

            self.button_a = Button("button_a")
            self.button_b = Button("button_b")
            self.button_x = Button("button_x")
            self.button_y = Button("button_y")
            self.button_trigger_l = Button("button_trigger_l")
            self.button_trigger_r = Button("button_trigger_r")
            self.button_select = Button("button_select")
            self.button_start = Button("button_start")
            self.button_mode = Button("button_mode")
            self.button_thumb_l = Button("button_thumb_l")
            self.button_thumb_r = Button("button_thumb_r")
            self.buttons = [
                self.button_a,
                self.button_b,
                self.button_x,
                self.button_y,
                self.button_trigger_l,
                self.button_trigger_r,
                self.button_select,
                self.button_start,
                self.button_mode,
                self.button_thumb_l,
                self.button_thumb_r,
            ]

        self._event_thread_stopped = Event()
        self._event_thread = Thread(target=self._event_loop)
        self._event_thread.start()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def _get_dev_file(self):
        return "/dev/input/js{idx}".format(idx=self.index)

    def _get_event_file(self):
        event_file_sysfs = glob(
            "/sys/class/input/js{idx}/device/event*".format(idx=self.index)
        )[0]
        event_number = int(os.path.basename(event_file_sysfs).replace("event", ""))
        return "/dev/input/event{number}".format(number=event_number)

    def _get_led_file(self):
        return "/sys/class/leds/xpad{idx}/brightness".format(idx=self.index)

    def _get_axes(self):
        axes = []
        buf = array("B", [0] * 64)
        ioctl(self._dev_file, JSIOCGAXMAP, buf)
        for axis in buf[: self.num_axes]:
            name = AXIS_NAMES.get(axis)
            if name is not None:
                name = name.lower()
                setattr(self, name, RawAxis(name))
                axes.append(getattr(self, name))
        return axes

    def _get_buttons(self):
        buttons = []
        buf = array("H", [0] * 200)
        ioctl(self._dev_file, JSIOCGBTNMAP, buf)
        for button in buf[: self.num_buttons]:
            name = BUTTON_NAMES.get(button)
            if name is not None:
                name = name.lower()
                setattr(self, name, Button(name))
                buttons.append(getattr(self, name))
        return buttons

    def _event_loop(self):
        while not self._event_thread_stopped.is_set():
            event = self.get_event()
            if event is not None and not event.is_init:
                self.process_event(event)
            time.sleep(0.001)

    def get_event(self):
        try:
            r, w, e = select.select([self._dev_file], [], [], 0)
            if self._dev_file in r:
                buf = self._dev_file.read(8)
            else:
                return
        except ValueError:
            # File closed in main thread
            return
        else:
            if buf:
                time_, value, type_, number = struct.unpack("IhBB", buf)
                time_ = round(BOOT_TIME + (time_ / 1000), 4)
                is_init = bool(type_ & JS_EVENT_INIT)
                return ControllerEvent(
                    time=time_, type=type_, number=number, value=value, is_init=is_init
                )

    def axis_callback(self, axis, val):
        if (
                axis.when_moved is not None
                and abs(val) > self.axis_threshold
                and callable(axis.when_moved)
            ):
                axis.when_moved(axis)

    def process_event(self, event):
        if event.type == JS_EVENT_BUTTON:

            if event.number >= 11 and event.number <= 14:
                if event.number == 11:
                    self.hat._value_x = -int(event.value)
                    val = self.hat._value_x
                if event.number == 12:
                    self.hat._value_x = int(event.value)
                    val = self.hat._value_x
                if event.number == 13:
                    self.hat._value_y = int(event.value)
                    val = self.hat._value_y
                if event.number == 14:
                    self.hat._value_y = -int(event.value)
                    val = self.hat._value_y

                self.axis_callback(self.hat, val)

            try:
                button = self.buttons[event.number]
            except IndexError:
                return
            else:
                button._value = event.value

                if (
                    button._value
                    and button.when_pressed is not None
                    and callable(button.when_pressed)
                ):
                    button.when_pressed(button)

                if (
                    not button._value
                    and button.when_released is not None
                    and callable(button.when_released)
                ):
                    button.when_released(button)

        if event.type == JS_EVENT_AXIS:
            if self.raw_mode:
                try:
                    axis = self.axes[event.number]
                except IndexError:
                    return
                else:
                    val = event.value / 32767
                    axis._value = val

            else:
                num = event.number
                val = event.value / 32767

                if num == 0:
                    self.axis_l._value_x = val
                if num == 1:
                    self.axis_l._value_y = val
                if num == 2:
                    self.trigger_l._value = (val + 1) / 2
                if num == 3:
                    self.axis_r._value_x = val
                if num == 4:
                    self.axis_r._value_y = val
                if num == 5:
                    self.trigger_r._value = (val + 1) / 2
                if num == 6:
                    self.hat._value_x = int(val)
                if num == 7:
                    self.hat._value_y = int(val * -1)

                axis = [
                    self.axis_l,
                    self.axis_l,
                    self.trigger_l,
                    self.axis_r,
                    self.axis_r,
                    self.trigger_r,
                    self.hat,
                    self.hat,
                ][num]

            self.axis_callback(axis, val)

    @property
    def driver_version(self):
        buf = array("i", [0])
        ioctl(self._dev_file, JSIOCGVERSION, buf)
        version_dev = struct.unpack("i", buf.tobytes())[0]
        version_dev = (version_dev >> 16, (version_dev >> 8) & 0xFF, version_dev & 0xFF)

        buf = array("i", [0])
        ioctl(self._event_file, EVIOCGVERSION, buf)
        version_ev = struct.unpack("i", buf.tobytes())[0]
        version_ev = (version_ev >> 16, (version_ev >> 8) & 0xFF, version_ev & 0xFF)

        return version_dev, version_ev

    @property
    def num_axes(self):
        if self.raw_mode:
            buf = array("B", [0] * 64)
            ioctl(self._dev_file, JSIOCGAXES, buf)
            return int(buf[0])
        else:
            return len(self.axes)

    @property
    def num_buttons(self):
        if self.raw_mode:
            buf = array("B", [0])
            ioctl(self._dev_file, JSIOCGBUTTONS, buf)
            return int(buf[0])
        else:
            return len(self.buttons)

    @property
    def name(self):
        buf = array("B", [0] * 64)
        ioctl(self._dev_file, JSIOCGNAME(len(buf)), buf)
        return buf.tostring().decode()

    def info(self):
        print("{0} at index {1}".format(self.name, self.index))
        print("Axes: {0}".format(self.num_axes))
        for axis in self.axes:
            print("\t{}".format(axis.name))
        print("Buttons: {0}".format(self.num_buttons))
        for button in self.buttons:
            print("\t{}".format(button.name))
        print("Rumble: {0}".format("yes" if self.has_rumble else "no"))
        print(
            "Driver version: {0}".format(
                " ".join("{}.{}.{}".format(*ver) for ver in self.driver_version)
            )
        )

    @property
    def has_rumble(self):
        buf = array("L", [0] * 4)
        has_ff = EVIOCGBIT(EV_FF, struct.calcsize("L") * len(buf))
        if ioctl(self._event_file, has_ff, buf) == -1:
            return False
        if (buf[1] >> FF_RUMBLE % (struct.calcsize("l") * 8)) & 1:
            return True
        return False

    def set_rumble(self, left, right, duration=1000):
        if not self.has_rumble:
            raise RuntimeError("this device doesn't support rumbling")

        if not (1 >= left >= 0 and 1 >= right >= 0):
            raise ValueError("left and right must be in range 0-1")

        if duration <= 0:
            raise ValueError("duration must be greater than 0")

        left_abs = int(left * 65535)
        right_abs = int(right * 65535)

        stop = input_event(EV_FF, self._ff_id, 0)
        if self._event_file.write(stop) == -1:
            return False
        self._event_file.flush()

        effect = ff_effect(FF_RUMBLE, -1, duration, 0, left_abs, right_abs)
        try:
            buf = ioctl(self._event_file, EVIOCSFF, effect)
        except OSError:
            # Heavy usage yields a
            # [Errno 28] No space left on device
            # Simply reset and continue rumbling :)
            self._ff_id = -1
            self._event_file.close()
            self._event_file = open(self._get_event_file(), "wb")
            return self.set_rumble(left, right, duration)

        self._ff_id = int.from_bytes(buf[1:3], "big")

        play = input_event(EV_FF, self._ff_id, 1)
        if self._event_file.write(play) == -1:
            return False
        self._event_file.flush()

        return True

    @property
    def has_led(self):
        return self._led_file is not None

    def set_led(self, status):
        if not self.has_led:
            raise RuntimeError("setting the LED status is not supported")

        if 0 > status > 15:
            raise ValueError("status must be in range 0-15")

        self._led_file.write(str(status))
        self._led_file.flush()

    def close(self):
        self._dev_file.close()
        self._event_file.close()
        if self._led_file is not None:
            self._led_file.close()

        self._event_thread_stopped.set()
        self._event_thread.join()

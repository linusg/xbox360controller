# xbox360controller
> A pythonic Xbox360 controller API built on top of the xpad Linux kernel driver.

[![PyPI Version][pypi-image]][pypi-url] [![Build Status][travis-image]][travis-url] [![Code Health][landscape-image]][landscape-url]

This Python Package aims to provide a pythonic and complete API for your Xbox360 and similar game controllers.
Currently it's built on top of the Linux kernel driver `xpad` so you can use it on almost any Linux distribution including your Rasperry Pi projects etc.

The following features are supported:

- Registering callbacks for **all** Buttons, Axes, Triggers and Hat in a `gpiozero`-inspired way
- Setting the LED circle; all `xpad` provided options are possible: blinking, rotating, setting individual LEDs on and off, ...
- Rumbling, both the left and right side can be controlled from 0 to 100 percent

## Installation

You will most likely need Python 3.4 or above.

Any Linux distribution:

```
pip3 install -U xbox360controller
```

You might also use a _virtual environment_, or do a per-user install by providing the `--user` flag to above command.
Global installations might require the usage of `sudo` or working directly from a root shell but are **not recommended**.

If the `pip3` command cannot be found, try `pip` or make sure to have pip installed properly:

```
sudo apt-get install python3-pip
```

## Usage

### Basics

```python
import signal
from xbox360controller import Xbox360Controller


def on_button_pressed(button):
    print('Button {0} was pressed'.format(button.name))


def on_button_released(button):
    print('Button {0} was released'.format(button.name))


def on_axis_moved(axis):
    print('Axis {0} moved to {1} {2}'.format(axis.name, axis.x, axis.y))

try:
    with Xbox360Controller(0, axis_threshold=0.2) as controller:
        # Button A events
        controller.button_a.when_pressed = on_button_pressed
        controller.button_a.when_released = on_button_released

        # Left and right axis move event
        controller.axis_l.when_moved = on_axis_moved
        controller.axis_r.when_moved = on_axis_moved

        signal.pause()
except KeyboardInterrupt:
    pass
```

The above code will run until `Ctrl+C` is pressed. Each time on of the left or right axis is moved, the event will be processed. Additionally, the events of the A button are being processed.
Please note, there seems to be a bug left that the KeyboardInterrupt will not show up directly when raised, but when the next controller event is registered. In case the program hangs on `Ctrl+C`, just press or move any of the controller's buttons or axes.

### `Xbox360Controller` parameters

The [`Xbox360Controller`](https://github.com/linusg/xbox360controller/blob/master/xbox360controller/controller.py#L131) classes constructor takes [a few parameters](https://github.com/linusg/xbox360controller/blob/master/xbox360controller/controller.py#L158):

- `index`: the index of the controller to use. If you have connected two controllers connected, the first one would be `0`, the second on `1` and so on. Defaults to `0` (obviously).
- `axis_threshold`: minimum value of an axis for its event to be triggered. This is useful to not get a flood of useless events with ridiculously small values even if the axis is at `(0, 0)`. Applies to all axes and triggers. Defaults to `0.2`.
- `raw_mode`: This tells the controller class to nod use a hardcoded set of axes, buttons, triggers and the hat expected for a regular Xbox360 controller but to use the `xpad` detection features. This allows support for basically every joystick or game controller supported by `xpad`, but is badly documented and currently very limited.
  Will probably improve the situation soon, though.

### Rumbling

```python
from xbox360controller import Xbox360Controller

with Xbox360Controller() as controller:
    controller.set_rumble(0.5, 0.5, 1000)
```

This will enable rumble on both sides of the controller with each 50% strength for one second (1000ms).

### LED

```python
import time
from xbox360controller import Xbox360Controller

with Xbox360Controller() as controller:
    controller.set_led(Xbox360Controller.LED_ROTATE)
    time.sleep(1)
    controller.set_led(Xbox360Controller.LED_OFF)
```

This will let the LED circle rotate for one second and then turn it off.
Available modes are:

- `LED_OFF`
- `LED_BLINK`
- `LED_TOP_LEFT_BLINK_ON`
- `LED_TOP_RIGHT_BLINK_ON`
- `LED_BOTTOM_LEFT_BLINK_ON`
- `LED_BOTTOM_RIGHT_BLINK_ON`
- `LED_TOP_LEFT_ON`
- `LED_TOP_RIGHT_ON`
- `LED_BOTTOM_LEFT_ON`
- `LED_BOTTOM_RIGHT_ON`
- `LED_ROTATE`
- `LED_BLINK_PREV`
- `LED_BLINK_SLOW_PREV`
- `LED_ROTATE_TWO`
- `LED_BLINK_SLOW`
- `LED_BLINK_ONCE_PREV`

### Available attributes and methods in non-raw mode

`controller` is an instance of `Xbox360Controller` with `raw_mode=False`.

- `Xbox360Controller.get_available()`: return a list of `Xbox360Controller` instances containing each available controller
- `controller.driver_version`: return the driver versions returned by `ioctl` with `JSIOCGVERSION` on the device file and `EVIOCGVERSION` on the event file. TBH, I'm not even sure what these mean :confused:
- `controller.num_axes`: return the total number of axes, triggers and hats
- `controller.num_buttons`: return the total number of buttons
- `controller.name`: return the controller's name as reported by `xpad`
- `controller.has_rumble`: return whether the controller supports rumbling or not
- `controller.has_led`: return whether the program will be able to set the led or not, this might also return `False` because of permission issues. See the LED section below.
- `controller.info()`: print some debug info, collected from the attributes stated above
- `controller.set_rumble(left, right, duration=1000)`: set the left and right rumbling strength for a given duration to the given percentage (`0.0`-`1.0`)
- `controller.set_led(status)`: set the LED circle's status, available are listed above
- `controller.close()`: close all open file objects, recommended for cleanup if not using the `with` statement.

`button` is an instance of `Button` and one of `controller.button_a`, `controller.button_b`, `controller.button_x`, `controller.button_y`, `controller.button_trigger_l`,  `controller.button_trigger_r`, `controller.button_thumb_l`, `controller.button_thumb_r`, `controller.button_select`, `controller.button_start`, `controller.button_mode`.

- `button.when_pressed`: holds callable object to be called when the button is pressed
- `button.when_released`: holds callable object to be called when the button is released
- `button.is_pressed`: holds boolean whether the button is currently pressed or not

`axis` is an instance of `Axis` and one of `controller.axis_l`, `controller.axis_r`, `controller.hat`

- `axis.when_moved`: holds callable object to be called when the axis is moved
- `axis.x`: holds the X value of the axis
- `axis.y`: holds the Y value of the axis

The axis values will be one of `1`, `0` or `-1`; from top to bottom or right to left.

`axis` is an instance of `RawAxis` and one of `controller.trigger_l`, `controller.trigger_r`

- `axis.when_moved`: holds callable object to be called when the axis is moved
- `axis.value`: holds the value of the axis

Advised to being used for internal stuff only, until properly documented:

- `controller.get_event()`: return the most recent controller event as a `ControllerEvent`
- `controller.process_event(event)`: process a `ControllerEvent` and update the controller's input device instances

### Debug information

```python
from xbox360controller import Xbox360Controller

with Xbox360Controller() as controller:
    controller.info()
```

## Development/contributing

This project is still in its early days and I really appreciate all kinds of contributions - may it be new or improved code, documentation or just a simple typo fix.
Just provide me a PR and I'll be happy to include your work!

For feature requests, general questions or problems you face regarding this package please [open an issue](https://github.com/linusg/xbox360controller/issues/new).

## Release History

Please see [`CHANGES.md`](https://github.com/linusg/xbox360controller/blob/master/CHANGES.md) for a complete release history.

## Authors

- Linus Groh ([**@linusg**](https://github.com/linusg/)) – mail@linusgroh.de

## License

All the code and documentation are distributed under the MIT license. See [`LICENSE`](https://github.com/linusg/xbox360controller/blob/master/LICENSE) for more information.

[pypi-image]: https://img.shields.io/pypi/v/xbox360controller.svg?style=flat-square
[pypi-url]: https://pypi.org/project/xbox360controller/
[travis-image]: https://img.shields.io/travis/linusg/xbox360controller/master.svg?style=flat-square
[travis-url]: https://travis-ci.org/linusg/xbox360controller
[landscape-image]: https://landscape.io/github/linusg/xbox360controller/master/landscape.svg?style=flat-square
[landscape-url]: https://landscape.io/github/linusg/xbox360controller


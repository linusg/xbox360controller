# xbox360controller
> A pythonic Xbox360 controller API built on top of the `xpad` Linux kernel driver.

[![PyPI Version][pypi-image]][pypi-url] [![Build Status][travis-image]][travis-url] [![Code Health][landscape-image]][landscape-url]

This Python Package aims to provide a pythonic and complete API for your Xbox360 and similar game controllers.
Currently it's built on top of the Linux kernel driver `xpad` so you can use it on almost any Linux distribution including your Rasperry Pi projects etc.

The following features are supported:

- Registering callbacks for **all** Buttons, Axes, Triggers and Hat in a `gpiozero`-inspired way
- Setting the LED circle; all `xpad` provided options are possible: blinking, rotating, setting individual LEDs on and off, ...
- Rumbling, both the left and right side can be controlled from 0 to 100 percent

## Installation

You will need Python 3.4 or above.

Any Linux distribution:

```
pip3 install -U xbox360controller
```

You might also use a _virtual environment_ or do a per-user install by providing the `--user` flag to above command.
Global installations might require the usage of `sudo` or working directly from a root shell but are **not recommended**.

If the `pip3` command cannot be found, try `pip` or make sure to have pip installed properly:

```
sudo apt install python3-pip
```

Of course you don't need `sudo` when working from a root shell.

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

See the [API reference](https://github.com/linusg/xbox360controller/blob/master/docs/API.md#xbox360controller-parameters) for a more detailed explanation of the `Xbox360Controller` class and how to use all available buttons, axes and the hat.

### Rumbling

```python
import time
from xbox360controller import Xbox360Controller

with Xbox360Controller() as controller:
    controller.set_rumble(0.5, 0.5, 1000)
    time.sleep(1)
```

This will enable rumble on both sides of the controller with each 50% strength for one second (1000ms). Note that the method call is non-blocking, thus we need to manually wait one second for the rumble to finish. You won't need this in a regular use case with `signal.pause()`.

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

See the [API reference](https://github.com/linusg/xbox360controller/blob/master/docs/API.md#led) for all available LED modes.

### Debug information

```python
from xbox360controller import Xbox360Controller

with Xbox360Controller() as controller:
    controller.info()
```

## Development/contributing

This project is now in a somewhat stable state, and I really appreciate all kinds of contributions - may it be new or improved code, documentation or just a simple typo fix.
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


# API

## `Xbox360Controller` parameters

The [`Xbox360Controller`](https://github.com/linusg/xbox360controller/blob/master/xbox360controller/controller.py#L131) classes constructor takes [a few parameters](https://github.com/linusg/xbox360controller/blob/master/xbox360controller/controller.py#L158):

- `index`: the index of the controller to use. If you have connected two controllers connected, the first one would be `0`, the second on `1` and so
  on. Defaults to `0` (obviously).
- `axis_threshold`: minimum value of an axis for its event to be triggered.
  This is useful to not get a flood of useless events with ridiculously small
  values even if the axis is at `(0, 0)`. Applies to all axes and triggers.
  Defaults to `0.2`.
- `raw_mode`: don't use a hardcoded set of axes, buttons, triggers and the hat
  expected for a regular Xbox360 controller but the `xpad` detection features.
  This allows support for basically every joystick or game controller
  supported by `xpad`, but is badly documented and currently very limited. I
  will probably improve the situation soon, though.

## Available attributes and methods in non-raw mode

`controller` is an instance of `Xbox360Controller` with `raw_mode=False`.

- `Xbox360Controller.get_available()`: return a list of `Xbox360Controller`
  instances containing each available controller
- `controller.driver_version`: return the driver versions returned by `ioctl`
  with `JSIOCGVERSION` on the device file and `EVIOCGVERSION` on the event
  file. TBH, I'm not even sure what these mean :confused:
- `controller.num_axes`: return the total number of axes, triggers and hats
- `controller.num_buttons`: return the total number of buttons
- `controller.name`: return the controller's name as reported by `xpad`
- `controller.has_rumble`: return whether the controller supports rumbling or
  not
- `controller.has_led`: return whether the program will be able to set the led
  or not, this might also return `False` because of permission issues. See the
  LED section below.
- `controller.info()`: print some debug info, collected from the attributes
  stated above
- `controller.set_rumble(left, right, duration=1000)`: set the left and right
  rumbling strength for a given duration to the given percentage (`0.0`-`1.0`)
- `controller.set_led(status)`: set the LED circle's status, available are
  listed above
- `controller.close()`: close all open file objects, recommended for cleanup if
  not using the `with` statement.

`button` is an instance of `Button` and one of `controller.button_a`, `controller.button_b`, `controller.button_x`, `controller.button_y`, `controller.button_trigger_l`,  `controller.button_trigger_r`, `controller.button_thumb_l`, `controller.button_thumb_r`, `controller.button_select`, `controller.button_start`, `controller.button_mode`.

- `button.when_pressed`: holds callable object to be called when the button is
  pressed
- `button.when_released`: holds callable object to be called when the button is
  released
- `button.is_pressed`: holds boolean whether the button is currently pressed or
  not

`axis` is an instance of `Axis` and one of `controller.axis_l`,
`controller.axis_r`, `controller.hat`

- `axis.when_moved`: holds callable object to be called when the axis is moved
- `axis.x`: holds the X value of the axis
- `axis.y`: holds the Y value of the axis

The axis values will be one of `1`, `0` or `-1`; from top to bottom or right to
left.

`axis` is an instance of `RawAxis` and one of `controller.trigger_l`,
`controller.trigger_r`

- `axis.when_moved`: holds callable object to be called when the axis is moved
- `axis.value`: holds the value of the axis

Advised to being used for internal stuff only, until properly documented:

- `controller.get_event()`: return the most recent controller event as a
  `ControllerEvent`
- `controller.process_event(event)`: process a `ControllerEvent` and update the
  controller's input device instances

## Rumbling

```python
from xbox360controller import Xbox360Controller

with Xbox360Controller() as controller:
    controller.set_rumble(0.5, 0.5, 1000)
    time.sleep(0.5)
```

This will enable rumble on both sides of the controller with each 50% strength
for one second (1000ms). The method call is non blocking, so in this example
we need to wait 0.5 more seconds until the script can exit, otherwise the
rumbling would not be noticed. In a more advanced use case with a loop you will
not need the sleep.

## LED

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

## Debug information

```python
from xbox360controller import Xbox360Controller

with Xbox360Controller() as controller:
    controller.info()
```

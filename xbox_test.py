from xbox360controller import Xbox360Controller
import signal


def on_button_pressed(button):
    print(f'Button {button} was pressed')


def on_button_released(button):
    print(f'Button {button.name} was released')


def on_axis_moved(axis):
    try:
        print(f'Axis {axis.name} moved to {axis.x} {axis.y}')
    except (AttributeError,):
        print(f'Axis {axis.name} moved to {axis.value}')


if __name__ == '__main__':
    try:
        with Xbox360Controller(0, axis_threshold=0.2) as controller:
            # Button events
            for button in controller.buttons:
                button.when_pressed = on_button_pressed
                button.when_released = on_button_released
            # Axes events
            for axis in controller.axes:
                axis.when_moved = on_axis_moved
            # controller.trigger_l.when_moved = on_axis_moved
            # controller.trigger_r.when_moved = on_axis_moved

            signal.pause()
    except KeyboardInterrupt:
        exit()

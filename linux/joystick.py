from xbox360controller.linux.input_event_codes import ABS_CNT, BTN_MISC, KEY_MAX
from xbox360controller.linux.ioctl import _IOR, _IOC, _IOC_READ, _IOW
from xbox360controller.linux.types import __u8, __u16, __u32

# https://github.com/torvalds/linux/blob/master/include/uapi/linux/joystick.h#L44
JS_EVENT_BUTTON = 0x01
JS_EVENT_AXIS = 0x02
JS_EVENT_INIT = 0x80

# JSIOCGAXES = 0x80016a11
# JSIOCGBUTTONS = 0x80016a12
# JSIOCGNAME = 0x80006a13
# JSIOCGAXMAP = 0x80406a32
# JSIOCGBTNMAP = 0x80406a34

# https://github.com/torvalds/linux/blob/master/include/uapi/linux/joystick.h#L61

# get driver version
JSIOCGVERSION = _IOR('j', 0x01, __u32)

# get number of axes
JSIOCGAXES = _IOR('j', 0x11, __u8)

# get number of buttons
JSIOCGBUTTONS = _IOR('j', 0x12, __u8)


# get identifier string
def JSIOCGNAME(len_):
    return _IOC(_IOC_READ, 'j', 0x13, len_)

# set axis mapping
JSIOCSAXMAP = _IOW('j', 0x31, __u8(ABS_CNT))

# get axis mapping
# JSIOCGAXMAP = _IOR('j', 0x32, __u8(ABS_CNT))
JSIOCGAXMAP = 0x80406a32

# set button mapping
JSIOCSBTNMAP = _IOW('j', 0x33, __u16(KEY_MAX - BTN_MISC + 1))

# get button mapping
# JSIOCGBTNMAP = _IOR('j', 0x34, __u16(KEY_MAX - BTN_MISC + 1))
JSIOCGBTNMAP = 0x80406a34

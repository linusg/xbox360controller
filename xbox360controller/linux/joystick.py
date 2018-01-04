from ctypes import c_uint8, c_uint16, c_uint32

from xbox360controller.linux.ioctl import _IOR, _IOC, _IOC_READ, _IOW

# https://github.com/torvalds/linux/blob/master/include/uapi/linux/joystick.h#L44
JS_EVENT_BUTTON = 0x01
JS_EVENT_AXIS = 0x02
JS_EVENT_INIT = 0x80

# https://github.com/torvalds/linux/blob/master/include/uapi/linux/joystick.h#L61

# get driver version
JSIOCGVERSION = _IOR('j', 0x01, c_uint32)

# get number of axes
JSIOCGAXES = _IOR('j', 0x11, c_uint8)

# get number of buttons
JSIOCGBUTTONS = _IOR('j', 0x12, c_uint8)


# get identifier string
def JSIOCGNAME(len_):
    return _IOC(_IOC_READ, 'j', 0x13, len_)

# set axis mapping
JSIOCSAXMAP = _IOW('j', 0x31, c_uint8)

# get axis mapping
# JSIOCGAXMAP = _IOR('j', 0x32, c_uint8)
JSIOCGAXMAP = 0x80406a32

# set button mapping
JSIOCSBTNMAP = _IOW('j', 0x33, c_uint16)

# get button mapping
# JSIOCGBTNMAP = _IOR('j', 0x34, c_uint16)
JSIOCGBTNMAP = 0x80406a34

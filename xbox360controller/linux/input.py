from struct import pack
from ctypes import c_buffer, c_uint32
from xbox360controller.linux.ioctl import _IOR, _IOC_READ, _IOC, _IOW


# https://github.com/torvalds/linux/blob/141e5dcaa7356077028b4cd48ec351a38c70e5e5/include/uapi/linux/input.h#L28-L46
def input_event(type_, code, value, tv_sec=0, tv_usec=0):
    return pack("2l2hi", tv_sec, tv_usec, type_, code, value)


# https://github.com/torvalds/linux/blob/141e5dcaa7356077028b4cd48ec351a38c70e5e5/include/uapi/linux/input.h#L128
EVIOCGVERSION = _IOR("E", 0x01, c_uint32)


# https://github.com/torvalds/linux/blob/141e5dcaa7356077028b4cd48ec351a38c70e5e5/include/uapi/linux/input.h#L174
def EVIOCGBIT(ev, len_):
    return _IOC(_IOC_READ, "E", 0x20 + ev, len_)


# https://github.com/torvalds/linux/blob/141e5dcaa7356077028b4cd48ec351a38c70e5e5/include/uapi/linux/input.h#L178
EVIOCSFF = _IOW("E", 0x80, c_buffer(b"0" * 47))  # 48


# https://github.com/torvalds/linux/blob/141e5dcaa7356077028b4cd48ec351a38c70e5e5/include/uapi/linux/input.h#L426-L463
def ff_effect(
    type_, id_, replay_lenght, replay_delay, strong_magnitude, weak_magnitude
):
    return pack(
        "2h6x2h2x2H28x",
        type_,
        id_,
        replay_lenght,
        replay_delay,
        strong_magnitude,
        weak_magnitude,
    )


# https://github.com/torvalds/linux/blob/141e5dcaa7356077028b4cd48ec351a38c70e5e5/include/uapi/linux/input.h#L469
FF_RUMBLE = 0x50

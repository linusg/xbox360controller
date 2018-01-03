from ctypes import sizeof

# # http://unix.superglobalmegacorp.com/Net2/newsrc/sys/ioctl.h.html
# # parameter length, at most 13 bits
# IOCPARM_MASK = 0x1fff
#
#
# def IOCPARM_LEN(x):
#     return (x >> 16) & IOCPARM_MASK
#
#
# def IOCBASECMD(x):
#     return x & ~IOCPARM_MASK
#
#
# def IOCGROUP(x):
#     return (x >> 8) & 0xff
#
# # max size of ioctl, mult. of NBPG
# IOCPARM_MAX = NBPG
#
# # no parameters
# IOC_VOID = 0x20000000
#
# # copy out parameters
# IOC_OUT = 0x40000000
#
# # copy in parameters
# IOC_IN = 0x80000000
#
# IOC_INOUT = IOC_IN | IOC_OUT
#
# # mask for IN/OUT/VOID
# IOC_DIRMASK = 0xe0000000
# _IOC_READ = 1
#
#
# def _IOC(inout, group, num, len_):
#     return inout | ((len_ & IOCPARM_MASK) << 16) | (ord(group) << 8) | num


# https://www.csie.ntu.edu.tw/~b03902082/codebrowser/pbrt/include/asm-generic/ioctl.h.html
# and
# https://stackoverflow.com/questions/20500947/what-is-the-equivalent-of-the-c-ior-function-in-python
_IOC_NRBITS = 8
_IOC_TYPEBITS = 8
_IOC_SIZEBITS = 14
_IOC_DIRBITS = 2

_IOC_NRSHIFT = 0
_IOC_TYPESHIFT = _IOC_NRSHIFT + _IOC_NRBITS
_IOC_SIZESHIFT = _IOC_TYPESHIFT + _IOC_TYPEBITS
_IOC_DIRSHIFT = _IOC_SIZESHIFT + _IOC_SIZEBITS

_IOC_NONE = 0
_IOC_WRITE = 1
_IOC_READ = 2


def _IOC(direction, type_, nr, size):
    return (direction << _IOC_DIRSHIFT) | (ord(type_) << _IOC_TYPESHIFT) \
        | (nr << _IOC_NRSHIFT) | (size << _IOC_SIZESHIFT)


def _IO(g, n):
    return _IOC(_IOC_NONE, g, n, 0)


def _IOR(g, n, t):
    return _IOC(_IOC_READ, g, n, sizeof(t))


def _IOW(g, n, t):
    return _IOC(_IOC_WRITE, g, n, sizeof(t))


def _IOWR(g, n, t):
    return _IOC(_IOC_READ | _IOC_WRITE, g, n, sizeof(t))

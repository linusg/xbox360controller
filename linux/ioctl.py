from ctypes import sizeof

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

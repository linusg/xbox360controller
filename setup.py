from setuptools import setup
from xbox360controller import __version__

with open('README.rst', 'r') as f:
    long_description = f.read()

setup(
    name='xbox360controller',
    packages=['xbox360controller', 'xbox360controller.linux'],
    version=__version__,
    description='A pythonic Xbox360 controller API built on top of the xpad '
                'Linux kernel driver.',
    long_description=long_description,
    author='Linus Groh',
    author_email='mail@linusgroh.de',
    license='MIT',
    url='https://github.com/linusg/xbox360controller',
    download_url='https://pypi.python.org/pypi/xbox360controller/',
    keywords=['xbox', 'xbox360', 'controller', 'gamepad', 'game',
              'raspberry pi', 'event', 'led', 'rumble'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Games/Entertainment',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System',
        'Topic :: System :: Hardware',
        'Topic :: System :: Hardware :: Hardware Drivers',
        'Topic :: Utilities'
    ],
)

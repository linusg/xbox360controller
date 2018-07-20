from setuptools import setup
from xbox360controller import __version__

try:
    with open('README.md', 'r') as f:
        long_description = f.read()
except (FileNotFoundError, UnicodeDecodeError):
    long_description = ""

setup(
    name='xbox360controller',
    packages=['xbox360controller', 'xbox360controller.linux'],
    version=__version__,
    description='A pythonic Xbox360 controller API built on top of the xpad '
                'Linux kernel driver.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Linus Groh',
    author_email='mail@linusgroh.de',
    license='MIT',
    url='https://github.com/linusg/xbox360controller',
    download_url='https://pypi.org/project/xbox360controller/',
    keywords=['xbox', 'xbox360', 'controller', 'gamepad', 'game',
              'raspberry pi', 'event', 'led', 'rumble'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
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

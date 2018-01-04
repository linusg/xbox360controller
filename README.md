# xbox360controller

[![PyPI Version][pypi-image]][pypi-url] [![Build Status][travis-image]][travis-url] [![Code Health][landscape-image]][landscape-url]

This Python Package aims to provide a pythonic and complete API for your Xbox360 and similar game controllers.
Currently it's built on top of the Linux kernel driver `xpad` so you can use it on almost any Linux distribution including your Rasperry Pi projects etc.

The following features are supported:

- Registering callbacks for **all** Buttons and Axes, Triggers and Hat in a `gpiozero`-inspired way

- Setting the LED circle; all `xpad` provided options are possible: blinking, rotating, setting individual LEDs on and off, ...

- Rumbling, both the left and right side can be controlled from 0 to 100 percent

## Installation

Any Linux distribution:

```
pip3 install -U xbox360controller
```

You might also use a _virtual environment_, or do a per-user install by providing the `--user` flag to above command.
Global installations might require the usage of `sudo` or working directly from a root shell but are **not recommended**.

If the `pip3` command cannot be found, try `pip` or make sure to have pip installed properly:

```
sudo apt-get install python3-pip
```

## Usage


## Development/contributing

This project is still in its early days and I really appreciate all kinds of contributions - may it be new or improved code, documentation or just a simple typo fix.
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


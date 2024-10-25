# Ulauncher Dice Roller

## Features

* Generate random numbers using semi-complex parameters
* Generate numbers using arithmetic (You *could* use this as a simple calculator)
* Set a default value to quickly generate a value without any extra input
* Reroll the number using the same parameters

## Supported parameters

| Symbol | Name           | Description                                          |         |
| :----: | -------------- | ---------------------------------------------------- | ------- |
|  `+`   | Addition       |                                                      | 1d4+2   |
|  `-`   | Subtraction    |                                                      | 1d4-2   |
|  `*`   | Multiplication |                                                      | 1d4*2   |
|  `/`   | Division       |                                                      | 1d4/2   |
|  `()`  | Parentheses    | Logically groups values                              | (1d2)d4 |
|  `kh`  | Keep Highest   | Keeps the highest value from a roll of multiple dice | 2d10kh  |
|  `kl`  | Keep Lowest    | Keeps the lowest value from a roll of multiple dice  | 2d10kl  |

## Credits

* Thanks to [Ulauncher](https://ulauncher.io/) for the extensible launcher.
* Idea and baseline code was influenced from [Laurens256](https://github.com/Laurens256)'s [Ulauncher Random Number Generator](https://github.com/Laurens256/ulauncher-random-number) extension.

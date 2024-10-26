# Ulauncher Dice Roller

Dice rolling extension for [Ulauncher](https://ulauncher.io/).

## Features

* Generate random numbers using semi-complex parameters
* Generate numbers using arithmetic (You *could* use this as a simple calculator)
* Set a default value to quickly generate a value without any extra input
* Reroll the number using the same parameters

## Supported parameters

| Symbol  | Name            | Description                                                 | Example | Output  |
| :-----: | --------------- | ----------------------------------------------------------- | ------- | ------- |
|  `#d#`  | Dice Roll       | Rolls the first value amount of the second value-sided dice | 2d4     | 2-8     |
|  `#dF`  | Fudge Dice ROll | Rolls the first value amount of 3-sided dice offset by -2   | 2dF     | -2-2    |
|   `+`   | Addition        |                                                             | 1d4+2   | 3-6     |
|   `-`   | Subtraction     |                                                             | 1d4-2   | -1-2    |
|   `*`   | Multiplication  |                                                             | 1d4*2   | 2,4,6,8 |
|   `/`   | Division        |                                                             | 1d4/2   | 1-2     |
|  `()`   | Parentheses     | Logically groups values                                     | (1d2)d4 | 1-8     |
|  `kh`   | Keep Highest    | Keeps the highest value from a roll of multiple dice        | 2d10kh  | 1-10    |
|  `kl`   | Keep Lowest     | Keeps the lowest value from a roll of multiple dice         | 2d10kl  | 1-10    |

## Credits

* Idea and base code from [Laurens256](https://github.com/Laurens256)'s [Ulauncher Random Number Generator](https://github.com/Laurens256/ulauncher-random-number) extension.

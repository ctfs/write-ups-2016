# Regex reverse

[![Latest Version](https://img.shields.io/github/release/niklongstone/regex-reverse.svg?style=flat-square)](https://github.com/niklongstone/regex-reverse/releases)
[![Software License](https://img.shields.io/badge/license-MIT-brightgreen.svg?style=flat-square)](LICENSE.md)
[![Build Status](https://img.shields.io/travis/niklongstone/regex-reverse/master.svg?style=flat-square)](https://travis-ci.org/niklongstone/regex-reverse)
[![Coverage Status](https://img.shields.io/scrutinizer/coverage/g/niklongstone/regex-reverse.svg?style=flat-square)](https://scrutinizer-ci.com/g/niklongstone/regex-reverse/code-structure)
[![Quality Score](https://img.shields.io/scrutinizer/g/niklongstone/regex-reverse.svg?style=flat-square)](https://scrutinizer-ci.com/g/niklongstone/regex-reverse)


Regular expression reverter, generates a string from the given regular expression.

## Install

Via [Composer](https://getcomposer.org/download/)

``` bash
$ composer require niklongstone/regex-reverse:'^0.4.0'
```

## Usage

``` php
<?php
require ('regex-reverse/vendor/autoload.php');
use RegRev\RegRev;

echo RegRev::generate('\d'); //ouput a random number
```
For a list of useful regular expression, please visit: [Awesome PCRE](https://github.com/niklongstone/awesome-regular-expression)

## Supported expressions

#### Character classes

| Expression | Description | Result                  |
|------------|-------------|-------------------------|
|    \d      |    digit    |      a number           |
|    \D      |  non digit  |    an alpha char        |
|    \w      |    word     | a alphanumeric char     |
|    \W      |  non word   | a non alphanumeric char |
|    \s      |    space    |    a blank space        |
|    \S      | non space   |    a non blank space    |

#### Conditional and subgroup
| Expression    | Description      | Example   |  Result     |
|---------------|------------------|-----------|-------------|
|    ()         |  subgroup        | (\d\w)+@  | 97a987Ss@   |
|    (a|b)      |  alternation     |  (a|i)nt  |    int      |
|    *          |  zero or more    |   \d*     |  123502     |
|    +          |  one or more     |   \d+     |   32133     |
|    ?          |  zero or one     |   \d?     |     3       |
|{n} {n,} {n,m} |from n to m times | \w{1,3}   |    np       |

#### Ranges
| Expression       | Description      |   Result     |
|------------------|------------------|--------------|
|    [0-9]         |  range 0 to 9    |      7       |
|    [a-d]         |  range a to b    |      b       |
|    [0-9c-f]      | range 0-9 or c-f |      d       |
|    [ab5\.]       | chars in list    |      b       |
|    [^ab5\.]      | chars not in list|      8       |

##Examples

| Expression                     | Result                  | Description
|--------------------------------|-------------------------|------------------------|
| `2\d{2}-\d{3}-\d{4}`           | 212-686-1234            | US phone number        |
| `\(\d{3}\)\s\d{7}`             | (957) 7583632           | phone with area code   |
| `\w+@\w+\.\D{2,3}`             | `yiuh@qwerty.com`       | email                  |
| `www\.\w+\.com`                | `www.h3MEb7k.com`       | URL                    |
| `192\.\d{3}.255.\d{1,3}`       | 192.134.255.4           | Ip address             |
| `\D{3,7}\s\D{2}\s\d{2,5}`      | mslchvi Rr 861          | US address             |
| `<TAG\s.*>.*?<\/TAG>`          |`<TAG fNol>ZPXApG</TAG>` | TAG                    |
| `004[0-9] \d{7,10}`            | 0044 75132145           | europe phone           |
|`SE[1-9]{1}\d{1}\s[A-Z]{2}\d{2}`| SE27 GU35               | london SE post code    |
|`SE[1-9]{1}\d{1}\s[A-Z]{2}\d{2}`| SE27 GU35               | london SE post code    |
| `organi[sz]e`                  | organise or organize    | US or UK spelling      |


## Other features
 - debug: `RegRev::debug()` will return an array of messages

## Contributing

Please see [CONTRIBUTING](CONTRIBUTING.md) for details.

## Credits

- [Nicola Pietroluongo](https://github.com/niklongstone)

## License

The MIT License (MIT). Please see [License File](LICENSE.md) for more information.

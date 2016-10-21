<?php
/**
 * This file is part of the RegexReverse package.
 *
 * (c) Nicola Pietroluongo <nik.longstone@gmail.com>
 *
 * For the full copyright and license information,
 * please view the LICENSE file that was distributed with this source code.
 */

namespace RegRev\Metacharacter\CharType;

use RegRev\Metacharacter\CharacterHandler;

/**
 * Class Unknown,
 * handles character not recognized by the supported expression.
 */
class Unknown extends CharacterHandler
{
    private $string;

    /**
     * {@inheritdoc}
     */
    public function generate()
    {
        return $this->string;
    }

    /**
     * {@inheritdoc}
     */
    public function isValid($string)
    {
        $this->string = $string[0];

        return true;
    }

    /**
     * @return string
     */
    public function getMatch()
    {
        return $this->string;
    }
}
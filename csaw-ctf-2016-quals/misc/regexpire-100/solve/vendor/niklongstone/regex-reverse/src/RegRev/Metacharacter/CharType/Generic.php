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
 * Class Generic,
 * provides supported for escaped generic characters,
 * returns the value set via setReturnValue.
 */
class Generic extends CharacterHandler
{
    private $returnValue;

    /**
     * {@inheritdoc}
     */
    public function generate()
    {
        return $this->returnValue;
    }

    /**
     * Sets the value should return the generate method.
     *
     * @param string $string
     */
    public function setReturnValue($string)
    {
        $this->returnValue = $string;
    }
}
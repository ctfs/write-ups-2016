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

/**
 * Defines an interface to handle list of characters.
 */
interface CharListInterface
{
    /**
     * Sets the character list
     *
     * @param string $charList
     */
    public function setChars($charList);

    /**
     * Gets the character list.
     *
     * @return string
     */
    public function getChars();
}
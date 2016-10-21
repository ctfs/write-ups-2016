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
 * Class CharType,
 * handles list of characters.
 */
class CharType extends CharacterHandler implements CharListInterface
{
    private $chars;

    /**
     * {@inheritdoc}
     */
    public function generate()
    {
        $randomIndex = rand(0, strlen($this->chars) -1);

        return $this->chars[$randomIndex];
    }

    /**
     * {@inheritdoc}
     */
    public function setChars($chars)
    {
        $this->chars = $chars;
    }

    /**
     * {@inheritdoc}
     */
    public function getChars()
    {
        return $this->chars;
    }
}
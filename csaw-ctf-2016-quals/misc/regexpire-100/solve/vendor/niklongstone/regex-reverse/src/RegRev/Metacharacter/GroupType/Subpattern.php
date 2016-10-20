<?php
/**
 * This file is part of the RegexReverse package.
 *
 * (c) Nicola Pietroluongo <nik.longstone@gmail.com>
 *
 * For the full copyright and license information,
 * please view the LICENSE file that was distributed with this source code.
 */

namespace RegRev\Metacharacter\GroupType;

use RegRev\Metacharacter\CharacterHandler;
use RegRev\RegRev;

/**
 * Class Subpattern,
 * handles the sub-pattern match.
 */
class Subpattern extends CharacterHandler
{
    const SQUARE_BRACKETS_PATTERN = '/(^\(.*\))/';

    /**
     * {@inheritdoc}
     */
    public function isValid($string)
    {
        foreach ($this->getPatterns() as $pattern) {
            if (preg_match('/\[\)/', $string, $match)) {
                $pattern = Subpattern::SQUARE_BRACKETS_PATTERN;
            }
            if (preg_match($pattern, $string, $match)) {
                $this->setMatch($match[0]);

                return true;
            }
        }

        return false;
    }

    /**
     * {@inheritdoc}
     */
    public function generate()
    {
        return RegRev::generate(substr($this->getMatch(), 1, -1));
    }
}
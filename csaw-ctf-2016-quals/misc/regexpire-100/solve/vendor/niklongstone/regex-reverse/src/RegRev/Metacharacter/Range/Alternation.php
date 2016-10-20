<?php
/**
 * This file is part of the RegexReverse package.
 *
 * (c) Nicola Pietroluongo <nik.longstone@gmail.com>
 *
 * For the full copyright and license information,
 * please view the LICENSE file that was distributed with this source code.
 */

namespace RegRev\Metacharacter\Range;

use RegRev\Metacharacter\CharacterHandler;
use RegRev\Metacharacter\CharType\Unknown;

/**
 * Class OneOrMore,
 * handles one or more condition.
 */
class Alternation extends CharacterHandler
{
    /**
     * {@inheritdoc}
     */
    public function generate()
    {
        $nullType = new Unknown();
        $this->setSuccessor($nullType);

        return;
    }
}
<?php
/**
 * This file is part of the RegexReverse package.
 *
 * (c) Nicola Pietroluongo <nik.longstone@gmail.com>
 *
 * For the full copyright and license information,
 * please view the LICENSE file that was distributed with this source code.
 */

namespace RegRev\Metacharacter\Quantifier;

use RegRev\Metacharacter\CharacterHandler;

/**
 * Class OneOrMore,
 * handles one or more condition.
 */
class OneOrMore extends CharacterHandler
{
    /**
     * {@inheritdoc}
     */
    public function generate()
    {
        $quantity = $this->getQuanitity(1, 10);

        return $this->generateQuanitity($quantity);
    }

    protected function getQuanitity($min, $max)
    {
        return rand($min, $max);
    }

    protected function generateQuanitity($quantity)
    {
        $result = null;
        for ($i = 0; $i < $quantity; $i ++) {
            if ($this->getPrevious()) {
                get_class($this->getPrevious());
                $result .= $this->getPrevious()->generate();
            }
        }

        return $result;
    }
}
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

/**
 * Class ZeroOrMore,
 * handles zero or more condition.
 */
class ZeroOrMore extends OneOrMore
{
    /**
     * {@inheritdoc}
     */
    public function generate()
    {
        $quantity = $this->getQuanitity(0, 10);

        return $this->generateQuanitity($quantity);
    }
}
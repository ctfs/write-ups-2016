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
 * Class NTimes,
 * handles an N times multiple match.
 */
class NTimes extends OneOrMore
{

    private $min;
    private $max;

    /**
     * {@inheritdoc}
     */
    public function isValid($string)
    {
        foreach ($this->getPatterns() as $pattern) {
            if (preg_match($pattern, $string, $match)) {
                $this->setMatch($match[0]);
                $this->setMin($match[1]);
                $this->setMax($match[2]);

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
        $quantity = $this->getMin();

        if ($max = $this->getMax()) {
            $quantity = $this->getQuanitity($quantity, $max);
        }
        $quantity--;

        return $this->generateQuanitity($quantity);
    }

    /**
     * Sets the min quantifier.
     *
     * @param integer $min
     */
    public function setMin($min)
    {
        $this->min = $min;
    }

    /**
     * Sets the max quantifier.
     *
     * @param integer $max
     */
    public function setMax($max)
    {
        $this->max = $max;
    }

    /**
     * Gets the min quantifier.
     *
     * @return integer
     */
    public function getMin()
    {
        return $this->min;
    }

    /**
     * Gets the max quantifier.
     *
     * @return integer
     */
    public function getMax()
    {
        return $this->max;
    }
}
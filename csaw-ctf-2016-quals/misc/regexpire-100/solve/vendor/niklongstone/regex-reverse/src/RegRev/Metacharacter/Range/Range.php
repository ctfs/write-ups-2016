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
use RegRev\Metacharacter\CharType\CharListInterface;

/**
 * Class Range,
 * handles the range match.
 */
class Range extends CharacterHandler implements CharListInterface
{
    /** @var  string */
    private $chars;

    /**
     * {@inheritdoc}
     */
    public function isValid($string)
    {
        foreach ($this->getPatterns() as $pattern) {
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
        $match = substr($this->getMatch(), 1, -1);
        $resultRange = '';
        $isNegation = $this->isNegation($match);
        $ranges = $this->getRanges($match);
        $resultRange .= $this->createRange($ranges);
        $resultRange .= $this->getSingleChars($match, $ranges);
        if ($isNegation) {
            $resultRange = $this->generateNegation($resultRange);
        }
        $randomIndex = rand(0, strlen($resultRange) - 1);

        return $resultRange[$randomIndex];
    }

    /**
     * Checks if the range is a negation (ie:[^..]).
     *
     * @param string $match
     *
     * @return bool
     */
    private function isNegation($match)
    {
        return $match[0] == '^';
    }

    /**
     * Gets single character list from the range (ie:[a4h-]).
     *
     * @param string $match
     * @param array  $ranges
     *
     * @return string|null
     */
    private function getSingleChars($match, $ranges)
    {
        foreach ($ranges as $range) {
            $match = str_replace($range, '', $match);
        }
        $match = preg_replace('/((\\\\)(?:.))/', '', $match);

        return $match;
    }

    /**
     * Gets characters range (ie:[a-f0-9]).
     *
     * @param string $match
     *
     * @return array
     */
    private function getRanges($match)
    {
        preg_match_all('/.-[^\\\]/', $match, $ranges);

        return $ranges[0];
    }

    /**
     * Removes the negated character from the available chars list.
     *
     * @param string $match
     *
     * @return string
     */
    private function generateNegation($match)
    {
        $match = str_split($match);
        $chars = str_split($this->getChars());
        foreach ($match as $negVal) {
            if (($key = array_search($negVal, $chars)) !== false) {
                if ($negVal == '\\') {
                    continue;
                }
                unset($chars[$key]);
            }
        }

        return implode('', $chars);
    }

    /**
     * Creates the characters ranges.
     *
     * @param array $ranges
     *
     * @return string
     */
    private function createRange($ranges)
    {
        $rangeOfString = '';
        foreach ($ranges as $range) {
           $rangeOfString .= implode('', range($range[0], $range[2]));
        }

        return $rangeOfString;
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
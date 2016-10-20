<?php
/**
 * This file is part of the RegexReverse package.
 *
 * (c) Nicola Pietroluongo <nik.longstone@gmail.com>
 *
 * For the full copyright and license information,
 * please view the LICENSE file that was distributed with this source code.
 */

namespace RegRev\Exception;

/**
 * Class RegExpNotValidException
 *
 * @package RevReg\Exception
 */
class RegExpNotValidException  extends \RuntimeException
{
    /**
     * Constructor
     * @param string $string
     */
    public function __construct($string)
    {
        parent::__construct(sprintf('The regular expression "%s" is not valid', $string));
    }
}
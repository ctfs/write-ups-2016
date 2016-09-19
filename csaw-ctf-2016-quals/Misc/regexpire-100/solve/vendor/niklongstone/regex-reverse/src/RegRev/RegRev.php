<?php
/**
 * This file is part of the RegexReverse package.
 *
 * (c) Nicola Pietroluongo <nik.longstone@gmail.com>
 *
 * For the full copyright and license information,
 * please view the LICENSE file that was distributed with this source code.
 */

namespace RegRev;
use RegRev\Exception\RegExpNotValidException;

/**
 * Class RevReg
 */
class RegRev
{
    /** @var array  */
    private static $typesFound = array();

    /** @var  ExpressionContainer */
    private static $expressions;

    /**
     * Generates the regular expression result.
     *
     * @param string $regExp
     *
     * @return mixed
     * @throws Exception\RegExpNotValidException
     */
    static public function generate($regExp)
    {
        if (@preg_match('/'.$regExp.'/', '') === false) {
            throw new RegExpNotValidException($regExp);
        }
        self::bootstrap();
        self::$typesFound = array();
        while (strlen($regExp) > 0) {
            foreach (self::$expressions as $type) {
                if ($type->isValid($regExp)) {
                    Debug::setMessage($type->getName() . ' ' . $type->getMatch());
                    self::$typesFound[] = clone $type;
                    $lengthOfMatch = strlen($type->getMatch());
                    $regExp = substr($regExp, $lengthOfMatch);

                    break;
                }
            }
        }

        return self::outPut();
    }

    /**
     * Configures with default values,
     * if custom values are not present.
     */
    static private function bootstrap()
    {
        if (self::$expressions === null) {
            $configuration = new Configuration();
            $parameters = $configuration->getConfig();
            self::$expressions = $configuration->setUp($parameters);
        }
    }

    /**
     * SetUp a custom configuration
     *
     * @param array $parameters
     */
    static public function setUp($parameters)
    {
        $configuration = new Configuration();
        self::$expressions = $configuration->setUp($parameters);
    }

    static private function outPut()
    {
        $typeFound = self::$typesFound[0];
        $totalTypesFound = count(self::$typesFound) -1;
        for ($i = 0; $i < $totalTypesFound; $i++) {
            self::$typesFound[$i]->setSuccessor(self::$typesFound[$i+1]);
        }

        return $typeFound->getResult();
    }

    /**
     * Returns debug messages.
     *
     * @return array
     */
    static public function debug()
    {
        return Debug::getMessages();
    }
}

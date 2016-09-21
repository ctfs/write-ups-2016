<?php
require ('vendor/autoload.php');
use RegRev\RegRev;

echo RegRev::generate($argv[1]); //ouput a random number
echo "\n";

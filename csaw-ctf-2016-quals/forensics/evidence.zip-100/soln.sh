#!/bin/bash
zipdetails evidence.zip | grep CRC | cut -d\  -f21 | paste -s -d'\0' - | grep --only-matching "$(echo -n 'flag' | xxd -p | tr '[:lower:]' '[:upper:]').*" | xxd -r -p

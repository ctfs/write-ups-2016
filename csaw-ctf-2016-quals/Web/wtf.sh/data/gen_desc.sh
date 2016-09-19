#!/usr/bin/env bash

# script to generate md files for challenge descriptions, sized for CTFd


for n in 1 2; do
    FILE="DESC_$n.md";
    rm "$FILE" 2>/dev/null; # ignore errors, it means first time generating
    touch "$FILE";
    echo "\`$ man $n wtf.sh\`" >> "$FILE";
    echo '```' >> "$FILE";
    MANWIDTH=55 man -l "wtf.${n}" >> "$FILE";
    echo '```' >> "$FILE";
    echo "Created ${FILE}";
done

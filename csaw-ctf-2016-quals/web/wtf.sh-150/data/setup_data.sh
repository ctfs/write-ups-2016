#!/usr/bin/env bash

MYDIR="$(dirname $0)/";

source lib.sh
source user_functions.sh
source post_functions.sh

rm .index_cache.html;
touch .index_cache.html;
chmod 777 .index_cache.html;

# gotta get dem sick references in there somewhere :)
USERS=("admin"
       # Hackers
       "Acid Burn" "Phantom Phreak" "The Plague"
       "Cereal Killer" "Zero Cool"
       # Ghost in the Shell
       "The Laughing Man" "The Puppet Master"
       # The matrix
       "Trinity" "Neo" "Morpheus"
       # Kung Fury
       "Hackerman"
       );

function random_password {
    (tr -cd "[:alnum:]" | head -c 32) < /dev/urandom;
}

function random_text {
    line_file="$(ls "${MYDIR}/hackers_lines/" | shuf | head -n 1)";
    ${MYDIR}/markov.sh "${MYDIR}/hackers_lines/${line_file}"
}

function random_digit {
    (tr -cd "[:digit:]" | head -c 1) < /dev/urandom;
}


echo "------------------------------------"
echo "---------- CREATING USERS ----------"
echo "------------------------------------"
for i in ${!USERS[@]}; do
    user=${USERS[$i]};
    pass=$(random_password);
    if [[ $(find_user_file ${user}) = 'NONE' ]]
    then
        echo ${user}:${pass}:$(create_user "${user}" "${pass}");
    else
        echo "${user} already exists D:";
    fi
done


# create a bunch of posts in a randomish order
echo "------------------------------------"
echo "---------- CREATING POSTS ----------"
echo "------------------------------------"
(seq 0 $(random_digit) \
| while read -r k; do
    for i in ${!USERS[@]}; do
        user=${USERS[$i]};
        echo "${k}" "${user}";
    done
done \
| shuf \
| while read -r n user; do # create posts
    post_id=$(create_post "${user}" "$(random_text)" "$(random_text)")
    echo "Created post with id ${post_id}" 1>&2;
    echo ${post_id}
done \
| while read -r post_id; do # reply to posts
    seq 0 $(random_digit) \
    | while read -r i; do
        user=$(shuf -e "${USERS[@]}" | head -n 1);
        reply "${post_id}" "${user}" "$(random_text)";
        echo "Added reply from ${user} to post ${post_id}" 1>&2;
    done
done) 2>&1

jobs

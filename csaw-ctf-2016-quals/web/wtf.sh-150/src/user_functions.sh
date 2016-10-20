#!/usr/local/bin/bash

function hash_password {
    local password=$1;
    (shasum <<< ${password}) | cut -d\  -f1;
}

# hash usernames for lookup in the users_lookup table
function hash_username {
    local username=$1;
    (shasum <<< ${username}) | cut -d\  -f1;
}

# generate a random token, base64 encoded
# on GNU base64 wraps at 76 characters, so we need to pass --wrap=0
function generate_token {
    (head -c 64 | (base64 --wrap=0 || base64)) < /dev/urandom 2> /dev/null;
}

function find_user_file {
    local username=$1;
    local hashed=$(hash_username "${username}");
    local f;
    if [[ -n "${username}" && -e "users_lookup/${hashed}" ]]
    then
        echo "users/$(cat "users_lookup/${hashed}/userid")";
    else
        echo "NONE"; # our failure case -- ugly but w/e...
    fi;
    return;
}

# The caller is responsible for checking that the user doesn't exist already calling this
function create_user {
    local username=$1;
    local password=$2;
    local hashed_pass=$(hash_password ${password});
    local hashed_username=$(hash_username "${username}");
    local token=$(generate_token);

    mkdir users 2> /dev/null; # make sure users directory exists
    touch users/.nolist; # make sure that the users dir can't be listed
    touch users/.noread; # don't allow reading of user files directly

    mkdir users_lookup 2> /dev/null; # make sure the username -> userid lookup directory exists
    touch users_lookup/.nolist; # don't let it be listed

    local user_id=$(basename $(mktemp users/XXXXX));


    # user files look like:
    #   username
    #   hashed_pass
    #   token
    echo "${username}" > "users/${user_id}";
    echo "${hashed_pass}" >> "users/${user_id}";
    echo "${token}" >> "users/${user_id}";


    mkdir "users_lookup/${hashed_username}" 2> /dev/null;
    touch "users_lookup/${hashed_username}/.nolist"; # lookup dir for this user can't be readable
    touch "users_lookup/${hashed_username}/.noread"; # don't allow reading the lookup dir
    touch "users_lookup/${hashed_username}/posts"; # lookup for posts this user has participated in
    echo "${user_id}" > "users_lookup/${hashed_username}/userid"; # create reverse lookup

    echo ${user_id};
}

function check_password {
    local username=$1;
    local password=$2;
    local userfile=$(find_user_file ${username});

    if [[ ${userfile} = 'NONE' ]]
    then
        return 1;
    fi

    local hashed_pass=$(hash_password ${password});
    local correct_hash=$(head -n2 ${userfile} | tail -n1);
    [[ ${hashed_pass} = ${correct_hash} ]];
    return $?;
}

function is_logged_in {
    contains 'TOKEN' ${!COOKIES[@]} && contains 'USERNAME' ${!COOKIES[@]};
    local has_cookies=$?
    local userfile=$(find_user_file ${COOKIES['USERNAME']});
    [[ ${has_cookies} \
        && ${userfile} != 'NONE' \
        && $(tail -n1 ${userfile} 2>/dev/null) = ${COOKIES['TOKEN']} \
        && $(head -n1 ${userfile} 2>/dev/null) = ${COOKIES['USERNAME']} \
    ]];
    return $?;
}

function get_users_posts {
    local username=$1;
    local hashed=$(hash_username "${username}");
    # we only have to iterate over posts a user has replied to
    while read -r post_id; do
        echo "posts/${post_id}";
    done < "users_lookup/${hashed}/posts";
}

#!/usr/bin/env bash

source user_functions.sh

# Create a new post. Returns the post id.
function create_post {
    local username=$1;
    local title=$2;
    local text=$3;
    local hashed=$(hash_username "${username}");

    # ensure posts dir exists and isn't listable.
    mkdir posts 2> /dev/null;
    touch posts/.nolist; # don't allow directory listing on posts
    touch posts/.noread; # don't allow file reads on post

    local post_id=$(basename $(mktemp --directory posts/XXXXX));


    echo ${username} > "posts/${post_id}/1";
    echo ${title} >> "posts/${post_id}/1";
    echo ${text} >> "posts/${post_id}/1";

    touch "posts/${post_id}/.nolist";
    touch "posts/${post_id}/.noread";


    # add to our cache for the homepage
    echo "<li><a href=\"/post.wtf?post=${post_id}\">$(htmlentities <<< ${title})</a> by $(htmlentities <<< ${username})</li>" >> .index_cache.html

    # add post to users' post cache
    local hashed=$(hash_username "${username}");
    echo "${post_id}/1" >> "users_lookup/${hashed}/posts";

    echo ${post_id};

}

function reply {
    local post_id=$1;
    local username=$2;
    local text=$3;
    local hashed=$(hash_username "${username}");

    curr_id=$(for d in posts/${post_id}/*; do basename $d; done | sort -n | tail -n 1);
    next_reply_id=$(awk '{print $1+1}' <<< "${curr_id}");
    next_file=(posts/${post_id}/${next_reply_id});
    echo "${username}" > "${next_file}";
    echo "RE: $(nth_line 2 < "posts/${post_id}/1")" >> "${next_file}";
    echo "${text}" >> "${next_file}";

    # add post this is in reply to to posts cache
    echo "${post_id}/${next_reply_id}" >> "users_lookup/${hashed}/posts";
}

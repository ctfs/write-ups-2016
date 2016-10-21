#!/usr/bin/env bash

# config stuff
PROCESS_LIMIT=512 # per connection
PROFILE=false

# shell options
shopt -s extglob;

# ~~ PROFILING ~~
if [[ $PROFILE = true ]]
then
    PS4='+ $(date "+%s.%N") $(if [[ ${FUNCNAME} = "" ]]; then echo NONE; else echo "${FUNCNAME}"; fi ) ${LINENO}\011 '
    exec 3>&2 2>/tmp/bashprof.$$.log
    set -x
fi

# sick facts about bash
declare -a BASH_FACTS=(
    $'Bash has an `until` keyword, which is equivalent to `while not`.' 
    $'Single and Double quotes do different things in bash -- single quotes do not interpolate variables, while double quotes do.' 
    $'When globbing on arrays in bash, you have the option to use [*] and [@], which appear to both return all the elements of the array. However, [*] acts like a "splat operator", while [@] keeps all everything constrained to the same argument.' 
    $'The bash array access syntax looks like ${array[$idx]}.' 
    $'If you forget the brackets in an array access, bash will just return the first element of the array.' 
    $'Bash didn\'t have Associative Arrays until Bash 4' 
    $'The idomatic way of iterating over all the lines in a file in bash is `while read -r line; do <something with line>; done < <filename>`' 
    $'Loops are just commands. So, you can pipe things into and out of them!'
    );

source lib.sh # import stdlib

VERSION="0.0.0.0.1 \"alphaest of bets\""
declare -a REPLY_HEADERS=(
    "X-Powered-By: wtf.sh ${VERSION}" # Fly the banner of wtf.sh proudly!
    "X-Bash-Fact: $(shuf --head-count=1 -e "${BASH_FACTS[@]}")" # select a random BASH FACT to include
);

declare -A URL_PARAMS # hashtable of url parameters
declare -A POST_PARAMS # hashtable of post parameters
declare -A HTTP_HEADERS # hashtable of http headers
declare -A COOKIES # hashtable of cookies



function log {
    echo "[`date`] $@" 1>&9
}

urldecode() {
    # urldecode <string>

    local url_encoded="${1//+/ }"
    printf '%b' "${url_encoded//%/\\x}"
}

max_page_include_depth=64
page_include_depth=0
function include_page {
    # include_page <pathname>
    local pathname=$1
    local cmd=""
    [[ "${pathname:(-4)}" = '.wtf' ]];
    local can_execute=$?;
    page_include_depth=$(($page_include_depth+1))
    if [[ $page_include_depth -lt $max_page_include_depth ]]
    then
        local line;
        while read -r line; do
            # check if we're in a script line or not ($ at the beginning implies script line)
            # also, our extension needs to be .wtf
            [[ "$" = "${line:0:1}" && ${can_execute} = 0 ]];
            is_script=$?;

            # execute the line.
            if [[ $is_script = 0 ]]
            then
                cmd+=$'\n'"${line#"$"}";
            else
                if [[ -n $cmd ]]
                then
                    eval "$cmd" || log "Error during execution of ${cmd}";
                    cmd=""
                fi
                echo $line
            fi
        done < ${pathname}
    else
        echo "<p>Max include depth exceeded!<p>"
    fi
}

function parse_headers {
    while read -r line; do
        if [[ $line = $'\r' || $line == $'\n' ]]
        then
            break
        else
            a=($line)
            key=${a[0]%?}
            value=${a[@]:1}
            HTTP_HEADERS[$key]=${value:0:-1}; # remove \r from end
        fi
    done
}

function parse_cookies {
    while read -d ';' -r cookie; do
        local key=$(cut -d\= -f1 <<< "${cookie}");
        local value=${cookie#*=};
        COOKIES[${key}]=${value};
    done <<< "${HTTP_HEADERS['Cookie']};" # append a ; so we still get the last field -- read drops the last thing >_<
}

function handle_connection {
    ulimit -u "${PROCESS_LIMIT}"; # limit num processes per connection

    # Parse query and any url parameters that may be in the path
    IFS=' ' read -r method path version

    # fast fail on empty request
    if [[ ${method} = '' ]]
    then
        return
    fi

    query=${path##*\?};
    if [[ $query != $path ]]
    then
        while read -d '&' -r param; do
            IFS='=' read key value <<< ${param};
            URL_PARAMS[$key]=$(urldecode $value)
        done <<< "${query}&" # add & so last argument is seen
    fi

    request=("$method" "$path" "$version")
    path=$(urldecode $(cut -d\? -f1 <<< "${path}")) # strip url parameters, urldecode

    # parse headers
    parse_headers;

    # parse out cookie values, if they exist
    if contains "Cookie" "${!HTTP_HEADERS[@]}"
    then
        parse_cookies;
    fi
    
    if [[ $method == "POST" ]]
    then
        # TODO: handle multipart bodies
        local line;
        local n;
        n=${HTTP_HEADERS['Content-Length']};
        read -n$n -r line;
        params=($(sed "s/\&/ /g" <<< "${line}"))
        for param in ${params[@]}; do
            IFS='=' read key value <<< ${param};
            POST_PARAMS[$key]=$(urldecode $value)
        done
    fi

    # if we know the IP (via an X-Forwarded-For header), stick the user in a sandbox
    # (Cloudflare will fill in this IP in prod, we can also have nginx fill it in in dev if we want)
    if contains "X-Forwarded-For" "${!HTTP_HEADERS[@]}"
    then
        sandbox_dir="$((cksum <<< ${HTTP_HEADERS["X-Forwarded-For"]}) | cut -d\  -f1).sandbox";
        # create sandbox if it doesn't exist
        if [[ ! -e "${sandbox_dir}" ]]
        then
            mkdir "${sandbox_dir}";
            # copy anything that isn't itself a sandbox to the dir
            cp -R !(*.sandbox) "${sandbox_dir}";
        fi
        cd "${sandbox_dir}";
    else
        log "WARNING: Not sandboxing: no X-Forwarded-For header found!"
    fi

    requested_path=$(pwd)/${path}

    # if a directory is requested, try each of the following, in order
    # index.wtf, index.html
    local index_fills=("index.wtf" "index.html");
    if [[ -d ${requested_path} ]]
    then
        for i in ${index_fills}; do
            if [[ -e "${requested_path}/${i}" ]]
            then
                requested_path="${requested_path}/${i}";
                break;
            fi
        done
    fi

    # check for possible directory traversals / other undesirable path elements by
    # removing them and 503-ing if the string was changed
    test_path=$(sed "s/\.\.//g" <<< "${requested_path}")
    if [[ ${test_path} != ${requested_path} ]]
    then
        echo "HTTP/1.1 503 Forbidden"
        echo "Content-Type: text/html"
        for reply_header in "${REPLY_HEADERS[@]}"; do
            echo "${reply_header}"
        done
        printf "\r\n\r\n"
        echo "<html><title>503</title><body>503 Forbidden</body></html>"
        echo "<p>Sorry, directory traversal is strongly frowned upon here at wtf.sh enterprises</p>";
        log "503: ${request[@]}"
        exit 0; # terminate early for 503
    fi

    [[ ! -e "${requested_path}/.nolist" ]];
    local can_list=$?;
    [[ ! -e "$(dirname "${requested_path}")/.noread" ]];
    local can_read=$?;

    if [[ -e ${requested_path}  ]]
    then
        if [[ -f ${requested_path} \
            && ${requested_path:(-4)} != ".log"\
            && ${can_read} = 0 ]] # can't end in .log, can't have .noread in the parent directory
        then
            echo "HTTP/1.1 200 OK"
            echo "Content-Type: text/html"
            for reply_header in "${REPLY_HEADERS[@]}"; do
                echo "${reply_header}"
            done
            printf "\r\n\r\n"
            include_page ${requested_path};
        elif [[ -d ${requested_path} \
            && ${can_list} = 0 ]] # handle directory listing if it isn't a file and no `.nolist` file in the directory
        then
            log "$(dirname "${requested_path}")/.noread"
            echo "HTTP/1.1 200 OK"
            echo "Content-Type: text/html"
            for reply_header in "${REPLY_HEADERS[@]}"; do
                echo "${reply_header}"
            done
            printf "\r\n\r\n"
            echo "<h3>Index of ${request[1]}</h3>"
            echo "<ul>"
            for d in ${requested_path}/*; do
                size_info=($(du -h ${requested_path} | tail -n 1))
                echo "<li><a href="/${request[1]#"/"}${d}">${d}</a>: ${size_info[0]}</li>"
            done
            echo "</ul>"
            echo "<font size=2>generated by wtf.sh ${VERSION} on $(date)</font>"
        else
            echo "HTTP/1.1 503 Forbidden"
            echo "Content-Type: text/html"
            for reply_header in "${REPLY_HEADERS[@]}"; do
                echo "${reply_header}"
            done
            printf "\r\n\r\n"
            echo "<title>503 Forbidden</title>";
            echo "<h3>I'm sorry, I'm afraid I can't let you see that</h3>";
            echo "<p>It seems that you tried to list a directory with a <code>.nolist</code> file in it, or a <code>.noread</code> file in it's parent, or a forbidden file type.</p>";
            echo "<p>If you think this was a mistake, I feel bad for you, son. I got 99 problems, but a 503 ain't one.</p>";
            log "503: ${request[@]}"
            exit 0;
        fi
        log "200: ${request[@]}"
        exit 0
    else
        # If we were noread or nolist, send a 503, even though the resource doesn't even exist -- we don't want to leak what forbidden resources do and do not exist
        if [[ ${can_read} = 1 || ${can_list} = 1 ]]; 
        then
            echo "HTTP/1.1 503 Not Found";
            echo "Content-Type: text/html"
            for reply_header in "${REPLY_HEADERS[@]}"; do
                echo "${reply_header}"
            done
            printf "\r\n\r\n"
            echo "<title>503 Forbidden</title>";
            echo "<h3>I'm sorry, I'm afraid I can't let you see that</h3>";
            echo "<p>It seems that you tried to list a directory with a <code>.nolist</code> file in it, or a <code>.noread</code> file in it's parent, or a forbidden file type.</p>";
            echo "<p>If you think this was a mistake, I feel bad for you, son. I got 99 problems, but a 503 ain't one.</p>";
            log "503: ${request[@]}"
        else
            echo "HTTP/1.1 404 Not Found"
            echo "Content-Type: text/html"
            for reply_header in "${REPLY_HEADERS[@]}"; do
                echo "${reply_header}"
            done
            printf "\r\n\r\n"
            echo "<html><title>404</title><body>404, not found:<code>${request[1]}</code></body></html>"
            log "404: ${request[@]}"
        fi
        exit 0
    fi
}

# start socat on specified port
function start_server {
    echo "wtf.sh ${VERSION}, starting!";
    socat -T10 TCP-LISTEN:$2,fork,readbytes=4096,backlog=256,reuseaddr EXEC:"$1 -r" 9>&1
    echo "Socket was occupied... try again later...";
}

if [[ $# != 1 ]]
then
    echo "Usage: $0 port"
    exit
fi

if [[ $1 == '-r' ]]
then
    handle_connection
else
    start_server $0 $1 # start server on specified port
fi

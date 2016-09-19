#!/usr/bin/env bash

cp -R /opt/wtf.sh /tmp/wtf_runtime;

# protect our stuff
chmod -R 555 /tmp/wtf_runtime/wtf.sh/*.wtf;
chmod -R 555 /tmp/wtf_runtime/wtf.sh/*.sh;
chmod 777 /tmp/wtf_runtime/wtf.sh/;

# set all dirs we could want to write into to be owned by www
# (We don't do whole webroot since we want the people to be able to create
#   files in webroot, but not overwrite existing files)
chmod -R 777 /tmp/wtf_runtime/wtf.sh/posts/;
chown -R www:www /tmp/wtf_runtime/wtf.sh/posts/;

chmod -R 777 /tmp/wtf_runtime/wtf.sh/users/;
chown -R www:www /tmp/wtf_runtime/wtf.sh/users/;

chmod -R 777 /tmp/wtf_runtime/wtf.sh/users_lookup/;
chown -R www:www /tmp/wtf_runtime/wtf.sh/users_lookup/;

# let's get this party started!
su www -c "/tmp/wtf_runtime/wtf.sh/wtf.sh 8000";

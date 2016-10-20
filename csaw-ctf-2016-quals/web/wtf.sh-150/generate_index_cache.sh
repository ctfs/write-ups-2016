#!/usr/bin/env bash

source lib.sh

rm .index_cache.html;

for post_file in posts/*; do
  post_file=$(basename $post_file);
  post_title=$(nth_line 2 < posts/$post_file | htmlentities);
  post_user=$(nth_line 1 < posts/$post_file | htmlentities);
  echo "<li><a href=\"/post.wtf?post=$post_file\">$post_title</a> by ${post_user}</li>";
done > .index_cache.html;

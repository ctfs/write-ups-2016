" Vim syntax file
" Language:	WTF.SH

runtime! syntax/html.vim

unlet b:current_syntax
syntax include @bash syntax/sh.vim
syntax region scriptCode start="^\$" end="$" contains=@bash

let b:current_syntax = 'html'

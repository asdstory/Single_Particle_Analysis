#!/usr/bin/env bash

# This script was adopted from https://github.com/Guillawme/scripts/blob/master/rename_all.sh
# Rename all files in directory to a base name plus number index.
# Can be dangerous, so use with care!

# Usage: rename_all.sh EXT BASENAME DRYRUN
# EXT: a file extension (e.g. txt), the rename operation will only operate on
# this file type in the current directory.
# BASENAME: the new name to rename files to (a numeric index will be appended).
# DRYRUN: if set (pass anything as argument), will print the rename operation
# instead of executing it.

if [ $# == 3 ]; then
    i=1
    for file in *."$1"; do
	echo "$file" `printf $2_%04d."$1" $i`
	i=$((i+1))
    done
elif [ $# == 2 ]; then
    i=1
    for file in *."$1"; do
	mv "$file" `printf $2_%04d."$1" $i`
	i=$((i+1))
    done
else
    echo "Wrong number of arguments"
    echo "Usage: rename_all.sh EXT BASENAME DRYRUN"
    echo "EXT: a file extension (e.g. txt), the rename operation will"
    echo "only operate on this file type in the current directory."
    echo "BASENAME: the new name to rename files to (a numeric index will"
    echo "be appended)."
    echo "DRYRUN:if set (pass anything as argument), will print the"
    echo "rename operation instead of executing it."
fi

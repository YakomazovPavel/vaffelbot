#!/bin/bash

COMMIT_HASH=$(git log -n 1 main --pretty=format:"%H")
LAST_COMMIT_HASH=$(ls /tmp/git_updater/)
if [[ "$LAST_COMMIT_HASH" =~ "$COMMIT_HASH" ]]; then
    echo "pass"
else
    rm -rfv /tmp/git_updater/*
    mkdir /tmp/git_updater/$COMMIT_HASH
fi 

echo $LAST_COMMIT_HASH
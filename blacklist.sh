#!/bin/bash

for domain in "$@" ; do
    status=$(wget --spider -S $domain 2>&1 | grep HTTP/ | awk '{print $2}')
    printf '%-40s: %s\n' $domain $status
done

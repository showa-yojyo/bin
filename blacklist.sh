#!/bin/bash

set -o errexit
set -o nounset
set -o pipefail

for url in "$@" ; do
    if [[ "$url" = http://* ]]; then
        status=$(wget --spider -S $url 2>&1 | grep HTTP/ | tail -1 | awk '{print $2}')
        printf '%-40s: %s\n' $url $status
    fi
done

#!/bin/bash
# Test if we're in a leap year (Bash Beginner's Guide)

set -o errexit
set -o nounset
set -o pipefail

year=${1:-$(date +%Y)}

if (( $year % 400 == 0 )) || ( (( $year % 4 == 0 )) && (( $year % 100 != 0)) ) ; then
    echo "This is a leap year. Don't forget to charge the extra day!"
else
    echo "This is not a leap year."
fi

# 要点：
# テスト式における (( arithmetic-expr ))
# 演算子 &&, ||

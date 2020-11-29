# scrapingtool.sh
# Usage: $ source scrapingtool.sh

WGET="wget --continue --wait=1 --random-wait --limit-rate=200k --quiet --show-progress --no-clobber"

function check_hxutils
{
    local hxselect=$(command -v hxselect)
    if [[ ! -x "$hxselect" ]]; then
        echo 'Error: $hxselect is not installed.' >&2
        echo 'Visit https://www.w3.org/Tools/HTML-XML-utils/README for installation'
        exit 1
    fi
}

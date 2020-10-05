#!/bin/bash
# An experimental scraper
#
# TODO: support scraping by a tag

function check_hxutils
{
    local hxselect=$(command -v hxselect)
    if [[ ! -x "$hxselect" ]]; then
        echo 'Error: $hxselect is not installed.' >&2
        echo 'Visit https://www.w3.org/Tools/HTML-XML-utils/README for installation'
        exit 1
    fi
}

function main
{
    # --wait makes fetching slow
    local wget="wget --continue --wait=1 --random-wait --limit-rate=400k --quiet --show-progress --no-clobber"

    # https://FQDN/category/id
    local post_remote="$1"

    # e.g. id
    local output_dir="${post_remote##*/}"

    # e.g. id/post.html
    local post_local="$output_dir/post.html"

    # e.g. id/images.txt
    local image_list_path="$output_dir/images.txt"

    if [[ -z "$post_remote" ]]; then
        echo 'Error: No URL provided.' >&2
        return 2
    fi

    check_hxutils

    # mkdir will fail if there is a normal file of the same name.
    mkdir -p "$output_dir"

    # Download the HTML file that contains URLs
    if [[ ! -f "$post_local" ]]; then
        $wget -O - "$post_remote" | hxclean > "$post_local"
    fi

    # Use the attribute node selector ::attr(content) with -c option.
    hxselect -c -s '\n' 'img[class*="size-large"]::attr(src)' < $post_local > "$image_list_path" 2>/dev/null
    $wget --input-file "$image_list_path" -P "$output_dir"
}

main "$@"

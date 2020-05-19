#!/bin/bash
# An experimental scraper

function check_hxutils
{
    local hxselect=$(command -v hxselect)
    if [[ ! -x "$hxselect" ]]; then
        echo 'Error: $hxselect is not installed.' >&2
        echo 'Visit https://www.w3.org/Tools/HTML-XML-utils/README for installation'
        exit 1
    fi
}

# Extract blog post URLs from given HTML file
function list_post_urls
{
    hxclean | hxselect -c -s '\n' 'h2>a::attr(href)'
}

# Extract image URLs from all posts
function list_image_urls
{
    for post in "$@" ;
    do
        hxwls "$post" | awk '/archives/ && /jpg/'
    done
}

# Main entry point
function main
{
    local remote_url_toc=$1
    local wget="wget --continue --wait=1 --random-wait --limit-rate=200k --quiet --show-progress"

    local output_dir="${remote_url_toc##*/}"
    local local_toc_path="$output_dir/toc.html"
    local post_list_path="$output_dir/posts.txt"
    local image_list_path="$output_dir/images.txt"

    if [[ -z "$remote_url_toc" ]] ; then
        echo 'Error: No URL provided.' >&2
        return 2
    fi

    check_hxutils
    mkdir -p "$output_dir"

    # Download the HTML file that contains URLs
    if [[ ! -f "$local_toc_path" ]]; then
        $wget -O - "$remote_url_toc" | hxclean > "$local_toc_path"
    fi

    # List URLs of blog posts
    list_post_urls < "$local_toc_path" > "$post_list_path" 2>/dev/null

    # Download HTML files
    $wget --input-file "$post_list_path" -P "$output_dir"

    # List URLs of remote images
    list_image_urls $output_dir/*.html \
        > "$image_list_path" 2>/dev/null

    # TODO: Warn if so many image files will be downloaded
    $wget --input-file "$image_list_path" -P "$output_dir"
}

main "$@"

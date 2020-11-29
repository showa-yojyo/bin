#!/bin/bash
# An experimental scraper (NOT TESTED YET)

# Include common features for web scraping
. scrapingtool.sh

function _visit_result_pages
{
    function _get_next_page
    {
        local search_result_page="$1"
        hxselect -c -s '\n' 'a.postslink::attr(href)' < "$1" 2>/dev/null | uniq
    }

    # Extract blog entry URLs from given HTML file
    function _list_post_urls
    {
        hxselect -c -s '\n' 'header a::attr(href)'
    }

    local first_search_result_url=$1
    local output_dir=$2
    local local_search_result_tmp="$output_dir/tmp.html"
    local post_list_file=$3

    # Immediately return if cache file exists
    if [[ -f "$post_list_file" ]]; then
        return 0
    fi

    $WGET -O - "$first_search_result_url" | hxclean > "$local_search_result_tmp"
    local next_result_url=$(_get_next_page "$local_search_result_tmp")
    while [[ -n "$next_result_url" ]]; do
        $WGET -O - "$next_result_url" | hxclean > "$local_search_result_tmp"
        # Append post URLs to a file
        _list_post_urls < "$local_search_result" >> "$post_list_file" 2>/dev/null
        next_result_url=$(_get_next_page "$next_result_url")
    done

    # Clean up
    rm -f "$local_search_result_tmp"
}

function _process_all_posts
{
    function _list_images
    {
        # Use the attribute node selector ::attr(content) with -c option.
        hxselect -c -s '\n' 'img[class*="size-large"]::attr(src)'
    }

    local output_dir=$1
    local post_list_file=$2

    for post_url in $(xargs -a "$post_list_file"); do
        # Prcessing ${post_url}...
        local subdir="${output_dir}/${post_url##*/}"
        mkdir -p "$subdir"

        local post_local="${subdir}/post.html"
        $WGET -O - "$post_url" | hxclean > "$post_local"

        local image_list_file="${subdir}/images.txt"
        _list_images < "$post_local" > "$image_list_file" 2>/dev/null
        $WGET --input-file "$image_list_file" -P "$subdir"
    done
}

function main
{
    local search_result_url=$1
    if [[ -z "$search_result_url" ]]; then
        echo 'Error: No URL provided.' >&2
        return 2
    fi

    # tag name
    local output_dir="${search_result_url##*/}"

    check_hx
    mkdir -p "$output_dir"

    local local_search_result="$output_dir"/posts.txt
    _visit_result_pages "$search_result_url" "$output_dir" "$local_search_result"
    _process_all_posts "$output_dir" "$local_search_result"
}

main "$@"

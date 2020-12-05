#!/bin/bash
# An experimental scraper

# Include common features for web scraping
. scrapingtool.sh

# Main entry point
function main
{
    function _crawl_search_result
    {
        function _get_next_page
        {
            local search_result_page="$1"
            hxclean $search_result_page | hxselect -s '\n' -c 'li.next > a::attr(href)' 2>/dev/null
        }

        local first_result="$1"
        local tmpfile="$2"
        local search_result="$3"

        echo $first_result > $search_result

        $WGET -O - $first_result | hxclean > $tmpfile

        next_result_url=$(_get_next_page $tmpfile)

        while [[ -n "$next_result_url" ]]; do
            $WGET -O - "$next_result_url" | hxclean > $tmpfile
            echo $next_result_url >> $search_result
            next_result_url=$(_get_next_page $tmpfile)
        done
        rm -f $tmpfile
    }

    # Extract blog post URLs from given HTML file
    function _list_post_urls
    {
        hxclean | hxselect -c -s '\n' 'h2>a::attr(href)'
    }

    # Extract image URLs from all posts
    function _list_image_urls
    {
        for post in "$@" ;
        do
            hxwls "$post" | awk '/archives/ && /jpg/'
        done | sort | uniq
    }

    local search_result_page_1_url=$1
    if [[ -z "$search_result_page_1_url" ]]; then
        echo 'Error: No URL provided.' >&2
        return 2
    fi

    check_hxutils

    local output_dir="${search_result_page_1_url##*/}"
    mkdir -p "$output_dir"

    local tmp_file_path="$output_dir"/tmp.html
    local search_result="$output_dir"/search_result.txt
    _crawl_search_result $search_result_page_1_url "$tmp_file_path" "$search_result"

    local output_search_results="$output_dir"/search_result_pages
    mkdir -p "$output_search_results"
    $WGET --input-file "$search_result" -P "$output_search_results"
    local wget_status=$?
    if [[ $wget_status -ne 0 ]]; then
        echo ERROR. Failed to download contents of "$search_result" >&2
        exit $wget_status
    fi

    local post_list_path="$output_dir"/posts.txt
    for name in "$output_search_results"/*; # html
    do
        # List URLs of blog posts
        _list_post_urls < "$name" >> "$post_list_path" 2>/dev/null
    done

    # Download HTML files
    local output_entries_dir="$output_dir"/entiries
    mkdir -p "$output_entries_dir"
    $WGET --input-file "$post_list_path" -P "$output_entries_dir"

    # List URLs of remote images
    local image_list_path="$output_dir"/images.txt
    _list_image_urls $output_entries_dir/*.html > "$image_list_path" 2>/dev/null
}

main "$@"

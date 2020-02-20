#!/bin/bash

BLACK_LIST=(
    http://moeimg.net/ \
    http://buhidoh.net/ \
    http://doujin-eromanga.com/ \
    http://nyafu.livedoor.biz/ \
    http://nijinchu.com/ \
    http://nijimoemoe.com/ \
    http://doucolle.net/ \
    https://tajigen.com/ \
    https://news.tokimeki-s.com/ \
    http://bakufu.jp/ \
    http://hnalady.com/ \
    https://nijifeti.com/ \
    http://momoniji.com/ \
    https://二次萌えエロ画像.com/ \
    https://2ji.pink/ \
    http://eromangaosa-mu.com/ \
    http://blog.livedoor.jp/wakusoku/ \
    https://www.nijioma.blog/ \
    https://dougle.one/ \
    http://adult-gazou.me/ \
    https://nijix.net/ \
    https://nijisenmon.work/ \
    https://erologz.com/ \
    https://www.niji-wired.info/ \
    http://blog.livedoor.jp/nizimoenews/ \
    https://tanishitorantan.site/
)

for domain in "${BLACK_LIST[@]}" ; do
    status=$(wget --spider -S $domain 2>&1 | grep HTTP/ | awk '{print $2}')
    printf '%-40s: %s\n' $domain $status
done

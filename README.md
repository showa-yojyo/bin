---
author: プレハブ小屋 <2386769+showa-yojyo@users.noreply.github.com>
title: README
---

# README

## What this repository is

This repository contains various script files for my use. Most of the script
files are written in Bash or Python so far.

## Installation

First, clone this repository to your `$HOME/.local/bin` directory (recommended).

```console
mkdir -p ~/.local/bin && cd $_ # optional
git clone https://github.com/showa-yojyo/bin.git .
```

And make sure the `PATH` environment variable includes this directory. If you
use Bash, modify the variable in `.bashrc` as below:

```shell
# change PATH so it includes one of your private bin directores
for dir in "$HOME/.local/bin" "$HOME/bin"; do
    if [[ -d "$dir" ]] ; then
        PATH="$dir:$PATH"
        break
    fi
done
```

## Dependencies

* [GNU Bash]
* [Python 3.x][Python]: Additionally, some scripts use some third party packages:
  * [Beautiful Soup]
  * [Click]
  * [dateutil]
  * [Docutils]
  * [Jinja2]
  * [Scrapy]
  * [PyYaml]
  * [JPHoliday]
  * [Pillow]
  * [python-stdnum]
* [ImageMagick]
* [FFmpeg]
* [fzf]

## How to file issues

If you find any issues in programs this repository, please miss them.

[GNU Bash]: <https://www.gnu.org/software/bash/>
[Python]: <https://www.python.org/>
[Beautiful Soup]: <https://www.crummy.com/software/BeautifulSoup/>
[dateutil]: <https://github.com/dateutil/dateutil>
[Docutils]: <https://sourceforge.net/projects/docutils/>
[Jinja2]: <https://palletsprojects.com/projects/jinja/>
[Scrapy]: <https://scrapy.org/>
[PyYAML]: <https://pyyaml.org/>
[FFmpeg]: <https://ffmpeg.org/>
[fzf]: <https://junegunn.github.io/fzf/> "fzf"
[ImageMagick]: <https://imagemagick.org/>
[JPHoliday]: <https://github.com/Lalcs/jpholiday>
[Click]: <https://click.palletsprojects.com/en/stable/>
[Pillow]: <https://pillow.readthedocs.io/en/stable/>
[python-stdnum]: <https://arthurdejong.org/python-stdnum/doc/>

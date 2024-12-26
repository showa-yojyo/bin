# README

## What is this?

This repository contains various script files for my use. Most of the script
files are written in Bash or Python so far.

## Installation

First, clone this repository to your `$HOME/.local/bin` directory (recommended).

```console
$ mkdir -p ~/.local/bin && cd $_ # optional
$ git clone https://github.com/showa-yojyo/bin.git .
```

And make sure the `PATH` environment variable includes this directory. For
example, in `.bash_profile`, set it as below:

```shell
# in .bash_profile or .profile

# set PATH so it includes user's private bin if it exists
for dir in "$HOME/.local/bin" "$HOME/bin"; do
    if [ -d "$dir" ] ; then
        PATH="$dir:$PATH"
        break
    fi
done
```

## Dependencies

* [GNU Bash]
* [Python 3.x][Python]: Additionally, some scripts use some third party
  packages:
  * [Beautiful Soup]
  * [Click]
  * [dateutil]
  * [Docutils]
  * [Jinja2]
  * [Scrapy]
  * [PyYaml]
  * [JPHoliday]
* [ImageMagick]
* [FFmpeg]

## Bug Reporting

Please do not report any issues you find to me.

[GNU Bash]: <https://www.gnu.org/software/bash/>
[Python]: <https://www.python.org/>
[Beautiful Soup]: <https://www.crummy.com/software/BeautifulSoup/>
[dateutil]: <https://github.com/dateutil/dateutil>
[Docutils]: <https://sourceforge.net/projects/docutils/>
[Jinja2]: <https://palletsprojects.com/projects/jinja/>
[Scrapy]: <https://scrapy.org/>
[PyYAML]: <https://pyyaml.org/>
[FFmpeg]: <https://ffmpeg.org/>
[ImageMagick]: <https://imagemagick.org/>
[JPHoliday]: <https://github.com/Lalcs/jpholiday>
[Click]: <https://click.palletsprojects.com/en/stable/>

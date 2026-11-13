---
author: プレハブ小屋 <2386769+showa-yojyo@users.noreply.github.com>
modified: 2026-11-14
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

And make sure the `PATH` environment variable includes this directory.

## Dependencies

* [GNU Bash]
* [Python]: Some scripts are to be run using tools such as [uv].
* [ImageMagick]
* [FFmpeg]
* [fzf]

## How to file issues

If you find any issues in programs this repository, please miss them.

[GNU Bash]: <https://www.gnu.org/software/bash/>
[Python]: <https://www.python.org/>
[uv]: <https://docs.astral.sh/uv/>
[FFmpeg]: <https://ffmpeg.org/>
[fzf]: <https://junegunn.github.io/fzf/> "fzf"
[ImageMagick]: <https://imagemagick.org/>

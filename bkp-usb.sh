#!/bin/bash
#
# bkp-usb.sh: 以下のフォルダを USB にコピーする Bash スクリプト
#
# * プレハブ小屋フォルダ以下のファイル群
# * ドラクエ命のビルド生成物ファイル群
# * 読書ノートのビルド生成物ファイル群
# * Subversion のレポジトリーフォルダにあるレポジトリー全部

# rsync の注意
# source, dest をフォルダとする。このとき
#
#   rsync -auv source dest
# と
#   rsync -auv source/ dest
#
# は違う。前者は dest/source が生成される。後者は dest/ の直下に
# source の中身が来る。

# function backup_repos:
# Subversion のレポジトリーを USB にバックアップ
function backup_repos
{
	local SRC=/cygdrive/d/svn-repos
	local DEST="${USB2}/bkp/svn-repos"

	rsync -auv --delete "${SRC}/" "${DEST}/"
}

# function backup_homedir:
# ~ 以下全部バックアップ
function backup_homedir
{
	local SRC="$HOME"
	local DEST="${USB2}/bkp/homedir"

	rsync -auv --delete --delete-excluded --exclude="build/" --exclude="cache/" "${SRC}/" "${DEST}/"
}

backup_repos
backup_homedir

#!/bin/bash

set -e

# the inputs:
TARGET="${TARGET:-x86/64}"
VERSION_PATH="${VERSION_PATH:-snapshots}"
UPSTREAM_URL="${UPSTREAM_URL:-https://downloads.immortalwrt.org}"

# prepare cache path
CACHE_PATH="/cache/$VERSION_PATH/$TARGET"
[ -d "$CACHE_PATH" ] || mkdir -p "$CACHE_PATH"

# use "*.Linux-x86_64.*" to create the imagebuilder
DOWNLOAD_FILE="imagebuilder-.*x86_64.tar.[xz|zst]"
DOWNLOAD_PATH="$VERSION_PATH/targets/$TARGET"

# check shasum
if [ -s "$CACHE_PATH/sha256sums" ]; then
	shasum_stamp="$(curl --retry 3 --retry-all-errors --retry-delay 10 -fsISL "$UPSTREAM_URL/$DOWNLOAD_PATH/sha256sums" | awk -F ': ' '/last-modified/ {print $2}' IGNORECASE=1)"
	if [ ! -s "$CACHE_PATH/sha256sums.stamp" ] || [ "$(cat "$CACHE_PATH/sha256sums.stamp")" != "$shasum_stamp" ]; then
		rm -rf "$CACHE_PATH/sha256sums" "$CACHE_PATH/sha256sums.stamp"
	fi
fi

# download imagebuilder/sdk shasum
if [ ! -s "$CACHE_PATH/sha256sums" ]; then
	curl --retry 3 --retry-all-errors --retry-delay 10 -fSL "$UPSTREAM_URL/$DOWNLOAD_PATH/sha256sums" -o "sha256sums"

	rm -rf "$CACHE_PATH/sha256sums"
	mv "sha256sums" "$CACHE_PATH"/

	rm -rf "$CACHE_PATH/sha256sums.stamp"
	echo -e "$shasum_stamp" > "$CACHE_PATH/sha256sums.stamp"
fi

# determine archive name
file_name="$(grep "$DOWNLOAD_FILE" "$CACHE_PATH/sha256sums" | cut -d "*" -f 2)"

# check imagebuilder/sdk archive
if [ -e "$CACHE_PATH/$file_name" ]; then
	grep "$file_name" "$CACHE_PATH/sha256sums" | sed "s,$file_name,$CACHE_PATH/$file_name,g" > "sha256sums_min"
	sha256sum -c "sha256sums_min" || rm -rf "$CACHE_PATH/$file_name"
fi

# download imagebuilder/sdk archive
if [ ! -e "$CACHE_PATH/$file_name" ]; then
	curl --retry 3 --retry-all-errors --retry-delay 10 -fSL "$UPSTREAM_URL/$DOWNLOAD_PATH/$file_name" -o "$file_name"

	# shrink checksum file to single desired file and verify downloaded archive
	grep "$file_name" "$CACHE_PATH/sha256sums" > "sha256sums_min"
	cat "sha256sums_min"
	sha256sum -c "sha256sums_min"

	rm -rf "$CACHE_PATH/$file_name"
	mv "$file_name" "$CACHE_PATH"/
fi

# cleanup
rm -vrf sha256sums_min keys/

tar xf "$CACHE_PATH/$file_name" --strip=1 --no-same-owner -C .

# prepare dl directory
[ -d "$CACHE_PATH/dl" ] || mkdir -p "$CACHE_PATH/dl"
ln -sf "$CACHE_PATH/dl" "dl"

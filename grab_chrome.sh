#!/bin/bash

# Script to grab the latest dev release of Google Chrome when using a
# Debian/Ubuntu system as a normal user. WARNING: not installing Chrome properly
# means that the sandbox won't run as setuid root, so some security stuff can't
# be set up.

set -e

if [ -e /google_chrome ] ; then
    echo /google_chrome directory already exists. Chickening out...
    exit 1
fi

URL=http://dl.google.com/linux/direct/google-chrome-unstable_current_amd64.deb

DEB=$(echo $URL | sed 's#.*/##')

[ -e $DEB ] || wget "$URL"

dpkg -i "$DEB" || apt-get --yes --fix-broken install
#TMPDIR=$(mktemp -d)
#dpkg-deb -x "$DEB" "$TMPDIR"
#mv "$TMPDIR"/opt/google/chrome-unstable /google_chrome
#rm -Rf "$TMPDIR"
#gdebi "$DEB"

#echo You can now run google_chrome/google-chrome
#echo You can move the google_chrome directory wherever you want.

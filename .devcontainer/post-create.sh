#!/bin/bash
f=/workspaces/num
current=$(cat $f 2>/dev/null)
new=$((current + 1))
echo $new > $f
echo "######## >> runs $new << ########"
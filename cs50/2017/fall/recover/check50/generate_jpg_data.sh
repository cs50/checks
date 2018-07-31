#!/bin/bash

# get the sizes of the jpegs in bytes
wc -c *.jpg > sizes.txt

# get the hashes of the jpegs
md5sum *.jpg > hashes.txt

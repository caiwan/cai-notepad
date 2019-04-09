#! /usr/bin/env sh

set -e

echo "Is shis entrpoint script runs after the image was set up, right?"
echo "Or shall I put configurations here, isn't it?"

echo "Execute $@"
exec $@

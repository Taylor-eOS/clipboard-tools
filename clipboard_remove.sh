#!/bin/bash
text=$(xclip -selection clipboard -o)
while [[ "$text" == *$'\n\n'* ]]; do
    text=${text//$'\n\n'/$'\n'}
done
printf "%s" "$text" | xclip -selection clipboard

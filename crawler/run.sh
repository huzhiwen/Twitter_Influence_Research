#!/bin/bash

max=83
quotient=$(($max / 4))
quotient_a=$(($max / 4 * 2))
quotient_b=$(($max / 4 * 3))


echo "Begin..."


# python new_crawler1.py $quotient &
osascript -e 'tell application "Terminal" to do script "cd Desktop/twitter-network/crawler && python new_crawler1.py '$quotient' "'

osascript -e 'tell application "Terminal" to do script "cd Desktop/twitter-network/crawler && python new_crawler2.py '$quotient' '$quotient_a'"'
osascript -e 'tell application "Terminal" to do script "cd Desktop/twitter-network/crawler && python new_crawler3.py '$quotient_a' '$quotient_b'"'
osascript -e 'tell application "Terminal" to do script "cd Desktop/twitter-network/crawler && python new_crawler4.py '$quotient_b' "'

#!/usr/bin/env bash

# APPLICATION ID = 53
# APPLICATION ACCOUNT = "KRI4UNYE3S6H4OC3T3I2JPG4475D7AJNXGQJKWWBEBJW7KJSBMWTY3R5MM"
# CHALLENGER ACCOUNT = "IAEP3WXYZTAG6CMEJNTFNIQXDK67PUR5DKGLBDOWTGBLZNEA5OGPBMPEF4"
# CHALLENGER HASH = "NDkzYTE1ZTdiZGE4OGIwNzI3MjA3MWNiY2ZkM2NiMDU5MjBiOTk5ODcyYjZmM2NmYTZlNGQxNjcxMmRiZjQzNA=="
# CHALLENGER HAND ="scissors"
# OPPONENT ACCOUNT = "P3PLNEUIRGEZRBHLNLLOIIHAMOFFTN365JJ7CDPCMQKK4BIPB7U7WFYYJU"
# OPPONENT HAND = "rock"
# WAGER = 10000

# from account je od prvog accounta
# drugi account
# hash vrednost informacija studenta

# to je na emn178.github.io/online-tools/index.html -> SHA256 -> pisem sta hocu, kopiram -> encode, base 64 (hex type)
# stavila sam hash vrednost 20190170
goal app call \
    --app-id 1082 \
    -f JMT4WKMO3WG3YC3OYETXPKRHMOMFDUTTFJE7VSPX6XY7GEEQTMUPBDA5XQ \
    --app-account VTJBTJN57GG3UE4G3PSCVWA5Y7LY3CRT7NXAOC72R22SJ7ETLI7RVMLF5U \
    --app-arg "str:resolve" \
    --app-arg "str:20190170" \
    -o play-start.tx

goal clerk send \
    -a 100000 \
    -t RX5BI54N5WNONAZNKNYETIQKBAHQ6C7YIUIS5JXOKZRB3HLXLRIHMHUFPM \
    -f JMT4WKMO3WG3YC3OYETXPKRHMOMFDUTTFJE7VSPX6XY7GEEQTMUPBDA5XQ \
    -o play-wager.tx

cat play-start.tx play-wager.tx > play-combined.tx
goal clerk group -i play-combined.tx -o play-grouped.tx
goal clerk split -i play-grouped.tx -o play-split.tx

goal clerk sign -i play-split-0.tx -o play-signed-0.tx
goal clerk sign -i play-split-1.tx -o play-signed-1.tx

cat play-signed-0.tx play-signed-1.tx > play-signed-final.tx

goal clerk rawsend -f play-signed-final.tx
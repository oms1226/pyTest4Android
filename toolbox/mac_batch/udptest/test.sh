#!/bin/bash

echo "################################################"
echo "# Echo Connect"
echo "################################################"

echo "# Echo Connect {3400..10000}"
for j in {3400..10000}
do
#    ./trtc_echo_client 1.232.90.69 $j > /dev/null
    ./trtc_echo_client 1.232.90.69 $j
done

echo "# Echo Done"

#!/bin/sh

for i in "$@"
do
case $i in
    -c|--clean)
    echo "# cleaning..."
    echo "# done..."
    ;;
    -b|--build)
    echo "# building..."
    rm -rf trtc_echo_client
    cmake .
    make
    echo "# done..."
    ;;
    -r|--run)
    echo "# running..."
    killall trtc_echo_client
    ./test.sh
    ;;
    -k|--kill)
    echo "# killing..."
    killall trtc_echo_client        
    ;;
    *)
    ;;
esac
done

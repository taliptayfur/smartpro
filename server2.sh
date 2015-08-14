#!/bin/bash

if [ "$#" -lt "6" ]; then
	echo "usage -> ./script.sh 'FPS' 'RESOLUTION' 'BITRATE' 'MAX_BITRATE' 'SLICE_MAX_SIZE' 'HOST:PORT' "

else
	FPS=$1
	RESOLUTION=$2
	BITRATE=$3
	MAX_BITRATE=$4
	param_vbv_bufsize=$(expr $MAX_BITRATE / $FPS)
	SLICE_MAX_SIZE=$5
	KEYINT=$FPS
	HOST=$6

	exec ffmpeg -f x11grab \
		 -s $RESOLUTION \
		 -framerate $FPS \
		 -i :0.0+1366,0 \
		 -vcodec libx264 \
		 -preset ultrafast \
		 -tune zerolatency \
		 -pix_fmt yuv420p \
		 -x264opts qpmin=10:bitrate=$BITRATE:vbv-maxrate=$MAX_BITRATE:vbv-bufsize=$param_vbv_bufsize:intra-refresh=1:slice-max-size=$SLICE_MAX_SIZE:keyint=$KEYINT:ref=1 \
		 -r $FPS \
		 -f avi tcp://$HOST?listen
fi
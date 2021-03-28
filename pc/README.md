###摄像头操作说明
~~~
raspivid --profile high -l -o tcp://0.0.0.0:12305 -hf -vf -t 0 -w 640 -h 480 -fps 40 &
~~~
~~~
-pf, --profile  : Specify H264 profile to use for encoding
H.264的四种画质级别，分别是baseline, extended, main, high：
Baseline Profile：基本画质。支持I/P 帧，只支持无交错（Progressive）和CAVLC；
Extended profile：进阶画质。支持I/P/B/SP/SI 帧，只支持无交错（Progressive）和CAVLC；(用的少)
Main profile：主流画质。提供I/P/B 帧，支持无交错（Progressive）和交错（Interlaced）， 也支持CAVLC 和CABAC 的支持；
High profile：高级画质。在main Profile 的基础上增加了8x8内部预测、自定义量化、 无损视频编码和更多的YUV 格式；

-l, --listen    : Listen on a TCP socket
-o, --output    : output to a remote IPv4 host
-hf, --hflip    : Set horizontal flip
-vf, --vflip    : Set vertical flip
-t, --timeout   : Time (in ms) to capture for
-w, --width     : Set image width <size>
-h, --height    : Set image height <size>
-fps, --framerate    : Specify the frames per second to record
&    : Running in the background
~~~


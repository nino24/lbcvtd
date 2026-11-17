ffmpeg -v error -y -i "$1"  -framerate 30 -i intro/%04d.png -framerate 30 -i wn1/%04d.png -framerate 30 -i wn2/%04d.png  -loop 1 -framerate 30 -t 12.9 -i pill.png -loop 1 -framerate 30 -t 5.9 -i pill.png  -framerate 30 -i outro/%04d.png  -f lavfi -t 0.7 -i "anoisesrc=c=pink:a=0.6:r=48000"  -filter_complex "
[0:v]fps=30,scale=w='trunc(1080*(1+(0.14*exp(-pow((t-34.85)/0.12\,2))+0.08*exp(-pow((t-54.65)/0.1\,2))))/2)*2':h='trunc(1920*(1+(0.14*exp(-pow((t-34.85)/0.12\,2))+0.08*exp(-pow((t-54.65)/0.1\,2))))/2)*2':eval=frame:flags=bicubic,crop=1080:1920:(iw-1080)/2:(ih-1920)/2,eq=brightness='(0.35*exp(-pow((t-34.85)/0.05\,2))+0.2*exp(-pow((t-54.65)/0.05\,2)))':eval=frame,tpad=stop_mode=clone:stop_duration=3.6,format=yuva420p[v];
[1:v]setpts=PTS+0.15/TB[i];[2:v]setpts=PTS+34.6/TB[w1];[3:v]setpts=PTS+54.4/TB[w2];
[4:v]format=rgba,fade=in:st=0:d=0.3:alpha=1,fade=out:st=12.6:d=0.3:alpha=1,setpts=PTS+41.5/TB[p1];
[5:v]format=rgba,fade=in:st=0:d=0.3:alpha=1,fade=out:st=5.6:d=0.3:alpha=1,setpts=PTS+58.8/TB[p2];
[6:v]setpts=PTS+64.76/TB[o];
[v][i]overlay=eof_action=pass[a1];[a1][w1]overlay=eof_action=pass[a2];[a2][w2]overlay=eof_action=pass[a3];
[a3][p1]overlay=eof_action=pass[a4];[a4][p2]overlay=eof_action=pass[a5];
[a5]ass=subs.ass[a6];[a6][o]overlay=eof_action=pass,format=yuv420p[out];
[7:a]bandpass=f=1800:width_type=o:w=2,afade=t=in:d=0.35:curve=exp,afade=t=out:st=0.35:d=0.35,volume=0.5,aformat=channel_layouts=stereo,asplit=2[wa][wb];
[wa]adelay=34450|34450[w1a];[wb]adelay=54300|54300,volume=0.7[w2a];
[0:a]aresample=48000,apad=pad_dur=3.6[voice];
[voice][w1a][w2a]amix=inputs=3:normalize=0:duration=first,loudnorm=I=-14:TP=-1:LRA=11,aresample=48000[au]"  -map "[out]" -map "[au]" -c:v libx264 -profile:v high -preset medium -b:v 16M -maxrate 20M -bufsize 32M -c:a aac -ar 48000 -b:a 320k -movflags +faststart -t 68.36 "$2"

mkdir processed
# ffmpeg -loop 1 -i logo.jpg -c:v libx264 -t 1 -pix_fmt yuv420p logo.mp4
# ffmpeg -i concat:"logo.mp4|video_dron_20.mp4|logo.mp4" -safe 0 -c copy output.mp4
echo logo.mp4 >> video_dron.txt
echo video_dron.mp4 >> video_dron.txt
echo logo.mp4 >> video_dron.txt
ffmpeg -f concat -safe 0 -i video_dron.txt -c copy c_video_dron.mp4
ffmpeg -ss 0 -t 20  -i "video_dron.mp4" -c copy l_video_dron.mp4
ffmpeg -i output.mp4 -c copy -aspect 16/9 a_video_dron.mp4
# dvelib

My code repository for helper functions, scripts and whatnot. The most useful is the oneliner to install my .bashrc:

pushd ~ && mv ~/.bashrc ~/.bashrc.\`date +%s\` && wget https://github.com/jhkoivis/dvelib/raw/master/production/userization/.bashrc && popd

or how to map a folder to letter V: in windows. Use your own account, not admin.

net use v: "\\\localhost\c$\Users\jhkoivis\Dropbox\" /persistent:yes

net use u: "\\wsl.localhost\Ubuntu" /persistent:yes

create forward - reverese loop from frames to input.mp4 and save it as output.mp4

```
ffmpeg -framerate 30 -i frame%05d.png input.mp4
ffmpeg -y -i input.mp4 -c copy forward.mp4
ffmpeg -y -i forward.mp4 -vf reverse reversed.mp4
printf "file 'input.mp4'\nfile 'reversed.mp4'\n" > mylist.txt
ffmpeg -y -f concat -safe 0 -i mylist.txt -c copy catenated.mp4
ffmpeg -y -catenated.mp4 -c:v libx264 -preset slow  -profile:v high -level:v 4.0 -pix_fmt yuv420p -crf 22 -codec:a aac -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" output.mp4
```

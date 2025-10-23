# dvelib

My code repository for helper functions, scripts and whatnot. The most useful is the oneliner to install my .bashrc:

pushd ~ && mv ~/.bashrc ~/.bashrc.\`date +%s\` && wget https://github.com/jhkoivis/dvelib/raw/master/production/userization/.bashrc && popd

or how to map a folder to letter V: in windows. Use your own account, not admin.

net use v: "\\\localhost\c$\Users\jhkoivis\Dropbox\" /persistent:yes

create forward - reverese loop from input.mp4 and save it as output.mp4

```
ffmpeg -y -i input.mp4 -c copy forward.mp4
ffmpeg -y -i forward.mp4 -vf reverse reversed.mp4
printf -y "file 'input.mp4'\nfile 'reversed.mp4'\n" > mylist.txt
ffmpeg -y -f concat -safe 0 -i mylist.txt -c copy output.mp4
```

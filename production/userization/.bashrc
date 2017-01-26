# ~/.bashrc

### User Customised Initialisation ###
### Place your preferences below ####


export PRINTER=munkki                    # Set the default printer
export PS1='\[\033[0;32m\]\h: `pwd`\n>\[\033[0m\] '
export TERM=vt100
export EDITOR=vim
export HISTFILESIZE=30000
export HISTCONTROL=erasedups
export LANG="en_US"
#export PROMPT_COMMAND="history -n; history -a"
shopt -s histappend
bind '"\e[A"':history-search-backward
bind '"\e[B"':history-search-forward


export TEXINPUTS=$TEXINPUTS:~/texmf/

export PATH=/usr/local/bin:/bin/:/usr/bin/:/opt/local/bin/:/sbin
export DYLD_LIBRARY_PATH=/usr/local/cuda/lib
export LD_LIBRARY_PATH=/usr/local/cuda/lib
export PYTHONPATH=''
#Common Aliases #####


#alias ll='ls -l'
#alias la='ls -la'
#alias lt='ls -latr'
#alias r='rm -rf'
#alias sshShor='ssh -tY hugo.hut.fi ssh -tY shor.hut.fi'
#alias sshHugo='ssh -tY hugo.hut.fi'
#alias dissh='/home/jko/localapps/disrep/dis/jko/scriptit/dissh.sh'
#alias essh='/home/jko/localapps/disrep/dis/jko/scriptit/essh.sh'
#alias fiber='/scratch/jko/dis/jko/scriptit/fiberClick.sh'
#alias multiFiber='/home/jko/localapps/disrep/dis/jko/scriptit/multifiber.sh'
#alias scpto='/scratch/jko/dis/jko/scriptit/scpTo.sh'
#alias scpfrom='/scratch/jko/dis/jko/scriptit/scpFrom.sh'
#alias gv='kghostview'
#alias gfortran='gfortran -L/usr/lib/gcc/i386-redhat-linux/3.4.6/'
#alias port='sudo /opt/local/bin/port'
#alias acroread='/Applications/Adobe\ Reader\ 9/Adobe\ Reader.app/Contents/MacOS/AdobeReader'
#alias open='/Users/jko/commands/myOpen.sh'

export TERM=xterm-color
export GREP_OPTIONS='--color=auto' GREP_COLOR='1;32'
export CLICOLOR=1


if test `uname` = Darwin; then 
	alias ls='ls'; 
	alias open='/Users/jko/commands/myOpen.sh'	
	alias ipython='/opt/local/bin/ipython-2.6'
  alias svn='/opt/local/bin/svn'
fi;

if test `uname` = Linux;  then 
	alias ls='ls --color=auto'; 
fi;


# terminal colors
export COLOR_NC='e[0m' # No Color
export COLOR_WHITE='e[1;37m'
export COLOR_BLACK='e[0;30m'
export COLOR_BLUE='e[0;34m'
export COLOR_LIGHT_BLUE='e[1;34m'
export COLOR_GREEN='e[0;32m'
export COLOR_LIGHT_GREEN='e[1;32m'
export COLOR_CYAN='e[0;36m'
export COLOR_LIGHT_CYAN='e[1;36m'
export COLOR_RED='e[0;31m'
export COLOR_LIGHT_RED='e[1;31m'
export COLOR_PURPLE='e[0;35m'
export COLOR_LIGHT_PURPLE='e[1;35m'
export COLOR_BROWN='e[0;33m'
export COLOR_YELLOW='e[1;33m'
export COLOR_GRAY='e[1;30m'
export COLOR_LIGHT_GRAY='e[0;37m'
alias colorslist="set | egrep 'COLOR_w*'"

# less colors (also man)
export LESS_TERMCAP_mb=$'\E[01;31m'
export LESS_TERMCAP_md=$'\E[01;31m'
export LESS_TERMCAP_me=$'\E[0m'
export LESS_TERMCAP_se=$'\E[0m'
export LESS_TERMCAP_so=$'\E[01;44;33m'
export LESS_TERMCAP_ue=$'\E[0m'
export LESS_TERMCAP_us=$'\E[01;32m'

#export LESS_TERMCAP_mb=$'\E[01;31m'       # begin blinking
#export LESS_TERMCAP_md=$'\E[01;38;5;74m'  # begin bold
#export LESS_TERMCAP_me=$'\E[0m'           # end mode
#export LESS_TERMCAP_se=$'\E[0m'           # end standout-mode
#export LESS_TERMCAP_so=$'\E[38;5;246m'    # begin standout-mode - info box
#export LESS_TERMCAP_ue=$'\E[0m'           # end underline
#export LESS_TERMCAP_us=$'\E[04;38;5;146m' # begin underline


setBackground() {
  osascript -e "tell application \"iTerm\"
    set current_terminal to (current terminal)
    tell current_terminal
      set current_session to (current session)
      tell current_session
        set background color to $1
      end tell
    end tell
  end tell"
}

su() {
  ( setBackground "{15000,0,0}" & )
  ( exec su $* )
  ( setBackground "{0,0,0}" & )
}

#vim() {
#	(setBackground "{65025,65025,65025}" &)
#	(exec vim $*)
#}

if [ -f /opt/local/etc/bash_completion ]; then
      . /opt/local/etc/bash_completion
fi

# original highlight: stackoverflow.com
function highlight() {
	declare -A fg_color_map
	fg_color_map[black]=30
	fg_color_map[red]=31
	fg_color_map[green]=32
	fg_color_map[yellow]=33
	fg_color_map[blue]=34
	fg_color_map[magenta]=35
	fg_color_map[cyan]=36
	 
	fg_c=$(echo -e "\e[1;${fg_color_map[$1]}m")
	c_rs=$'\e[0m'
	sed -u s"/$2/$fg_c\0$c_rs/g"
}

# shorthand: all green, all arguments
function hl() { 
	fg_c=$(echo -e "\e[1;32m")
	c_rs=$'\e[0m'
	local d="\|";
	search=`printf "%s" "${@/#/$d}"`
	sed -u s"/$search/$fg_c\0$c_rs/g"
}





###### end of Common Aliases #####

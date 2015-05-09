# Standard Python modules
# =======================
import os
import subprocess
import sys

# DICE modules
# ============
from core.app import BasicApp


class DakotaApp(BasicApp):

    app_name = "NoNameDakotaApp"

    def __init__(self, parent, instance_name, status):
        BasicApp.__init__(self, parent, instance_name, status)

        self.dakota_files = dict()

    def register_dakota_file(self, path, var):
        self.dakota_files[path] = var
        self.signal(path)

    def dakota_exec(self, args, stdout=None, stderr=None, cwd=None):

        # Set Environment
        # ===============
        os.environ['LD_LIBRARY_PATH'] = "/home/ros/Programs/Dakota/dakota-6.1.0.Linux.x86_64/bin:/home/ros/Programs/Dakota/dakota-6.1.0.Linux.x86_64/lib"
        os.environ['PATH'] = '/home/ros/Programs/Dakota/dakota-6.1.0.Linux.x86_64/bin:/home/ros/Programs/Dakota/dakota-6.1.0.Linux.x86_64/test'

        dir_path = os.getcwd()
        os.chdir(self.current_run_path())
        f_args = [self.dice.settings.value(self, ['DAKOTA', 'dakota'])]
        f_args.extend(args)
        self.debug(f_args)
        self.debug(os.environ)
        os.environ = {
            'INSTANCE': '', 'LC_NUMERIC': 'de_DE.UTF-8', 'XDG_GREETER_DATA_DIR': '/var/lib/lightdm-data/ros', 'UPSTART_EVENTS': 'started xsession', 'XCURSOR_SIZE': '0', 'LESSOPEN': '| /usr/bin/lesspipe %s', 'XDG_VTNR': '7', 'LOGNAME': 'ros', 'USER': 'ros', 'XCURSOR_THEME': 'win8', 'PATH': '/home/ros/Programs/Dakota/dakota-6.1.0.Linux.x86_64/bin:/home/ros/Programs/Dakota/dakota-6.1.0.Linux.x86_64/test:/home/ros/Programs/Dakota/dakota-6.1.0.Linux.x86_64/bin:/home/ros/Programs/Dakota/dakota-6.1.0.Linux.x86_64/test:/home/ros/Programs/simFlow/simFlow-2.0:/home/ros/Programs/paraview/ParaView-4.3.1-Linux-64bit/bin/:/home/ros/Programs/simFlow/simFlow-2.0:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/home/ros/Programs/MATLAB/R2013b/bin:/home/ros/Programs/blender/blender-2.72b-linux-glibc211-x86_64/', 'LC_PAPER': 'de_DE.UTF-8', 'GNOME_KEYRING_CONTROL': '/run/user/1000/keyring-ri1LmO', 'PAM_KWALLET_LOGIN': '/tmp//ros.socket', 'LD_LIBRARY_PATH': ':/home/ros/Programs/Dakota/dakota-6.1.0.Linux.x86_64/bin:/home/ros/Programs/Dakota/dakota-6.1.0.Linux.x86_64/lib:/home/ros/Programs/Dakota/dakota-6.1.0.Linux.x86_64/bin:/home/ros/Programs/Dakota/dakota-6.1.0.Linux.x86_64/lib', 'KDE_FULL_SESSION': 'true', 'LANG': 'en_US.UTF-8', 'PROFILEHOME': '', 'TERM': 'xterm', 'SHELL': '/bin/bash', 'XDG_SESSION_PATH': '/org/freedesktop/DisplayManager/Session0', 'XAUTHORITY': '/tmp/kde-ros/xauth-1000-_0', 'LANGUAGE': 'en_US:en', 'SESSION_MANAGER': 'local/ros-Notebook:@/tmp/.ICE-unix/2638,unix/ros-Notebook:/tmp/.ICE-unix/2638', 'LC_MONETARY': 'de_DE.UTF-8', 'XDG_SESSION_ID': 'c2', 'MANDATORY_PATH': '/usr/share/gconf/kde-plasma.mandatory.path', 'KONSOLE_PROFILE_NAME': 'Shell', 'KDE_SESSION_VERSION': '4', 'UPSTART_INSTANCE': '', 'JOB': 'dbus', 'WINDOWID': '69206034', 'SESSIONTYPE': '', 'IM_CONFIG_PHASE': '1', 'GPG_AGENT_INFO': '/run/user/1000/keyring-ri1LmO/gpg:0:1', 'HOME': '/home/ros', 'KONSOLE_DBUS_SESSION': '/Sessions/1', 'XDG_SESSION_DESKTOP': 'kde-plasma', 'SHLVL': '1', 'KDE_SESSION_UID': '1000', 'XDG_RUNTIME_DIR': '/run/user/1000', 'LC_IDENTIFICATION': 'de_DE.UTF-8', 'LC_ADDRESS': 'de_DE.UTF-8', 'LESSCLOSE': '/usr/bin/lesspipe %s %s', 'SSH_AUTH_SOCK': '/run/user/1000/keyring-ri1LmO/ssh', 'KONSOLE_DBUS_SERVICE': ':1.1181', 'QT_PLUGIN_PATH': '/home/ros/.kde/lib/kde4/plugins/:/usr/lib/kde4/plugins/', 'GDMSESSION': 'kde-plasma', 'LC_NAME': 'de_DE.UTF-8', 'UPSTART_JOB': 'startkde', 'TEXTDOMAINDIR': '/usr/share/locale/', 'GTK2_RC_FILES': '/etc/gtk-2.0/gtkrc:/home/ros/.gtkrc-2.0:/home/ros/.kde/share/config/gtkrc-2.0', 'XDG_DATA_DIRS': '/usr/share:/usr/share/kde-plasma:/usr/local/share/:/usr/share/', 'XDG_SEAT_PATH': '/org/freedesktop/DisplayManager/Seat0', 'COLORFGBG': '15;0', 'XDG_CURRENT_DESKTOP': 'KDE', 'GS_LIB': '/home/ros/.fonts', 'SHELL_SESSION_ID': '939a493ec7e440009237262a0b8b56ee', '_': '/usr/bin/python', 'GNOME_KEYRING_PID': '2276', 'DBUS_SESSION_BUS_ADDRESS': 'unix:abstract=/tmp/dbus-TTVqd8zrxq', 'SESSION': 'kde-plasma', 'DESKTOP_SESSION': 'kde-plasma', 'UPSTART_SESSION': 'unix:abstract=/com/ubuntu/upstart-session/1000/2279', 'XDG_CONFIG_DIRS': '/etc/xdg/xdg-kde-plasma:/usr/share/upstart/xdg:/etc/xdg', 'DEFAULTS_PATH': '/usr/share/gconf/kde-plasma.default.path', 'XDG_SESSION_TYPE': 'x11', 'XDG_SEAT': 'seat0', 'OLDPWD': '/', 'GDM_LANG': 'en_US', 'LC_TELEPHONE': 'de_DE.UTF-8', 'LC_MEASUREMENT': 'de_DE.UTF-8', 'PWD': '/home/test/dice/TestProject/run/samplingExperiment_1', 'GTK_RC_FILES': '/etc/gtk/gtkrc:/home/ros/.gtkrc:/home/ros/.kde/share/config/gtkrc', 'TEXTDOMAIN': 'im-config', 'DISPLAY': ':0', 'LC_TIME': 'de_DE.UTF-8', 'LS_COLORS': 'rs=0:di=01;34:ln=01;36:mh=00:pi=40;33:so=01;35:do=01;35:bd=40;33;01:cd=40;33;01:or=40;31;01:su=37;41:sg=30;43:ca=30;41:tw=30;42:ow=34;42:st=37;44:ex=01;32:*.tar=01;31:*.tgz=01;31:*.arc=01;31:*.arj=01;31:*.taz=01;31:*.lha=01;31:*.lz4=01;31:*.lzh=01;31:*.lzma=01;31:*.tlz=01;31:*.txz=01;31:*.tzo=01;31:*.t7z=01;31:*.zip=01;31:*.z=01;31:*.Z=01;31:*.dz=01;31:*.gz=01;31:*.lrz=01;31:*.lz=01;31:*.lzo=01;31:*.xz=01;31:*.bz2=01;31:*.bz=01;31:*.tbz=01;31:*.tbz2=01;31:*.tz=01;31:*.deb=01;31:*.rpm=01;31:*.jar=01;31:*.war=01;31:*.ear=01;31:*.sar=01;31:*.rar=01;31:*.alz=01;31:*.ace=01;31:*.zoo=01;31:*.cpio=01;31:*.7z=01;31:*.rz=01;31:*.cab=01;31:*.jpg=01;35:*.jpeg=01;35:*.gif=01;35:*.bmp=01;35:*.pbm=01;35:*.pgm=01;35:*.ppm=01;35:*.tga=01;35:*.xbm=01;35:*.xpm=01;35:*.tif=01;35:*.tiff=01;35:*.png=01;35:*.svg=01;35:*.svgz=01;35:*.mng=01;35:*.pcx=01;35:*.mov=01;35:*.mpg=01;35:*.mpeg=01;35:*.m2v=01;35:*.mkv=01;35:*.webm=01;35:*.ogm=01;35:*.mp4=01;35:*.m4v=01;35:*.mp4v=01;35:*.vob=01;35:*.qt=01;35:*.nuv=01;35:*.wmv=01;35:*.asf=01;35:*.rm=01;35:*.rmvb=01;35:*.flc=01;35:*.avi=01;35:*.fli=01;35:*.flv=01;35:*.gl=01;35:*.dl=01;35:*.xcf=01;35:*.xwd=01;35:*.yuv=01;35:*.cgm=01;35:*.emf=01;35:*.axv=01;35:*.anx=01;35:*.ogv=01;35:*.ogx=01;35:*.aac=00;36:*.au=00;36:*.flac=00;36:*.m4a=00;36:*.mid=00;36:*.midi=00;36:*.mka=00;36:*.mp3=00;36:*.mpc=00;36:*.ogg=00;36:*.ra=00;36:*.wav=00;36:*.axa=00;36:*.oga=00;36:*.spx=00;36:*.xspf=00;36:', 'KDE_MULTIHEAD': 'false'
        }
        # subprocess.Popen(['/home/ros/Programs/Dakota/dakota-6.1.0.Linux.x86_64/bin/dakota', '-i', 'input.in'], env=os.environ)
        subprocess.Popen(['dakota', '-i', 'input.in'], env=os.environ)
        # result = self.run_process(f_args, stdout=stdout, stderr=stderr, cwd=cwd, env=os.environ)
        os.chdir(dir_path)
        # return result
import os
import subprocess
import json

class githubutil:

    def checkVersion():
        pass

    def fullUpdate():
        output = subprocess.check_output(['curl https://api.github.com/repos/sh4d0w28/raspberry-pi-experiments/releases/latest'], shell=True)
        release = json.loads(output.decode())

        tarball = release['tarball_url']
        tag = release['tag_name']
        comment = release['name']

        subprocess.run(['cd /home/pi/robot && wget ' + tarball + ' -O - | tar -xz'], shell=True)
        dirs = os.scandir("/home/pi/robot")
        for dir in dirs:
            if dir.is_dir and dir.name.startswith("sh4d0w28"):
                subprocess.run(['cd /home/pi/robot && rm -rf work && mv ' + dir.name + ' work'], shell=True)
                subprocess.run(['echo "' + tag +'\n' + comment + '" | tee /home/pi/robot/work/release.txt'], shell=True)

if __name__=='__main__':
    githubutil.fullUpdate()
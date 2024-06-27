import subprocess

import subprocess

class monitorHelper:

    def cpu_temp(self):
        try:
            output = subprocess.check_output(['cat', '/sys/class/thermal/thermal_zone0/temp'])
            temp = int(output)
            return round(temp / 1000, 1)
        except IndexError as e:
            return ""
        except subprocess.CalledProcessError as e:
            print(e.output)
            return ""

    def docker_stat(self):
        try:
            output = subprocess.check_output(['docker', 'stats', '--no-stream', '--format', 'json'])
            decoded_data = output.decode('utf-8')
            json_objects = decoded_data.strip().split('\n')
            return json_objects
        except IndexError as e:
            return ""
        except subprocess.CalledProcessError as e:
            print(e.output)
            return ""
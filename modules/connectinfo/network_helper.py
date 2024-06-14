import subprocess

class networkHelper:

    def getWifiSsid():
        try:
            output = subprocess.check_output(['/usr/sbin/iwgetid'])
            wifissid = str(output).split('"')[1]
            return wifissid
        except IndexError as e:
            return ""
        except subprocess.CalledProcessError as e:
            print(e.output)
            return ""

    def getNgrokIp():
        resultUrl = {
            "tcpurl" : "",
            "httpurl": ""
        }
        try:
            output = subprocess.check_output(['curl http://127.0.0.1:4040/api/tunnels | jq ".tunnels[].public_url"'], shell=True)
            urls = output.splitlines()
            for url in urls:
                cleanurl = url.strip(b'"') 
                if cleanurl.startswith(b'tcp'):
                    resultUrl['tcpurl'] = cleanurl
                if cleanurl.startswith(b'https'):
                    resultUrl['httpurl'] = cleanurl.replace(b".ngrok.io", b"")
        except IndexError as e:
            return resultUrl
        except subprocess.CalledProcessError as e:
            print(e.output)
            return resultUrl
            
        return resultUrl

    def getExtIp():
        try:
            output = subprocess.check_output(['hostname', '-I'])
            localip = str(output).split(' ')[0].split("'")[1]
            return localip
        except IndexError as e:
            return ""
        except subprocess.CalledProcessError as e:
            print(e.output)
            return ""
import subprocess

import cron.py_path
from global_settings import Settings

settings = Settings()

if __name__ == '__main__':
    for attr in dir(settings):
        if attr.startswith('_'):
            continue
        print attr, getattr(settings, attr)

    cmd = 'pfctl -a "ext_services/80" -f -'
    s = "pass in proto tcp from any to (%s) port 80\n" % settings.IF_EXT
    print "DDD", cmd, ':', s
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE,)
    print "DDD1", proc.stdin
    proc.stdin.write(s)
    proc.stdin.close()
    #out = proc.stdout.readlines()
    print "XXX", proc.stdout.readlines()




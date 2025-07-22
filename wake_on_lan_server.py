import subprocess, time, os
from datetime import datetime

def log(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

def _main():
    target_ip = os.getenv('TARGET_IP')
    target_mac = os.getenv('TARGET_MAC')

    check_interval_env = os.getenv('CHECK_INTERVAL')
    if check_interval_env is None:
        check_interval = 30
        log("CHECK_INTERVAL not defined. Using default: 30s.")
    else:
        try:
            check_interval = int(check_interval_env)
        except ValueError:
            log(f"Invalid CHECK_INTERVAL='{check_interval_env}'. Using default: 30s.")
            check_interval = 30

    if not target_ip or not target_mac:
        log("Missing variables: TARGET_IP or TARGET_MAC.")
        return

    log(f"Monitoring {target_ip} / {target_mac} every {check_interval}s")
    was_online = True

    while True:
        is_alive = subprocess.call(['ping', '-c', '1', target_ip],
                                   stdout=subprocess.DEVNULL,
                                   stderr=subprocess.STDOUT) == 0

        if is_alive:
            if not was_online:
                log(f"{target_ip} is now ONLINE.")
                was_online = True
        else:
            log(f"{target_ip} is OFFLINE. Sending WOL packet to {target_mac}")
            try:
                subprocess.Popen(['/usr/sbin/etherwake', '-b', target_mac],
                                 stdout=subprocess.PIPE)
            except Exception as e:
                log(f"Error executing etherwake: {e}")
            was_online = False

        time.sleep(check_interval)

if __name__ == '__main__':
    _main()

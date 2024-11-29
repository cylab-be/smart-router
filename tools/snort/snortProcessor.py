import subprocess
from django.utils import timezone
from dashboard.models import SnortAlert
import re

def parse_snort_alert(alert):
    print(alert)
    pattern = re.compile(
        r'(?P<timestamp>\d{2}/\d{2}-\d{2}:\d{2}:\d{2}\.\d{6})\s+\[\*\*\]\s+\[\d+:(?P<sid>\d+):\d+\]\s+(?P<alert_name>.+?)\s+\[\*\*\]\s+\[Classification:\s+(?P<classification>.+?)\]\s+\[Priority:\s+(?P<priority>\d+)\]\s+\{(?P<protocol>\w+)\}\s+(?P<src_ip>\d+\.\d+\.\d+\.\d+)(?::(?P<src_port>\d+))?\s+->\s+(?P<dest_ip>\d+\.\d+\.\d+\.\d+)(?::(?P<dest_port>\d+))?'
    )
    match = pattern.match(alert)
    if match:
        data = match.groupdict()
        data['priority'] = int(data['priority'])
        data['src_port'] = int(data['src_port'])
        data['dest_port'] = int(data['dest_port'])
        return data
    return None

def save_snort_alert(alert_data):
    SnortAlert.objects.create(
        timestamp=timezone.now(),
        alert_name=alert_data['alert_name'],
        classification=alert_data['classification'],
        priority=alert_data['priority'],
        src_ip=alert_data['src_ip'],
        src_port=alert_data['src_port'],
        dest_ip=alert_data['dest_ip'],
        dest_port=alert_data['dest_port']
    )

def run_snort(interface):
    snort_command = [
        "snort",
        "-c", "/etc/snort/snort.conf",
        "-i", f"{interface}",
        "-A", "console",
        "-l", ".",
        "--daq-dir", "/usr/lib/daq"
    ]

    process = subprocess.Popen(snort_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print("Process running Snort")
    try:
        while True:
            output = process.stdout.readline()
            if output:
                alert_data = parse_snort_alert(output.strip())
                if alert_data:
                    save_snort_alert(alert_data)
                    print(alert_data)
            elif process.poll() is not None:
                break
    except KeyboardInterrupt:
        process.terminate()
        print("Snort process terminated.")

if __name__ == "__main__":
    run_snort()
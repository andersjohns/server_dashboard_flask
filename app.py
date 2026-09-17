from flask import Flask, render_template
import psutil
import shutil
import subprocess
import time
from datetime import timedelta

app = Flask(__name__)

def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

def get_memory_usage():
    memory = psutil.virtual_memory()
    return {
        "percent": memory.percent,
        "used_gb": round(memory.used / (1024 ** 3), 2),
        "total_gb": round(memory.total / (1024 ** 3), 2)
    }

def get_disk_usage():
    disk = shutil.disk_usage("/")
    used = disk.used
    total = disk.total
    percent = round((used / total) * 100, 1)
    return {
        "percent": percent,
        "used_gb": round(used / (1024 ** 3), 2),
        "total_gb": round(total / (1024 ** 3), 2)
    }

def get_temperature():
    """
    Leser temperatur på Raspberry Pi.
    Fungerer på Raspberry Pi OS.
    Returnerer None hvis temperatur ikke kan leses.
    """
    try:
        result = subprocess.check_output(["vcgencmd", "measure_temp"]).decode("utf-8")
        # Eksempel: temp=42.8'C
        temp = result.replace("temp=", "").replace("'C", "").strip()
        return temp
    except Exception:
        return None

def get_uptime():
    uptime_seconds = time.time() - psutil.boot_time()
    return str(timedelta(seconds=int(uptime_seconds)))

@app.route("/")
def index():
    server_status = {
        "cpu": get_cpu_usage(),
        "memory": get_memory_usage(),
        "disk": get_disk_usage(),
        "temperature": get_temperature(),
        "uptime": get_uptime()
    }
    return render_template("index.html", status=server_status)

if __name__ == "__main__":
    # host=0.0.0.0 gjør at andre maskiner på nettverket kan nå Flask-appen
    app.run(host="0.0.0.0", port=8080, debug=True)

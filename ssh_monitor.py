import re
import time
from rich.console import Console
from rich.table import Table

console = Console()

log_file = "/var/log/auth.log"
pattern = re.compile(r"Failed password.*from ([\d\.]+|::1)")

# Track IP attempts
ip_counts = {}

def monitor_log():
    with open(log_file, "r") as file:
        # Move to the end of the file
        file.seek(0, 2)

        while True:
            line = file.readline()

            if not line:
                time.sleep(0.5)
                continue

            match = pattern.search(line)
            if match:
                ip = match.group(1)
                ip_counts[ip] = ip_counts.get(ip, 0) + 1

                # Display info with rich colors
                console.print(f"[bold red]Failed login from [yellow]{ip}[/yellow] - total: {ip_counts[ip]}[/bold red]")

                # Show alert if more than 3 attempts
                if ip_counts[ip] >= 3:
                    console.print(f"[bold white on red] ALERT: {ip} has {ip_counts[ip]} failed attempts! [/]")

try:
    console.print("[cyan]📡 SSH Log Monitor Started. Watching for failed login attempts...[/cyan]")
    monitor_log()
except KeyboardInterrupt:
    console.print("\n[bold green]🛑 Exiting SSH Log Monitor.[/bold green]")

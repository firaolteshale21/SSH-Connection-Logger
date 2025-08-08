import re

log_file = "/var/log/auth.log"

# New regex - matches both IPv4 and IPv6 (::1)
pattern = re.compile(r"Failed password.*from ([\d\.]+|::1)")


ip_counts = {}

with open(log_file, "r") as file:
    for line in file:
        match = pattern.search(line)
        if match:
            ip = match.group(1)
            ip_counts[ip] = ip_counts.get(ip, 0) + 1

print("\nFailed SSH login attempts by IP:\n")
for ip, count in ip_counts.items():
    print(f"{ip}: {count} attempts")

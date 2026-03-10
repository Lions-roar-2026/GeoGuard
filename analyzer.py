import csv
import geoip2.database
import os

from geoip2.errors import AddressNotFoundError

from utils.anomaly import detect_anomalies

# classify IP addresses as server/bot
CLOUD_KEYWORDS = ['amazon', 'google', 'microsoft', 'azure', 'digitalocean',
                  'hetzner', 'ovh', 'linode', 'alibaba', 'oracle', 'host']


def get_asn_org(ip, reader):
    try:
        response = reader.asn(ip)
        return response.autonomous_system_organization or "Unknown"
    except AddressNotFoundError:
        print(f"debug: ip {ip} not found in database.")
        return "Unknown"
    except ValueError:
        print(f"debug: invalid ip format: {ip}")
        return "Invalid"
    except Exception as e:
        print(f"debug: unexpected error for {ip}: {e}")
        return "Unknown"


def run_analysis(input_file, output_file):
    db_path = 'GeoLite2-ASN.mmdb'
    results = []

    if not os.path.exists(db_path):
        print(f"error: Database file '{db_path}' not found!")
        return

    print(f"Starting analysis on {input_file}...")

    with geoip2.database.Reader(db_path) as reader, \
            open(input_file, 'r') as f_in, \
            open(output_file, 'w', newline='', encoding='utf-8') as f_out:

        writer = csv.writer(f_out)
        writer.writerow(['IP address', 'Organization', 'Classification'])

        for line in f_in:
            ip = line.split('#')[0].strip()
            if not ip: continue

            org_name = get_asn_org(ip, reader)

            # check if the organization name contains any cloud/server keywords
            is_bot = any(k in org_name.lower() for k in CLOUD_KEYWORDS)
            user_type = "bot/server" if is_bot else "pc/mobile"

            results.append({'ip': ip, 'type': user_type})

            writer.writerow([ip, org_name, user_type])
            print(f"processed {ip}: {user_type}")

    print(f"success report saved to: {output_file}")

    print(f"debug: Total results length: {len(results)}")
    detect_anomalies(results, threshold=50)


if __name__ == "__main__":
    run_analysis('input_ips.txt', 'detailed_analysis_report.csv')
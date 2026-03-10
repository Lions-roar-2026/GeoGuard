import csv
import geoip2.database
import os

from geoip2.errors import AddressNotFoundError
from utils.sync import sync_db_file
from utils.anomaly import detect_anomalies

# classify ip addresses as server/bot
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
    # setup configuration for DB files
    db_configs = [
        {"source": r'C:\dbmaxmined\GeoLite2-ASN.mmdb', "dest": 'GeoLite2-ASN.mmdb'},
        {"source": r'C:\dbmaxmined\GeoLite2-Country.mmdb', "dest": 'GeoLite2-Country.mmdb'}
    ]

    # sync all databases
    print("Starting database sync...")
    for db in db_configs:
        sync_db_file(db['source'], db['dest'])

    # verify files existence
    for db in db_configs:
        if not os.path.exists(db['dest']):
            print(f"error db file {db['dest']} not found!")
            return
    results = []
    print(f"starting analysis on {input_file}...")

    with geoip2.database.Reader('GeoLite2-ASN.mmdb') as asn_reader, \
            geoip2.database.Reader('GeoLite2-Country.mmdb') as country_reader, \
            open(input_file, 'r') as f_in, \
            open(output_file, 'w', newline='', encoding='utf-8') as f_out:

        writer = csv.writer(f_out)
        writer.writerow(['ip address', 'organization', 'classification'])

        for line in f_in:
            ip = line.split('#')[0].strip()
            if not ip: continue

            org_name = get_asn_org(ip, asn_reader)
            is_bot = any(k in org_name.lower() for k in CLOUD_KEYWORDS)
            user_type = "bot/server" if is_bot else "pc/mobile"

            results.append({'ip': ip, 'type': user_type})
            writer.writerow([ip, org_name, user_type])
            print(f"Processed {ip}: {user_type}")

    print(f"Success report saved to: {output_file}")
    detect_anomalies(results, threshold=50)


if __name__ == "__main__":
    run_analysis('input_ips.txt', 'detailed_analysis_report.csv')
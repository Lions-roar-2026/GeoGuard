import csv
import geoip2.database
import os

# Keywords used to classify IP addresses as server/bot
CLOUD_KEYWORDS = ['amazon', 'google', 'microsoft', 'azure', 'digitalocean',
                  'hetzner', 'ovh', 'linode', 'alibaba', 'oracle', 'host']


def get_asn_org(ip, reader):
    """
    Retrieves the organization name associated with an IP address from the ASN database.

    Args:
        ip (str): The IP address to look up.
        reader: The geoip2 database reader object.

    Returns:
        str: The name of the organization, or 'Unknown' if not found.
    """
    try:
        response = reader.asn(ip)
        return response.autonomous_system_organization if response.autonomous_system_organization else "Unknown"
    except Exception:
        return "Unknown"


def run_analysis(input_file, output_file):
    """
    IP analysis process: reads IPs, performs lookups,
    classifies the traffic type, and saves the results to a CSV file.

    Args:
        input_file (str): Path to the input file containing IP addresses.
        output_file (str): Path to save the resulting CSV report.
    """
    db_path = 'GeoLite2-ASN.mmdb'

    if not os.path.exists(db_path):
        print(f"Error: Database file '{db_path}' not found!")
        return

    print(f"Starting analysis on {input_file}...")

    with geoip2.database.Reader(db_path) as reader, \
            open(input_file, 'r') as f_in, \
            open(output_file, 'w', newline='', encoding='utf-8') as f_out:

        writer = csv.writer(f_out)
        writer.writerow(['IP Address', 'Organization', 'Classification'])

        for line in f_in:
            ip = line.strip()
            if not ip: continue

            org_name = get_asn_org(ip, reader)

            # Check if the organization name contains any cloud/server keywords
            is_bot = any(k in org_name.lower() for k in CLOUD_KEYWORDS)
            user_type = "bot/Server" if is_bot else "pc/mobile"

            writer.writerow([ip, org_name, user_type])
            print(f"Processed {ip}: {user_type}")

    print(f"success report saved to: {output_file}")


if __name__ == "__main__":
    run_analysis('input_ips.txt', 'detailed_analysis_report.csv')
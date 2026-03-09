import geoip2.database
import os

db_path = os.path.join(os.path.dirname(__file__), '..', 'GeoLite2-ASN.mmdb')
with geoip2.database.Reader(db_path) as reader:
    # checking amazon ip from asn db
    ip = '52.94.10.1'
    response = reader.asn(ip)

    print(f"ip: {ip}")
    print(f"asn: {response.autonomous_system_number}")
    print(f"organization: {response.autonomous_system_organization}")
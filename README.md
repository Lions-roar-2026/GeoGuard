# GeoGuard
An offline tool for IP geolocation and bot detection using MaxMind GeoLite2 databases.
This project is an automated tool designed to process lists of IP addresses and enrich them with network metadata. It leverages the MaxMind GeoLite2 ASN database to perform high-speed lookups, providing detailed information about the Autonomous System Number (ASN) and the organization associated with each IP address

## Features
- **Geolocation:** Identifies the country of origin for any IP address.
- **ASN Lookup:** Identifies the organization owning the IP.
- **Bot Detection:** Automatically classifies IPs as 'bot' if they originate from known cloud service providers.

## Getting Started
1. Install requirements: `pip install geoip2`
2. Download `GeoLite2-Country.mmdb` and `GeoLite2-ASN.mmdb` from MaxMind.
3. Add your IPs to `input_ips.txt`.
4. Run: `python analyzer.py`

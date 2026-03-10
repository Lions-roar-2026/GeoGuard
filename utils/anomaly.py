def detect_anomalies(results, threshold=50):
    """
    Analyzes the list of results to detect if bot/server
    traffic exceeds a specific percentage threshold.
    """

    # check if the results list is empty to avoid division by zero.
    if len(results) == 0:
        print("no data available for anomaly detection.")
        return False

    # count the number of items classified as 'bot/Server'
    bot_count = 0
    for item in results:
        if item['type'] == 'bot/Server':
            bot_count += 1

    # calculate the percentage of bot/server traffic
    total_ips = len(results)
    bot_percentage = (bot_count / total_ips) * 100

    # pint the  report to the console
    print(f"\n--- security anomaly report ---")
    print(f"total ip's analyzed: {total_ips}")
    print(f"bot/server traffic: {bot_percentage:.2f}%")

    # check if the threshold is exceeded and trigger an alert
    if bot_percentage > threshold:
        print(f"alert: security threshold of {threshold}% exceeded!")
        print("possible automated scanning or malicious activity detected.")
        return True

    return False
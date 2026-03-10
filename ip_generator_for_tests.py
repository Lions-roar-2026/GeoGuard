import random

def generate_test_ips(filename="input_ips_2.txt", count=100):
    """Generates a random list of fake IP addresses for testing."""
    with open(filename, 'w') as f:
        for i in range(count):
            ip = f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
            f.write(ip + "\n")
    print(f"generated {count} test ips in {filename}")

if __name__ == "__main__":
    generate_test_ips()
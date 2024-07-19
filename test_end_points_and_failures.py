import requests
import time
import logging

# Configure logging to print to console
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_endpoints():
    # Test /home endpoint
    logging.info("Testing /home endpoint...")
    try:
        response = requests.get('http://localhost:5000/home')
        logging.info(f"/home response: {response.status_code} {response.text}")
    except Exception as e:
        logging.error(f"Error testing /home endpoint: {e}")

    # Test /heartbeat endpoint
    logging.info("Testing /heartbeat endpoint...")
    try:
        response = requests.get('http://localhost:5000/heartbeat')
        logging.info(f"/heartbeat response: {response.status_code}")
    except Exception as e:
        logging.error(f"Error testing /heartbeat endpoint: {e}")

    # Test /rep endpoint
    logging.info("Testing /rep endpoint...")
    try:
        response = requests.get('http://localhost:5000/rep')
        logging.info(f"/rep response: {response.status_code} {response.text}")
    except Exception as e:
        logging.error(f"Error testing /rep endpoint: {e}")

    # Simulate server failure
    logging.info("Simulating server failure by removing server1...")
    try:
        response = requests.delete('http://localhost:5000/rm', json={'hostnames': ['server1']})
        logging.info(f"/rm response: {response.status_code} {response.text}")
        logging.info("Waiting for load balancer to detect server failure...")
        time.sleep(10)  # Wait for the load balancer to detect the failure
    except Exception as e:
        logging.error(f"Error simulating server failure: {e}")

    # Test /home endpoint again after failure
    logging.info("Testing /home endpoint again after server failure...")
    try:
        response = requests.get('http://localhost:5000/home')
        logging.info(f"/home response after failure: {response.status_code} {response.text}")
    except Exception as e:
        logging.error(f"Error testing /home endpoint after failure: {e}")

    # Add a new server
    logging.info("Adding a new server server7...")
    try:
        response = requests.post('http://localhost:5000/add', json={'hostnames': ['server7']})
        logging.info(f"/add response: {response.status_code} {response.text}")
        logging.info("Waiting for the new server to be added...")
        time.sleep(10)  # Wait for the new server to be added
    except Exception as e:
        logging.error(f"Error adding new server: {e}")

    # Test /rep endpoint again to verify the new server was added
    logging.info("Testing /rep endpoint again after adding new server...")
    try:
        response = requests.get('http://localhost:5000/rep')
        logging.info(f"/rep response after adding new server: {response.status_code} {response.text}")
    except Exception as e:
        logging.error(f"Error testing /rep endpoint after adding new server: {e}")

if __name__ == "__main__":
    test_endpoints()

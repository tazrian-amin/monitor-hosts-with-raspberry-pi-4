# Monitor Hosts with Raspberry Pi 4

## Overview

This repository contains a Python script designed to monitor the availability of specified websites and send email notifications when any of them are unreachable. It is specifically tailored for running on a Raspberry Pi 4, making it a cost-effective and efficient solution for continuous website monitoring. Here's a breakdown of its components and functionality:

1. **Imports and Configuration**

   - Imports necessary modules like `aiohttp` for asynchronous HTTP requests, `asyncio` for asynchronous programming, `os` for environment variables, `datetime` for timestamps, and `smtplib` and `email.message` for sending emails.
   - `hosts_to_check` lists the URLs of the websites to be monitored.
   - `check_interval` defines how often (in seconds) the script checks the websites.
   - Environment variables `EMAIL`, `PASSWORD`, and `TO_EMAIL` are used for email authentication and specifying the recipient.

2. **Asynchronous Function: `check_host_reachability`**

   - This coroutine function takes a web session and a host URL as input.
   - It attempts to make an HTTP GET request to the host. If the response status is 200 (OK), the host is considered reachable; otherwise, it is deemed unreachable.
   - Exceptions (like network errors) are caught and also result in the host being marked unreachable.

3. **Asynchronous Function: `check_multiple_hosts`**

   - Creates an `aiohttp.ClientSession` to manage web requests.
   - Enters an infinite loop where it performs the following steps every `check_interval` seconds:
     - Prints the current time (as the last check time).
     - Creates asynchronous tasks to check each host's reachability.
     - `asyncio.gather` is used to run these tasks concurrently.
     - Determines if any hosts are unreachable and prints a list if there are any.
     - If there are unreachable hosts, it calls `send_notification` with this list.
     - Waits for `check_interval` seconds before the next iteration.

4. **Function: `send_notification`**

   - Takes a list of unreachable hosts as input.
   - Constructs an email message with the details of the unreachable hosts and the current time.
   - Uses `smtplib` to send an email via Gmail's SMTP server (`smtp.gmail.com`) on port 465 with SSL encryption.
   - Handles any exceptions during email sending and prints an error message if one occurs.

5. **Main Execution Block**
   - If the script is run as the main program, it calls `asyncio.run(check_multiple_hosts())` to start the monitoring loop.

## Key Features

- **Asynchronous Monitoring**: Uses `asyncio` and `aiohttp` for efficient asynchronous website checking.
- **Email Notifications**: Sends an email alert if any monitored website becomes unreachable.
- **Customizable**: Easy to configure for different websites and email settings.

## Prerequisites

- Raspberry Pi 4 set up with Raspberry Pi OS.
- Python 3.x installed.
- Internet connection for the Raspberry Pi.
- SMTP server details for sending email notifications.

## Installation

1. **Clone the Repository**

   ```pi@raspberrypi
   sudo git clone https://github.com/tazrian-amin/monitor-hosts-with-raspberry-pi-4.git
   cd monitor-hosts-with-raspberry-pi-4
   ```

2. **Install Required Packages**
   ```pi@raspberrypi
   sudo apt install python3-aiohttp
   ```

## Configuration

1. **Set Environment Variables**: You need to set your email credentials and the recipient's email as environment variables. This can be done by editing your `/etc/environment` file on your Raspberry Pi.

   Open the `/etc/environment` file in a text editor:

   ```pi@raspberrypi
   sudo nano /etc/environment
   ```

   Add the Variables:

   ```pi@raspberrypi
   EMAIL='your-email@gmail.com'
   PASSWORD='your-email-password'
   TO_EMAIL='recipient-email@gmail.com'
   ```

   **Reboot**: Changes in `/etc/environment` will be effective after a reboot.

2. **Modify Host List**: Edit the `hosts_to_check` list in the script to include the URLs of the websites you want to monitor.

## Usage

Run the script using the following command:

```pi@raspberrypi
python monitor_hosts.py
```

That's it! The script will then start monitoring the specified websites and will send an email notification if any of them are unreachable.

import aiohttp
import asyncio
import os
from datetime import datetime
from email.message import EmailMessage
import smtplib

# Configuration
hosts_to_check = ["tazrian.dev", "www.mining-sentry.com", "www.lutango.com", "pwbdesignservice.com"]
check_interval = 300  # in seconds

# Environment Variables for Sensitive Data
email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")
to_email = os.getenv("TO_EMAIL")

async def check_host_reachability(session, host):
    try:
        async with session.get(f"http://{host}", timeout=10) as response:
            if response.status == 200:
                return host, "is reachable"
            else:
                return host, "is unreachable"
    except Exception as e:
        return host, f"is unreachable due to error: {e}"

async def check_multiple_hosts():
    async with aiohttp.ClientSession() as session:
        while True:
            print(f"Last Hosts Checking time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            tasks = [check_host_reachability(session, host) for host in hosts_to_check]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            unreachable_hosts = [host for host, status in results if "is unreachable" in status]

            if unreachable_hosts:
                print(f"The following list of hosts is unavailable during the check at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}:\n{', '.join(unreachable_hosts)}")
                send_notification(unreachable_hosts)
            else:
                print(f"All hosts are available during the last check: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

            await asyncio.sleep(check_interval)
            
def send_notification(unreachable_hosts):
    msg = EmailMessage()
    msg.set_content("\n".join(unreachable_hosts) + " is unreachable. Time: " + str(datetime.now()))
    msg['Subject'] = "Unreachable Hosts Notification"
    msg['From'] = email
    msg['To'] = to_email

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(email, password)
            smtp.send_message(msg)
            print("We have sent an email to the Admin to notify the exception with details.")
    except Exception as e:
        print(f"There was an error while sending an email to the Admin about the exception occurred: {e}")

if __name__ == '__main__':
    asyncio.run(check_multiple_hosts())
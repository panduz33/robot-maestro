import os
import asyncio
from datetime import datetime
from telegram import Bot
from telegram.error import TelegramError
from robot.api import ExecutionResult, ResultVisitor
import socket
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def get_device_info():
    hostname = socket.gethostname()
    try:
        ip_address = socket.gethostbyname(hostname)
    except socket.gaierror:
        ip_address = "Unknown"
    return hostname, ip_address

async def send_telegram_message(bot, message):
    try:
        await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")
        print("[INFO] Telegram message sent successfully.")
        return True
    except TelegramError as e:
        print(f"[WARNING] Telegram API error: {e}")
    except Exception as e:
        print(f"[WARNING] Unexpected error sending Telegram message: {e}")
    return False

async def retry_send_telegram_message(bot, message, hostname, ip_address, start_time):
    retry_count = 0
    while True:
        success = await send_telegram_message(bot, message)
        if success:
            if retry_count > 0:  # Only send resolution if retry happened
                resolve_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                resolution_msg = (
                    f"✅ *Previous failure notification successfully sent!*\n"
                    f"Device: {hostname} ({ip_address})\n"
                    f"Start Time: {start_time}\n"
                    f"Resolve Time: {resolve_time}"
                )
                await send_telegram_message(bot, resolution_msg)
            break
        else:
            retry_count += 1
            print("[INFO] Telegram send failed, retrying in 30 seconds...")
            await asyncio.sleep(30)


def notify_robot_failures(output_xml_path):
    result = ExecutionResult(output_xml_path)
    result.suite.visit(ResultVisitor())

    failed_tests = []

    # Check root suite tests
    for test in result.suite.tests:
        if test.status == 'FAIL':
            failed_tests.append(f"{result.suite.name} -> {test.name}: {test.message}")

    # Check nested suites
    for suite in result.suite.suites:
        for test in suite.tests:
            if test.status == 'FAIL':
                failed_tests.append(f"{suite.name} -> {test.name}: {test.message}")

    hostname, ip_address = get_device_info()
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if failed_tests:
        message_body = "\n".join(failed_tests)
        message = (
            f"❌ *Robot Test Failed!*\n"
            f"Device: {hostname} ({ip_address})\n"
            f"Start Time: {start_time}\n\n"
            f"Failures:\n{message_body}"
        )
    else:
        message = (
            f"✅ *All Robot Tests Passed*\n"
            f"Device: {hostname} ({ip_address})\n"
            f"Start Time: {start_time}"
        )

    bot = Bot(token=TELEGRAM_TOKEN)

    # Create a fresh event loop to avoid 'event loop closed' errors
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(retry_send_telegram_message(bot, message, hostname, ip_address, start_time))
    finally:
        loop.close()

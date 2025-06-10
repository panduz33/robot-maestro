from telegram import Bot
from telegram.error import TelegramError
import socket
import os
import asyncio
import time
from datetime import datetime
from dotenv import load_dotenv

from robot.api import ExecutionResult, ResultVisitor

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

def get_device_info():
    hostname = socket.gethostname()
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
    except Exception:
        ip_address = "Unavailable"
    return hostname, ip_address

async def send_telegram_message(bot, message):
    try:
        await bot.send_message(chat_id=CHAT_ID, text=message)
        return True
    except TelegramError as e:
        print(f"[WARNING] Telegram API error: {e}")
    except Exception as e:
        print(f"[WARNING] Unexpected error sending Telegram message: {e}")
    return False

def notify_robot_failures(output_xml_path):
    result = ExecutionResult(output_xml_path)
    result.suite.visit(ResultVisitor())

    failed_tests = []
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

    while True:
        try:
            success = asyncio.run(send_telegram_message(bot, message))
            if success:
                resolve_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                resolution_msg = (
                    f"✅ *Previous failure notification successfully sent!*\n"
                    f"Device: {hostname} ({ip_address})\n"
                    f"Resolve Time: {resolve_time}"
                )
                # Optional: send resolve time as second message
                asyncio.run(send_telegram_message(bot, resolution_msg))
                break
            else:
                raise Exception("Failed to send message, will retry...")
        except Exception as e:
            print(f"[WARNING] Message send failed: {e}")
            print("[INFO] Retrying in 30 seconds...")
            time.sleep(30)  # Wait 30 seconds before retrying


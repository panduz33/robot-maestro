import asyncio
from telegram import Bot
from robot.api import ExecutionResult, ResultVisitor
import socket
import os
from dotenv import load_dotenv

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

async def send_telegram_message(message):
    bot = Bot(token=TELEGRAM_TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text=message)

def notify_robot_failures(output_xml_path):
    result = ExecutionResult(output_xml_path)
    result.suite.visit(ResultVisitor())

    failed_tests = []
    for suite in result.suite.suites:
        for test in suite.tests:
            if test.status == 'FAIL':
                failed_tests.append(f"{suite.name} -> {test.name}: {test.message}")

    hostname, ip_address = get_device_info()

    if failed_tests:
        message = f"❌ Robot Test Failed on {hostname} ({ip_address}):\n\n" + "\n".join(failed_tests)
    else:
        message = f"✅ All Robot Tests Passed on {hostname} ({ip_address})."

    try:
        loop = asyncio.get_running_loop()
        # If already in an event loop, create a task
        asyncio.create_task(send_telegram_message(message))
    except RuntimeError:
        # No event loop running, safe to use asyncio.run
        asyncio.run(send_telegram_message(message))

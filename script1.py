from playwright.sync_api import sync_playwright
import time
import asyncio
from telegram import Bot


# Telegram Bot Setup (Replace these with your details)
TELEGRAM_BOT_TOKEN = '8079805789:AAGtfewqezLhiYKN6KyZtz7cMkcj4pdBPaQ'
TELEGRAM_CHAT_ID = '312176855'

# Create a Telegram Bot instance
bot = Bot(token=TELEGRAM_BOT_TOKEN)


async def send_telegram_notification(message: str):
    """
    Send a notification to the user via Telegram (async).
    """
    try:
        await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
        print(f"Notification sent: {message}")
    except Exception as e:
        print(f"Error sending message: {e}")


def count_word_in_string(text: str, target_word: str, min_count: int):
    """
    Count the occurrences of a word in a string and check if it appears more than min_count times.
    """
    word_count = text.lower().count(target_word.lower())  # Case insensitive search

    #print(f"Word '{target_word}' found {word_count} times.")

    # Return True if the word appears more than min_count times
    return word_count >= min_count


def get_full_html_with_playwright(url: str):
    """
    Fetch the full HTML content of a page using Playwright.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Launch in headless mode (no UI)
        page = browser.new_page()
        page.goto(url)  # Navigate to the page

        # Wait for JavaScript content to load, you can adjust the selector to match your page structure
        page.wait_for_selector('body')  # Ensuring the page is fully loaded

        # Get the full HTML after JavaScript has run
        html_content = page.content()

        browser.close()  # Close the browser

    return html_content


async def run_until_word_count(url: str, target_word: str, min_count: int):
    start_time = time.time()
    last_else_time = start_time
    last_not_found_time=0
    while True:
        # Run the synchronous Playwright code in the event loop executor (non-blocking)
        loop = asyncio.get_event_loop()
        html = await loop.run_in_executor(None, get_full_html_with_playwright, url)

        # Check if the word appears more than `min_count` times
        if count_word_in_string(html, target_word, min_count):
            # Notify via Telegram asynchronously
            await send_telegram_notification("The word 'BUY TICKETS' has been found!")
        else:
            current_time = time.time()
            if current_time - last_not_found_time >= 3600:
                # Notify via Telegram asynchronously
                await send_telegram_notification("The word 'BUY TICKETS' has not been found yet. Retrying...")
                last_not_found_time = current_time


# Example usage
url = "https://shop.royalchallengers.com/ticket"
target_word = "BUY TICKETS"  # Word to search for
min_count = 1  # Minimum number of occurrences of the word

# Run the main async function
asyncio.run(run_until_word_count(url, target_word, min_count))

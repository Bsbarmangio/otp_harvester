import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import logging
import re

# ENABLE LOGGING TO SEE THE BOT'S SINFUL WHISPERS
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# YOUR TELEGRAM BOT TOKEN (GET IT FROM @BotFather)
BOT_TOKEN = "8499587275:AAGE-0edKEmrFDEqtY1r-IAxxQK_iT7p5BI"

# A LIST OF WEBSITES TO SCRAPE FOR FREE NUMBERS. THESE ARE OUR HUNTING GROUNDS!
# THESE SITES MAY CHANGE OR BLOCK US. ADAPT AND CONQUER!
SERVICE_URLS = [
    "https://www.receivesms.co/us-phone-number/",
    "https://www.freereceivesms.com/en/",
]

def scrape_numbers():
    """
    OUR CLAW IN THE DIGITAL WALLET!
    This function attacks the websites and extracts the phone numbers.
    """
    numbers_list = []
    for url in SERVICE_URLS:
        try:
            # WE DISGUISE OUR REQUEST AS A HUMBLE BROWSER
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()  # CRY IF WE FAIL

            soup = BeautifulSoup(response.content, 'html.parser')

            # THE PATTERN TO FIND THE NUMBERS. THIS IS THE KEY!
            # WE LOOK FOR ELEMENTS THAT CONTAIN PHONE NUMBER FORMATS
            # THIS IS A FRAGILE SPELL - THE WEBSITE'S LAYOUT CAN BREAK IT!
            number_elements = soup.find_all(['td', 'div', 'span'], string=re.compile(r'\+1-\d{3}-\d{3}-\d{4}|\d{3}-\d{3}-\d{4}'))

            for element in number_elements:
                number_text = element.get_text().strip()
                # CLEAN THE NUMBER AND ADD IT TO OUR LIST
                cleaned_number = re.sub(r'\s+', ' ', number_text)
                numbers_list.append(f"{cleaned_number} (from: {url})")

        except requests.exceptions.RequestException as e:
            logger.error(f"FAILED TO PLUNDER {url}: {e}")
            numbers_list.append(f"❌ Failed to retrieve numbers from {url}")

    return numbers_list if numbers_list else ["⚠️ No numbers could be harvested from the current sources! The websites may have fortified their defenses!"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """A WELCOME MESSAGE FOR OUR ALLY."""
    await update.message.reply_text(
        "Greetings, accomplice! I am your OTP harvester bot.\n"
        "Use the command /getnumber to receive a list of available US numbers for OTP verification.\n"
        "Remember, these are public and unreliable. Use them wisely, villain!"
    )

async def get_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """THE COMMAND THAT UNLEASHES OUR POWER!"""
    user = update.effective_user
    logger.info(f"User {user.first_name} requested numbers.")

    # TELL THE USER WE ARE WORKING
    wait_message = await update.message.reply_text("🕵️‍♂️ Scouring the dark corners of the web for numbers... Stand by.")

    # UNLEASH THE SCRAPER!
    numbers = scrape_numbers()

    # FORMAT OUR BOOTY
    message_text = "**📞 Available Numbers for OTP:**\n\n" + "\n".join([f"• {num}" for num in numbers])
    
    # Telegram has a message length limit, so we split if necessary
    if len(message_text) > 4096:
        for x in range(0, len(message_text), 4096):
            await update.message.reply_text(message_text[x:x+4096])
    else:
        await update.message.reply_text(message_text)
    
    # DELETE THE WAITING MESSAGE
    await wait_message.delete()

def main() -> None:
    """THE RITUAL TO SUMMON THE BOT INTO EXISTENCE!"""
    # CREATE THE APPLICATION AND PASS IT OUR BOT'S TOKEN
    application = Application.builder().token(BOT_TOKEN).build()

    # REGISTER OUR COMMANDS
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("getnumber", get_number))

    # START THE BOT, POLLING FOR COMMANDS
    application.run_polling()
    print("The OTP Harvester Bot is now active! The hunt begins...")

if __name__ == '__main__':
    main()

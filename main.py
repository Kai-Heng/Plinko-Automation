import datetime
import time
import threading
import csv
import pickle
import keyboard

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import undetected_chromedriver as uc

# Global variable to store the target balance
target_balance = None
running = True  # Flag to control execution
log_file = "plinko_log.csv"  # Log file to store bets
log_multiplier = "plinko_multiplier_log.csv"
has_cookies = False

# Global flag for pause/resume
paused = False


def toggle_pause():
    """Toggle between pause and resume."""
    global paused
    paused = not paused
    state = "Paused" if paused else "Resumed"
    print(f"{state} automation...")


def update_target():
    """Function to dynamically update the target balance."""
    global target_balance, running
    while running:
        user_input = input()
        if user_input.lower() == "stop":
            print("Stopping automation...")
            running = False
            break
        elif user_input.lower() == "p":
            toggle_pause()

        else:
            try:
                target_balance = float(user_input)
                print(f"\nNew target set: {target_balance}")
            except ValueError:
                print("Invalid input. Enter a valid number.")

def log_bet(count, bet_amount, balance):
    """Save each bet and balance to a CSV file."""
    with open(log_file, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([count, bet_amount, balance])

def log_loss(count, multiplier):
    """Log the loss event with a timestamp."""
    with open(log_multiplier, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([count, multiplier])

def track_losses(driver):
    """Track and log occurrences of loss multipliers (e.g., 0.2×)."""
    wait = WebDriverWait(driver, 8)
    
    multiplier_xpath = (By.XPATH, "//*[@id='main-content']/div[1]/div/div/div/div/div[1]/div[2]/div/div[2]/div/button")  # Modify if needed
    
    wait.until(EC.presence_of_element_located(multiplier_xpath))
    cnt = 0

    while True:
        try:
            # Find loss elements
            multiplier_el = driver.find_element(*multiplier_xpath)

            multiplier_text = multiplier_el.text.strip()

            if multiplier_text:
                cnt += 1
                log_loss(cnt, multiplier_text)  # Save to CSV
            else:
                print("⚠️ No multiplier detected (button might be empty).")

            time.sleep(1)  # Adjust frequency to reduce CPU usage

        except Exception as e:
            print(f"Loss tracking error: {e}")

def save_cookies(driver, file_path="stake_cookies.pkl"):
    """Saves cookies after manual login."""
    with open(file_path, "wb") as f:
        pickle.dump(driver.get_cookies(), f)
    print("✅ Cookies saved successfully!")

def stake_plinko_automation(cookies_file):
    # 1) Set up Selenium WebDriver
    options = uc.ChromeOptions()
    options.add_argument("--mute-audio")    
    # If you want it hidden / no UI:
    # options.add_argument("--headless")
    
    
    options.headless = False  # Run in normal mode, not headless

    driver = uc.Chrome(options=options)
    
    try:
        # 2) Go to Stake Plinko
        driver.get("https://stake.us/casino/games/plinko")

    # Load saved cookies
        try:
            with open(cookies_file, "rb") as f:
                cookies = pickle.load(f)
                for cookie in cookies:
                    driver.add_cookie(cookie)
            global has_cookies
            has_cookies = True
            print("✅ Cookies loaded successfully!")
            print("\nEnter new target balance (or type 'stop' to exit): ")

            # Refresh to apply cookies
            driver.refresh()
            time.sleep(3)
        except Exception as e:
            print("❌ No saved cookies found or error loading:", e)

        
        # 3) Pause so you can log in.
        #    Once logged in and have the Plinko page ready, press Enter in your console:
        input("🔑 Log in to your Stake account, navigate to Plinko. Then press Enter to continue...")
        if(has_cookies == False):
            save_cookies(driver)


        # 5) Wait for the essential elements
        wait = WebDriverWait(driver, 20)

        # SELECTORS (as you provided in your snippet)
        wallet_sel   = (By.XPATH, "//*[@id='svelte']/div[2]/div[2]/div[3]/div/div/div/div[2]/div/div/div/button/div/div/span[1]/span")
        betinput_sel = (By.XPATH, "//*[@id='main-content']/div[1]/div/div/div/div/div[1]/div[1]/label[1]/div/div[1]/input")
        playbtn_sel  = (By.XPATH, "//*[@id='main-content']/div[1]/div/div/div/div/div[1]/div[1]/button")

        # Wait for them to appear/be clickable
        wait.until(EC.visibility_of_element_located(wallet_sel))
        wait.until(EC.visibility_of_element_located(betinput_sel))
        wait.until(EC.element_to_be_clickable(playbtn_sel))

        loss_thread = threading.Thread(target=track_losses, args=(driver,), daemon=True)
        loss_thread.start()

        counter = 0
        while running:

            if paused:
                print("⚠️ Automation is paused. Waiting to resume...")
                time.sleep(1)
                continue

            # Grab the wallet/balance text
            wallet_el = driver.find_element(*wallet_sel)
            balance_text = wallet_el.text.strip()
            # If there's a currency symbol, remove it (e.g. '$').
            # For stake.com, it might be just a number, so skip if not needed.
            balance_text = balance_text.replace(",", "")
            
            try:
                balance = float(balance_text)
            except ValueError:
                print(f"❌ Couldn’t parse balance from '{balance_text}'. Exiting.")
                break
            
            if balance >= target_balance:
                print(f"🚨 Reached target balance: {target_balance}. Stopping...")
                break

            # 1% of current balance
            bet_amount = balance * 0.001

            if (counter % 5 == 0):
                bet_amount = balance * 0.01

            if(bet_amount < 0.01):
                bet_amount = 0.01

            
            bet_input = driver.find_element(*betinput_sel)
            play_btn  = driver.find_element(*playbtn_sel)

            # Clear input, enter new bet
            bet_input.clear()
            bet_input.send_keys(str(bet_amount))

            wait.until(lambda driver: driver.find_element(*playbtn_sel).is_enabled())

            # Click Play
            play_btn.click()

            counter += 1
            print(f"{counter}. [AutoBet] Placed bet = {bet_amount:.2f} | Current wallet approx: {balance}")
            
            log_bet(counter, bet_amount, balance)

            # Wait a bit so the site can update the new balance
            time.sleep(0.005)

    finally:
        print("🔴 Automation finished. (Close the browser manually or uncomment the quit line below.)")
        # driver.quit()  # <--- Uncomment to auto-close browser at script end

if __name__ == "__main__":
    with open(log_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Bet Number", "Bet Amount", "Wallet Balance"])  # CSV Header

    with open(log_multiplier, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Bet Number", "Multiplier"])  # CSV Header

    # Start the target update thread
    target_thread = threading.Thread(target=update_target, daemon=True)
    target_thread.start()

    # Start automation
    stake_plinko_automation("/Users/kaiheng/Documents/python-venv/stake_cookies.pkl")

    # keyboard.wait("esc")  # Keeps listening for "p" to pause/resume

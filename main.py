# main.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

def join_google_meet(meet_link: str):
    chrome_driver_path = r"C:\Webdrivers\chromedriver.exe"  # ✅ Your ChromeDriver path
    user_data_dir = r"C:\Users\shail\AppData\Local\Google\Chrome\User Data"  # ✅ Your Chrome user data
    profile_directory = "Profile 11"  # ✅ Your selected Chrome profile

    options = webdriver.ChromeOptions()
    options.add_argument(f"--user-data-dir={user_data_dir}")
    options.add_argument(f"--profile-directory={profile_directory}")
    options.add_argument("--start-maximized")
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

    print(f"🔗 Opening Meet Link: https://meet.google.com/eha-pbie-umu")
    driver.get("https://meet.google.com/eha-pbie-umu")
    time.sleep(10)

    # 🔇 Turn off Microphone
    try:
        mic_button = driver.find_element(By.XPATH, "//div[@aria-label='Turn off microphone']")
        mic_button.click()
        print("🔇 Microphone turned off.")
    except Exception as e:
        print("⚠️ Microphone button not found or already off.", e)

    # 📷 Turn off Camera
    try:
        cam_button = driver.find_element(By.XPATH, "//div[@aria-label='Turn off camera']")
        cam_button.click()
        print("📷 Camera turned off.")
    except Exception as e:
        print("⚠️ Camera button not found or already off.", e)

    # 🔕 Disable notification prompt
    try:
        not_now = driver.find_element(By.XPATH, "//span[contains(text(),'Not now')]")
        not_now.click()
        print("🔕 Disabled notifications prompt.")
    except:
        print("🔕 No notifications prompt appeared.")

    # ✅ Try to join the meeting
    try:
        ask_to_join = driver.find_element(By.XPATH, "//span[contains(text(), 'Ask to join')]")
        ask_to_join.click()
        print("🚀 Clicked 'Ask to join'")
    except:
        try:
            join_now = driver.find_element(By.XPATH, "//span[contains(text(), 'Join now')]")
            join_now.click()
            print("🚀 Clicked 'Join now'")
        except Exception as e:
            print("❌ Could not join the meeting.", e)

    # Wait inside the meeting
    time.sleep(60)
    driver.quit()

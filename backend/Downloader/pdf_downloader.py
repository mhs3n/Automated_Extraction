from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import os

# Get the script directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Set up Chrome options with user profile
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("user-data-dir=/home/Ray/selenium_profile")
chrome_options.add_argument("profile-directory=Profile 1")
chrome_options.add_argument("--disable-web-security")
chrome_options.add_argument("--disable-site-isolation-trials")
chrome_options.add_argument("--allow-running-insecure-content")
chrome_options.add_argument("--disable-features=IsolateOrigins,site-per-process")

# Set download directory
chrome_options.add_experimental_option("prefs", {
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": False
})

# File paths for tracking seen numbers and last downloaded position
seen_numeros_file = os.path.join(script_dir, "seen_numeros.txt")
last_downloaded_file = os.path.join(script_dir, "last_downloaded.txt")

# Load seen numeros from file
if os.path.exists(seen_numeros_file):
    with open(seen_numeros_file, "r") as f:
        seen_numeros = set(line.strip() for line in f if line.strip())
else:
    seen_numeros = set()

# Load last downloaded position
if os.path.exists(last_downloaded_file):
    with open(last_downloaded_file, "r") as f:
        last_downloaded = f.read().strip().split(",")
        last_year = last_downloaded[0] if last_downloaded else None
        last_journal = int(last_downloaded[1]) if len(last_downloaded) > 1 else 1
else:
    last_year = None
    last_journal = 1

# Launch Chrome
driver = webdriver.Chrome(options=chrome_options)
driver.get('http://www.iort.gov.tn/WD120AWP/WD120Awp.exe/CTX_5188-50-iZdJWgygIC/RechercheAnnonceNumero/SYNC_1510360320')

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'A32')))

# Define years to download
years_to_download = ['2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023']
for year in years_to_download:
    if last_year and int(year) < int(last_year):
        continue  # Skip years already completed


    select_year_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'A32')))
    Select(select_year_element).select_by_visible_text(year)
    print(f"Selected year: {year}")

    for journal_number in range(last_journal, 999):
        formatted_journal_number = f"{journal_number:03}"
        journal_number_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'A30')))
        journal_number_input.clear()
        journal_number_input.send_keys(formatted_journal_number)

        go_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'z_A5_IMG')))
        go_button.click()
        time.sleep(3)

        # Extract "Numéro" from page
        try:
            numero_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="A6_1"]/table/tbody/tr[10]/td[2]')))
            numero_text = numero_element.text.strip()

            if numero_text in seen_numeros:
                print(f"Skipping duplicate Numéro {numero_text} for {year}-{formatted_journal_number}")
                continue  # Skip download

            # Save processed Numéro immediately
            seen_numeros.add(numero_text)
            with open(seen_numeros_file, "a") as f:
                f.write(numero_text + "\n")

        except:
            print(f"Could not find Numéro for {year}-{formatted_journal_number}. Skipping.")
            continue

        # Attempt to download the PDF
        try:
            download_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, 'z__1_A29_IMG')))
            ActionChains(driver).move_to_element(download_button).click().perform()
            print(f"Downloading PDF {formatted_journal_number} for year {year}...")

            time.sleep(5)  # Wait for download to complete

            # Save last downloaded position
            with open(last_downloaded_file, "w") as f:
                f.write(f"{year},{journal_number}")

        except:
            print(f"No download button for journal {formatted_journal_number} in year {year}.")
            break

    last_journal = 1  # Reset journal number for the next year
    seen_numeros.clear()
    with open(seen_numeros_file, "w") as f:
        pass  # Empty the file



print("Download process completed.")
driver.quit()

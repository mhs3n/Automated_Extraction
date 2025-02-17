# PDF Downloader

This script automates the downloading of PDFs from the Journal Officiel de la République Tunisienne website. It navigates through the website using Selenium, selects years and journal numbers, extracts unique "Numéro" values, and downloads the corresponding PDFs.

## How It Works

### Browser Setup:
- Uses Google Chrome with a pre-configured user profile (Profile 1) to allow downloads without pop-ups.
- Disables certain security features to enable seamless interaction with the website.

### Duplicate Check:
- Extracts the "Numéro" from each journal.
- If the number has already been processed (stored in `seen_numeros.txt`), the script skips the download.

### Download Logic:
- Iterates through journal numbers for selected years (2014, 2024, 2025).
- Saves the last downloaded position in `last_downloaded.txt` to resume from where it stopped.

### File Storage:
- All downloaded PDFs are stored in the designated directory.
- `seen_numeros.txt` and `last_downloaded.txt` are created in the script’s directory (`/home/Ray/Desktop/Automated_extraction/backend/Downloader/`).

## Notes
- The Chrome profile has been modified to allow automatic downloads without confirmation prompts.
- Ensure that the correct Chrome profile path is set before running the script.
- Run the script in an environment with Google Chrome and Selenium WebDriver installed.

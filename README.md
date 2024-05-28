<!-- PROJECT LOGO -->

<br />
<div align="center">
  <a href="https://github.com/pushkar708/realestate_features">
  </a>

<h3 align="center">Real Estate Data Scrapper</h3>

<p align="center">
    This is a Data scarpper built to work on a Specific Website.
    <br />
    <br />
    <a href="https://github.com/pushkar708/realestate_features/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/pushkar708/realestate_features/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>

<!-- ABOUT THE PROJECT -->

## About The Project

[![Product Name Screen Shot][product-screenshot]]()

This project is a Python-based web scraper that extracts real estate data from the website: `https://www.realestate.com.au/.` The scraper allows users to input a location and specify the information they need, such as property details, prices, and more. The scraper then navigates to the website, retrieves the relevant data, and saves it in a structured format.

### Built With

* Python
* Selenium

<!-- GETTING STARTED -->

## Getting Started

### Prerequisites

* Python
  Get a free Installation Guide at [https://www.python.org/downloads/](https://www.python.org/downloads/)

### Installation

1. Clone the repo

   ```sh
   git clone https://github.com/pushkar708/realestate_features.git
   ```
2. Install Python packages

   ```sh
   pip install -r requirements.txt
   ```
3. Enter your chrome path in `config.json`

   ```sh
   "chrome_path": = 'ENTER YOUR CHROME PATH'
   ```

   Example:-

   ```sh
   "chrome_path": "C:\\Program Files\\Google\\Chrome\\Application/chrome.exe"
   ```

<!-- USAGE EXAMPLES -->

## Usage

### Close all existing chrome tabs (Required)

### Open a Terminal:

<ul>
<li>Locate and open a terminal application on your computer.</li>
</ul>

### Navigate to the Directory:

<ul>
<li>Use the cd command to change the current working directory to the location of your Python script.</li>
</ul>

### Run the Python Script:

<ul>
<li>In the terminal, execute the command python UI.py to run your Python script.</li>
</ul>

### Interact with the Tkinter Window:

<ul>
<li>After running the script, a Tkinter window will open, displaying the Chrome browser path and checkboxes for the user to select which elements to fetch from the website.</li>
</ul>

### Interact with the Chrome Window:

<ul>
<li>Upon populating the tkinter window and clicking the submit button, a new Chrome window will open displaying a popup containing the website URL. The user can copy the URL from this popup or visit the website manually. After the website loads, the user must choose from the following options: 
<ul>
<li>Buy (Properties available for purchase)</li>
<li>Rent (Properties available for rent)</li>
<li>Sold (Properties already sold)</li>
</ul>

[![Product Name Screen Shot][website-screenshot]]()

<li>After selecting an option, the user must enter the desired location in the text box to fetch or scrape the data.</li>
<li>Once the website lists the properties, the scraper will automatically retrieve the URLs from the current page (supporting up to 25 at a time) and gather the necessary data in a separate tab.</li>
<li>After scraping the URLs, the window will return to the original listings. The user can then choose another page to scrape without reconfiguring the settings.</li>
<li>The scraper will remain idle in the background until the user requests another page to be scraped.</li>
<li>When the user decides to stop, they will manually close the Chrome window, and the scraper will process the data into an Excel file and a JSON file.</li>

<!-- ROADMAP -->

## In Case of blank screen
If a blank screen appears after copying and visiting the URL, follow these steps:

1. Open another tab (In the same chrome).
2. Paste the url the this tab and press Enter.
3. Once the website loads in the new tab, close this tab and return to the original tab.
4. Reload the original tab, and the scraper will now be connected to this tab.

## Roadmap

- [X] Automatic Data scrapper
- [X] Supports input for data to be scrapped by user
- [X] Supports 25 listings at a time
- [X] Scrape information about each property
- [X] Saves the scrapped data into multiple formats
- [X] Keeps itself idle untill user asks
- [X] Can scrape data for all 3 types (Buy, Rent, Sold)
  - [X] Saves all 3 format in seperate sheets (Excel)

<!-- CONTACT -->

## Contact

Pushkar Agarwal - pushkar2agarwal@gmail.com

Project Link: [https://github.com/pushkar708/realestate_features](https://github.com/pushkar708/realestate_features)

<!-- MARKDOWN LINKS & IMAGES -->

<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[product-screenshot]: images/screenshot.png
[website-screenshot]: images/website.png

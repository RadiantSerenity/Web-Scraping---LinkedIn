# LinkedIn Job Listings Scraper

## Introduction

This repository contains a Python script for web scraping job listings from LinkedIn. It's designed to extract detailed information about Data Science job listings in Barcelona and its proximity, organizing the data into a CSV file. This project showcases how to leverage Python libraries for web scraping and data manipulation to gather valuable insights from public job postings on LinkedIn.

## Features

The script automates the collection of the following information from LinkedIn job listings:
- Job ID
- Job Title
- Company Name
- Location
- State
- Posting Date
- Offer URL
- Number of Applicants
- Seniority Level
- Python Requirement
- SQL Requirement

The collected data is saved into a CSV file, providing a structured dataset of job listings for further analysis or review.

## Prerequisites

To run the script, you'll need Python 3.x installed on your system along with several libraries. The required libraries include:
- `requests` for making HTTP requests
- `BeautifulSoup` (part of `bs4`) for parsing HTML content
- `numpy` for numerical operations
- `pandas` for data manipulation and exporting to CSV

Install the required libraries using the following command:

```bash
pip install requests beautifulsoup4 numpy pandas

## Disclaimer

This script is provided for educational and informational purposes only. Web scraping can violate the terms of service of some websites, including LinkedIn.
Users should operate the script responsibly and adhere to LinkedIn's terms of service. It's recommended to use official APIs for data collection when available and ensure compliance
with legal and ethical standards.

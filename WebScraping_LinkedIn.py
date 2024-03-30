"""
### Web Scraping with Python - LinkedIn

!!Attention!!: This python code creates a CSV-file with various information on LinkedIn job listings. 
The CSV-file will be saved in your current working directory. 
If you cannot find it, check your base directory or your current working directory


"""

import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import time
import re
import os

# We provide information about which is the current working directory on the computer.
# In the current working directory the CSV-file that is created through this code will be saved.

print(f"The CSV-file, that is produced, will be saved in the current working directory.\nThe following is the current working directory: {os.getcwd()} \nPlease navigate to the current working directory in order to find the produced CSV-file.")
print("Please check your base directory if the CSV-file is not in your current working directory.")

# list with the infomration catgeories we want to scrape for every Data Science job listing in Barcelona (or close proximity)

information_catgeories = ["Job ID", "Job Title", "Company Name", "Location", "State", "Posting Date", "Offer URL", "Number of Applicants",
                          "Seniority", "Python Required", "SQL Required"]

# In this first function, we scrape all the Data Science job listings in Barcelona (and in close proximity of it)
# from Linkedin using the request and the bs4 libraries.

# With regrad to the bs4 libaray we rely on the BeautifulSoup class and create object from this blueprint.

def scraping_linkedin_for_needed_info():
    
    # by changing pageNum=0 to for example pageNum=1 in the link below we can access the second page of Data Science job listings instead 
    # of the first page
    url = 'https://www.linkedin.com/jobs/search?keywords=Data%20Scientist&location=Spain%20Catalonia%20Barcelona&pageNum=0'
    response = requests.get(url)
    
    if response.status_code == 200:
        
        soup = BeautifulSoup(response.text, 'html.parser')
        job_listings = soup.find_all('div', {'class':'job-search-card'})
        
    else:
       print("Failed to fetch job listings. Please try again.")
       
    return job_listings

# we continue to work with the returned object of class "bs4.element.ResultSet"
# this object was assigned to the variable called "job_listings_fetched"
job_listings_fetched = scraping_linkedin_for_needed_info()
#print(type(job_listings_fetched))

#for job in job_listings_fetched:
    #print(job)
    #break

# Below we have the function called "detailed_job_posting" which returns the content of the "detailed job posting" 
# site of a respective job. This content is needed afterward.

def detailed_job_posting(job_url):
    
    # We make a request to the job details page of the respective "job card" and create a new, second BeautifulSoup object.
    # In order to do that we use the url of the detailed job posting/page which is provided by the related "job card",
    # respectively by the related "job-search-card".
    # This url is an input into this function.
    
    job_details_response = requests.get(job_url)
    job_details_soup = BeautifulSoup(job_details_response.text, 'html.parser')
    
    # We use the sleep method in order to pause briefly after we have scraped a detailed job description.
    # This is done in order to avoid being caught and blocked by LinkedIn.
    # LinkedIn can block you if it caughts you scrapping.
    
    time.sleep(0.1)
    
    return job_details_soup

# The function below helps to extract the job ID based on the respective job listings link which was extracted before.
# Given that such a link alwayas has the same structure we can use the .split() method and regular expresions to extract the actual job ID 
# in a reliable way from the provided Link.

def get_job_id_from_url(job_url):
    
    try:
        job_url_short = job_url.split("?refId")[0]  # Only consider the part of the URL before "?refId"
        job_id = re.search(r'\d{10}', job_url_short).group()  # Find a sequence of 10 digits --> Job ID
        return int(job_id)  # Convert job_id to integer to ensure it's a pure number
    
    except (AttributeError, ValueError, IndexError):
        return np.nan

# We create a function called "python_required(job_details_soup)" that deals with the respective detailed job posting
# and returns either true if Python is requried in the job description or false if Python is not required.
# The detailed job posting is accessed using the link/url of this detailed job positing.
# The url of the detailed job posting was previously extracted using the job card, respectievly the respective, retrived "job-search-card".

def python_required(_detailed_job_posting_):
    
    # job describtion is accessed
    if _detailed_job_posting_.find('div', {'class': 'description__text'}) is not None:
        job_description = _detailed_job_posting_.find('div', {'class': 'description__text'}).get_text(strip=True)
    else:
        return(np.nan)
    
    if job_description is not None: 
        python_required = 'python' in job_description.lower()
        return python_required
    else:
        return(np.nan)
   
# We create a function called "SQL_required(job_details_soup)" that deals with the respective detailed job posting
# and returns either True if SQL is requried in the job description or False if SQL is not required.
# The detailed job posting is accessed using the link/url of this detailed job positing.
# The url of the detailed job posting was previously extracted using the job card, respectievly the respective, retrived "job-search-card".  
   
def SQL_required(_detailed_job_posting_):
    
    # job describtion is accessed
    if _detailed_job_posting_.find('div', {'class': 'description__text'}) is not None:
        job_description = _detailed_job_posting_.find('div', {'class': 'description__text'}).get_text(strip=True)
    else:
        return(np.nan)
    
    if job_description is not None: 
        SQL_required_ = 'sql ' in job_description.lower()
        return SQL_required_
    else:
        return(np.nan)

# We create a function called "get_seniority(job_details_soup)" that deals with the respective, detailed job 
# posting and extracts the seniority level required for the job.
# The detailed job posting is accessed using the link/url of this detailed job positing.
# The url of the detailed job posting was previously extracted using the job card, respectievly the respective, retrived "job-search-card".

def get_seniority(_detailed_job_posting_):
    
    # Find the job description section
    criteria_section = _detailed_job_posting_.find("ul", {"class": "description__job-criteria-list"})
    #print(criteria_section)
    
    # Check if the criteria list exists
    if criteria_section:
        # Find all 'li' elements within the 'ul' list
        for criteria_item in criteria_section.find_all("li", class_="description__job-criteria-item"):
            # The criteria title is in a 'h3' tag
            criteria_title = criteria_item.find("h3", class_="description__job-criteria-subheader").get_text(strip=True)
        
            # Check if the criteria title contains any known indicator of seniority level
            seniority_indicators = ["seniority level", "nivel de antigüedad"]
            if any(indicator in criteria_title.lower() for indicator in seniority_indicators):
                # The seniority level is in the 'span' tag
                seniority_level = criteria_item.find("span", class_="description__job-criteria-text").get_text(strip=True)
                seniority_level = seniority_level.lower()
                #print(seniority_level)
                if type(seniority_level) == "string":
                    seniority_level = seniority_level.lower()
                    return(adjust_seniority(seniority_level))
                else:
                    return(adjust_seniority(seniority_level))
    else:
        # in case there is no value provided (None is received) we add a numpy NAN
        return(adjust_seniority(np.nan))
    
# After we have extracted seniority from LinkedIn using the function above, we now make sure that we 
# always have the right seniority levels in English no matter whether we actually retrive them in
# English or Spanish.
# This function is called by the one above.

def adjust_seniority(seniority_extracted):
    if (seniority_extracted == "internship" or seniority_extracted  == "pasantía"):
        return "Internship"
    elif (seniority_extracted == "entry level" or seniority_extracted == "sin experiencia"):
        return "Entry Level"
    elif (seniority_extracted == "associate" or seniority_extracted == "intermedio"):
        return "Associate"
    elif (seniority_extracted == "mid-senior level" or seniority_extracted == "algo de responsabilidad"):
        return "Mid-senior Level"
    elif (seniority_extracted == "director"):
        return "Director"
    elif (seniority_extracted == "executive"):
        return "Executive"
    elif (seniority_extracted == "not applicable" or seniority_extracted == "no corresponde"):
        return "Not Applicable"
    else:
        return(np.nan)
    
    
# In the functio below we deal with the state of the Linkedin job posting.
# We translate the received information to phrases that are easier to interpret for humans

def deal_with_state(job):
    try:
        if (job.find('span', {"class":'result-benefits__text'})):
            state = job.find('span', {"class":'result-benefits__text'}).text.strip()
            if state == "Be an early applicant":
                return "Early Applicants"
            elif state == "Actively Hiring" or state == "Actively Recruiting":
                return "On-going"
            else:
                return "Others"
        else:
            return np.nan
    except:
        return np.nan
    
# Now we want to extract the number of applicants that applied for a certain job.
# In the function below we use the link to the respective detailed job description. 
# Based on the detailed job description, we extract the number of applicants.

def get_number_of_applicants(_detailed_job_posting_, job_url):
    
    # if job_url is not None search for number of applications via the link to the detailed job description
    # otherwise return None for number of applicants because we have no link to work with

    if (type(job_url) is not None):
        
        try:
            new_url = str(job_url)
            JSON_response = requests.get(new_url)
        
            job_soup_2 = BeautifulSoup(JSON_response.text, 'html.parser')
        
        except:
            pass
        
        # Extratct the number of applicants and if that does not work we return NaN
        try:
            number_of_applicants = job_soup_2.find(class_ = "num-applicants__caption").text.strip()
            number_of_applicants_str = number_of_applicants.split(" ").pop(-2)
            number_of_applicants_int = int(number_of_applicants_str)
            #print(number_of_applicants)
            
            return number_of_applicants_int 
        
        except:
            return np.nan
    else:
        return np.nan
            
# In the next step we generate a dictionary with the needed key & value pairs so that
# we can create a dataframe in the end containing the needed information for each job listing

def handle_and_prepare_the_scraped_data(job_listings_fetched, information_catgeories):

    # we create an empty job dictionary that shall be filled as part of this function
    job_dictionary = {} 
    
    # We initilaize multiple keys for the dictionary called "job_dictionary" that corresspond to the different 
    # information categories we fetch (job title, company name, etc.) for every job listing.
    # We assign to every key an empty list that shall be filled in the following steps.
    
    for category in information_catgeories:
        job_dictionary[category] = []
        
    # We iterate through all job listings that were scrapped and assign the relevent information to the respective category/key
    # in the dictionary.
    
    # The .strip() method is used to remove any unnecessary leading or trailing whitespaces.
    
    for job in job_listings_fetched:
        
        # We extract the link to the detailed job posting which is part of the respective "job card"/"job-search-card"
        # which has been scrapped above. 
        # We need to access the detailed job posting because in the "job card"/"job-search-card" are not all needed infos provided. 
        base_link = job.find('a', class_='base-card__full-link')
        job_url = base_link['href']
        #print(job_url)
        
        # We call the function called "detailed_job_posting" which returns the content of the "detailed job posting" site.
        # This content is needed afterward.
        _detailed_job_posting_ = detailed_job_posting(job_url)
        
        #adding Job ID to the dictionary
        job_dictionary["Job ID"].append(get_job_id_from_url(job_url))
        
        # adding Job Titles to the dictionary
        if (job.find('h3', {'class': 'base-search-card__title'}) is not None):
            job_dictionary["Job Title"].append(job.find('h3', {'class': 'base-search-card__title'}).text.strip())
        else:
            # in case there is no value provided (None is received) we add a numpy NAN
            job_dictionary["Job Title"].append(np.nan)
        
        # adding Company Name to the dictionary
        if (job.find('a', {'class': 'hidden-nested-link'}) is not None):
            job_dictionary["Company Name"].append(job.find('a', {'class': 'hidden-nested-link'}).text.strip())
        else:
            # in case there is no value provided (None is received) we add a numpy NAN
            job_dictionary["Company Name"].append(np.nan)
        
        # adding Location to the dictionary
        if (job.find('span', {'class': 'job-search-card__location'}) is not None):
            job_dictionary["Location"].append(job.find('span', {'class': 'job-search-card__location'}).text.strip())
        else: 
            # in case there is no value provided (None is received) we add a numpy NAN
            job_dictionary["Location"].append(np.nan)
        
        # adding State to the dictionary   
        job_dictionary["State"].append(deal_with_state(job))
       
        # adding Posting Date to the dictionary
        time_element = job.find('time', class_='job-search-card__listdate')
        
        # extracing the datetime attribute
        #datetime_attribute = time_element['datetime'] if time_element else None
        
        # extracting the text inside the <time> element
        if time_element is not None:
            job_dictionary["Posting Date"].append(time_element.get_text(strip=True))
        else: 
            # in case there is no value provided (None is received) we add a numpy NAN
            job_dictionary["Posting Date"].append(np.nan)
        
        # adding Offer URL to the dictionary 
        anchor_tag = job.find('a', class_='base-card__full-link')
        href_link = anchor_tag['href']
        
        if (job.find('a', class_='base-card__full-link') is not None):
            
            # we extract the link of the job posting going from the base_card to the href (hyper reference), repsectievly the link of the
            # respective job posting
            base_link = job.find('a', class_='base-card__full-link')
            href_link = base_link['href']
            
            # we add the link to the job_dictionary
            job_dictionary["Offer URL"].append(href_link)
            
        else: 
            # in case there is no value provided (None is received) we add a numpy NAN
            job_dictionary["Offer URL"].append(np.nan)
            
        # adding Number of Applicants to the dictionary   
        # in case there is no value provided (None is received) we add a numpy NAN
        job_dictionary["Number of Applicants"].append(get_number_of_applicants(_detailed_job_posting_, job_url))

        # adding Seniority to the dictionary
        # In order to do that we call the function called "get_seniority" and extract the seniority out 
        # of the detailed job posting which was already called with a get request above.
        
        job_dictionary["Seniority"].append(get_seniority(_detailed_job_posting_))

            
        # adding whether Python is required ("Python Required") for a certain job to the dictionary
        # In order to do that we call the function called "python_required(job_details_soup)" and extract out of the job 
        # description, which is part of the detailed job posting which was already called with a get request above, whether Pyton
        # is required or not, respectievly whether Python is in the job description as keyword or not.
        job_dictionary["Python Required"].append(python_required(_detailed_job_posting_))
        
        # adding whether SQL is required ("SQL Required") for a certain job to the dictionary
        # In order to do that we call the function called "sql_required(job_details_soup)" and extract out of the job 
        # description, which is part of the detailed job posting which was already called with a get request above, whether SQL
        # is required or not, respectievly whether SQL is in the job description as keyword or not.
        job_dictionary["SQL Required"].append(SQL_required(_detailed_job_posting_))
        
    # debugging
    #for category in information_catgeories:
        #print(f"{category}: {len(job_dictionary[category])}")
        
    
    return job_dictionary
        
        
job_dict = handle_and_prepare_the_scraped_data(job_listings_fetched, information_catgeories)

#print(job_dict)

# In the last step we create a function that transforms our job_dictionary into a pandas DataFrame

def create_pandas_dataframe_based_on_dictionary(job_dict):
    
    # based on the dictionary created above we create a dataframe, respectievly the dictionary is transformed into a dataframe
    df_job_listings = pd.DataFrame(job_dict)

    # In case there are still missing values that were not replaced by a numpy nan above, they shall be replaced by a numpy nan at this point.
    df_job_listings = df_job_listings.replace("", np.nan)
    
    # We dont want to have an index in the exported dataframe so we get rid of the index
    # and export the dataframe as CSV.
    # we also make sure that NaN values are correctly indicated
    
    df_job_listings.to_csv("CSV_file_Assignment_2_Team_6_Section_A.csv", index = False, na_rep='NaN')
    
    
    return df_job_listings
    
df = create_pandas_dataframe_based_on_dictionary(job_dict)



"""
Task 3

Collecting anniversaries from Wikipedia
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

import re
from bs4 import BeautifulSoup
from filter_urls import find_urls, find_articles

# Month names to submit for, from Wikipedia:Selected anniversaries namespace
months_in_namespace = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]


def extract_anniversaries(html: str, month: str) -> list[str]:
    """Extract all the passages from the html which contain an anniversary, and save their plain text in a list.
        For the pages in the given namespace, all the relevant passages start with a month href
         <p>
            <b>
                <a href="/wiki/April_1" title="April 1">April 1</a>
            </b>
            :
            ...
        </p>

    Parameters:
        - html (str): The html to parse
        - month (str): The month in interest, the page name of the Wikipedia:Selected anniversaries namespace

    Returns:
        - ann_list (list[str]): A list of the highlighted anniversaries for a given month
                                The format of each element in the list is:
                                '{Month} {day}: Event 1 (maybe some parentheses); Event 2; Event 3, something, something\n'
                                {Month} can be any month in the namespace and {day} is a number 1-31
    """
    
    # parse the HTML
    soup = BeautifulSoup(html, 'html.parser')

    # Get all the paragraphs:
    paragraphs = soup.find_all('p')

    # Filter the passages to keep only the highlighted anniversaries
    ann_list = []

    # Find special anniversaries through finding the ones with links
    pattern = rf'<p>.*?<a href="/wiki/{month}_(\d+)".*?title="{month} \1">{month} \1'
    
    # Filter the paragraphs to find the anniversaries, and saving them to a list
    for paragraph in paragraphs:
        text = paragraph.get_text()
        match = re.search(pattern, str(paragraph), flags=re.IGNORECASE)
       
        if match and len(text.split())<3:
            ann_list.append(text.strip())
    

    print(ann_list)
    return ann_list

if __name__ == "__main__":
    # Test code
    text = """
            <p></p>
            <p>Nothing about a month here</p>
            <p>October 3:</p>
            <p><a href="/wiki/October_1" title="October 1">October 1</a></p>
            <p><b><a href="/wiki/October_19" title="October 19">October 19</a></b></p>
            <p>Text that should not be there<b><a href="/wiki/October_10" title="October 10">October 10</a></b></p>
            <p><a href="October_29" title="October 29">October 29</a></p>
            <table>
            </table>
    """
    ann = extract_anniversaries(text, 'October')
    sol = ["October 1", "October 19"]
    print(sol)



def anniversary_list_to_df(ann_list: list[str]) -> pd.DataFrame:
    """Transform the list of anniversaries into a pandas dataframe.

    Parameters:
        ann_list (list[str]): A list of the highlighted anniversaries for a given month
                                The format of each element in the list is:
                                '{Month} {day}: Event 1 (maybe some parenthesis); Event 2; Event 3, something, something\n'
                                {Month} can be any month in months list and {day} is a number 1-31
    Returns:
        df (pd.Dataframe): A (dense) dataframe with columns ["Date"] and ["Event"] where each row represents a single event
    """
    raise NotImplementedError("remove me to begin task")

    # Store the split parts of the string as a table
    ann_table = ...
    # Headers for the dataframe
    headers = ["Date", "Event"]
    df = ...
    return df


def anniversary_table(
    namespace_url: str, month_list: list[str], work_dir: str | Path
) -> None:
    """Given the namespace_url and a month_list, create a markdown table of highlighted anniversaries for all of the months in list,
        from Wikipedia:Selected anniversaries namespace

    Parameters:
        - namespace_url (str):  Full url to the "Wikipedia:Selected_anniversaries/" namespace
        - month_list (list[str]) - List of months of interest, referring to the page names of the namespace
        - work_dir (str | Path) - (Absolute) path to your working directory

    Returns:
        None
    """
    raise NotImplementedError("remove me to begin task")

    # Loop through all months in month_list
    # Extract the html from the url (use one of the already defined functions from earlier)
    # Gather all highlighted anniversaries as a list of strings
    # Split into date and event
    # Render to a df dataframe with columns "Date" and "Event"
    # Save as markdown table

    work_dir = Path(work_dir)
    output_dir = work_dir / "tables_of_anniversaries"

    for month in month_list:
        page_url = ...
        html = ...
        # Get the list of anniversaries
        ann_list = ...

        # Render to a dataframe
        df = ...

        # Convert to an .md table
        table = ...

        # Save the output
        ...


if __name__ == "__main__":
    # make tables for all the months
    work_dir = ...
    namespace_url = "https://en.wikipedia.org/wiki/Wikipedia:Selected_anniversaries/"
    ...



 #pattern = rf'<p><.*?/wiki/{month}_\d+" title="{month} \d{1,2}">{month} \d{1,2}</a>'
    #pattern = rf'<a href="/wiki/{month}_{day}" title="{month} {day}">{month} {day}</a>'

    # pattern = rf'<p><.*?/wiki/{month}_\d+" title="{month} \d{1,2}">{month} \d{1,2}</a>'
    
    # pattern = rf'<p><[a-zA-Z0-9=":;\s]*\bhref="/wiki/{month}_\d+".*?>{month}\b'




            

    # for paragraph in paragraphs:
    #     text = paragraph.get_text()
    #     #print(text.strip())
    #     text_list.append(text.strip())

    # for article in articles:
    #     for text in text_list:
    #         if month in article:
    #             print(article)
        
    #         #ann_list.append(text.strip())
"""
Task 3

Collecting anniversaries from Wikipedia
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

import os
import re
from bs4 import BeautifulSoup
from filter_urls import find_urls, find_articles
from requesting_urls import get_html

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
        
        if match:
            # print(text)
            parts = re.split(rf"(?<={month})", text)
            # print('parts')
            # print(parts)
            if len(parts[0])<10:
                ann_list.append(text.strip())
    

    # print(f'LIST: {ann_list}')
    return ann_list



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
    # Store the split parts of the string as a table
    ann_table = []
    
    # Headers for the dataframe
    headers = ["Date", "Event"]
    
    # regex for split ;
    event_split = r';(?![^(]*\))'

    # Iterate through each entry in the aniversary list
    for ann in ann_list:
        #print(f'Anniversary is {ann}')

        # Splitting the string into date and event parts
        date_part, _, event_part = ann.partition(':')
        date_part = date_part.strip()

        # print(f'DATE PART IS {date_part}')
        # print(f'EVENT PART IS {event_part}')

        # If there is no event part, skip 
        if not event_part.strip():
            continue

        # For events on the same date
        # Split the event part into individual events, ignoring semicolons within parentheses
        events = re.split(event_split, event_part)
        #print(events)
        
        for event in events:
            event = event.strip()
            if event:  # Only append if there is an event
                ann_table.append([date_part, event])

    # Create a DataFrame from the ann_table list
    df = pd.DataFrame(ann_table, columns=headers)
    
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
    
    #print(f'NAME SPACE URL {namespace_url} \n')

    # Loop through all months in month_list
    # Extract the html from the url (use one of the already defined functions from earlier)
    # Gather all highlighted anniversaries as a list of strings
    # Split into date and event
    # Render to a df dataframe with columns "Date" and "Event"
    # Save as markdown table

    work_dir = Path(work_dir)
    output_dir = work_dir/"tables_of_anniversaries"

    # Create the directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True) 

    for month in month_list:
        #print(month)
        page_url = f"{namespace_url}{month}"
        html = get_html(page_url)
        
        # Get the list of anniversaries
        ann_list = extract_anniversaries(html, str(month))
        #print(ann_list)

        # Render to a dataframe
        df = anniversary_list_to_df(ann_list)
        #print(df)

        # Convert to an .md table
        table = df.to_markdown(index=False)
        
        # Save the output
        output_file = output_dir/f"anniversaries_{month.lower()}.md"
        with open(output_file, 'w') as outfile:
            outfile.write(table)


if __name__ == "__main__":
    # make tables for all the months
    work_dir = Path(__file__).parent.absolute()
    namespace_url = "https://en.wikipedia.org/wiki/Wikipedia:Selected_anniversaries/"
    test = anniversary_table(namespace_url, months_in_namespace, work_dir)



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
    #ann = extract_anniversaries(text, 'October')
    #sol = ["October 1", "October 19"]
    #print(sol)



if __name__ == "__main__":
    # Test code
    sample_list = [
    "May 19: The creator has birthday! ; Beautiful day\n",
    "December 1: just a beautiful day (always?); Winter is coming (No daylight past 15:00)",
    "November 2: ",
    "October 1",
    "June 3: Another beautiful day; hmmm, (1999)\n",
    "May 3: Just an exuse to put ugly character in test 35$56781-dg///c.*@",
]
    #res_df = anniversary_list_to_df(sample_list)

    #print(res_df)


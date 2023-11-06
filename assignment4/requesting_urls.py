"""
Task 1.1 - requesting HTML documents with HTTP
"""
from __future__ import annotations

import requests
from pathlib import Path


def get_html(url: str, params: dict | None = None, output: str | None = None):
    """Get an HTML page and return its contents.

    Args:
        url (str):
            The URL to retrieve.
        params (dict, optional):
            URL parameters to add.
        output (str, optional):
            (optional) path where output should be saved.
    Returns:
        html (str):
            The HTML of the page, as text.
    """

    # current_dir = Path(__file__).parent.absolute()
    # passing the optional parameters argument to the get function
 
    response = requests.get(url, params=params)

    
    if response.status_code == 200:
        #print('Requesting url. Success!')
        html_str = response.text

        if output:
            # if output is specified, the request url and text content are written
            # to the file at `output`.
            # The first line should be the URL,
            # and the rest of the file should be the response contents.
            with open(output, 'w') as outfile:
                outfile.write(f'URL: {url} \n')
                outfile.write(f'{html_str}')

        return html_str
    
    else:
        print(f'An error has occurred. Could not retrieve url. Status code: {response.status_code}')

        return None


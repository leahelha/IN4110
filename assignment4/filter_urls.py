"""
Task 1.2, 1.3

Filtering URLs from HTML
"""

from __future__ import annotations

from requesting_urls import get_html
import re
from urllib.parse import urljoin, urlparse
import numpy as np

#list_of_urls = find_urls(html_str)



def find_urls(
    html: str,
    base_url: str = "https://en.wikipedia.org",
    output: str | None = None,
) -> set[str]:
    """
    Find all the url links in a html text using regex

    Arguments:
        html (str): html string to parse
        base_url (str): the base url to the wikipedia.org pages
        output (Optional[str]): file to write to if wanted
    Returns:
        urls (Set[str]) : set with all the urls found in html text
    """
    #print(html)
    # create and compile regular expression(s)
    url_pat = re.compile(r'<a\s+[^>]*href="([^"]*)"[^>]*>', flags=re.IGNORECASE)
  

    urls = set()
    print(url_pat.search(html))
    pot_match = url_pat.finditer(html) #potential matches
   
    for match in pot_match:
        url = match.group(1)
        url = re.sub(r'#.*', '', url)  #strip urls of everything after #

        if len(url)>0:   # Some of the urls end up with len = 0, we don't want these
            if not url.startswith('http'):
                if url.startswith('//'):
                    url = 'https:' + url #base_url.rstrip('/') + '/' + url.lstrip('/')
                
                if url.startswith('/'):
                    url = base_url.rstrip('/') + '/' + url.lstrip('/')
            
            urls.add(url)
       
    
    # 1. find all the anchor tags, then
    # 2. find the urls href attributes

    # Write to file if requested
    if output:
        print(f"Writing to: {output}")
        with open(output, 'w') as outfile:
            for link in urls:
            
                outfile.write(f'{link}')

   
    return urls


def find_articles(html: str, output: str | None = None) -> set[str]:
    """Finds all the wiki articles inside a html text. Make call to find urls, and filter
    arguments:
        - text (str) : the html text to parse
        - output (str, optional): the file to write the output to if wanted
    returns:
        - (Set[str]) : a set with urls to all the articles found
    """
    
    urls = find_urls(html)
    pattern = re.compile(r'https?://[^:/\s]*wikipedia[^:\s]*(?![^:]*:)')
    # pattern = re.compile(r'https?://\S*wikipedia\S*(?:(?!:).)*\b')
    # pattern = re.compile(r'https?://\S*wikipedia\S*(?![^:]*:)\b')
    wiki_pat = re.compile(r'\S*wiki\S*')
    articles = set()
    wikis = set()

    for link in urls:
        match = pattern.search(link)
        wiki = wiki_pat.search(link)
        if wiki:
            wikis.add(wiki.group(0))
        if match:
            article = match.group(0)            
            if ';' not in article: 
                articles.add(article)
    
    # Write to file if wanted
    if output:
        
        with open(output, 'w') as outfile:
            for article in articles:
                outfile.write(f'{article}\n') 
        
    
    return articles


# Regex example

def find_img_src(html: str):
    """Find all src attributes of img tags in an HTML string

    Args:
        html (str): A string containing some HTML.

    Returns:
        src_set (set): A set of strings containing image URLs

    The set contains every found src attribute of an img tag in the given HTML.
    """
    # img_pat finds all the <img alt="..." src="..."> snippets
    # this finds <img and collects everything up to the closing '>'
    img_pat = re.compile(r"<img[^>]+>", flags=re.IGNORECASE)
    # src finds the text between quotes of the `src` attribute
    src_pat = re.compile(r'src="([^"]+)"', flags=re.IGNORECASE)
    src_set = set()
    # first, find all the img tags
    for img_tag in img_pat.findall(html):
        # then, find the src attribute of the img, if any
        match = src_pat.search(img_tag)
        if match:
            src_set.add(match.group(1))
    return src_set





                    
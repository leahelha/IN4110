# IN3110 strømpris

## Tasks completed: 
5.1, 5.2 and 5.3

## Requirements:
Clone the assignment5 folder on your PC
Install all required packages with 'pip install -e .'

The required packagese are listed in requirements.txt

## Features of project

strompris.py gathers a JSON file of information from https://www.hvakosterstrommen.no/api/v1/prices/[year]/[month]-[day]_[location].json

This is collected by the function fetch_day_prices in strompris.py.
In the file you may select the date by setting a datetime.date(year, month, day). Don't use any leading 0s.
You may also select location from the list ["NO1", "NO2", "NO3","NO4","NO5"], representing regions in Norway.

Default values are given in file, the date will be today and location "NO1" which is Oslo.

For fetch_prices you produce a DataFrame from several days. Default is 7 days. 

The function plot_prices returns an Altair chart. When the whole code runs, this plot will be shown in a temporary location in your browser. 

app.py allows for the use of FastAPI to run strompris.py

## Running
Run strompris.py by executing:
'python3 strompris.py'

Define your parameters in the file, or let the defaults run.


Run app.py by running in your terminal:
'python3 app.py'

And then open the link that is given. There's your plot!
Note this will also save the plot as an html file for you.

Once you are in the browser, you may adjust the location and time range for the visualization of the data.

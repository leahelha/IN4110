"""
strompris fastapi app entrypoint
"""
from __future__ import annotations

import datetime
import os

import uvicorn
from typing import List, Optional
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

import altair as alt
from fastapi import FastAPI, Query, Request
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from strompris import (
    ACTIVITIES,
    LOCATION_CODES,
    fetch_day_prices,
    fetch_prices,
    plot_activity_prices,
    plot_daily_prices,
    plot_prices,
)

app = FastAPI()
templates = Jinja2Templates(directory="templates")


# `GET /` should render the `strompris.html` template
# with inputs:
# - request
# - location_codes: location code dict
# - today: current date

@app.get("/")
def strompris_template(request: Request):
    inputs = {
        "request": request,
        "location_codes": LOCATION_CODES.keys(),
        "today": datetime.date.today()

    }

    template = templates.TemplateResponse('strompris.html', inputs)
    return template


# GET /plot_prices.json should take inputs:
# - locations (list from Query)
# - end (date)
# - days (int, default=7)
# all inputs should be optional
# return should be a vega-lite JSON chart (alt.Chart.to_dict())
# produced by `plot_prices`
# (task 5.6: return chart stacked with plot_daily_prices)

@app.get('/plot_prices.json')
def plot_prices_json(
    locations: Optional[List[str]] = Query(default=None),
    end: Optional[datetime.date] = None,
    days: Optional[int] = 7
):
    
    # Getting the DataFrame produced through function defined in strompris.py
    df = fetch_prices(end, days, locations)

    # Getting chart from function defined in strompris.py
    chart = plot_prices(df)

    # Converting chart to vega-lite JSON char alt.Chart.to_dict()
    json_chart = chart.to_dict()

    return json_chart

# Task 5.6 (bonus):
# `GET /activity` should render the `activity.html` template
# activity.html template must be adapted from `strompris.html`
# with inputs:
# - request
# - location_codes: location code dict
# - activities: activity energy dict
# - today: current date


...

# Task 5.6:
# `GET /plot_activity.json` should return vega-lite chart JSON (alt.Chart.to_dict())
# from `plot_activity_prices`
# with inputs:
# - location (single, default=NO1)
# - activity (str, default=shower)
# - minutes (int, default=10)


...


# mount your docs directory as static files at `/help`

...


def main():
    """Launches the application on port 5000 with uvicorn"""
    # use uvicorn to launch your application on port 5000
    uvicorn.run(app, port=5000)


if __name__ == "__main__":
    main()

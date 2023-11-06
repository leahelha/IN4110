"""
Task 4

collecting olympic statistics from wikipedia
"""

from __future__ import annotations

from pathlib import Path
from requesting_urls import get_html
from bs4 import BeautifulSoup
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
# Countries to submit statistics for
scandinavian_countries = ["Norway", "Sweden", "Denmark"]

# Summer sports to submit statistics for
summer_sports = ["Sailing", "Athletics", "Handball", "Football", "Cycling", "Archery"]


def report_scandi_stats(url: str, sports_list: list[str], work_dir: str | Path) -> None:
    """
    Given the url, extract and display following statistics for the Scandinavian countries:

      -  Total number of gold medals for for summer and winter Olympics
      -  Total number of gold, silver and bronze medals in the selected summer sports from sport_list
      -  The best country in number of gold medals in each of the selected summer sports from sport_list

    Display the first two as bar charts, and the last as an md. table and save in a separate directory.

    Parameters:
        url (str) : url to the 'All-time Olympic Games medal table' wiki page
        sports_list (list[str]) : list of summer Olympic games sports to display statistics for
        work_dir (str | Path) : (absolute) path to your current working directory

    Returns:
        None
    """


    work_dir = Path(work_dir)
    # Make a call to get_scandi_stats
    country_dict = get_scandi_stats(url)
    print(country_dict)

    stats_dir = work_dir / "olympic_games_results"
    stats_dir.mkdir(parents=True, exist_ok=True) 

    # Plot the summer/winter gold medal stats
    plot_scandi_stats(country_dict, stats_dir)

    
    # Iterate through each sport and make a call to get_sport_stats
    # Plot the sport specific stats
    # Make a call to find_best_country_in_sport for each sport
    # Create and save the md table of best in each sport stats


    best_in_sport = {}
    # Valid values for medal ["Gold" | "Silver" |"Bronze"]
    medal = "Gold" #["Gold", "Silver", "Bronze"]
   
    for sport in sports_list:
        results: dict[str, dict[str, int]] = {}

        for country, info in country_dict.items():
            #print(country, info)
            medals = get_sport_stats(info['url'], sport)
            results[country] = medals
        
        #print(results)

        # Plot the sport-specific medal stats and save the figure
        plot_sport_stats(results, sport, stats_dir)

        best_country = find_best_country_in_sport(results, medal)
        best_in_sport[sport] = best_country
    
    #Creating markdown table
    create_markdown_table(best_in_sport, stats_dir)
    #print(best_in_sport)



def get_scandi_stats(
    url: str,
) -> dict[str, dict[str, str | dict[str, int]]]:
    """Given the url, extract the urls for the Scandinavian countries,
       as well as number of gold medals acquired in summer and winter Olympic games
       from 'List of NOCs with medals' table.

    Parameters:
      url (str): url to the 'All-time Olympic Games medal table' wiki page

    Returns:
      country_dict: dictionary of the form:
        {
            "country": {
                "url": "https://...",
                "medals": {
                    "Summer": 0,
                    "Winter": 0,
                },
            },
        }

        with the tree keys "Norway", "Denmark", "Sweden".
    """
    
    # Gettting html from url
    html = get_html(url)
    # Parsing html
    soup = BeautifulSoup(html, 'html.parser')
    

    base_url = "https://en.wikipedia.org"

    # Using Beautiful Soup to make tabel
    table = soup.find('table', {'class': 'wikitable'})
    rows = table.find_all('tr')

    country_dict: dict[str, dict[str, str | dict[str, int]]] = {}
   

    for row in rows:
        cols = row.find_all('td')
        if cols:
            country_name = cols[0].get_text().strip()
            country_name = country_name.split()  #Get rid of some extra stuff next to the names
            #print(country_name)
            
            if country_name[0] in scandinavian_countries:
                #print(country_name)

                # URL to the country's Olympic page
                country_url = base_url + cols[0].find('a')['href']
                #print(country_url)

                # Gold medals for summer and winter:
                summer_gold = int(cols[2].get_text().strip())
                winter_gold = int(cols[7].get_text().strip())
                # print(summer_gold)
                # print(winter_gold)

                country_dict[country_name[0]] = {
                    "url": country_url,
                    "medals": {
                        "Summer": summer_gold,
                        "Winter": winter_gold,
                    },
                }
        

    return country_dict

def get_sport_stats(country_url: str, sport: str) -> dict[str, int]:
    """Given the url to country specific performance page, get the number of gold, silver, and bronze medals
      the given country has acquired in the requested sport in summer Olympic games.

    Parameters:
        - country_url (str) : url to the country specific Olympic performance wiki page
        - sport (str) : name of the summer Olympic sport in interest. Should be used to filter rows in the table.

    Returns:
        - medals (dict[str, int]) : dictionary of number of medal acquired in the given sport by the country
                          Format:
                          {"Gold" : x, "Silver" : y, "Bronze" : z}
    """
    
    # Gettting html from url
    html = get_html(country_url)
    # Parsing html
    soup = BeautifulSoup(html, 'html.parser')
    # Using Beautiful Soup to make tabel
    tables = soup.find_all('table', {'class': 'wikitable'})
    #print(table[1])

    medals = {
        "Gold": 0,
        "Silver": 0,
        "Bronze": 0,
    }

    for table in tables:
        rows = table.find_all('tr')

        for row in rows:
            cols = row.find_all('td')
            
            if cols:
                #print(row.text.strip())
            
                sport_name = row.text.strip()#cols[0].text.strip()
                sport_name = sport_name.lower()

                #print(sport_name = np.where(cols==f"title={sport}"))
                if sport_name[:len(sport)] == sport.lower():
                    # print(sport_name[:len(sport)])
                    # print(sport)
                    medals["Gold"] = int(cols[0].text.strip())
                    medals["Silver"] = int(cols[1].text.strip())
                    medals["Bronze"] = int(cols[2].text.strip())
                    break  # Exit the loop after finding the sport

                    
    return medals

def find_best_country_in_sport(
    results: dict[str, dict[str, int]], medal: str = "Gold"
) -> str:
    """Given a dictionary with medal stats in a given sport for the Scandinavian countries, return the country
        that has received the most of the given `medal`.

    Parameters:
        - results (dict) : a dictionary of country specific medal results in a given sport. The format is:
                        {"Norway" : {"Gold" : 1, "Silver" : 2, "Bronze" : 3},
                         "Sweden" : {"Gold" : 1, ....},
                         "Denmark" : ...
                        }
        - medal (str) : medal type to compare for. Valid parameters: ["Gold" | "Silver" |"Bronze"]. Should be used as a key
                          to the medal dictionary.
    Returns:
        - best (str) : name of the country(ies) leading in number of gold medals in the given sport
                       If one country leads only, return its name, like for instance 'Norway'
                       If two countries lead return their names separated with '/' like 'Norway/Sweden'
                       If all or none of the countries lead, return string 'None'
    """
    
    valid_medals = {"Gold", "Silver", "Bronze"}
    if medal not in valid_medals:
        raise ValueError(
            f"{medal} is invalid parameter for ranking, must be in {valid_medals}"
        )

    items = results.items()

    # Counting nr of {medal} for each country
    count = {}
    for country, stats in items:
        count.update({country: stats[medal]})
    
    # Finding the highest nr of {medal}
    max_medals = max(count.values())

    # Get the requested medals and determine the best
    best = [country for country, count in count.items() if count == max_medals]
    
    # Make sure to return no more than 2 'best' countries, and none if there are 0 medals
    if len(best)==3 or max_medals == 0:
        return 'None'
    else:
        return '/'.join(best)


# if __name__ == "__main__":
    #Testing
    # url = 'https://en.wikipedia.org/wiki/All-time_Olympic_Games_medal_table'
    # scandi_dic = get_scandi_stats(url)
    # medals = get_sport_stats("https://en.wikipedia.org/w/index.php?title=Norway_at_the_Olympics&oldid=1153387488", "Tennis")
    # medals = get_sport_stats('https://en.wikipedia.org/wiki/Denmark_at_the_Olympics', 'Cycling')
    # print(medals)

    # results = {
    #     "Norway" : {"Gold" : 2, "Silver" : 1, "Bronze" : 3},
    #     "Sweden" : {"Gold" : 2, "Silver" : 2, "Bronze" : 3},
    #     "Denmark" : {"Gold" : 2, "Silver" : 2, "Bronze" : 3},
    #     }
    
    # best = find_best_country_in_sport(results, 'Gold')
    # #print(best)

# Define your own plotting functions and optional helper functions


def plot_sport_stats(results: dict[str, dict[str, int]], sport: str, output_dir: Path) -> None:
    """
    Plot the sport-specific medal stats for Scandinavian countries and save the figure as a PNG.

    Parameters:
        results (dict): A dictionary with countries as keys and another dictionary with medal types as keys and counts as values.
        sport (str): The name of the sport.
        output_dir (Path): The directory where the PNG file will be saved.
    """
    
    countries = list(results.keys())
    gold_medals = [results[country]['Gold'] for country in countries]
    silver_medals = [results[country]['Silver'] for country in countries]
    bronze_medals = [results[country]['Bronze'] for country in countries]


    x = range(len(countries))
    width = 0.2

    fig, ax = plt.subplots()

    # Plotting each medal type in grouped fashion
    ax.bar(x, gold_medals, width, label='Gold', color='gold')
    ax.bar([p + width for p in x], silver_medals, width, label='Silver', color='silver')
    ax.bar([p + width * 2 for p in x], bronze_medals, width, label='Bronze', color='#cd7f32')

    
    ax.set_ylabel('Medals')
    ax.set_title(f'Number of medals in {sport} by Scandinavian country')
    ax.set_xticks([p + width for p in x])
    ax.set_xticklabels(countries)
    ax.legend()

    
    plt.tight_layout()
    fig.savefig(output_dir / f'{sport}_medal_ranking.png')
    #plt.show()

    


def create_markdown_table(best_in_sport: dict[str, str], stats_dir: Path) -> None:
    """
    Create a markdown table that lists the best Scandinavian country in each sport based on the number of gold medals.

    Parameters:
        best_in_sport (dict): A dictionary with sports as keys and the best country as values.
        stats_dir (Path): The directory where the markdown file will be saved.

    This function generates a markdown table with two columns: 'Sport' and 'Best country'.
    It then calls the `save_markdown_table` function to write this table to a markdown file.
    """
    table_data = [{"Sport": sport, "Best country": country} for sport, country in best_in_sport.items()]
    save_markdown_table(table_data, stats_dir / 'best_of_sport_by_Gold.md')

def save_markdown_table(data: list[dict[str, str]], filename: Path) -> None:
    """
    Save a list of dictionaries as a markdown table to the specified filename.

    Parameters:
        data (list of dict): A list of dictionaries where each dictionary represents a row in the table.
        filename (Path): The complete file path for the markdown file to be saved.

    This function converts the list of dictionaries into a pandas DataFrame and then uses the
    `to_markdown` method to create a markdown formatted string. This string is then written to
    the file specified by `filename`.
    """
    markdown = pd.DataFrame(data).to_markdown(index=False)
    with open(filename, 'w') as f:
        f.write(markdown)




def plot_scandi_stats(
    country_dict: dict[str, dict[str, str | dict[str, int]]],
    output_parent: str | Path | None = None,
) -> None:
    """Plot the number of gold medals in summer and winter games for each of the scandi countries as bars.

    Parameters:
      results (dict[str, dict[str, int]]) : a nested dictionary of country names and the corresponding number of summer and winter
                            gold medals from 'List of NOCs with medals' table.
                            Format:
                            {"country_name": {"Summer" : x, "Winter" : y}}
      output_parent (str | Path) : parent file path to save the plot in
    Returns:
      None
    """
    countries = list(country_dict.keys())
    summer_medals = [country_dict[country]['medals']['Summer'] for country in countries]
    winter_medals = [country_dict[country]['medals']['Winter'] for country in countries]

    x = np.arange(len(countries)) 
    width = 0.35 

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, summer_medals, width, label='Summer', color='green')
    rects2 = ax.bar(x + width/2, winter_medals, width, label='Winter', color='blue')

   
    ax.set_ylabel('Gold Medals')
    ax.set_title('Gold Medals by Scandinavian Countries in Summer and Winter Olympics')
    ax.set_xticks(x)
    ax.set_xticklabels(countries)
    ax.legend()


    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  
                        textcoords="offset points",
                        ha='center', va='bottom')

    autolabel(rects1)
    autolabel(rects2)

    fig.tight_layout()

    
    plt.savefig(output_parent / 'total_medal_ranking.png')
    #plt.show()  





# run the whole thing if called as a script, for quick testing
if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/All-time_Olympic_Games_medal_table"
    work_dir = Path(__file__).parent.absolute()
    report_scandi_stats(url, summer_sports, work_dir)



"""   
SCRAP 
 # First, plot the total medal ranking for all sports
    plot_total_medal_ranking(country_dict, stats_dir)

    # Then, plot the medal ranking for each sport
    for sport in sports_list:
        plot_sport_medal_ranking(country_dict, sport, stats_dir)

    # Finally, create the markdown table for the best country in each sport
    create_markdown_table(best_in_sport, stats_dir)



work_dir = Path(work_dir)
    stats_dir = work_dir / "olympic_games_results"

     # Extracting the data for plotting
    countries = list(country_dict.keys())
    summer_medals = [country_dict[country]['medals']['Summer'] for country in countries]
    winter_medals = [country_dict[country]['medals']['Winter'] for country in countries]

    # Setting the positions and width for the bars
    positions = range(len(countries))
    bar_width = 0.35

    # Plotting both summer and winter medals
    fig, ax = plt.subplots()
    summer_bars = ax.bar(positions, summer_medals, bar_width, label='Summer Olympics')
    winter_bars = ax.bar([p + bar_width for p in positions], winter_medals, bar_width, label='Winter Olympics')

    # Adding some text for labels, title and axes ticks
    ax.set_xlabel('Countries')
    ax.set_ylabel('Gold Medals')
    ax.set_title('Total number of gold medals in Summer and Winter Olympics')
    ax.set_xticks([p + bar_width / 2 for p in positions])
    ax.set_xticklabels(countries)
    ax.legend()

    # Saving the figure
    plt.tight_layout()
    plt.savefig(stats_dir / 'total_medal_ranking.png')
    plt.close()
    
    
    def plot_total_medal_ranking(country_dict, stats_dir):
    
    countries = list(country_dict.keys())
    summer_medals = [country_dict[country]['medals']['Summer'] for country in countries]
    winter_medals = [country_dict[country]['medals']['Winter'] for country in countries]

    x = range(len(countries))
    fig, ax = plt.subplots()
    ax.bar(x, summer_medals, width=0.4, label='Summer', align='center')
    ax.bar(x, winter_medals, width=0.4, label='Winter', align='edge')
    ax.set_xticks(x)
    ax.set_xticklabels(countries)
    ax.legend()
    plt.savefig(stats_dir / 'total_medal_ranking.png')
    plt.close()

    
    
    
    
    
    """
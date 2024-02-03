from bs4 import BeautifulSoup
from pandas import DataFrame
from requesting_url import get_html


def get_data_lol(url: str) -> DataFrame:
    """Given the url, return a df with all the rows acquired from lolpro

    Parameters:
        url (str): url to lol pro

    Returns:
        DataFrame with all the data scrapped
    """
    html = get_html(url)
    soup = BeautifulSoup(html, "html.parser")

    # Get the table
    table = soup.find("table", {"data-v-069f53bc": True})
    table_body = table.find("tbody")
    rows = table_body.find_all("tr")

    players = DataFrame()
    players["rank"] = []
    players["player"] = []
    players["country"] = []
    players["lp"] = []

    for row in rows:
        cols = row.find_all("td")

        player_rank = cols[0].get_text()
        player_name = cols[1].find("div", {"class": "player-name"}).text
        player_country = cols[1].find("i").get("title")

        # if headless off
        player_lp = cols[3].find("div", class_="rank-long").text.strip().split()[1]

        # if headleass on
        #player_lp = cols[3].find("span", class_="rank-lp").text

        players = players._append(
            {
                "player": player_name,
                "rank": player_rank,
                "country": player_country,
                "lp": player_lp,
            },
            ignore_index=True,
        )
    print(players.to_markdown(index=False))

    return players


def main():
    url = "https://lolpros.gg/ladders"
    df = get_data_lol(url)


if __name__ == "__main__":
    main()

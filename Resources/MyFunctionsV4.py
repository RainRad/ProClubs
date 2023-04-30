import requests
from bs4 import BeautifulSoup as soup

def simple_link_stripper(club_link):
    partial_strip = club_link[club_link.find('-'):]
    id_in_list_form = [x for x in partial_strip if x.isdigit()]
    cleaned_id = ''.join(id_in_list_form)
    return int(cleaned_id)

def comparison_link_stripper(club_id, comparison_link):
    numbers_only_list = [x for x in comparison_link if x.isdigit()]
    numbers_only = ''.join(numbers_only_list)
    cleaned_id = numbers_only[len(f'23{club_id}'):]
    return(int(cleaned_id))

def scrape(url):
    response = requests.get(url)
    site = soup(response.content, 'html.parser')
    return site

def dash_string_to_list(string):
    list = [int(num) for num in string.split('-')]
    return list

def division(site):
    images = site.find_all("img")
    string = images[1].get("alt", "")
    division = int(string.split()[1] + ' ')
    return division

def best_season_division(site):
    images = site.find_all("img")
    string = images[2].get("alt", "")
    division = int(string.split()[1] + ' ')
    return division


def last_ten_matches(site):
    win = site.find_all("li", class_="badge list-inline-item match-result me-1 px-0 text-light bg-result-win")
    loss = site.find_all("li", class_="badge list-inline-item match-result me-1 px-0 text-light bg-result-loss")
    draw = site.find_all("li", class_="badge list-inline-item match-result me-1 px-0 text-light bg-result-draw")
    games = win + loss + draw
    clean_games = [game.text.strip() for game in games]
    clean_games_string = ''.join(clean_games)
    return clean_games_string

def general_info(site):
    output = {}
    
    # General Scrape covering multiple data fields
    data = site.find_all("div", "col-auto font-tabular-nums fw-bold")
    trophy_data = site.find_all("span", "me-1")
    club_name = site.find("h1", "h4 mb-0")
    
    # Club name
    output["Club Name"] = club_name.text.strip()
    
    # Returns a integer # of games played
    output["Matches Played"] = int(data[10].text.strip())
    
    # Returns a list of [win, loss, draw]
    win_loss_draw_record = dash_string_to_list(data[11].text.strip())
    output["Wins"] = win_loss_draw_record[0]
    output["Losses"] = win_loss_draw_record[1]
    output["Draws"] = win_loss_draw_record[2]
    
    # Gathers Goal Info 
    output["Goals Scored"] = int(data[12].text.strip())
    output["Goals Per Match"] = float(data[13].text.strip())
    output["Goals Conceded"] = int(data[14].text.strip())
    output["Goals Conceded Per Match"] = float(data[15].text.strip())
    output["Goal Difference"] = output["Goals Scored"] - output["Goals Conceded"]

    # Gather Seasons Info
    output["Seaons Played"] = int(data[17].text.strip())
    promotion_hold_relegation = dash_string_to_list(data[18].text.strip())
    output["Promotions"] = promotion_hold_relegation[0]
    output["Holds"] = promotion_hold_relegation[1]
    output["Relegations"] = promotion_hold_relegation[2]
    
    # Best Season
    output["Best Season"] = int(data[19].text.strip())
    
    # Region
    output["Region"] = data[20].text.strip()
    
    # Stadium
    output["Stadium"] = data[21].text.strip()
    if output["Stadium"] == "":
        output["Stadium"] = "N/A"
        
    # Ranking Points
    output["Total Rank Points"] = data[22].text.strip()
    output["League Points"] = data[23].text.strip()
    output["Cup Points"] = data[24].text.strip()
    
    # Trophy Info
    output["Div 1 Titles"] = int(trophy_data[1].text.strip())
    output["Other Divisions"] = int(trophy_data[2].text.strip())
    output["Total Trophies"] = int(trophy_data[3].text.strip())
    
    return(output)


def club_scrape(console, club):
    
    # Create Storage for Club Data
    club_data = {}
    
    # Goes to club page
    url = f"https://proclubshead.com/23/club/{console}-{club}/"
    site = scrape(url)
    
    try:
        # Scrape General Data
        general_info_output = general_info(site)

        club_data["club_name"] = general_info_output["Club Name"]
        club_data["active"] = "Yes"
        club_data["console"] = console
        club_data["club_id"] = club
        # Scrape and Store Division
        club_data["division"] = division(site)

        # Scrape, Store Recent Match Record
        club_data["ten_match_record"] = last_ten_matches(site)

        # Store W/L/D
        club_data["total_games"] = general_info_output["Wins"] + general_info_output["Losses"] + general_info_output["Draws"]
        club_data["wins"] = general_info_output["Wins"]
        club_data["losses"] = general_info_output["Losses"]
        club_data["draws"] = general_info_output["Draws"]

        # Store Goal Info
        club_data["goals_scored"] = general_info_output["Goals Scored"]
        club_data["goals_per_match"] = general_info_output["Goals Per Match"]
        club_data["goals_conceded"] = general_info_output["Goals Conceded"]
        club_data["goals_conceded_per_match"] = general_info_output["Goals Conceded Per Match"]
        club_data["goal_difference"] = general_info_output["Goal Difference"]

        # Store Seaons Info
        club_data["promotions"] = general_info_output["Promotions"]
        club_data["holds"] = general_info_output["Holds"]
        club_data["relegations"] = general_info_output["Relegations"]

        # Best Season 
        club_data["best_season_div"] = best_season_division(site)
        club_data["best_season_points"] = general_info_output["Best Season"]

        # Region 
        club_data["region"] = general_info_output["Region"]

        # Stadium
        club_data["stadium"] = general_info_output["Stadium"]

        # Ranking Points
        club_data["total_rank_points"] = general_info_output["Total Rank Points"]
        club_data["league_points"] = general_info_output["League Points"]
        club_data["cup_points"] = general_info_output["Cup Points"]

        # Trophy Data
        club_data["div_1_titles"] = general_info_output["Div 1 Titles"]
        club_data["other_div_titles"] = general_info_output["Other Divisions"]
        club_data["total_trophies"] = general_info_output["Total Trophies"]
    
    except:
        club_data["club_name"] = ""
        club_data["active"] = "No"
        club_data["console"] = console
        club_data["club_id"] = club
        # Scrape and Store Division
        club_data["division"] = 0

        # Scrape, Store Recent Match Record
        club_data["ten_match_record"] = ""

        # Store W/L/D
        club_data["total_games"] = 0
        club_data["wins"] = 0
        club_data["losses"] = 0
        club_data["draws"] = 0

        # Store Goal Info
        club_data["goals_scored"] = 0
        club_data["goals_per_match"] = 0
        club_data["goals_conceded"] = 0
        club_data["goals_conceded_per_match"] = 0
        club_data["goal_difference"] = 0

        # Store Seaons Info
        club_data["promotions"] = 0
        club_data["holds"] = 0
        club_data["relegations"] = 0

        # Best Season 
        club_data["best_season_division"] = 0
        club_data["best_season"] = 0

        # Region 
        club_data["region"] = ""

        # Stadium
        club_data["stadium"] = ""

        # Ranking Points
        club_data["total_rank_points"] = 0
        club_data["league_points"] = 0
        club_data["cup_points"] = 0

        # Trophy Data
        club_data["div_1_titles"] = 0
        club_data["other_div_titles"] = 0
        club_data["total_trophies"] = 0
    return club_data



def win_loss_assign(match_data, home_team, away_team):
    if int(home_team[0]) > int(away_team[0]):
            match_data["Winning Team"] = int(home_team[0])

def to_float(string):
    clean_string = string.strip('%')
    float_value = float(clean_string)
    return float_value 

    
def last_five_match_scrape(console, club_id, club_name):    
    try:
        match_data = []
        individual_player_perform_data = []

        url = f"https://proclubshead.com/23/club-league-matches/{console}-{club_id}/"
        site = scrape(url)
        games = site.find_all("div", class_="bg-gradient border border-secondary mb-3 pt-3 px-3 rounded-3")
        names = site.find_all('div', 'col text-start text-truncate')
        club_names = [name.text.strip() for name in names]
        counter = 0 
        
        for game in games:

            opponent_info = {}
            game_data = {}
            match_individual_player_perform_data = []

            game_info_home = game.find_all("div", class_="col-auto font-tabular-nums fw-bold order-first")
            game_info_home = [x.text.strip() for x in game_info_home]
            game_info_away = game.find_all("div", class_="col-auto font-tabular-nums fw-bold")
            game_info_away = [x.text.strip() for x in game_info_away]
            opp_name  = club_names[counter]
            counter += 1
            
            #Obtains Home and away team season/round and opponent ID to generate game_id
            home_team_season = game_info_home[11]
            home_team_round = game_info_home[10]

            away_team_season = game_info_away[11]
            away_team_round = game_info_away[10] 

            away_club_link_raw = game.find_all("a", class_="btn btn-sm btn--fifa-primary")
            away_club_id = simple_link_stripper(away_club_link_raw[0]['href'])
            away_club_name = game.find_all('div', class_='away_club_link_raw')


            # generates and assigns game_id
            if club_id > away_club_id:
                game_data["game_id"] = int(f"{club_id}{home_team_season}{home_team_round}")
            else:
                game_data["game_id"] = int(f"{away_club_id}{away_team_season}{away_team_round}")

            game_data["console"] = console


            home_goals = int(game_info_home[0])
            away_goals = int(game_info_away[0])
            if home_goals > away_goals:
                game_data["winning_club"] = club_name
            elif home_goals < away_goals:
                game_data["winning_club"] = opp_name
            elif home_goals == away_goals:
                game_data["winning_club"] = 'Draw'

            num_players = game.find('span', class_ ="ms-1 small").text.strip()
            num_players = parse_numbers(num_players)
            # store home team data
            game_data["h_club"] = club_name
            game_data["h_club_id"] = club_id
            game_data["h_goals"] = home_goals
            game_data["h_shots"] = int(game_info_home[1])
            game_data["h_shot_percent"] = to_float(game_info_home[2])/100
            game_data["h_passes_made"] = int(game_info_home[3])
            game_data["h_pass_attempts"] = int(game_info_home[4])
            game_data["h_pass_percent"] = to_float(game_info_home[5])/100
            game_data["h_tackles_made"] = int(game_info_home[6])
            game_data["h_tackle_attempts"] = int(game_info_home[7])
            game_data["h_tackle_percent"] = to_float(game_info_home[8])/100
            game_data["h_red_cards"] = int(game_info_home[9])
            game_data["h_players_in_match"] = num_players[0]
            game_data["h_forward"] = 0
            game_data["h_midfielder"] = 0
            game_data["h_defender"] = 0
            game_data["h_goalkeeper"] = 0
            game_data["h_any"] = 0
            game_data["h_season"] = home_team_season
            game_data["h_round"] = home_team_round


            # Store opponent date
            game_data["opp_club"] = opp_name
            game_data["opp_club_id"] = away_club_id
            game_data["opp_goals"] = away_goals
            game_data["opp_shots"] = int(game_info_away[1])
            game_data["opp_shot_percent"] = to_float(game_info_away[2])/100
            game_data["opp_passes_made"] = int(game_info_away[3])
            game_data["opp_pass_attempts"] = int(game_info_away[4])
            game_data["opp_pass_percent"] = to_float(game_info_away[5])/100
            game_data["opp_tackles_made"] = int(game_info_away[6])
            game_data["opp_tackle_attempts"] = int(game_info_away[7])
            game_data["opp_tackle_percent"] = to_float(game_info_away[8])/100
            game_data["opp_red_cards"] = int(game_info_away[9])
            game_data["opp_players_in_match"] = num_players[1]
            game_data["opp_forward"] = 0
            game_data["opp_midfielder"] = 0
            game_data["opp_defender"] = 0
            game_data["opp_goalkeeper"] = 0
            game_data["opp_any"] = 0
            game_data["opp_season"] = away_team_season
            game_data["opp_round"] = away_team_round

            for player in game.find_all('div', class_='fade modal'):
                player_info_id = player.get('id')
                second_digit = int(player_info_id.split('-')[3])

                if second_digit == 1:
                    x = player.find_all('span')
                    x_position = x[4]['class'][3]
                    position = x_position.split('-')[3]
                    player_data = player.find_all("div", class_="col-auto font-tabular-nums fw-bold")

                    individual_game_data = {}
                    individual_game_data["game_id"] = game_data["game_id"]
                    individual_game_data["name"] = player.find("div", class_='fs-5').text.strip()
                    individual_game_data["club"] = club_id
                    individual_game_data["position"] = position
                    individual_game_data["rating"] = float(player_data[0].text.strip())
                    individual_game_data["motm"] = player_data[1].text.strip()
                    individual_game_data["goals"] = int((player_data[2].text.strip()).split('|')[0].strip())
                    individual_game_data["shots"] = int((player_data[3].text.strip()).split('|')[0].strip())
                    individual_game_data["shot_percent"] = float((player_data[4].text.split('|')[0].strip()).strip('%')) /100
                    individual_game_data["assist"] = int((player_data[5].text.strip()).split('|')[0].strip())
                    individual_game_data["passes_made"] = int((player_data[6].text.strip()).split('|')[0].strip())
                    individual_game_data["pass_attempts"] = int((player_data[7].text.strip()).split('|')[0].strip())
                    individual_game_data["pass_percent"] = float((player_data[8].text.split('|')[0].strip()).strip('%')) /100
                    individual_game_data["tackles_made"] = int((player_data[9].text.strip()).split('|')[0].strip())
                    individual_game_data["tackle_attempts"] =int((player_data[10].text.strip()).split('|')[0].strip())
                    individual_game_data["tackle_percent"] = float((player_data[11].text.split('|')[0].strip()).strip('%')) /100
                    individual_game_data["red_card"] = player_data[12].text.strip()
                    try:
                        saves = float(player_data[13].text.strip())
                        if saves > 0:
                            individual_game_data["gk_saves"] = saves
                        else: 
                            individual_game_data["gk_saves"] = 0
                    except:
                        individual_game_data["gk_saves"] = 0

                    match_individual_player_perform_data.append(individual_game_data)

                    # Count and store number of players for each position
                    if position == 'forward':
                        game_data["h_forward"] += 1
                    if position == 'midfielder':
                        game_data["h_midfielder"] += 1
                    if position == 'defender':
                        game_data["h_defender"] += 1
                    if position == 'goalkeeper':
                        game_data["h_goalkeeper"] += 1
                    if position == 'any':
                        game_data["h_any"] += 1

                if second_digit == 2:
                    x = player.find_all('span')
                    x_position = x[4]['class'][3]
                    position = x_position.split('-')[3]
                    player_data = player.find_all("div", class_="col-auto font-tabular-nums fw-bold")

                    individual_game_data = {}
                    individual_game_data["game_id"] = game_data["game_id"]
                    individual_game_data["name"] = player.find("div", class_='fs-5').text.strip()
                    individual_game_data["club"] = away_club_id
                    individual_game_data["position"] = position
                    individual_game_data["rating"] = float(player_data[0].text.strip())
                    individual_game_data["motm"] = player_data[1].text.strip()
                    individual_game_data["goals"] = int((player_data[2].text.strip()).split('|')[0].strip())
                    individual_game_data["shots"] = int((player_data[3].text.strip()).split('|')[0].strip())
                    individual_game_data["shot_percent"] = float((player_data[4].text.split('|')[0].strip()).strip('%')) /100
                    individual_game_data["assist"] = int((player_data[5].text.strip()).split('|')[0].strip())
                    individual_game_data["passes_made"] = int((player_data[6].text.strip()).split('|')[0].strip())
                    individual_game_data["pass_attempts"] = int((player_data[7].text.strip()).split('|')[0].strip())
                    individual_game_data["pass_percent"] = float((player_data[8].text.split('|')[0].strip()).strip('%')) /100
                    individual_game_data["tackles_made"] = int((player_data[9].text.strip()).split('|')[0].strip())
                    individual_game_data["tackle_attempts"] =int((player_data[10].text.strip()).split('|')[0].strip())
                    individual_game_data["tackle_percent"] = float((player_data[11].text.split('|')[0].strip()).strip('%')) /100
                    individual_game_data["red_card"] = player_data[12].text.strip()
                    try:
                        saves = int(player_data[13].text.strip())
                        if saves > 0:
                            individual_game_data["gk_saves"] = saves
                        else: 
                            individual_game_data["gk_saves"] = 0
                    except:
                        individual_game_data["gk_saves"] = 0


                    match_individual_player_perform_data.append(individual_game_data)

                    # Count and store number of players for each position
                    if position == 'forward':
                        game_data["opp_forward"] += 1
                    if position == 'midfielder':
                        game_data["opp_midfielder"] += 1
                    if position == 'defender':
                        game_data["opp_defender"] += 1
                    if position == 'goalkeeper':
                        game_data["opp_goalkeeper"] += 1
                    if position == 'any':
                        game_data["opp_any"] += 1

            match_data.append(game_data)
            individual_player_perform_data.extend(match_individual_player_perform_data)
    except Exception as e: 
        print(e)
        pass
    return match_data, individual_player_perform_data

def ten_match_average(s):
    count = 0
    total = 0
    for c in s:
        if c == 'W':
            total += 3
        elif c == 'D':
            total += 1
        elif c == 'L':
            total += 0
        count += 1
    return total / count

def set_win_loss(row):
    if row['winning_club'] == row['h_club_name']:
        return 'Home'
    elif row['winning_club'] == row['opp_club_name']:
        return 'Away'
    else:
        return 'Draw'
    
def winning_club_id(row):
    if row.h_club == row.winning_club:
        return row.h_club_id
    elif row.opp_club == row.winning_club:
        return row.opp_club_id
    else:
        return 0
    
def win_loss_draw_club_assign(row):
    if row.winning_club_id == row.club:
        return 'win'
    elif row.winning_club_id == 0:
        return 'draw'
    else:
        return 'loss'
    
def parse_numbers(string):
    numbers = string.strip('()').split('-')
    return [int(numbers[0]), int(numbers[1])]

def clean_up(row, clubs):
    name = 'Opponent info'
    if row.opp_club_id in clubs.club_id.values:
        result = clubs[clubs['club_id'] == row.opp_club_id]
        name = result.club_name.values[0]
        row.opp_club = name
        if row.winning_club == 'Opponent info':
            row.winning_club = name
    else:
        missing_clubs = row.opp_club_id
        console = row.console
    return row

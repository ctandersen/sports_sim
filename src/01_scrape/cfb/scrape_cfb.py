"""
Provides utilities to download and parse data from basketball-reference.com. Note that
the tables sometimes changes over the season, so you will need to inspect a variety of
years to make sure to handle table structure changes.

We keep everything here in text format on purpose, other scripts can handle data validation
and type casting to suit the need of the model. Goal here is to simply scrape the webpage.
"""
import bs4

from web.fetch import fetch

CFB_REF_URL = 'https://www.sports-reference.com/cfb/'

def get_season_ratings(season: int) -> list[dict]:
    ratings_list = []

    '''
    The table changes for season 1996 to exclude ties (6th column) from
    the win-loss record as sudden death OT was implemented in college football,
    thus moving all the columns over one after where ties used to be 
    '''
    ties_offset = 1 if season < 1996 else 0
    
    url = f'{CFB_REF_URL}years/{season}-ratings.html'
    html = fetch(url, pause_seconds=3.5)
    soup = bs4. BeautifulSoup(html, features='html.parser')
    tbody = soup.find('tbody')
    
    for tr in tbody.find_all('tr'):
        team_entry = {}
        try:
            th = tr.find('th')
            td_list = list(tr.find_all('td'))            
            team_entry['season'] = str(season)
            team_entry['rank'] = th.text
            team_entry['name'] = td_list[0].text
            team_entry['conf_div'] = td_list[1].text
            team_entry['ap_rank'] = td_list[2].text
            team_entry['wins'] = td_list[3].text
            team_entry['losses'] = td_list[4].text
            team_entry['ties'] = '0' if ties_offset == 0 else td_list[5].text
            team_entry['osrs'] = td_list[5 + ties_offset].text
            team_entry['dsrs'] = td_list[6 + ties_offset].text
            team_entry['srs'] = td_list[7 + ties_offset].text
            team_entry['scoring_off'] = td_list[8 + ties_offset].text
            team_entry['scoring_def'] = td_list[9 + ties_offset].text
            team_entry['passing_off'] = td_list[10 + ties_offset].text
            team_entry['passing_def'] = td_list[11 + ties_offset].text
            team_entry['rushing_off'] = td_list[12 + ties_offset].text
            team_entry['rushing_def'] = td_list[13 + ties_offset].text
            team_entry['total_off'] = td_list[14 + ties_offset].text
            team_entry['total_def'] = td_list[15 + ties_offset].text
            
            ratings_list.append(team_entry)
            
        except Exception:
            continue
    
    return ratings_list        

def get_season_standings(season: int) -> list[dict]:
    standings_list = []
    
    '''
    The table changes for season 1996 to exclude ties (4th and 8th column) from
    the win-loss record as sudden death OT was implemented in college football,
    thus moving all the columns over one or two after where ties used to be 
    '''
    ties_offset = 1 if season < 1996 else 0
    
    url = f'{CFB_REF_URL}years/{season}-standings.html'
    html = fetch(url, pause_seconds=3.5)
    soup = bs4. BeautifulSoup(html, features='html.parser')
    tbody = soup.find('tbody')
    
    for tr in tbody.find_all('tr'):
        team_entry = {}
        try:
            th = tr.find('th')
            td_list = list(tr.find_all('td'))            
            team_entry['season'] = str(season)
            team_entry['rank'] = th.text
            team_entry['name'] = td_list[0].text
            team_entry['conf_div'] = td_list[1].text
            team_entry['wins'] = td_list[2].text
            team_entry['losses'] = td_list[3].text
            team_entry['ties'] = '0' if ties_offset == 0 else td_list[4].text
            team_entry['win_pct'] = td_list[4 + ties_offset].text
            team_entry['conf_wins'] = td_list[5 + ties_offset].text
            team_entry['conf_losses'] = td_list[6 + ties_offset].text
            team_entry['conf_ties'] = '0' if ties_offset == 0 else td_list[6 + ties_offset * 2].text
            team_entry['conf_win_pct'] = td_list[7 + ties_offset * 2].text
            team_entry['points_per_game_off'] = td_list[8 + ties_offset * 2].text
            team_entry['points_per_game_def'] = td_list[9 + ties_offset * 2].text
            team_entry['srs'] = td_list[10 + ties_offset * 2].text
            team_entry['sos'] = td_list[11 + ties_offset * 2].text
            team_entry['ap_rank_pre'] = td_list[12 + ties_offset * 2].text
            team_entry['ap_rank_high'] = td_list[13 + ties_offset * 2].text
            team_entry['ap_rank'] = td_list[14 + ties_offset * 2].text
            team_entry['notes'] = td_list[15 + ties_offset * 2].text
            
            standings_list.append(team_entry)
            
        except Exception:
            continue
    
    return standings_list


def get_season_schedule(season: int) -> list[dict]:
    games_list = []
    
    '''
    The table changes for season 2013 to include the time of the game,
    thus moving all the columns over one where time was added (3rd column) 
    '''
    time_offset = 0 if season < 2013 else 1
   
    url = f'{CFB_REF_URL}years/{season}-schedule.html'
    html = fetch(url, pause_seconds=3.5)
    soup = bs4. BeautifulSoup(html, features='html.parser')
    tbody = soup.find('tbody')
    
    for tr in tbody.find_all('tr'):
        game_entry = {}
        try:
            th = tr.find('th')
            td_list = list(tr.find_all('td'))            
            game_entry['season'] = str(season)
            game_entry['id'] = th.text
            game_entry['week'] = td_list[0].text
            game_entry['date'] = td_list[1].text
            game_entry['time'] = None if time_offset == 1 else td_list[2].text
            game_entry['day'] = td_list[2 + time_offset].text
            game_entry['winner'] = td_list[3 + time_offset].text
            game_entry['winner_pts'] = td_list[4 + time_offset].text
            game_entry['location'] = td_list[5 + time_offset].text
            game_entry['loser'] = td_list[6 + time_offset].text
            game_entry['loser_pts'] = td_list[7 + time_offset].text
            game_entry['notes'] = td_list[8 + time_offset].text
            
            games_list.append(game_entry)
            
        except Exception:
            continue
    
    return games_list

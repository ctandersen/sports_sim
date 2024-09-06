from dataclasses import dataclass
from enum import Enum
from typing import Optional, Union, Any
from numbers import Number
from pydantic import BaseModel, validator


class PlayoffFormat(Enum):
    '''
    Describes the type of college football playoff format used
    '''
    NONE = 1
    BCS = 2
    FOUR = 3
    TWELVE = 4


class Team(BaseModel):
    season: int 
    rank: int 
    name: str 
    conf_div: str 
    ap_rank: Optional[int] 
    wins: int 
    losses: int 
    ties: int 
    osrs: Optional[float] 
    dsrs: Optional[float] 
    srs: Optional[float] 
    scoring_off: Optional[float] 
    scoring_def: Optional[float] 
    passing_off: Optional[float] 
    passing_def: Optional[float] 
    rushing_off: Optional[float] 
    rushing_def: Optional[float] 
    total_off: Optional[float] 
    total_def: Optional[float]
    
    @validator('ap_rank','osrs','dsrs','srs','scoring_off',
               'scoring_def','passing_off','passing_def',
               'rushing_off','rushing_def','total_off','total_def',pre=True)
    def never_empty_none(cls, v: str) -> Union[None, str]:
        if v == "":
            return None 
        return v
        
    @validator('wins','losses','ties', pre=True)
    def never_empty_0(cls, v: str) -> Union[None, str]:
        if v == "":
            return '0' 
        return v
    
    @property
    def conference(self):
        return self.conf_div if self.conf_div.find('(') == -1 else self.conf_div.split('(')[0].strip()

    @property
    def division(self):
        return None if self.conf_div.find('(') == -1 else self.conf_div.split('(')[1].replace(')','').strip()

class Game(BaseModel):
    pass

class Season(BaseModel):
    teams: list[Team]
    year: int
    conferences: set[str]
    conf_div: set[str]
    playoffs: PlayoffFormat
    schedule: list[Game] = []

    def add_team(self, team_add: Team) -> Any:
        for index, team in enumerate(self.teams):
            if team.name == team_add.name:
                self.teams.remove(index)
                break
        self.teams.append(team_add)
        self.conferences.add(team_add.conference)
        self.conf_div.add(team_add.conf_div)
        return self


class League(BaseModel):
    seasons: list[Season]

    @property
    def seasons_years(self) -> list[int]:
        return [season.year for season in self.seasons]
    
    @property
    def season_count(self) -> list[int]:
        return len(self.seasons)
    
    def add_team(self, team_add: Team) -> Any:
        '''
        Need to check if a season year already exists. If not, we
        need to initiate a new season, if so, we need to find the
        index of the season, select it, and add team to it. The season
        add_team function will check for Team's existence
        '''
        # print(f'Adding: {team_add.name} from {team_add.season} season')
        if team_add.season in self.seasons_years:
            season_index = self.seasons_years.index(team_add.season)
            season = self.seasons[season_index]           
            season.add_team(team_add)
        else:
            if team_add.season >= 2024:
                playoff_format = PlayoffFormat.TWELVE
            elif team_add.season >= 2014:
                playoff_format = PlayoffFormat.FOUR
            elif team_add.season >= 1998:
                playoff_format = PlayoffFormat.BCS
            else:
                playoff_format = PlayoffFormat.BCS
                    
            self.seasons.append(
                Season.model_validate(
                    {'teams': [team_add],
                     'year': team_add.season,
                     'conferences': {team_add.conference},
                     'conf_div': {team_add.conf_div},
                     'playoffs': playoff_format
                     }
                )
            )
        return self
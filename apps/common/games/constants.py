from enum import Enum


class GamesRoutes(Enum):
    all_games = 'all-games'


TEAM_NAMES = (
    'Оранжевые',
    'Синие',
    'Зеленые'
)

PLAYER_POSITIONS = (
    ('GK', 'Goalkeeper'),
    ('DF', 'Defender'),
    ('ST', 'Striker'),
    ('PL', 'Player')
)

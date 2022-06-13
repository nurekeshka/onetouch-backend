from apps.common.games.constants import TEAM_NAMES
from enum import Enum


class Emoji (Enum):
    football = '⚽'
    heart = '❤️'
    explosion = '💥'
    bomb = '💣'
    rocket = '🚀'
    fire = '🔥'
    commet = '☄️'
    lightning = '⚡'
    danger = '⚠️'
    stop = '🚫'
    calendar = '🗓'
    marker = '📍'
    clock = '🕖'
    people = '👥'
    money = '💰'
    pencil = '✏️'
    credit_card = '💳'
    orange = '🟧'
    blue = '🟦'
    green = '🟩'
    running_guy = '🏃‍♂️'
    voice = '📢'

TEAM_EMOJI = {
    TEAM_NAMES[0]: Emoji.orange.value,
    TEAM_NAMES[1]: Emoji.blue.value,
    TEAM_NAMES[2]: Emoji.green.value,
}

LOGO_URL = 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/EA_Sports_monochrome_logo.svg/1200px-EA_Sports_monochrome_logo.svg.png'

MONTHES = [
    None,
    'января',
    'февраля',
    'марта',
    'апреля',
    'мая',
    'июня',
    'июля',
    'августа',
    'сентрября',
    'октября',
    'ноября',
    'декабря'
]

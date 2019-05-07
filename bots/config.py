from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from bots.models import ViberBotToken


bot_configuration = BotConfiguration(
    name='TopMarketTest',
    avatar='http://viber.com/avatar.jpg',
    auth_token='YOUR_AUTH_TOKEN_HERE'
)

viber = Api(bot_configuration)

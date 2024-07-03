from telegram import Bot

class Telegram_Module:
    def __init__(self, api_token, group_chat_id):
        """
        Initialize the Telegram_Module with API token and group chat ID.

        Args:
        - api_token (str): API token for accessing the Telegram Bot API.
        - group_chat_id (str): ID of the group chat where messages will be sent.
        """
        self.bot_token = api_token
        self.group_chat_id = group_chat_id
        self.bot = Bot(token=self.bot_token)

    async def send_message(self, message):
        """
        Send a message to the specified group chat.

        Args:
        - message (str): The message text to send.
        """
        await self.bot.send_message(chat_id=self.group_chat_id, text=message)

#bot.py
import discord
import Ledger
import configparser
 
class DiscordBot:
    def __init__(self, token):
        self.token = token
        intents = discord.Intents.all()
        self.client = discord.Client(intents=intents)
        ledger = Ledger.LedgerGraph()
 
        @client.event
        async def on_message(self, message):
            self.history.append(message)
            print(f'Message received in channel {message.channel.name}: {message.author.name}: {message.content}')

            if message.content == "Hello World!":
                reversed_message = message.content[::-1]
                ledger.add_line('2023-05-05', '2023-05-05', 'expense', False, 100, 'line1', 'description1')

                await message.channel.send(reversed_message)
                await message.channel.send(ledger.get_all_lines())
                ledger.remove_line('line1')
                await message.channel.send(ledger.get_all_lines())



 
    def run(self):
        self.client.run(self.token)
 
if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config.ini')
    token = config.get('discord', 'token')
    print(token)
    bot = DiscordBot(token)
    bot.run()
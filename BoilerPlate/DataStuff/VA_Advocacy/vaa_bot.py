#vaa_bot.py
import discord
import EntityIO
import configparser

class DiscordBot:
    def __init__(self, token):
        self.token = token
        intents = discord.Intents.all()
        self.client = discord.Client(intents=intents)
        self.guild = None
        self.members = []
        self.roles = []
        self.channels = []
        self.history = []
        entity_io = EntityIO.EntityIO()

        @self.client.event
        async def on_ready():
            print(f'Logged in as {self.client.user.name} ({self.client.user.id})')
            for guild in self.client.guilds:
                print(f'Joined server: {guild.name} (ID: {guild.id})')
                self.guild = guild
                self.members = self.guild.members
                for member in self.members:

                    entity_io.add_entity(
                        entity_id=member.id,
                        name=member.name,
                        date_initiated="",
                        date_inactive="",
                        entity_type="",
                        objective_set="",
                        party_set="",
                        party_role_set="",
                        contact_hashes=""
                    )
                self.channels = self.guild.text_channels
                
                print(f'Loaded {len(self.members)} members')

                # Print out all the channels in the guild
                for channel in self.channels:
                    print(f'Channel: {channel.name} (ID: {channel.id})')

                    # Fetch message history of the channel
                    messages = []
                    async for message in channel.history(limit=None):
                        messages.append(message)

                    for message in messages:

                        print(f'{message.channel.name}: {message.author.name}: {message.content}')

        @self.client.event
        async def on_message(message):
            self.history.append(message)
            print(f'Message received in channel {message.channel.name}: {message.author.name}: {message.content}')


    def run(self):
        self.client.run(self.token)

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config.ini')
    token = config.get('discord', 'token')
    print(token)
    bot = DiscordBot(token)
    bot.run()
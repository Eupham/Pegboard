import discord
import Ledger
import configparser
import redis_flush
 
class DiscordBot:
    def __init__(self, token):
        self.token = token
        self.history = []
        intents = discord.Intents.all()
        self.client = discord.Client(intents=intents)
        self.ledger = Ledger.LedgerGraph()
        self.flush = redis_flush.RedisDB()
 
        @self.client.event
        async def on_message(message):
            self.history.append(message)

            if message.content == "esaelP Hello World!":
                reversed_message = message.content[::-1]
                await message.channel.send(reversed_message)
                self.ledger.add_line('2023-05-05', '2023-05-05', 'expense', False, 100, 'line1', 'description1')
                await message.channel.send(self.ledger.get_all_lines())
                self.ledger.remove_line('line1')
                await message.channel.send(self.ledger.get_all_lines())
            
            if message.content == "esaelP flush it all":
                reversed_message = message.content[::-1]
                await message.channel.send(reversed_message)
                self.flush.delete_all()
                await message.channel.send("All keys and data have been deleted from Redis.")

            if message.content.startswith("esaelP add_line "):
                content = message.content.split("add_line ")[1]
                values = content.split(":")
                if len(values) == 7:
                    date, date_accrued, line_type, accrued_bool, amount, line_id, description = values
                    self.ledger.add_line(date, date_accrued, line_type, accrued_bool, amount, line_id, description)
                    await message.channel.send(f"Added line with ID {line_id}.")
                else:
                    await message.channel.send("Invalid input. Please provide date:date_accrued:type:accrued_bool:amount:id:description.")

            if message.content.startswith("esaelP remove_line "):
                line_id = message.content.split("remove_line ")[1]
                self.ledger.remove_line(line_id)
                await message.channel.send(f"Removed line with ID {line_id}.")

            if message.content == "esaelP get_all_lines":
                lines = self.ledger.get_all_lines()
                if not lines:
                    await message.channel.send("No lines found.")
                else:
                    for line in lines:
                        await message.channel.send(f"Date: {line[0]}, Date Accrued: {line[1]}, Type: {line[2]}, Accrued Bool: {line[3]}, Amount: {line[4]}, ID: {line[5]}, Description: {line[6]}")

            if message.content.startswith("esaelP s_lines "):
                args = message.content.split("s_lines ")[1].split(":")
                property_name = args[0]
                property_value = args[1]
                lines = self.ledger.s_lines(property_name, property_value)
                if not lines:
                    await message.channel.send(f"No lines found with {property_name} = {property_value}.")
                else:
                    for line in lines:
                        await message.channel.send(f"Date: {line[0]}, Date Accrued: {line[1]}, Type: {line[2]}, Accrued Bool: {line[3]}, Amount: {line[4]}, ID: {line[5]}, Description: {line[6]}")

            # if message.content.startswith("esaelP range_s_dates "):
            #     # Extract the start and end dates from the message content
            #     _, start_date, end_date = message.content.split()

            #     # Call the range_s_dates method with the extracted dates
            #     result = my_object.range_s_dates(start_date, end_date)

            #     # Send the result back to the user
            #     await message.channel.send(result)

    def run(self):
        self.client.run(self.token)
 
if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config.ini')
    token = config.get('discord', 'token')
    bot = DiscordBot(token)
    bot.run()

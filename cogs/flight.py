from nextcord.ext import commands
from nextcord.utils import get
import nextcord
import json
from nextcord import SlashOption


class Flight(commands.Cog):

    '''
    Flight data mock-up

    {'lff':
        [
            {
                'user': <Member id=106828075274149888 name='Grimnir' discriminator='3890' bot=False nick='Xeraos' guild=<Guild id=358048911144779777 name='emoji' shard_id=0 chunked=True member_count=3>>,
                'aircraft': 'FA-18C',
                'notes': None,
                'flight': None
            }
        ],
    'flights': [
            {
                'name' : "biguses"
                'lead' : interaction.user
                'members' : [{user, aircraft}]
                'size' : 1
                'flight-Notes' : ''
            }
        ]
    }
    '''

    # init vars and task loops
    def __init__(self, bot):
        self.bot = bot
        self.flight_data = {
            # holding array for pilots looking for flight
            "lff": [],
            # currently existing flights
            "flights": [

            ]
        }
        self.available_aircraft = []
        try:
            with open("available_aircraft.json") as available_aircraft_file:
                self.available_aircraft = json.load(available_aircraft_file)
            print("available_aircraft loaded")
            available_aircraft_file.close()
        except IOError as e:
            print("No available_aircraft.json detected!")
            raise e

    # if for some reason we crash and start up again
    # remove all gci roles from all guilds
    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            for member in guild.members:
                role = get(member.guild.roles, name="Looking for Flight")
                if role in member.roles:
                    await member.remove_roles(role)

    @nextcord.slash_command(name="flight", guild_ids=[358048911144779777, 772617490827313162, 924753029402619924])
    async def flight(self):
        pass

    @flight.subcommand(description='Get a listing of current flights pilots LFF')
    async def listing(self, interaction: nextcord.Interaction, show: bool = SlashOption(description='Show Listing pubicly?', default=False, required=False)):
        embed = nextcord.Embed(
            title=f"Pilots Looking For Flight",
            description="Use `!help flight` for assistance.",
            color=0x03B300,
        )
        embed.set_author(
            name=interaction.user, icon_url=interaction.user.avatar.url)

        pilotsLFF = ''

        if len(self.flight_data['lff']) > 0:
            for pilot in self.flight_data['lff']:
                pilotsLFF = pilotsLFF + \
                    f"`{pilot['user']}` - `{pilot['aircraft']}` - `{pilot['notes']}`\n"
        else:
            pilotsLFF = 'None!'

        pilotsLFF = pilotsLFF + '\n\n***Active Flights***\n\n'

        embed.add_field(name='Current Pilots LFF',
                        value=pilotsLFF, inline=False)

        for flight in self.flight_data['flights']:

            members_string = ''
            empty_slots = '`--Empty Slot--`\n'
            for count, member in enumerate(flight['members'], start=1):
                members_string = members_string + \
                    f'`{flight["name"]} 1-{count}` | `{member["user"].name}` - `{member["aircraft"]}`\n'

            if (flight['size'] - len(flight['members'])) > 0:
                empty_slots = empty_slots * \
                    (flight['size'] - len(flight['members']))

            flight_string = f'''
            Flight Description: `{flight['notes']}`
            Flight Lead: `{flight['lead']}`
            Slots: `{len(flight['members'])}/{flight['size']}`
            ***Flight Slots***
            {members_string} {empty_slots}
            '''
            embed.add_field(name=flight['name'],
                            value=flight_string, inline=True)

        await interaction.response.send_message(embed=embed, ephemeral=not(show))

    @flight.subcommand(description="Set yourself as looking for flight")
    async def lff(self, interaction: nextcord.Interaction,
                  aircraft: str = SlashOption(
                      description='What Airframe are you planning to fly?', choices=[
                          "F-14A",
                          "F-14B",
                          "F/A-18C",
                          "JF-17",
                          "AV-8N",
                          "A10-C",
                          "A10-C II",
                          "A10-A",
                          "AJ-37",
                          "C101",
                          "SU-25",
                          "MIG-29A",
                          "MIG-29G",
                          "SU-27",
                          "MIG-21"
                      ]

                  ),

                  notes: str = SlashOption(
                      description="Notes That you wish to add for your listing.",
                      required=False,
                      default="N/A"
                  )):
        if not any(user["user"] == interaction.user for user in self.flight_data['lff']):

            self.flight_data['lff'].append({
                "user": interaction.user,
                "aircraft": aircraft,
                "notes": notes,
                "flight": None
            })
            role = get(interaction.user.guild.roles,
                       name="Looking For Flight")
            await interaction.user.add_roles(role)
            await interaction.response.send_message("Done!", ephemeral=True)

    @flight.subcommand(description="Create a Flight for people to join.")
    async def create(self, interaction: nextcord.Interaction,
                     flight_name: str = SlashOption(name='name',
                                                    description='The callsign of your flight'),
                     flight_size: int = SlashOption(
                         name='size', description='The Size of your Flight', max_value=6, min_value=2),
                     flight_notes: str = SlashOption(
                         name='notes', description='Extra infomation to displayed about the flight', default='N/A', required=False
                     )
                     ):
        # check to see if the user has an already open flight
        if not any(flight["lead"] == interaction.user for flight in self.flight_data['flights']) or interaction.user.guild_permissions.administrator:

            self.flight_data['flights'].append({
                'name': flight_name.capitalize(),
                'lead': interaction.user,
                'members': [],
                'size': flight_size,
                'notes': flight_notes
            })
            await interaction.response.send_message("Done!", ephemeral=True)

        else:
            await interaction.response.send_message('You have already created a flight. Please retire the flight before creating another.')

    @flight.subcommand(description="Join a Flight")
    async def join(self, interaction: nextcord.Interaction,
                   flight_name: str = SlashOption(name='name',
                                                  description='The callsign of your flight'),
                   aircraft: str = SlashOption(
                       description='What Airframe are you planning to fly?',
                       choices=[
                           "F-14A",
                           "F-14B",
                           "F/A-18C",
                           "JF-17",
                           "AV-8N",
                           "A10-C",
                           "A10-C II",
                           "A10-A",
                           "AJ-37",
                           "C101",
                           "SU-25",
                           "MIG-29A",
                           "MIG-29G",
                           "SU-27",
                           "MIG-21"
                       ])):
        if any(flight["name"] == flight_name for flight in self.flight_data['flights']):
            for flight in self.flight_data['flights']:
                for member in flight['members']:
                    if interaction.user == member['user']:
                        await interaction.response.send_message(
                            'You are in a Flight already. Please leave using `!leave` before joining another flight.')
                        return

        for flight in self.flight_data['flights']:
            if flight['name'] == flight_name:
                if len(flight['members']) < flight['size']:
                    flight['members'].append(
                        {
                            'user': interaction.user,
                            'aircraft': aircraft
                        }
                    )
                    await interaction.response.send_message("Done!", ephemeral=True)
                else:
                    await interaction.response.send_message(
                        f'Flight `{flight_name}` is currently full')

    @flight.subcommand(description="Leave a Flight")
    async def leave(self, interaction: nextcord.Interaction):
        for flight in self.flight_data['flights']:
            for count, member in enumerate(flight['members']):
                if member['user'] == interaction.user:
                    flight['members'].pop(count)
                    await interaction.response.send_message("Done!")
                    return

    @flight.subcommand(description="Create a Flight for people to join.")
    async def retire(self, interaction: nextcord.Interaction):
        for count, flight in enumerate(self.flight_data['flights']):
            if flight['lead'] == interaction.user:
                self.flight_data['flights'].pop(count)
                await interaction.response.send_message("Done!")
                return


def setup(bot):
    bot.add_cog(Flight(bot))

import discord

# Create a bot instance
bot = discord.Client(intents=discord.Intents.all())

# Prompt for bot token
bot_token = input('Enter your Discord bot token: ')
prefix = input('Enter the command with prefix that you want to use to copy server(!test or $start): ') or "$start"

@bot.event
async def on_ready():
    print('Logged on as', bot.user.name)

    # Print intro with GitHub reference
    print('Welcome to the DiscoCloner!')
    print('This bot is created by ghalbeyou (https://github.com/ghalbeyou)')
    print('Bot token has been provided and the bot is ready to start.\nYou can read documents in the main github page: https://github.com/ghalbeyou')

@bot.event
async def on_message(message: discord.Message):
    # Check if the message is from the bot itself to avoid an infinite loop
    if message.author == bot.user:
        return

    # Check if the message is a command to start the channel and role copying process
    if message.content.startswith(prefix):
        # Get the source server ID and destination server ID from the console
        source_server_id = message.author.guild.id #input('Enter source server ID: ')
        destination_server_id = input('Enter the Destination server ID (123456789): ')

        # Fetch the source server and destination server objects
        source_server = bot.get_guild(int(source_server_id))
        destination_server = bot.get_guild(int(destination_server_id))

        if source_server is None:
            print('Source server not found.')
            return

        if destination_server is None:
            print('Destination server not found.')
            return

        # Fetch all categories in the source server
        source_categories = source_server.categories

        # Create categories in the destination server
        for source_category in source_categories:
            # Create a category in the destination server with the same name and permissions as the source category
            permissions = source_category.overwrites
            new_category = await destination_server.create_category_channel(name=source_category.name,
                                                                            overwrites=permissions)
            print(f'Clone successful for category: {new_category.name}')

            # Fetch all channels within the source category
            source_channels = source_category.text_channels

            # Create channels in the destination category
            for source_channel in source_channels:
                # Check if the channel is hidden and has read_messages permission set to False
                if source_channel.overwrites_for(source_server.default_role).read_messages is False:
                    # Create a hidden channel in the destination category with the same name and permissions as the source channel
                    overwrites = source_channel.overwrites
                    hidden_channel = await new_category.create_text_channel(name=source_channel.name,
                                                                             overwrites=overwrites)
                    print(f'Clone successful for hidden channel: {hidden_channel.name} (Category: {new_category.name})')
                else:
                    # Create a regular channel in the destination category with the same name and permissions as the source channel
                    new_channel = await new_category.create_text_channel(name=source_channel.name)
                    print(f'Clone successful for channel: {new_channel.name} (Category: {new_category.name})')

        # Fetch all roles in the source server
        source_roles = source_server.roles

        # Create roles in the destination server
        for source_role in source_roles:
            # Exclude @everyone role
            if source_role.name == '@everyone':
                continue

            # Create a role in the destination server with the same name, color, and permissions as the source role
            permissions = source_role.permissions
            color = source_role.color
            hoist = source_role.hoist
            mentionable = source_role.mentionable
            new_role = await destination_server.create_role(name=source_role.name, permissions=permissions,color=color, hoist=hoist, mentionable=mentionable)
            print(f'Clone successful for role: {new_role.name}')
            print('\nClone was successfully done. thanks for using this repo. make sure to give it a star;)')
bot.run(token=bot_token)
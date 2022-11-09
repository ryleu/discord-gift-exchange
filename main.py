#!/bin/env python3

import interactions
import random
import time
from os import environ

def main():
    bot = interactions.Client(token = environ['TOKEN'])

    @bot.event(
        name = 'on_ready'
    )
    async def on_ready():
        print(f'logged in as {bot.me.name}')

    @bot.command(
        name = 'create',
        description = 'Create a new gift exchange event'
    )
    async def create_command(ctx: interactions.CommandContext):
        await ctx.send(
            f'**Gift Exchange**\n\nParticipants:\n<@{ctx.author.id}>',
            components = interactions.spread_to_rows(
                interactions.Button(style = 3, custom_id = 'join_exchange', label = 'Join'),
                interactions.Button(style = 4, custom_id = 'leave_exchange', label = 'Leave'),
                interactions.Button(style = 1, custom_id = 'randomize_exchange', label = 'Randomize')
            )
        )
    
    @bot.component('join_exchange')
    async def join_exchange(ctx: interactions.ComponentContext):
        if str(ctx.author.id) in ctx.message.content:
            return await ctx.send('You\'re already in the exchange.', ephemeral = True)
        
        await ctx.edit(ctx.message.content + f'\n<@{ctx.author.id}>')
    
    @bot.component('leave_exchange')
    async def join_exchange(ctx: interactions.ComponentContext):
        if str(ctx.author.id) not in ctx.message.content:
            return await ctx.send('You\'re not in the exchange.', ephemeral = True)
        
        await ctx.edit(ctx.message.content.replace(f'\n<@{ctx.author.id}>', ''))

    @bot.component('randomize_exchange')
    async def randomize_exchange(ctx: interactions.ComponentContext):
        people = [ int(x[2:-1]) for x in ctx.message.content.split('Participants:\n')[1].split('\n') ]
        owner = people[0]
        if ctx.author.id != owner:
            return await ctx.send('You do not have permission to use this function.', ephemeral = True)
        
        await ctx.edit(
            components = interactions.spread_to_rows(
                interactions.Button(style = 3, custom_id = 'confirm_randomize_exchange', label = 'Confirm'),
                interactions.Button(style = 4, custom_id = 'cancel_randomize_exchange', label = 'Cancel')
            )
        )
    
    @bot.component('cancel_randomize_exchange')
    async def cancel_randomize_exchange(ctx: interactions.ComponentContext):
        people = [ int(x[2:-1]) for x in ctx.message.content.split('Participants:\n')[1].split('\n') ]
        owner = people[0]
        if ctx.author.id != owner:
            return await ctx.send('You do not have permission to use this function.', ephemeral = True)
        
        await ctx.edit(
            components = interactions.spread_to_rows(
                interactions.Button(style = 3, custom_id = 'join_exchange', label = 'Join'),
                interactions.Button(style = 4, custom_id = 'leave_exchange', label = 'Leave'),
                interactions.Button(style = 1, custom_id = 'randomize_exchange', label = 'Randomize')
            )
        )
    
    @bot.component('confirm_randomize_exchange')
    async def confirm_randomize_exchange(ctx: interactions.ComponentContext):
        people = [ int(x[2:-1]) for x in ctx.message.content.split('Participants:\n')[1].split('\n') ]
        owner = people[0]
        if ctx.author.id != owner:
            return await ctx.send('You do not have permission to use this function.', ephemeral = True)

        if len(people) <= 1:
            return await ctx.send('There are not enough people to randomize.', ephemeral = True)
        
        await ctx.defer()
        
        people_dict = {}
        randomized = False

        attempts = 0

        while not(randomized):
            attempts += 1

            people_dict = {}
            temp_people = people.copy()
            
            for person in people:
                index = random.randint(0, len(temp_people) - 1)
                people_dict[person] = temp_people.pop(index)
            
            randomized = True

            for person in people:
                if people_dict[person] == person:
                    randomized = False
                    break

        for person in people:
            time.sleep(1)
            user = await interactions.get(bot, interactions.User, object_id = person)
            try:
                await user.send(f'You were assigned <@{people_dict[person]}> from the gift exchange in <#{ctx.channel.id}>.')
            except interactions.api.error.LibraryException:
                await ctx.channel.send(f'Failed to message <@{person}> (`{person}`). Please check your privacy settings in this server to ensure that "Direct Messages" is enabled.')

        await ctx.send(f'Finished assigning users. Took {attempts} attempt(s).')

    bot.start()

if __name__ == '__main__':
    main()
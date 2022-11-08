#!/bin/env python3

import interactions
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
            '**Gift Exchange**\n\nParticipants:',
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
        await ctx.send('You do not have permission to use this function.', ephemeral = True)

    bot.start()

if __name__ == '__main__':
    main()
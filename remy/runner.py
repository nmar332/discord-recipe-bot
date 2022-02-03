import logging 

import telegram

import discord

import spoonacular_helper as sp

import exceptions

import random

import exceptions

import config

spoon = sp.SpoonacularFacade()

discord_token = "DISCORD KEY HERE"

client = discord.Client()

@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))
    
@client.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    #channel = str(message.channel.name)
    print(f'{username}: {user_message} ')
    
    if message.author == client.user:
        return
    #message.channel.name == 'recipes'
    if 1 == 1 :
        if user_message.lower() == 'hello' or user_message.lower() == 'hi' or user_message.lower() == 'hey':
            if username == "whitesodaboy":
                await message.author.send("Ḧ̵͖͖̦̥̗̳̇̀͗̚͜ę̷͚̈l̸̩̞͍̈̍̂̉l̷̠̮͍͎̺̐̅͜ö̵̤̞́̉̈́̕͝ ̶̢̊Ş̴͕͈̻͇̪̯̔̎̈́̓̆̈́͝e̷͚̪̅̎t̶̻͖̫̙̄̔́͐h̷̡̰̝̭̝͕̒͑̾.̶̲̈.̸̡̲͉͓̣̼̤̓͋̈͂̆̔.̸̡̞͇̪̜̐̽̄̀̅.̷̘̜̝̣͚̻̬̓̽͆̓̾̽͘")
            elif username == "SpazFish":
                await message.author.send("Ḧ̵͖͖̦̥̗̳̇̀͗̚͜ę̷͚̈l̸̩̞͍̈̍̂̉l̷̠̮͍͎̺̐̅͜ö̵̤̞́̉̈́̕͝ ̶̢̊Ş̴͕͈̻͇̪̯̔̎̈́̓̆̈́͝e̷͚̪̅̎t̶̻͖̫̙̄̔́͐h̷̡̰̝̭̝͕̒͑̾.̶̲̈.̸̡̲͉͓̣̼̤̓͋̈͂̆̔.̸̡̞͇̪̜̐̽̄̀̅.̷̘̜̝̣͚̻̬̓̽͆̓̾̽͘")
            else:
                await message.author.send(f'Hi {username}! : ), you can type !help for more information.')
            return
        
        elif user_message.lower() == "what do you use to stir?":
            await message.channel.send("A toothpick!")
            
        elif user_message.lower() == '!allowedtags':
            await message.channel.send("I've dm'd you a list of allowed tags!")
            tags = []
            for i in config.ALLOWED_TAGS:
                i = i.replace("'", "")
                tags.append(i)
            diets= tags[:10]
            intolerances= tags[10:22]
            cuisines = tags[22:48]
            meal_types = tags[48:]
            await message.author.send("**Allowed Tags**\n" + "__Diets__\n" + ", ".join(diets) +
                                      "\n\n__Intolerances__\n" + ", ".join(intolerances) +
                                    "\n\n__Cuisines__\n" + ", ".join(cuisines) +
                                    "\n\n__Meal Types__\n" + ", ".join(meal_types)
                                    )
            
        elif user_message.lower() == 'bye':
            await message.channel.send("Goodbye!")
            
        elif user_message.lower() == '!help':
           await message.channel.send("You can use the following commands to talk to me:\n"
            "!recipe 'ingredient 1, ingredient2...' or just leave blank for a random recipe\n"
            "!mealtype 'diets, intolerances, cuisines, meal types'\n"
            "!allergy 'allgeries' \n"
            "!happyhour\n"
            "!allowedtags\n"
            )
           
        elif "!mealtype" in user_message.lower():
            await message.channel.send("Fetching random recipe... \n")
            context = user_message.split('!mealtype')[1]
            context = context.split(',')
            all_args = []
            for i in context:
                a = i.strip()
                all_args.append(a)
            #all_args = ",".join(context.args).lower().split(",")
            for value in all_args:
                print(value)
                if value not in config.ALLOWED_TAGS:
                    await message.channel.send("Illegal tag used, type !allowedtags to view a list of legal tags. \n")
                    raise exceptions.InvalidRandomTagError()

            # Consolidate valid tags into single query
            tags = ",".join(all_args)
            recipe = spoon.get_random_recipe(tags=tags)
            if recipe == "empty":
                await message.channel.send("No recipes found")
            else:
                text_message, parse_mode = format_message_and_get_parse_mode(recipe)
                discord_dict = {'<b>': "**", '</b>': "**", "<u>": "__", "</u>": "__", }
                for i, j in discord_dict.items():
                    text_message = text_message.replace(i, j)
                
                try:
                    await message.channel.send(text_message)
                except:
                    await message.channel.send("Hmm... thats weird, some error occured. Maybe the recipe was too long for discord...")
            
            
        
        
        elif "!allergy" in user_message.lower():
            allergies = user_message.split('!allergy')[1]
            allergies = allergies.split(',')
            if len(allergies[0].strip()) > 0:
            
                allergies2 = []
                for i in allergies:
                    a = i.strip()
                    allergies2.append(a)
                if not len(allergies2[0]) == 0:
                    await message.channel.send(f'Looking for a random recipe without {str(allergies2)[1:-1]}. \n')
                    while True:
                        recipe = spoon.get_random_recipe()
                        count = 1
                        total_list_len = len(allergies2) + len(recipe['extendedIngredients'])
                        for i in recipe['extendedIngredients']:
        
                            for j in allergies2:
                                #j.lower() != i['nameClean'] or 
                                if j.lower() not in i['nameClean']:
                                    print("Checking if {} == {}".format(j.lower(), i['nameClean']))
                                    count += 1
                                else:
                                    print("{} == {} | ALLERGY FOUND".format(j.lower(), i['nameClean']))         
                        if count >= total_list_len:
                            
                            break
                        print("RECIPE HAS ALLERGY, DO NOT SEND")
                    txt_message, parse_mode = format_message_and_get_parse_mode(recipe)
                    
                
                discord_dict = {'<b>': "**", '</b>': "**", "<u>": "__", "</u>": "__", }
                for i, j in discord_dict.items():
                    txt_message = txt_message.replace(i, j)
                
                try:
                    await message.channel.send(txt_message)
                except:
                    await message.channel.send("Hmm... thats weird, some error occured. Maybe the recipe was too long for discord...")
            
                 
                await message.channel.send("**Disclaimer** This bot checks if your allergy is in a certain recipes ingredients list pulled from the spoonacular database. Please proceed with caution as some items within ingredients may not be disclosed and might trigger allergies.")
            else:
                await message.channel.send("Please include an allergy.")
            
            
        elif "!recipe" in user_message.lower():
            ingredients = user_message.split('!recipe')[1]
            ingredients = ingredients.split(',')
            ingredients2 = []
            for i in ingredients:
                a = i.strip()
                ingredients2.append(a)
            print(ingredients2)
            if not len(ingredients2[0]) == 0:
                await message.channel.send(f'Looking for a random recipe containing {str(ingredients2)[1:-1]}. \n')
                recipe_ids = spoon.get_recipe_ids_for_ingredients(ingredients2)
                
                if not recipe_ids:
                        await message.channel.send(f"No recipe was found containing {str(ingredients2)[1:-1] }. \n") 
                        raise exceptions.RecipesNotFoundError()
                else:
                    recipe_ids = spoon.get_recipe_ids_for_ingredients(ingredients)
                    print("120")
                    if not recipe_ids:
                        logging.info("No recipes found.")
                        raise exceptions.RecipesNotFoundError()
                    len_random = len(recipe_ids)
                    random_int = random.randint(0, len_random-1)
                    recipes = spoon.get_recipes_for_ids(recipe_ids)
                    
                    
                    for recipe in recipes:
                        txt_message, parse_mode = format_message_and_get_parse_mode(recipe)
                        
            else:
                await message.channel.send("Fetching random recipe... \n")
                recipe = spoon.get_random_recipe()
                txt_message, parse_mode = format_message_and_get_parse_mode(recipe)
                
            
                    
            discord_dict = {'<b>': "**", '</b>': "**", "<u>": "__", "</u>": "__", }
            for i, j in discord_dict.items():
                txt_message = txt_message.replace(i, j)
            try:
                await message.channel.send(txt_message)
            except:
                await message.channel.send("Hmm... thats weird, some error occured. Maybe the recipe was too long for discord...")
            
        
        elif user_message.lower() == "!happyhour":
            await message.channel.send("Fetching random drink... \n")
            recipe_id = spoon.get_random_alcoholic_beverage_recipe_id()
            recipe = spoon.get_recipes_for_ids([recipe_id])
            text_message, parse_mode = format_message_and_get_parse_mode(recipe[0])
            print(recipe)
            discord_dict = {'<b>': "**", '</b>': "**", "<u>": "__", "</u>": "__", }
            for i, j in discord_dict.items():
                text_message = text_message.replace(i, j)
            try:
                await message.channel.send(text_message)
            except:
                await message.channel.send("Hmm... thats weird, some error occured. Maybe the recipe was too long for discord...")
        
        else:
            await message.author.send(f'Hi {username}! : ), you can type !help for more information.')
            
            
'''WIP!!!!!!!!!!!!!!!!!!!!!!WIP!!!!!!!!!!!!!!!!!!!!!!!!!!WIP

WIP elif "!recipecard" in user_message.lower():
            card = spoon.gen_recipe_card(4632)
            await message.channel.send(card) 


'''      
    
    
    
def format_message_and_get_parse_mode(recipe):
    """Formats a message and returns the proper parse mode.
    
    Args:
        recipe: json-like dict of recipe data.
    Returns:
        Tuple of formatted message and parse mode
    """
    logging.info(
        f"Formatting the recipe: {recipe['title']} | id: {recipe['id']}")
    parse_mode = telegram.ParseMode.HTML
    message = sp.SpoonacularFacade.format_recipe_data_as_html(
        recipe)

    if len(message) > config.TELEGRAM_MESSAGE_CHAR_LIMIT:
        logging.info("Recipe too long! Formatting a link instead.")
        link = sp.SpoonacularFacade.format_recipe_title_link_as_markdown(recipe)
        message = (
            f"This recipe was too long to send here\! Here's the "
            f"link instead: {link}"
        )
        parse_mode = telegram.ParseMode.MARKDOWN_V2

    return message, parse_mode


client.run(discord_token)

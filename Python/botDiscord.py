import discord
from discord.ext import commands
from commandhisto import historique_commandes
from hashmap_data import Hashmap
import asyncio
import random
import os
import googlesearch 
import tree

intents = discord.Intents.all()
History = historique_commandes()
historique_utilisateurs = Hashmap(100)
client = commands.Bot(command_prefix="!", intents=intents)

@client.event
async def on_ready():
    print("Le bot est prêt !")
    asyncio.create_task(sauvegarde_periodique())
    await charger_donnees(historique_utilisateurs)

# Commande member_join
@client.event
async def on_member_join(member):
    general_channel = client.get_channel(1091337387294068788) # Remplacer 1234567890 par l'ID du canal général
    await general_channel.send("Bienvenue sur le serveur, {} !".format(member.mention))

# Commande hello
@client.command(name='hello')
async def hello(ctx):
    await ctx.send('Hello!')
    ajouter_historique_utilisateur(ctx.author.id, "!hello")
    History.add_command("!hello")

# Commande del
@client.command(name="del")
async def delete(ctx):
    await ctx.channel.purge(limit=10)
    ajouter_historique_utilisateur(ctx.author.id, "!del")
    History.add_command("!del")

# Commande helpi
@client.command(name="helpi")
async def helpi(ctx):
    commands = {
        "!hello": "Affiche un message de salutation.",
        "!sondage": "Crée un sondage avec des options.",
        "!rappel": "Programme un rappel pour l'utilisateur."
    }

    commands_text = "\n".join([f"{command}: {description}" for command, description in commands.items()])
    message = f"Voici la liste des commandes disponibles :\n```{commands_text}```"
    
    await ctx.send(message)


# Commande sondage
@client.command()
async def sondage(ctx, *, arguments):
    arguments = arguments.split('|')
    question = arguments[0]
    options = arguments[1:]

    if len(options) < 2 or len(options) > 10:
        await ctx.send('Vous devez fournir entre 2 et 10 options.')
        return

    message = f'{question}\n\n'
    for i, option in enumerate(options):
        message += f'{i+1}\U000020e3: {option}\n'
    poll = await ctx.send(message)

    for i in range(len(options)):
        emoji = f'{i+1}\U000020e3'
        await poll.add_reaction(emoji)
    ajouter_historique_utilisateur(ctx.author.id, "!sondage")
    History.add_command("!sondage")

# Commande rappel
@client.command()
async def rappel(ctx, temps: int, *, message):
    """Programme un rappel pour l'utilisateur"""
    await asyncio.sleep(temps)
    user = client.get_user(ctx.author.id)
    await user.send(f"Rappel : {message}")
    ajouter_historique_utilisateur(ctx.author.id, "!rappel")
    History.add_command("!rappel")

# Commande pierre-feuille-ciseaux
@client.command()
async def pfc(ctx, choix):
    choices = ['pierre', 'feuille', 'ciseaux']
    bot_choice = random.choice(choices)
    
    if choix not in choices:
        await ctx.send("Veuillez choisir entre 'pierre', 'feuille' ou 'ciseaux'")
    elif choix == bot_choice:
        await ctx.send(f"{bot_choice.capitalize()} ! Égalité !")
    elif (choix == 'pierre' and bot_choice == 'ciseaux') or \
         (choix == 'feuille' and bot_choice == 'pierre') or \
         (choix == 'ciseaux' and bot_choice == 'feuille'):
        await ctx.send(f"{bot_choice.capitalize()} ! Vous avez gagné !")
    else:
        await ctx.send(f"{bot_choice.capitalize()} ! Vous avez perdu !")
    ajouter_historique_utilisateur(ctx.author.id, "!pfc")
    History.add_command("!pfc")

# Commande gif chat
@client.command()
async def chat(ctx):
    await ctx.send('https://media.giphy.com/media/3oz8xLd9DJq2l2VFtu/giphy.gif')
    History.add_command("!chat")
    ajouter_historique_utilisateur(ctx.author.id, "!chat")



jokes = [
    "Pourquoi les plongeurs plongent-ils toujours en arrière et jamais en avant ? Parce que sinon ils tombent dans le bateau !",
    "Qu'est-ce qui est jaune et qui attend ? Jonathan.",
    "Qu'est-ce qui est petit, jaune, et qui est dangereux pour les dents ? Une petite boule de billard.",
    "Quel est le comble pour un électricien ? Ne pas être au courant.",
    "Quel est le comble pour un plombier ? De prendre la fuite.",
    "Pourquoi les poissons n'aiment-ils pas jouer au tennis ? Parce qu'ils ont peur des balles.",
    "Qu'est-ce qu'un oiseau sur un arbre qui chante faux ? Un playback.",
    "Qu'est-ce qu'un jardinier qui prend son temps ? Un légumineux.",
    "Qu'est-ce que crie un poisson lorsqu'il se cogne contre un mur ? 'Dam !'",
    "Qu'est-ce qu'un oiseau sur un arbre qui chante faux ? Un playback.",
    
]

# Commande blague
@client.event
async def on_message(message):
    global jokes  
    if message.author == client.user:
        return

    if message.content.startswith('!blague'):
        if len(jokes) == 0:
            jokes = [  
               "Pourquoi les plongeurs plongent-ils toujours en arrière et jamais en avant ? Parce que sinon ils tombent dans le bateau !",
                "Qu'est-ce qui est jaune et qui attend ? Jonathan.",
                "Qu'est-ce qui est petit, jaune, et qui est dangereux pour les dents ? Une petite boule de billard.",
                "Quel est le comble pour un électricien ? Ne pas être au courant.",
                "Quel est le comble pour un plombier ? De prendre la fuite.",
                "Pourquoi les poissons n'aiment-ils pas jouer au tennis ? Parce qu'ils ont peur des balles.",
                "Qu'est-ce qu'un oiseau sur un arbre qui chante faux ? Un playback.",
                "Qu'est-ce qu'un jardinier qui prend son temps ? Un légumineux.",
                "Qu'est-ce que crie un poisson lorsqu'il se cogne contre un mur ? 'Dam !'",
                "Qu'est-ce qu'un oiseau sur un arbre qui chante faux ? Un playback.",
                
            ]
        joke = random.choice(jokes)
        jokes.remove(joke)  
        await message.channel.send(joke)

# Commande recherche google
'''class Google(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.google_api_key = os.environ.get('AIzaSyD52WBiflVrrQzr8F-SMQeSVgBB1LR-ySU')

    @commands.command()
    async def google(self, ctx, *, query):
        """Effectue une recherche sur Google et renvoie les résultats"""
        search_results = googlesearch.search(query, num_results=5, api_key=self.google_api_key)
        results_text = "\n".join(search_results)
        await ctx.send(f"Résultats de la recherche pour '{query}':\n{results_text}")

def setup(bot):
    bot.add_cog(Google(bot))'''

# Commande full_history
@client.command(name="full_history")
async def full_history(ctx):
    all_commands = History.get_all_commands()
    await ctx.channel.send(all_commands)
    History.add_command("!full_history")
    ajouter_historique_utilisateur(ctx.author.id, "!full_history")
    
# Commande last_command
@client.command(name="last_command")
async def last_command(ctx):
    last_cmd = History.get_last_command()
    await ctx.channel.send(last_cmd)
    History.add_command("!last_command")
    ajouter_historique_utilisateur(ctx.author.id, "!last_command")

# Commande clear_command
@client.command(name="clear_command")
async def clear_command(ctx):
    History.clear()
    History.add_command("!clear_command")
    ajouter_historique_utilisateur(ctx.author.id, "!clear_command")

# fonction qui ajoute la commande à l'historique de l'utilisateur
def ajouter_historique_utilisateur(id_utilisateur, commande):
    if historique_utilisateurs.get(id_utilisateur) is None:
        historique_utilisateurs.append(id_utilisateur, [commande])
    else:
        historique_utilisateurs.append(id_utilisateur, historique_utilisateurs.get(id_utilisateur) + [commande])



# Sauvegarde les données dans un fichier JSON
@client.event
async def on_disconnect():
    await sauvegarde_donnees(historique_utilisateurs)  # Sauvegarder les données dans le fichier historique.json avant la déconnexion

async def sauvegarde_donnees(historique_utilisateurs):
    try:
        filename = 'historique.json'

        historique_utilisateurs.sauvegarder_donnees('historique.json')  # Appeler la fonction de sauvegarde de la classe Hashmap

    except Exception as e:
        print(f"Une erreur s'est produite lors de la sauvegarde des données : {e}")

async def charger_donnees(historique_utilisateurs):
    try:
        filename = 'historique.json'

        historique_utilisateurs.charger_donnees('historique.json')  # Appeler la fonction de chargement de la classe Hashmap

    except Exception as e:
        print(f"Une erreur s'est produite lors du chargement des données : {e}")

async def sauvegarde_periodique():
    try:
        while True:
            await sauvegarde_donnees(historique_utilisateurs)  # Appeler la fonction de sauvegarde périodiquement

            # Attendre 1 heure avant la prochaine sauvegarde
            await asyncio.sleep(5)
    except Exception as e:
        print(f"Une erreur s'est produite lors de la sauvegarde périodique des données : {e}")

# Commande historique
@client.command()
async def historique(ctx):
    historique = historique_utilisateurs.get(ctx.author.id)
    if historique is None:
        await ctx.send("Vous n'avez pas encore utilisé de commande !")
    else:
        message = "Voici votre historique de commandes : \n\n"
        for commande in historique:
            message += str(commande) + "\n"
        await ctx.send(message)




#tree
client.discussion = tree.DiscussionSystem()

@client.command()
async def discussion(ctx):
    client.discussion.reset_discussion()
    await ctx.send(client.discussion.get_response())

@client.command()
async def answer(ctx, response):
    client.discussion.process_answer(response)
    await ctx.send(client.discussion.get_response())

# Commande "reset"
@client.command()
async def reset(ctx):
    client.discussion.reset_discussion()
    await ctx.send("La discussion a été réinitialisée.")

# Commande "speak_about"
@client.command()
async def speak_about(ctx, topic):
    response = client.discussion.speak_about(topic)
    await ctx.send(response)



    
client.run("bot_id")

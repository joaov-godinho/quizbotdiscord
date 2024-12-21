import os
import discord
from discord import app_commands
from discord.ui import Button, View
import asyncio
import random
from dotenv import load_dotenv

load_dotenv()

id_do_servidor = 758148968826929193

# Banco de dados de animações
ANIMATIONS = {

    "Cyberpunk 2077": {"frames": ["frame1_cyberpunk2077.png", "frame2_cyberpunk2077.png", "frame3_cyberpunk2077.png", "frame4_cyberpunk2077.png", "frame5_cyberpunk2077.png"], 
                       "valid_answers": ["cyberpunk", "cyberpunk 2077", "cyberpunk: edgerunners", "cyberpunk edgerunners"]
                       },
    "Violet Evergarden": {"frames": ["frame1_violetevergarden.png", "frame2_violetevergarden.png", "frame3_violetevergarden.png", "frame4_violetevergarden.png", "frame5_violetevergarden.png"], 
                       "valid_answers": ["violet evergarden"]
                       },
    "Food Wars": {"frames": ["frame1_food wars.png", "frame2_food wars.png", "frame3_food wars.png", "frame4_food wars.png", "frame5_food wars.png"], 
                       "valid_answers": ["foodwars", "food wars", "shokugeki no souma"]
                       },
    "Akira": {"frames": ["frame1_akira.png", "frame2_akira.png", "frame3_akira.png", "frame4_akira.png", "frame5_akira.png"], 
                       "valid_answers": ["akira"]
                       },
    "Furi Kuri Alternative": {"frames": ["frame1_furikuri.png", "frame2_furikuri.png", "frame3_furikuri.png", "frame4_furikuri.png", "frame5_furikuri.png"], 
                       "valid_answers": ["furikuri", "furi kuri", "furi kuri alternative", "flcl"]
                       },
    "D-gray Man": {"frames": ["frame1_dgrayman.png", "frame2_dgrayman.png", "frame3_dgrayman.png", "frame4_dgrayman.png", "frame5_dgrayman.png"], 
                       "valid_answers": ["d-gray man", "dgray man", "d-gray"]
                       },
    "Akashic Records": {"frames": ["frame1_akashic.png", "frame2_akashic.png", "frame3_akashic.png", "frame4_akashic.png", "frame5_akashic.png"], 
                       "valid_answers": ["akashic", "akashic records", "Rokudenashi Majutsu Koushi to Akashic Records", "Akashic Records of Bastard Magic Instructor"]
                       },
    "Bakuman": {"frames": ["frame1_bakuman.jpg", "frame2_bakuman.jpg", "frame3_bakuman.jpg", "frame4_bakuman.jpg", "frame5_bakuman.png"], 
                       "valid_answers": ["bakuman"]
                       },
    "Owarimonogatari": {"frames": ["frame1_owarimonogatari.jpg", "frame2_owarimonogatari.jpg", "frame3_owarimonogatari.jpg", "frame4_owarimonogatari.jpg", "frame5_owarimonogatari.png"], 
                       "valid_answers": ["owarimonogatari"]
                       },
    "Burning Kabaddi": {"frames": ["frame1_kabaddi.png", "frame2_kabaddi.png", "frame3_kabaddi.png", "frame4_kabaddi.png", "frame5_kabaddi.png"], 
                       "valid_answers": ["burning kabaddi", "shakunetsu kabaddi"]
                       },
    "Kamisama Hajimemashita": {"frames": ["frame1_kamisama.jpg", "frame2_kamisama.jpg", "frame3_kamisama.jpg", "frame4_kamisama.jpg", "frame5_kamisama.jpg"], 
                       "valid_answers": ["kamisama hajimemashita", "kamisama kiss"]
                       },
    "Call of the Night": {"frames": ["frame1_cotn.png", "frame2_cotn.png", "frame3_cotn.png", "frame4_cotn.png", "frame5_cotn.png"], 
                       "valid_answers": ["call of the night", "yofukashi no uta"]
                       },
    "Bokutachi wa Benkyo ga Dekinai": {"frames": ["frame1_bokutachi.jpg", "frame2_bokutachi.jpg", "frame3_bokutachi.jpg", "frame4_bokutachi.jpg", "frame5_bokutachi.jpg"], 
                       "valid_answers": ["bokutachi wa benkyo ga dekinai", "bokutachi", "bokuben", "we can't study"]
                       },
    "K-on": {"frames": ["frame1_kon.png", "frame2_kon.png", "frame3_kon.png", "frame4_kon.png", "frame5_kon.png"], 
                       "valid_answers": ["kon", "k-on"]
                       },
    "Shingeki no Kyojin": {"frames": ["frame1_aot.jpg", "frame2_aot.jpg", "frame3_aot.jpg", "frame4_aot.jpg", "frame5_aot.jpg"], 
                       "valid_answers": ["shingeki no kyojin", "attack on titan", "aot", "snk"]
                       },
    "Yuri Yuri": {"frames": ["frame1_yuriyuri.png", "frame2_yuriyuri.png", "frame3_yuriyuri.png", "frame4_yuriyuri.png", "frame5_yuriyuri.png"], 
                       "valid_answers": ["yuri yuri"]
                       },
    "Majo no Tabitabi": {"frames": ["frame1_majotabi.png", "frame2_majotabi.png", "frame3_majotabi.png", "frame4_majotabi.png", "frame5_majotabi.png"], 
                       "valid_answers": ["majo no tabitabi", "Wandering Witch: The Journey of Elaina"]
                       },
    "Tenki no Ko": {"frames": ["frame1_tenkinoko.jpg", "frame2_tenkinoko.jpg", "frame3_tenkinoko.jpg", "frame4_tenkinoko.jpg", "frame5_tenkinoko.png"], 
                       "valid_answers": ["tenki no ko", "Weathering with You"]
                       },
    "Nier:Automata": {"frames": ["frame1_nier.png", "frame2_nier.png", "frame3_nier.png", "frame4_nier.png", "frame5_nier.png"], 
                       "valid_answers": ["nier automata", "NieR:Automata Ver1.1a", "nier", "nier:automata", "nier: automata"]
                       },
    "Anohana": {"frames": ["frame1_anohana.jpg", "frame2_anohana.jpg", "frame3_anohana.jpg", "frame4_anohana.jpg", "frame5_anohana.jpg"], 
                       "valid_answers": ["anohana", "Ano Hi Mita Hana no Namae wo Bokutachi wa Mada Shiranai", "Anohana: The Flower We Saw That Day"]
                       },
    "Monster": {"frames": ["frame1_monster.jpg", "frame2_monster.jpg", "frame3_monster.jpg", "frame4_monster.jpg", "frame5_monster.jpg"], 
                       "valid_answers": ["monster"]
                       },
    "Vivy: Fluorite Eye's Song": {"frames": ["frame1_vivy.png", "frame2_vivy.png", "frame3_vivy.png", "frame4_vivy.png", "frame5_vivy.png"], 
                       "valid_answers": ["vivy flourite eyes song", "vivy", "Vivy: Fluorite Eye's Song"]
                       },
    "Boku no Hero Academia": {"frames": ["frame1_bnha.jpg", "frame2_bnha.jpg", "frame3_bnha.jpg", "frame4_bnha.jpg", "frame5_bnha.jpg"], 
                       "valid_answers": ["boku no hero academia", "bnha", "my hero academia"]
                       },
    "Fruits Basket": {"frames": ["frame1_fbasket.jpg", "frame2_fbasket.jpg", "frame3_fbasket.jpg", "frame4_fbasket.jpg", "frame5_fbasket.jpg"], 
                       "valid_answers": ["fruits basket", "furuba"]
                       },
    "One Piece": {"frames": ["frame1_op.jpg", "frame2_op.jpg", "frame3_op.jpg", "frame4_op.jpg", "frame5_op.jpg"], 
                       "valid_answers": ["one piece", "op"]
                       },
    "Vinland Saga": {"frames": ["frame1_vinland.jpg", "frame2_vinland.jpg", "frame3_vinland.jpg", "frame4_vinland.jpg", "frame5_vinland.jpg"], 
                       "valid_answers": ["vinland saga"]
                       },
    "Dr. Stone": {"frames": ["frame1_drstone.png", "frame2_drstone.jpg", "frame3_drstone.jpg", "frame4_drstone.jpg", "frame5_drstone.jpg"], 
                       "valid_answers": ["dr stone", "dr. stone"]
                       },
}

class QuizBot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.all())
        self.synced = False
        self.current_game = None  # Armazena o estado do jogo
        self.scores = {}
        self.answered_users = set()
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await self.tree.sync(guild=discord.Object(id=id_do_servidor))
            self.synced = True
        print(f"Bot conectado como {self.user}.")

class StartQuizButton(Button):
    def __init__(self, channel):
        super().__init__(label="Iniciar Novo Jogo", style=discord.ButtonStyle.green)
        self.channel = channel

    async def callback(self, interaction: discord.Interaction):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("Apenas administradores podem iniciar um novo jogo.", ephemeral=True)
            return

        await interaction.response.send_message("🎮 **Iniciando novo jogo!**", ephemeral=True)
        await start_game(self.channel, interaction.client)

async def start_game(channel, bot):
    if bot.current_game is not None:
        await channel.send("⚠️ Um jogo já está em andamento! Aguarde o término antes de iniciar outro.")
        return

    bot.current_game = {
        "remaining_animes": list(ANIMATIONS.keys()),
        "rounds_left": 27,
        "channel_id": channel.id,
    }
    bot.scores.clear()
    await channel.send("🎮 **Novo Jogo Iniciado!** Prepare-se para 27 rodadas de quiz.")
    await start_round(channel, bot)

async def start_round(channel, bot):
    if bot.current_game is None or bot.current_game["rounds_left"] == 0:
        await end_game(channel, bot)
        return

    bot.current_game["rounds_left"] -= 1
    bot.answered_users.clear()

    remaining_animes = bot.current_game["remaining_animes"]
    animation_name = random.choice(remaining_animes)
    bot.current_game["remaining_animes"].remove(animation_name)

    quiz = ANIMATIONS[animation_name]
    frames = quiz["frames"][:5]
    bot.current_game["current_quiz"] = {
        "answer": animation_name,
        "frames": frames,
        "current_frame": 0,
    }

    await channel.send(f"🎮 **Rodada {27 - bot.current_game['rounds_left']}/27!** Adivinhe o nome da animação.")

    for frame_index, frame in enumerate(frames):
        if bot.current_game is None or bot.current_game["channel_id"] != channel.id:
            return

        bot.current_game["current_quiz"]["current_frame"] = frame_index + 1
        frame_path = f"C:\\Projects\\quizbot\\imagens\\{frame}"

        try:
            await channel.send(file=discord.File(frame_path))
        except FileNotFoundError:
            await channel.send(f"Erro: O frame '{frame}' não foi encontrado no diretório.")
            bot.current_game = None
            return
        except PermissionError:
            await channel.send(f"Erro: Permissões insuficientes para acessar o arquivo '{frame}'.")
            bot.current_game = None
            return

        await asyncio.sleep(20)

    if bot.current_game is not None and bot.current_game.get("channel_id") == channel.id:
        answer = bot.current_game["current_quiz"]["answer"]
        await channel.send(f"⏳ Fim da rodada! A resposta correta era **{answer}**.")
        bot.current_game["current_quiz"] = None

    await start_round(channel, bot)

async def end_game(channel, bot):
    await channel.send("🏁 **O jogo terminou! Aqui está o ranking final:**")
    await send_ranking(channel, bot)
    bot.current_game = None

async def send_ranking(channel, bot):
    ranking = sorted(bot.scores.items(), key=lambda item: item[1], reverse=True)
    ranking_message = "🏆 **Ranking Final**:\n" + "\n".join(
        f"<@{user_id}>: {score} pontos" for user_id, score in ranking
    )

    view = View()
    view.add_item(StartQuizButton(channel))

    await channel.send(ranking_message, view=view)

@app_commands.command(name="responder", description="Envie sua resposta para o quiz atual.")
async def responder_command(interaction: discord.Interaction, resposta: str):
    bot = interaction.client
    if not bot.current_game or "current_quiz" not in bot.current_game or not bot.current_game["current_quiz"]:
        await interaction.response.send_message("⚠️ Não há nenhum quiz ativo no momento.", ephemeral=True)
        return

    current_quiz = bot.current_game["current_quiz"]
    valid_answers = [ans.lower() for ans in ANIMATIONS[current_quiz["answer"]]["valid_answers"]]
    user_answer = resposta.lower().strip()
    user_id = interaction.user.id

    if user_id in bot.answered_users:
        await interaction.response.send_message("⚠️ Você já acertou esta rodada! Aguarde a próxima para responder novamente.", ephemeral=True)
        return

    if user_answer in valid_answers:
        bot.answered_users.add(user_id)
        points = max(5 - (current_quiz["current_frame"] - 1), 1)
        bot.scores[user_id] = bot.scores.get(user_id, 0) + points

        await interaction.response.send_message(
            f"🎉 Você acertou! A resposta correta era **{current_quiz['answer']}**. Você ganhou **{points} pontos**!", ephemeral=True
        )
    else:
        await interaction.response.send_message("❌ Resposta incorreta. Tente novamente!", ephemeral=True)

@app_commands.command(name="quiz", description="Inicia um quiz.")
async def quiz_command(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("Apenas administradores podem iniciar um quiz.", ephemeral=True)
        return

    await start_game(interaction.channel, interaction.client)

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
if not TOKEN:
    raise ValueError("O token do bot não foi definido. Defina a variável DISCORD_BOT_TOKEN no seu ambiente.")

bot = QuizBot()
bot.tree.add_command(responder_command, guild=discord.Object(id=id_do_servidor))
bot.tree.add_command(quiz_command, guild=discord.Object(id=id_do_servidor))
bot.run(TOKEN)

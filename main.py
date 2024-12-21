import os
import discord
from discord import app_commands
from discord.ui import Button, View
import asyncio
import random
from dotenv import load_dotenv

load_dotenv()

id_do_servidor = 925926517454827541

# Banco de dados de animações
ANIMATIONS = {
    "naruto": {"frames": ["frame1_naruto.jpg", "frame2_naruto.jpg", "frame3_naruto.jpg", "frame4_naruto.jpg", "frame5_naruto.jpg"]},
    "onepiece": {"frames": ["frame1_onepiece.jpg", "frame2_onepiece.jpg", "frame3_onepiece.jpg", "frame4_onepiece.jpg", "frame5_onepiece.jpg"]},
    "aot": {"frames": ["frame1_aot.jpg", "frame2_aot.jpg", "frame3_aot.jpg", "frame4_aot.jpg", "frame5_aot.jpg"]},
}

class QuizBot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.all())
        self.synced = False
        self.current_quiz = None
        self.scores = {}
        self.answered_users = set()  # Armazena IDs dos usuários que já responderam corretamente na rodada
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await self.tree.sync(guild=discord.Object(id=id_do_servidor))
            self.synced = True
        print(f"Bot conectado como {self.user}.")

class StartQuizButton(Button):
    def __init__(self, channel):
        super().__init__(label="Iniciar Nova Rodada", style=discord.ButtonStyle.green)
        self.channel = channel

    async def callback(self, interaction: discord.Interaction):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("Apenas administradores podem iniciar uma nova rodada.", ephemeral=True)
            return

        await interaction.response.send_message("🎮 **Iniciando nova rodada!**", ephemeral=True)
        await start_quiz(self.channel, interaction.client)

async def start_quiz(channel, bot):
    if bot.current_quiz is not None:
        await channel.send("⚠️ Um quiz já está em andamento! Aguarde o término antes de iniciar outro.")
        return

    animation_name, quiz = random.choice(list(ANIMATIONS.items()))
    frames = quiz["frames"][:5]
    bot.current_quiz = {
        "answer": animation_name,
        "frames": frames,
        "current_frame": 0,
        "channel_id": channel.id,
    }
    bot.answered_users.clear()  # Limpar os usuários que acertaram na rodada anterior

    await channel.send("🎮 **Novo Quiz Iniciado!** Adivinhe o nome da animação com base nos frames.")

    for frame_index, frame in enumerate(frames):
        if bot.current_quiz is None or bot.current_quiz.get("channel_id") != channel.id:
            return

        bot.current_quiz["current_frame"] = frame_index + 1
        frame_path = f"C:\\Projects\\quizbot\\imagens\\{frame}"

        try:
            await channel.send(file=discord.File(frame_path))
        except FileNotFoundError:
            await channel.send(f"Erro: O frame '{frame}' não foi encontrado no diretório.")
            bot.current_quiz = None
            return
        except PermissionError:
            await channel.send(f"Erro: Permissões insuficientes para acessar o arquivo '{frame}'.")
            bot.current_quiz = None
            return

        await asyncio.sleep(10)

    if bot.current_quiz is not None and bot.current_quiz.get("channel_id") == channel.id:
        await channel.send(f"⏳ Fim da rodada! A resposta correta era **{animation_name}**.")
        bot.current_quiz = None

    await send_ranking(channel, bot)

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
    if not bot.current_quiz or interaction.channel.id != bot.current_quiz["channel_id"]:
        await interaction.response.send_message("⚠️ Não há nenhum quiz ativo no momento.", ephemeral=True)
        return

    correct_answer = bot.current_quiz["answer"].lower()
    user_answer = resposta.lower().strip()
    user_id = interaction.user.id

    if user_id in bot.answered_users:
        await interaction.response.send_message("⚠️ Você já acertou esta rodada! Aguarde a próxima para responder novamente.", ephemeral=True)
        return

    if user_answer == correct_answer:
        bot.answered_users.add(user_id)
        points = max(5 - (bot.current_quiz["current_frame"] - 1), 1)
        bot.scores[user_id] = bot.scores.get(user_id, 0) + points

        await interaction.response.send_message(
            f"🎉 Você acertou! A resposta correta era **{correct_answer}**. Você ganhou **{points} pontos**!", ephemeral=True
        )
    else:
        await interaction.response.send_message("❌ Resposta incorreta. Tente novamente!", ephemeral=True)

@app_commands.command(name="quiz", description="Inicia um quiz.")
async def quiz_command(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("Apenas administradores podem iniciar um quiz.", ephemeral=True)
        return

    await start_quiz(interaction.channel, interaction.client)

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
if not TOKEN:
    raise ValueError("O token do bot não foi definido. Defina a variável DISCORD_BOT_TOKEN no seu ambiente.")

bot = QuizBot()
bot.tree.add_command(responder_command, guild=discord.Object(id=id_do_servidor))
bot.tree.add_command(quiz_command, guild=discord.Object(id=id_do_servidor))
bot.run(TOKEN)

import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))
TARGET_CHANNEL_ID = int(os.getenv("TARGET_CHANNEL_ID"))

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)


# === MODAL UNTUK BUAT EMBED === #
class EmbedModal(discord.ui.Modal, title="Buat Embed"):
    judul = discord.ui.TextInput(label="Judul", placeholder="Masukkan judul embed", required=False, max_length=256)
    deskripsi = discord.ui.TextInput(label="Deskripsi", style=discord.TextStyle.paragraph, placeholder="Masukkan isi deskripsi...", required=True, max_length=4000)
    warna = discord.ui.TextInput(label="Warna Embed (hex, misalnya #00ffcc)", required=False)

    async def on_submit(self, interaction: discord.Interaction):
        hex_color = self.warna.value.lstrip("#") or "2b2d31"
        try:
            color = discord.Color(int(hex_color, 16))
        except:
            color = discord.Color.default()

        embed = discord.Embed(
            title=self.judul.value or None,
            description=self.deskripsi.value,
            color=color
        )

        view = discord.ui.View(timeout=300)

        async def kirim_callback(btn_interaction: discord.Interaction):
            channel = interaction.client.get_channel(TARGET_CHANNEL_ID)
            if channel:
                await channel.send(embed=embed)
                await btn_interaction.response.edit_message(content="✅ Embed berhasil dikirim!", embed=None, view=None)
            else:
                await btn_interaction.response.send_message("⚠️ Channel tidak ditemukan.", ephemeral=True)

        async def edit_callback(btn_interaction: discord.Interaction):
            await btn_interaction.response.send_modal(EmbedModal())

        view.add_item(discord.ui.Button(label="✅ Kirim", style=discord.ButtonStyle.success, custom_id="kirim"))
        view.add_item(discord.ui.Button(label="🔁 Edit", style=discord.ButtonStyle.secondary, custom_id="edit"))

        view.children[0].callback = kirim_callback
        view.children[1].callback = edit_callback

        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


# === COMMAND: /buat_embed === #
@bot.tree.command(name="buat_embed", description="Buat embed interaktif")
@discord.app_commands.guilds(discord.Object(id=GUILD_ID))
async def buat_embed(interaction: discord.Interaction):
    await interaction.response.send_modal(EmbedModal())


# === COMMAND: /ping (tes bot) === #
@bot.tree.command(name="ping", description="Tes bot aktif")
@discord.app_commands.guilds(discord.Object(id=GUILD_ID))
async def ping_command(interaction: discord.Interaction):
    await interaction.response.send_message("🏓 Pong dari AxenX!", ephemeral=True)


# === BOT READY EVENT === #
@bot.event
async def on_ready():
    try:
        print(f"🔍 Jumlah command sebelum sync: {len(bot.tree.get_commands())}")
        for cmd in bot.tree.get_commands():
            print(f"🔹 Ditemukan command: /{cmd.name}")

        synced = await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
        print(f"✅ Slash command berhasil disinkron: {len(synced)} command")
        print(f"🤖 Bot siap sebagai {bot.user}")
    except Exception as e:
        print(f"❌ Gagal sync command: {e}")


# === JALANKAN BOT === #
bot.run(TOKEN)

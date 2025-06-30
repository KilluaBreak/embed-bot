# bot_embed_creator.py – Discord Bot untuk Membuat Embed Lengkap dengan Preview & Edit (Tanpa Prefix)

import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID", 0))
TARGET_CHANNEL_ID = int(os.getenv("TARGET_CHANNEL_ID", 0))

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

class ConfirmView(discord.ui.View):
    def __init__(self, embed: discord.Embed):
        super().__init__(timeout=60)
        self.embed = embed
        self.sent = False

    @discord.ui.button(label="Kirim", style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not interaction.user.guild_permissions.manage_guild:
            await interaction.response.send_message("❌ Hanya admin yang boleh mengirim embed.", ephemeral=True)
            return

        if TARGET_CHANNEL_ID:
            channel = bot.get_channel(TARGET_CHANNEL_ID)
            if channel:
                await channel.send(embed=self.embed)
                await interaction.response.edit_message(content="✅ Embed berhasil dikirim ke channel target.", embed=None, view=None)
            else:
                await interaction.response.edit_message(content="❌ Channel target tidak ditemukan.", embed=None, view=None)
        else:
            await interaction.response.edit_message(content="✅ Embed:", embed=self.embed, view=None)

    @discord.ui.button(label="Edit Ulang", style=discord.ButtonStyle.blurple)
    async def edit_embed(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(EmbedModal())

class EmbedModal(discord.ui.Modal, title="Buat Embed Baru"):
    judul = discord.ui.TextInput(label="Judul", placeholder="Masukkan judul embed...", max_length=256)
    deskripsi = discord.ui.TextInput(label="Deskripsi", style=discord.TextStyle.paragraph, placeholder="Isi isi embed di sini...", max_length=4000)
    warna = discord.ui.TextInput(label="Warna Hex (opsional)", required=False, placeholder="#00ffcc")
    gambar = discord.ui.TextInput(label="Gambar URL (opsional)", required=False, placeholder="https://...")
    thumbnail = discord.ui.TextInput(label="Thumbnail URL (opsional)", required=False, placeholder="https://...")

    async def on_submit(self, interaction: discord.Interaction):
        if not interaction.user.guild_permissions.manage_guild:
            await interaction.response.send_message("❌ Hanya admin yang boleh membuat embed.", ephemeral=True)
            return

        color = discord.Color.default()
        if self.warna.value:
            try:
                color = discord.Color(int(self.warna.value.replace("#", "0x"), 16))
            except:
                pass

        embed = discord.Embed(title=self.judul.value, description=self.deskripsi.value, color=color)
        embed.set_footer(text=f"Dibuat oleh {interaction.user.display_name}")

        if self.gambar.value:
            embed.set_image(url=self.gambar.value)
        if self.thumbnail.value:
            embed.set_thumbnail(url=self.thumbnail.value)

        # Preview dan opsi edit ulang
        await interaction.response.send_message(content="📌 Preview embed kamu:", embed=embed, view=ConfirmView(embed), ephemeral=True)

@bot.tree.command(name="buat_embed", description="Buka form untuk membuat embed lengkap")
async def buat_embed(interaction: discord.Interaction):
    await interaction.response.send_modal(EmbedModal())

@bot.event
async def on_ready():
    await bot.tree.sync(guild=discord.Object(id=GUILD_ID) if GUILD_ID else None)
    print(f"✅ Bot embed aktif sebagai {bot.user}")

bot.run(TOKEN)

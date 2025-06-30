import os
import discord
import random
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)


# Fungsi random warna jika warna kosong
def random_color():
    return discord.Color.from_rgb(random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))


# Modal Input untuk Embed Builder
class EmbedModal(discord.ui.Modal, title="📝 Buat Embed"):
    judul = discord.ui.TextInput(label="Judul", required=False, max_length=256)
    deskripsi = discord.ui.TextInput(label="Deskripsi", style=discord.TextStyle.paragraph, required=True, max_length=4000)
    warna = discord.ui.TextInput(label="Warna (hex, contoh: #ffcc00)", required=False)
    thumbnail = discord.ui.TextInput(label="Link Thumbnail (opsional)", required=False)
    gambar = discord.ui.TextInput(label="Link Gambar Utama (opsional)", required=False)

    async def on_submit(self, interaction: discord.Interaction):
        color_input = self.warna.value.lstrip("#") or None
        try:
            color = discord.Color(int(color_input, 16)) if color_input else random_color()
        except:
            color = random_color()

        embed = discord.Embed(
            title=self.judul.value or None,
            description=self.deskripsi.value,
            color=color
        )

        if self.thumbnail.value:
            embed.set_thumbnail(url=self.thumbnail.value)
        if self.gambar.value:
            embed.set_image(url=self.gambar.value)

        embed.set_footer(text=f"Dibuat oleh {interaction.user.display_name}")

        # Ambil list channel text
        channels = [channel for channel in interaction.guild.text_channels if channel.permissions_for(interaction.user).send_messages]

        # Buat dropdown untuk pilih channel tujuan
        options = [discord.SelectOption(label=ch.name, value=str(ch.id)) for ch in channels[:25]]

        select = discord.ui.Select(placeholder="Pilih channel untuk mengirim embed", options=options)
        view = discord.ui.View(timeout=300)

        async def select_callback(select_interaction: discord.Interaction):
            channel_id = int(select.values[0])
            channel = interaction.client.get_channel(channel_id)

            if channel:
                confirm_view = discord.ui.View(timeout=300)

                async def kirim_callback(btn_inter: discord.Interaction):
                    await channel.send(embed=embed)
                    await btn_inter.response.edit_message(content="✅ Embed berhasil dikirim!", embed=None, view=None)

                async def edit_callback(btn_inter: discord.Interaction):
                    await btn_inter.response.send_modal(EmbedModal())

                confirm_view.add_item(discord.ui.Button(label="✅ Kirim", style=discord.ButtonStyle.success))
                confirm_view.add_item(discord.ui.Button(label="🔁 Edit", style=discord.ButtonStyle.secondary))
                confirm_view.children[0].callback = kirim_callback
                confirm_view.children[1].callback = edit_callback

                await select_interaction.response.edit_message(embed=embed, content=None, view=confirm_view)

        select.callback = select_callback
        view.add_item(select)

        await interaction.response.send_message(content="📑 Preview embed kamu di bawah:", embed=embed, view=view, ephemeral=True)


# Command untuk membuka modal
@bot.tree.command(name="buat_embed", description="Buat embed interaktif dengan UI lengkap")
@discord.app_commands.guilds(discord.Object(id=GUILD_ID))
async def buat_embed(interaction: discord.Interaction):
    await interaction.response.send_modal(EmbedModal())


# Command test
@bot.tree.command(name="ping", description="Tes apakah bot aktif")
@discord.app_commands.guilds(discord.Object(id=GUILD_ID))
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("🏓 AxenX aktif!", ephemeral=True)


# Sinkronisasi command saat bot siap
@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
        print(f"✅ Slash command berhasil disinkron: {len(synced)} command")
        print(f"🤖 Bot aktif sebagai {bot.user}")
    except Exception as e:
        print(f"❌ Gagal sync command: {e}")

bot.run(TOKEN)

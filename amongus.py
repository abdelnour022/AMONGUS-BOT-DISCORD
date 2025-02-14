import discord
from discord.ext import commands
from discord.ui import Button, View

# إدخال التوكن الخاص بالبوت مباشرة
bot_token = "MTMwOTUxMDA3MzQ4NzMzMTQwMA.GvSlJ2.T--k-UlhY9n5GFq-a9ooLLZMXVktHopmIe-uOU"
command_prefix = "!"  # بادئة الأوامر
owner_id = "1305949911577006210"  # معرف المالك (اختياري)

# إعداد البوت
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.members = True

bot = commands.Bot(command_prefix=command_prefix, intents=intents)

# متغيرات لتخزين كود الغرفة، حالة اللعبة، والغرفة الصوتية
room_code = ""
game_active = False
voice_channel = None  # تعريف المتغير على مستوى عالمي

# عندما يعمل البوت
@bot.event
async def on_ready():
    print(f"✅ Bot is online as {bot.user}")

# أمر لتعيين كود الغرفة
@bot.command()
async def setcode(ctx, code):
    """تعيين كود الغرفة"""
    global room_code, game_active
    room_code = code
    game_active = True
    await ctx.send(f"✅ تم تعيين كود الغرفة: `{code}`")

# أمر لتحديد الغرفة الصوتية باستخدام ID
@bot.command()
async def setvoice(ctx, channel_id: int):
    """تحديد الغرفة الصوتية باستخدام ID"""
    global voice_channel
    try:
        channel = await ctx.guild.fetch_channel(channel_id)
        if isinstance(channel, discord.VoiceChannel):  # التحقق من أن الغرفة صوتية
            voice_channel = channel
            await ctx.send(f"🎙️ تم تعيين الغرفة الصوتية: `{channel.name}`")
        else:
            await ctx.send("⚠️ الـ ID المحدد لا يعود إلى غرفة صوتية.")
    except discord.NotFound:
        await ctx.send("⚠️ لم يتم العثور على غرفة بهذا الـ ID.")
    except discord.Forbidden:
        await ctx.send("🚫 البوت لا يمتلك أذونات كافية للوصول إلى هذه الغرفة.")
    except Exception as e:
        await ctx.send(f"❌ حدث خطأ: {e}")

# واجهة رسومية (Embed) مع الأزرار
@bot.command()
async def panel(ctx):
    """عرض لوحة التحكم"""
    global voice_channel
    if not voice_channel:
        await ctx.send("⚠️ يجب تحديد الغرفة الصوتية باستخدام الأمر `!setvoice <ID>`.")
        return

    # إنشاء Embed
    embed = discord.Embed(
        title="Among Us Game Info",
        description="لوحة التحكم الخاصة باللعبة",
        color=0xff0000
    )
    embed.add_field(name="Room Code", value=room_code if room_code else "❓ غير معرّف", inline=False)
    embed.add_field(name="📌 Hosted By", value=f"{ctx.author.mention}", inline=True)
    embed.add_field(name="🎙️ Voice Channel", value=voice_channel.mention, inline=True)
    embed.set_footer(text="BOT CREATED BY ABDELNOUR ✨")

    # إنشاء الأزرار
    mute_button = Button(label="Mute All", style=discord.ButtonStyle.danger)
    unmute_button = Button(label="Unmute All", style=discord.ButtonStyle.success)
    end_button = Button(label="End Panel", style=discord.ButtonStyle.primary)

    # وظائف الأزرار
    async def mute_all(interaction):
        if voice_channel:
            for member in voice_channel.members:
                await member.edit(mute=True)
            await interaction.response.send_message("✅ تم كتم جميع الأعضاء في الغرفة الصوتية!", ephemeral=True)
        else:
            await interaction.response.send_message("⚠️ لم يتم تعيين غرفة صوتية بعد.", ephemeral=True)

    async def unmute_all(interaction):
        if voice_channel:
            for member in voice_channel.members:
                await member.edit(mute=False)
            await interaction.response.send_message("✅ تم إلغاء الكتم عن جميع الأعضاء في الغرفة الصوتية!", ephemeral=True)
        else:
            await interaction.response.send_message("⚠️ لم يتم تعيين غرفة صوتية بعد.", ephemeral=True)

    async def end_panel(interaction):
        global room_code, game_active, voice_channel
        room_code = ""
        game_active = False
        voice_channel = None
        await interaction.response.send_message("🛑 تم إنهاء الجولة والجلسة!", ephemeral=True)
        await message.delete()

    # ربط الأزرار بوظائفها
    mute_button.callback = mute_all
    unmute_button.callback = unmute_all
    end_button.callback = end_panel

    # إضافة الأزرار إلى واجهة
    view = View()
    view.add_item(mute_button)
    view.add_item(unmute_button)
    view.add_item(end_button)

    # إرسال الرسالة مع الأزرار
    message = await ctx.send(embed=embed, view=view)

# تشغيل البوت
bot.run(bot_token)


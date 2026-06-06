import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv
from datetime import datetime
import random
import string
import asyncio
import json

# Load .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Load emojis from .env
EMOJI_BAN = os.getenv('EMOJI_BAN', '<:Hammer:1512437228016766976>')
EMOJI_KICK = os.getenv('EMOJI_KICK', '<:Trash:1512440687478702190>')
EMOJI_MUTE = os.getenv('EMOJI_MUTE', '<:Lock:1512437511169900715>')
EMOJI_UNMUTE = os.getenv('EMOJI_UNMUTE', '<:Plus:1512437485538513117>')
EMOJI_INFO = os.getenv('EMOJI_INFO', '<:Info:1512437258190585996>')
EMOJI_USER = os.getenv('EMOJI_USER', '<:User:1512437457591730326>')

# Logo URL for embeds
LOGO_URL = 'https://cdn.discordapp.com/attachments/1450878351303507998/1512463690463445074/IMG_20260605_163738.png?ex=6a242f14&is=6a22dd94&hm=5247b858fbc6226d73071ffc5ba427d4a6205b5718239d1fc4703be7efd763c4'

# Bot configuration
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='/', intents=intents)

# Bot ready event
@bot.event
async def on_ready():
    # Load settings from file
    load_settings()
    
    try:
        synced = await bot.tree.sync()
        print(f'{len(synced)} commands synchronized.')
    except Exception as e:
        print(f'Command sync error: {e}')
    
    # Set bot status
    activity = discord.Activity(type=discord.ActivityType.watching, name="discord.gg/QtbarynSq")
    await bot.change_presence(activity=activity, status=discord.Status.online)
    
    print(f'{bot.user} logged in!')
    print(f'Bot ID: {bot.user.id}')
    print(f'✅ Custom emojis loaded!')
    print(f'Emojis: Ban={EMOJI_BAN}, Kick={EMOJI_KICK}, Mute={EMOJI_MUTE}, Unmute={EMOJI_UNMUTE}')

# About command
@bot.tree.command(name="about", description="Information about the bot")
async def about(interaction: discord.Interaction):
    """About the bot"""
    embed = discord.Embed(
        title="About Skibidi Union Bot",
        description="Welcome to Skibidi Union Bot - Your Ultimate Server Management Assistant",
        color=discord.Color(0x000000)
    )
    
    embed.add_field(
        name="What is Skibidi Union Bot?",
        value="Skibidi Union Bot is a powerful Discord bot designed to help manage your server efficiently. With advanced moderation tools, user information commands, and more, Skibidi Union Bot makes server management easier than ever.",
        inline=False
    )
    
    embed.add_field(
        name="Key Features",
        value="• Moderation Tools (Ban, Kick, Mute, Unmute)\n• User Information & Profiles\n• Server Statistics\n• Case Management System\n• Easy-to-use Slash Commands",
        inline=False
    )
    
    embed.add_field(
        name="Moderation Commands",
        value="/ban - Ban a user from the server\n/kick - Kick a user from the server\n/mute - Mute a user\n/unmute - Unmute a user",
        inline=False
    )
    
    embed.add_field(
        name="Utility Commands",
        value="/ping - Check bot latency\n/hello - Get a greeting\n/userinfo - View user information\n/help - View all commands",
        inline=False
    )
    
    embed.add_field(
        name="Need Help?",
        value="Use `/help` to view all available commands organized by category.",
        inline=False
    )
    embed.add_field(name="\u200b", value="\u200b", inline=False)
    
    embed.set_footer(text="Made by Skibidi Union Bot • Version 1.0")
    embed.set_image(url=LOGO_URL)
    
    await interaction.response.send_message(embed=embed)

# Help command with dropdown menu
class CommandSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Utility Commands", description="Bot utility commands", value="utility"),
            discord.SelectOption(label="Moderation Commands", description="Server moderation tools", value="moderation"),
            discord.SelectOption(label="Info Commands", description="Information commands", value="info"),
        ]
        super().__init__(placeholder="Choose a category...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "utility":
            embed = discord.Embed(
                title="Utility Commands",
                description="Bot utility and helper commands",
                color=discord.Color(0x000000)
            )
            embed.add_field(
                name="/ping",
                value="Check the bot's latency and connection speed",
                inline=False
            )
            embed.add_field(
                name="/hello",
                value="Get a greeting from the bot",
                inline=False
            )
            embed.add_field(
                name="/userinfo [@user]",
                value="View detailed information about a user",
                inline=False
            )
            embed.add_field(name="\u200b", value="\u200b", inline=False)
            embed.set_image(url=LOGO_URL)
        elif self.values[0] == "moderation":
            embed = discord.Embed(
                title="Moderation Commands",
                description="Server moderation and management tools",
                color=discord.Color(0x000000)
            )
            embed.add_field(
                name="/ban [@user] [reason]",
                value="Ban a user from the server",
                inline=False
            )
            embed.add_field(
                name="/kick [@user] [reason]",
                value="Kick a user from the server",
                inline=False
            )
            embed.add_field(
                name="/mute [@user] [reason]",
                value="Mute a user (prevent them from speaking)",
                inline=False
            )
            embed.add_field(
                name="/unmute [@user]",
                value="Remove mute from a user",
                inline=False
            )
            embed.add_field(name="\u200b", value="\u200b", inline=False)
            embed.set_image(url=LOGO_URL)
        else:  # info
            embed = discord.Embed(
                title="Info Commands",
                description="Learn about the bot",
                color=discord.Color(0x000000)
            )
            embed.add_field(
                name="/about",
                value="Learn more about Skibidi Union Bot and its features",
                inline=False
            )
            embed.add_field(
                name="/help",
                value="View this command list with categories",
                inline=False
            )
            embed.add_field(name="\u200b", value="\u200b", inline=False)
            embed.set_image(url=LOGO_URL)

        await interaction.response.edit_message(embed=embed)

class CommandSelectView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(CommandSelect())

@bot.tree.command(name="help", description="View all commands")
async def help_command(interaction: discord.Interaction):
    """View all commands"""
    embed = discord.Embed(
        title="Skibidi Union Bot Commands",
        description="Select a category to view commands",
        color=discord.Color(0x000000)
    )
    embed.add_field(name="\u200b", value="\u200b", inline=False)
    embed.set_image(url=LOGO_URL)
    
    view = CommandSelectView()
    await interaction.response.send_message(embed=embed, view=view)

# Ping command
@bot.tree.command(name="ping", description="Check bot latency")
async def ping(interaction: discord.Interaction):
    """Bot latency"""
    latency = round(bot.latency * 1000)
    embed = discord.Embed(
        title="Bot Latency",
        description="Connection speed to Discord servers",
        color=discord.Color(0x000000)
    )
    embed.add_field(
        name="Latency (Ping)",
        value=f"```\n{latency}ms\n```",
        inline=False
    )
    if latency < 100:
        status = "Excellent"
    elif latency < 200:
        status = "Good"
    else:
        status = "Slow"
    embed.add_field(name="Status", value=status, inline=False)
    embed.add_field(name="\u200b", value="\u200b", inline=False)
    embed.set_image(url=LOGO_URL)
    await interaction.response.send_message(embed=embed)

# Hello command
@bot.tree.command(name="hello", description="Get a greeting")
async def hello(interaction: discord.Interaction):
    """Get a greeting"""
    embed = discord.Embed(
        title="Welcome!",
        description="Welcome to Skibidi Union Bot! Here you can learn about what the bot can do.",
        color=discord.Color(0x000000)
    )
    embed.add_field(
        name="User",
        value=f"```\n{interaction.user.name}\n```",
        inline=False
    )
    embed.add_field(
        name="Available Commands",
        value="```\n/ping - Check bot speed\n/userinfo - View user info\n/help - View all commands\n/about - About the bot\n```",
        inline=False
    )
    embed.add_field(name="\u200b", value="\u200b", inline=False)
    embed.set_image(url=LOGO_URL)
    await interaction.response.send_message(embed=embed)

# User info command
@bot.tree.command(name="userinfo", description="View user information")
@app_commands.describe(member="User to view (leave blank for yourself)")
async def userinfo(interaction: discord.Interaction, member: discord.Member = None):
    """User information"""
    if member is None:
        member = interaction.user
    
    embed = discord.Embed(
        title=f"User Information - {member.name}",
        description="Complete user details",
        color=discord.Color(0x000000)
    )
    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
    
    embed.add_field(
        name="User ID",
        value=f"```\n{member.id}\n```",
        inline=False
    )
    embed.add_field(
        name="Account Created",
        value=f"```\n{member.created_at.strftime('%d/%m/%Y - %H:%M:%S')}\n```",
        inline=False
    )
    embed.add_field(
        name="Joined Server",
        value=f"```\n{member.joined_at.strftime('%d/%m/%Y - %H:%M:%S')}\n```",
        inline=False
    )
    embed.add_field(
        name="Roles",
        value=f"```\n{len(member.roles)} roles\n```" if member.roles else "No roles",
        inline=False
    )
    embed.add_field(name="\u200b", value="\u200b", inline=False)
    embed.set_image(url=LOGO_URL)
    
    await interaction.response.send_message(embed=embed)

# BAN COMMAND (Moderation)
@bot.tree.command(name="ban", description="Ban a user from the server")
@app_commands.describe(member="User to ban", reason="Ban reason")
@app_commands.checks.has_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
    """Ban a user"""
    await member.ban(reason=reason)
    
    case_id = "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
    
    now = datetime.now()
    months = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}
    tarih = f"{now.day} {months[now.month]} {now.year}"
    saat = now.strftime("%H:%M")
    
    embed = discord.Embed(
        title=f"{EMOJI_BAN} Member banned",
        description=f"**{interaction.guild.name}**",
        color=discord.Color(0x000000)
    )
    
    embed.add_field(name="CaseID", value=f"#{case_id}", inline=True)
    embed.add_field(name="Who?", value=f"@{member.name}", inline=True)
    embed.add_field(name="Moderator", value=f"@{interaction.user.name}", inline=True)
    embed.add_field(name="\u200b", value="\u200b", inline=False)
    embed.add_field(name="When?", value=f"{tarih} {saat}", inline=False)
    embed.add_field(name="Reason", value=f"```\n{reason}\n```", inline=False)
    embed.add_field(name="\u200b", value="\u200b", inline=False)
    embed.set_image(url=LOGO_URL)
    
    await interaction.response.send_message(embed=embed)

# KICK COMMAND (Moderation)
@bot.tree.command(name="kick", description="Kick a user from the server")
@app_commands.describe(member="User to kick", reason="Kick reason")
@app_commands.checks.has_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
    """Kick a user"""
    await member.kick(reason=reason)
    
    case_id = "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
    
    now = datetime.now()
    months = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}
    tarih = f"{now.day} {months[now.month]} {now.year}"
    saat = now.strftime("%H:%M")
    
    embed = discord.Embed(
        title=f"{EMOJI_KICK} Member kicked",
        description=f"**{interaction.guild.name}**",
        color=discord.Color(0x000000)
    )
    
    embed.add_field(name="CaseID", value=f"#{case_id}", inline=True)
    embed.add_field(name="Who?", value=f"@{member.name}", inline=True)
    embed.add_field(name="Moderator", value=f"@{interaction.user.name}", inline=True)
    embed.add_field(name="\u200b", value="\u200b", inline=False)
    embed.add_field(name="When?", value=f"{tarih} {saat}", inline=False)
    embed.add_field(name="Reason", value=f"```\n{reason}\n```", inline=False)
    embed.add_field(name="\u200b", value="\u200b", inline=False)
    embed.set_image(url=LOGO_URL)
    
    await interaction.response.send_message(embed=embed)

# MUTE COMMAND (Moderation)
@bot.tree.command(name="mute", description="Mute a user")
@app_commands.describe(member="User to mute", reason="Mute reason")
@app_commands.checks.has_permissions(manage_roles=True)
async def mute(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
    """Mute a user"""
    muted_role = discord.utils.get(interaction.guild.roles, name="Muted")
    
    if muted_role is None:
        muted_role = await interaction.guild.create_role(name="Muted")
    
    await member.add_roles(muted_role)
    
    case_id = "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
    
    now = datetime.now()
    months = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}
    tarih = f"{now.day} {months[now.month]} {now.year}"
    saat = now.strftime("%H:%M")
    
    embed = discord.Embed(
        title=f"{EMOJI_MUTE} Member muted",
        description=f"**{interaction.guild.name}**",
        color=discord.Color(0x000000)
    )
    
    embed.add_field(name="CaseID", value=f"#{case_id}", inline=True)
    embed.add_field(name="Who?", value=f"@{member.name}", inline=True)
    embed.add_field(name="Moderator", value=f"@{interaction.user.name}", inline=True)
    embed.add_field(name="\u200b", value="\u200b", inline=False)
    embed.add_field(name="When?", value=f"{tarih} {saat}", inline=False)
    embed.add_field(name="Reason", value=f"```\n{reason}\n```", inline=False)
    embed.add_field(name="\u200b", value="\u200b", inline=False)
    embed.set_image(url=LOGO_URL)
    
    await interaction.response.send_message(embed=embed)

# UNMUTE COMMAND (Moderation)
@bot.tree.command(name="unmute", description="Unmute a user")
@app_commands.describe(member="User to unmute")
@app_commands.checks.has_permissions(manage_roles=True)
async def unmute(interaction: discord.Interaction, member: discord.Member):
    """Unmute a user"""
    muted_role = discord.utils.get(interaction.guild.roles, name="Muted")
    
    if muted_role is None:
        error_embed = discord.Embed(
            title="Error",
            description="Muted role not found!",
            color=discord.Color(0x000000)
        )
        await interaction.response.send_message(embed=error_embed)
        return
    
    await member.remove_roles(muted_role)
    
    case_id = "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
    
    now = datetime.now()
    months = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}
    tarih = f"{now.day} {months[now.month]} {now.year}"
    saat = now.strftime("%H:%M")
    
    embed = discord.Embed(
        title=f"{EMOJI_UNMUTE} Member unmuted",
        description=f"**{interaction.guild.name}**",
        color=discord.Color(0x000000)
    )
    
    embed.add_field(name="CaseID", value=f"#{case_id}", inline=True)
    embed.add_field(name="Who?", value=f"@{member.name}", inline=True)
    embed.add_field(name="Moderator", value=f"@{interaction.user.name}", inline=True)
    embed.add_field(name="\u200b", value="\u200b", inline=False)
    embed.add_field(name="When?", value=f"{tarih} {saat}", inline=False)
    embed.add_field(name="\u200b", value="\u200b", inline=False)
    embed.set_image(url=LOGO_URL)
    
    await interaction.response.send_message(embed=embed)

# Error handler
@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.MissingPermissions):
        embed = discord.Embed(
            title="Error",
            description="You don't have permission to use this command!",
            color=discord.Color(0x000000)
        )
        embed.set_image(url=LOGO_URL)
        await interaction.response.send_message(embed=embed, ephemeral=True)
    elif isinstance(error, app_commands.MissingRequiredArgument):
        embed = discord.Embed(
            title="Error",
            description="Missing arguments! Please use the command correctly.",
            color=discord.Color(0x000000)
        )
        embed.set_image(url=LOGO_URL)
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        embed = discord.Embed(
            title="Unknown Error",
            description=f"```\n{str(error)[:200]}\n```",
            color=discord.Color(0x000000)
        )
        embed.set_image(url=LOGO_URL)
        await interaction.response.send_message(embed=embed, ephemeral=True)

# ========== TICKET SYSTEM ==========

# Ticket Emojis
EMOJI_BELL = '<:Bell:1512440875094114374>'
EMOJI_CLOCK = '<:Clock:1512440645359501422>'
EMOJI_DISLIKE = '<:Dislike:1512440830970040350>'
EMOJI_GEAR = '<:Gear:1512440611079196712>'
EMOJI_EXCLAMATION = '<:Exclemation:1512440592750350366>'
EMOJI_GLOBE = '<:Globe:1512440626967478272>'
EMOJI_HAMMER = '<:Hammer:1512437228016766976>'
EMOJI_INFO_TICKET = '<:Info:1512437258190585996>'
EMOJI_LOCK = '<:Lock:1512437511169900715>'
EMOJI_MINUS = '<:Minus:1512440803555938344>'
EMOJI_PAPERPLANE = '<:Paperplane:1512437557626146877>'
EMOJI_PLUS = '<:Plus:1512437485538513117>'
EMOJI_SUPPORTER = '<:Supporter:1512437155581001880>'
EMOJI_SUPPORTER_ONLINE = '<:SupporterOnline:1512440722496950362>'
EMOJI_SUPPORTER_TOTAL = '<:SupporterTotal:1512440747276767353>'
EMOJI_THUMBSTICK = '<:Thumbstick:1512437592849645628>'
EMOJI_TICKET = '<:Ticket:1512437354328232037>'
EMOJI_TIME = '<:Time:1512437616333819964>'
EMOJI_TRASH_TICKET = '<:Trash:1512440687478702190>'
EMOJI_USER_TICKETS = '<:User:1512437457591730326>'
EMOJI_USER_MINUS = '<:UserMinus:1512437426746822767>'
EMOJI_USER_HISTORY = '<:User_History:1512440667786448967>'
EMOJI_TRANSCRIPT = '<:transkript:1512437394564190238>'

# Ticket Images
TICKET_WELCOME_BANNER = 'https://images-ext-1.discordapp.net/external/7HmHXSrYxi9kmV4qM7ZQbVh_x-iJyvhpRgJBHUyH2sQ/https/s3.galaxybot.app/media/embeds/banner/ticket/ticketWelcomeDefaultBanner.png?format=webp&quality=lossless&width=1860&height=443'
TICKET_PANEL_BANNER = 'https://s3.galaxybot.app/media/embeds/banner/ticket/ticketDefaultBanner.png'

# Ticket Categories
TICKET_CATEGORIES = {
    'support': {'name': 'Support', 'emoji': EMOJI_SUPPORTER, 'color': 0x3498db},
    'billing': {'name': 'Billing', 'emoji': EMOJI_GEAR, 'color': 0xe74c3c},
    'general': {'name': 'General', 'emoji': EMOJI_GLOBE, 'color': 0x2ecc71},
    'bug': {'name': 'Bug Report', 'emoji': EMOJI_DISLIKE, 'color': 0xf39c12},
}

# Ticket Category Storage (guild_id: category_id)
TICKET_CATEGORY_SETUP = {}

# Ticket Log Channel Storage (guild_id: channel_id)
TICKET_LOG_CHANNEL = {}

# Ticket Info Storage (channel_id: {user_id, ticket_number, category, members})
TICKET_INFO = {}

# Ticket Claimed By (channel_id: moderator_id)
TICKET_CLAIMED_BY = {}

# Audit Log Channel Storage (guild_id: channel_id)
AUDIT_LOG_CHANNEL = {}

# Welcome Channel Storage (guild_id: channel_id)
WELCOME_CHANNEL = {}

# ========== SETTINGS STORAGE ==========
SETTINGS_FILE = 'bot_settings.json'

def load_settings():
    """Load settings from JSON file"""
    global TICKET_CATEGORY_SETUP, TICKET_LOG_CHANNEL, AUDIT_LOG_CHANNEL, WELCOME_CHANNEL
    
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, 'r') as f:
                data = json.load(f)
                TICKET_CATEGORY_SETUP = {int(k): v for k, v in data.get('TICKET_CATEGORY_SETUP', {}).items()}
                TICKET_LOG_CHANNEL = {int(k): v for k, v in data.get('TICKET_LOG_CHANNEL', {}).items()}
                AUDIT_LOG_CHANNEL = {int(k): v for k, v in data.get('AUDIT_LOG_CHANNEL', {}).items()}
                WELCOME_CHANNEL = {int(k): v for k, v in data.get('WELCOME_CHANNEL', {}).items()}
                print(f"✅ Settings loaded from {SETTINGS_FILE}")
        except Exception as e:
            print(f"⚠️ Error loading settings: {e}")
    else:
        print(f"📝 No settings file found. Creating new one.")

def save_settings():
    """Save settings to JSON file"""
    try:
        data = {
            'TICKET_CATEGORY_SETUP': TICKET_CATEGORY_SETUP,
            'TICKET_LOG_CHANNEL': TICKET_LOG_CHANNEL,
            'AUDIT_LOG_CHANNEL': AUDIT_LOG_CHANNEL,
            'WELCOME_CHANNEL': WELCOME_CHANNEL,
        }
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"⚠️ Error saving settings: {e}")

# Reason Modal
class TicketReasonModal(discord.ui.Modal, title="Ticket Reason"):
    reason = discord.ui.TextInput(label="What is the reason for your ticket?", style=discord.TextStyle.long, placeholder="Enter your reason here...", min_length=10)
    
    def __init__(self, category, user_interaction):
        super().__init__()
        self.category = category
        self.user_interaction = user_interaction

# Add Member Modal
class AddMemberModal(discord.ui.Modal, title="Add Member to Ticket"):
    member = discord.ui.TextInput(label="Member ID or mention", style=discord.TextStyle.short, placeholder="@user or user ID")
    reason = discord.ui.TextInput(label="Reason for adding", style=discord.TextStyle.short, placeholder="Why are they added?", required=False)
    
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        
        channel = interaction.channel
        if channel.id not in TICKET_INFO:
            await interaction.followup.send("❌ This is not a ticket channel!", ephemeral=True)
            return
        
        try:
            # Parse member
            member_str = self.member.value.strip()
            if member_str.startswith('<@'):
                member_id = int(member_str.replace('<@', '').replace('>', '').replace('!', ''))
            else:
                member_id = int(member_str)
            
            member = await interaction.guild.fetch_member(member_id)
            
            # Add member to ticket
            if member.id not in TICKET_INFO[channel.id].get('members', []):
                if 'members' not in TICKET_INFO[channel.id]:
                    TICKET_INFO[channel.id]['members'] = []
                TICKET_INFO[channel.id]['members'].append(member.id)
            
            # Give permissions
            await channel.set_permissions(member, read_messages=True, send_messages=True)
            
            embed = discord.Embed(
                title=f"{EMOJI_PLUS} Member Added",
                description=f"{member.mention} has been added to the ticket",
                color=discord.Color(0x2ecc71)
            )
            if self.reason.value:
                embed.add_field(name="Reason", value=self.reason.value, inline=False)
            embed.set_image(url=LOGO_URL)
            
            await channel.send(embed=embed)
            await interaction.followup.send("✅ Member added!", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"❌ Error: {str(e)}", ephemeral=True)

# Remove Member Modal
class RemoveMemberModal(discord.ui.Modal, title="Remove Member from Ticket"):
    member = discord.ui.TextInput(label="Member ID or mention", style=discord.TextStyle.short, placeholder="@user or user ID")
    reason = discord.ui.TextInput(label="Reason for removal", style=discord.TextStyle.short, placeholder="Why are they removed?", required=False)
    
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        
        channel = interaction.channel
        if channel.id not in TICKET_INFO:
            await interaction.followup.send("❌ This is not a ticket channel!", ephemeral=True)
            return
        
        try:
            # Parse member
            member_str = self.member.value.strip()
            if member_str.startswith('<@'):
                member_id = int(member_str.replace('<@', '').replace('>', '').replace('!', ''))
            else:
                member_id = int(member_str)
            
            member = await interaction.guild.fetch_member(member_id)
            
            # Remove member from ticket
            if 'members' in TICKET_INFO[channel.id] and member.id in TICKET_INFO[channel.id]['members']:
                TICKET_INFO[channel.id]['members'].remove(member.id)
            
            # Remove permissions
            await channel.set_permissions(member, read_messages=False, send_messages=False)
            
            embed = discord.Embed(
                title=f"{EMOJI_USER_MINUS} Member Removed",
                description=f"{member.mention} has been removed from the ticket",
                color=discord.Color(0xe74c3c)
            )
            if self.reason.value:
                embed.add_field(name="Reason", value=self.reason.value, inline=False)
            embed.set_image(url=LOGO_URL)
            
            await channel.send(embed=embed)
            await interaction.followup.send("✅ Member removed!", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"❌ Error: {str(e)}", ephemeral=True)
    
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        
        reason = str(self.reason.value)
        category = self.category
        user = self.user_interaction.user
        guild = interaction.guild
        
        # Get ticket category from setup
        if guild.id not in TICKET_CATEGORY_SETUP:
            error_embed = discord.Embed(
                title="Error",
                description="Ticket category has not been setup yet! Ask an admin to run `/ticket-setup`",
                color=discord.Color(0xff0000)
            )
            await interaction.followup.send(embed=error_embed, ephemeral=True)
            return
        
        parent_category_id = TICKET_CATEGORY_SETUP[guild.id]
        parent_category = guild.get_channel(int(parent_category_id))
        
        # Create ticket channel
        ticket_number = random.randint(1000, 9999)
        channel_name = f"ticket-{ticket_number}"
        
        try:
            # Get admin role for permissions (fallback to first role with manage_messages)
            admin_role = None
            for role in guild.roles:
                if role.permissions.administrator or role.permissions.manage_messages:
                    admin_role = role
                    break
            
            # Create channel with private permissions
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            }
            
            # Add admin/mod role permissions if found
            if admin_role:
                overwrites[admin_role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
            
            # Create channel in the selected category
            ticket_channel = await guild.create_text_channel(
                name=channel_name,
                topic=f"Ticket #{ticket_number} - {TICKET_CATEGORIES[category]['name']} - {user.name}",
                category=parent_category,
                overwrites=overwrites
            )
            
            # Send welcome embed
            welcome_embed = discord.Embed(
                title=f"{EMOJI_TICKET} Welcome to your ticket.",
                description="Welcome, please first write down your question or complaint.",
                color=TICKET_CATEGORIES[category]['color']
            )
            welcome_embed.add_field(name="\u200b", value="\u200b", inline=False)
            welcome_embed.add_field(name="• Write it down immediately and wait for our staff.", value="\u200b", inline=False)
            welcome_embed.add_field(name="• Thank you for your understanding.", value="\u200b", inline=False)
            welcome_embed.add_field(name="\u200b", value="\u200b", inline=False)
            welcome_embed.set_image(url=TICKET_WELCOME_BANNER)
            
            await ticket_channel.send(embed=welcome_embed)
            
            # Send reason embed
            reason_embed = discord.Embed(
                title="Ticket Information",
                description=f"Reason: {reason}",
                color=TICKET_CATEGORIES[category]['color']
            )
            reason_embed.add_field(name=f"{EMOJI_TICKET} CaseID", value=f"#{ticket_number}", inline=True)
            reason_embed.add_field(name=f"{EMOJI_CLOCK} Category", value=TICKET_CATEGORIES[category]['name'], inline=True)
            reason_embed.add_field(name=f"{EMOJI_USER} Creator", value=f"@{user.name}", inline=True)
            reason_embed.add_field(name="\u200b", value="\u200b", inline=False)
            reason_embed.set_image(url=TICKET_PANEL_BANNER)
            
            await ticket_channel.send(embed=reason_embed)
            
            # Send action buttons
            view = TicketActionsView(ticket_channel.id)
            await ticket_channel.send("**Ticket Actions:**", view=view)
            
            # Store ticket info
            TICKET_INFO[ticket_channel.id] = {
                'user_id': user.id,
                'ticket_number': ticket_number,
                'category': category,
                'created_at': datetime.now(),
                'members': []
            }
            
            # Send log message if log channel is set
            if guild.id in TICKET_LOG_CHANNEL:
                log_channel = guild.get_channel(TICKET_LOG_CHANNEL[guild.id])
                if log_channel:
                    log_embed = discord.Embed(
                        title=f"{EMOJI_TICKET} New ticket created",
                        description=f"**{guild.name}**",
                        color=TICKET_CATEGORIES[category]['color']
                    )
                    log_embed.add_field(name=f"{EMOJI_TICKET} CaseID", value=f"#{ticket_number}", inline=True)
                    log_embed.add_field(name=f"{EMOJI_CLOCK} Category", value=TICKET_CATEGORIES[category]['name'], inline=True)
                    log_embed.add_field(name=f"{EMOJI_USER} Created by", value=f"@{user.name}", inline=True)
                    log_embed.add_field(name="\u200b", value="\u200b", inline=False)
                    log_embed.add_field(name=f"{EMOJI_PAPERPLANE} Ticket channel", value=ticket_channel.mention, inline=False)
                    log_embed.add_field(name=f"{EMOJI_CLOCK} When?", value=datetime.now().strftime('%d/%m/%Y - %H:%M:%S'), inline=False)
                    log_embed.set_image(url=LOGO_URL)
                    await log_channel.send(embed=log_embed)
            
            # Send response to user
            response_embed = discord.Embed(
                title=f"{EMOJI_TICKET} Ticket Created",
                description=f"Your ticket has been created! {ticket_channel.mention}",
                color=TICKET_CATEGORIES[category]['color']
            )
            response_embed.set_image(url=LOGO_URL)
            
            await interaction.followup.send(embed=response_embed, ephemeral=True)
        except Exception as e:
            error_embed = discord.Embed(
                title="Error",
                description=f"Failed to create ticket: {str(e)}",
                color=discord.Color(0xff0000)
            )
            await interaction.followup.send(embed=error_embed, ephemeral=True)

# Ticket Category Select
class TicketCategorySelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label=cat_data['name'], emoji=cat_data['emoji'], value=cat_key, description=f"Open a {cat_data['name']} ticket")
            for cat_key, cat_data in TICKET_CATEGORIES.items()
        ]
        super().__init__(placeholder="Select a category...", min_values=1, max_values=1, options=options)
    
    async def callback(self, interaction: discord.Interaction):
        category = self.values[0]
        modal = TicketReasonModal(category, interaction)
        await interaction.response.send_modal(modal)

class TicketCategoryView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(TicketCategorySelect())

# Ticket Actions View
class TicketActionsView(discord.ui.View):
    def __init__(self, channel_id):
        super().__init__(timeout=None)
        self.channel_id = channel_id
    
    @discord.ui.button(label="Claim", style=discord.ButtonStyle.green, emoji="✅")
    async def claim_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        channel = interaction.guild.get_channel(self.channel_id)
        if not channel:
            await interaction.response.send_message("❌ Ticket channel not found!", ephemeral=True)
            return
        
        if self.channel_id in TICKET_CLAIMED_BY:
            claimer = interaction.guild.get_member(TICKET_CLAIMED_BY[self.channel_id])
            await interaction.response.send_message(f"❌ This ticket is already claimed by {claimer.mention}", ephemeral=True)
            return
        
        TICKET_CLAIMED_BY[self.channel_id] = interaction.user.id
        
        embed = discord.Embed(
            title=f"{EMOJI_USER_HISTORY} Ticket Claimed",
            description=f"{interaction.user.mention} has claimed this ticket",
            color=discord.Color(0x3498db)
        )
        embed.set_image(url=LOGO_URL)
        await channel.send(embed=embed)
        
        await interaction.response.send_message(f"✅ You claimed the ticket!", ephemeral=True)
    
    @discord.ui.button(label="Add Member", style=discord.ButtonStyle.blurple, emoji=EMOJI_PLUS)
    async def add_member_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = AddMemberModal()
        await interaction.response.send_modal(modal)
    
    @discord.ui.button(label="Remove Member", style=discord.ButtonStyle.red, emoji=EMOJI_USER_MINUS)
    async def remove_member_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = RemoveMemberModal()
        await interaction.response.send_modal(modal)

@bot.tree.command(name="ticket-setup", description="Setup ticket category (Admin only)")
@app_commands.checks.has_permissions(administrator=True)
async def ticket_setup(interaction: discord.Interaction, category: discord.CategoryChannel):
    """Setup where tickets will be created"""
    TICKET_CATEGORY_SETUP[interaction.guild.id] = category.id
    save_settings()
    
    embed = discord.Embed(
        title=f"{EMOJI_GEAR} Ticket Setup",
        description=f"Ticket category has been set to {category.mention}",
        color=discord.Color(0x2ecc71)
    )
    embed.add_field(name="\u200b", value="\u200b", inline=False)
    embed.set_image(url=LOGO_URL)
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="ticket", description="Create a support ticket")
async def ticket(interaction: discord.Interaction):
    """Create a ticket"""
    embed = discord.Embed(
        title=f"{EMOJI_TICKET} Create a Ticket",
        description="Select a category to create a support ticket",
        color=discord.Color(0x000000)
    )
    embed.add_field(name="\u200b", value="\u200b", inline=False)
    embed.set_image(url=TICKET_WELCOME_BANNER)
    
    view = TicketCategoryView()
    await interaction.response.send_message(embed=embed, view=view)

@bot.tree.command(name="logs", description="Set audit logs channel (Admin only)")
@app_commands.checks.has_permissions(administrator=True)
async def logs(interaction: discord.Interaction, channel: discord.TextChannel):
    """Setup audit logs channel"""
    AUDIT_LOG_CHANNEL[interaction.guild.id] = channel.id
    save_settings()
    
    embed = discord.Embed(
        title=f"{EMOJI_GEAR} Audit Logs Setup",
        description=f"Audit logs channel has been set to {channel.mention}",
        color=discord.Color(0x2ecc71)
    )
    embed.add_field(name="\u200b", value="\u200b", inline=False)
    embed.add_field(name="Events tracked:", value=f"{EMOJI_HAMMER} Bans • {EMOJI_USER_MINUS} Kicks • {EMOJI_TRASH_TICKET} Message Delete • {EMOJI_INFO_TICKET} Message Edit • {EMOJI_GEAR} Server Updates • {EMOJI_PLUS} Role Changes", inline=False)
    embed.set_image(url=LOGO_URL)
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="welcome", description="Set welcome channel (Admin only)")
@app_commands.checks.has_permissions(administrator=True)
async def welcome(interaction: discord.Interaction, channel: discord.TextChannel):
    """Setup welcome channel"""
    WELCOME_CHANNEL[interaction.guild.id] = channel.id
    save_settings()
    
    embed = discord.Embed(
        title=f"{EMOJI_BELL} Welcome Channel Setup",
        description=f"Welcome channel has been set to {channel.mention}",
        color=discord.Color(0x2ecc71)
    )
    embed.add_field(name="\u200b", value="\u200b", inline=False)
    embed.add_field(name=f"{EMOJI_INFO_TICKET} Info", value="New members will receive a welcome message in this channel!", inline=False)
    embed.set_image(url=LOGO_URL)
    
    await interaction.response.send_message(embed=embed)

# ========== AUDIT LOG EVENTS ==========

@bot.event
async def on_member_ban(guild: discord.Guild, user: discord.User):
    """Log when a member is banned"""
    if guild.id not in AUDIT_LOG_CHANNEL:
        return
    
    log_channel = guild.get_channel(AUDIT_LOG_CHANNEL[guild.id])
    if not log_channel:
        return
    
    embed = discord.Embed(
        title=f"{EMOJI_HAMMER} Member Banned",
        description=f"**{guild.name}**",
        color=discord.Color(0xe74c3c)
    )
    embed.add_field(name=f"{EMOJI_USER_TICKETS} User", value=f"@{user.name}", inline=True)
    embed.add_field(name=f"{EMOJI_CLOCK} When?", value=datetime.now().strftime('%d/%m/%Y - %H:%M:%S'), inline=True)
    embed.add_field(name="\u200b", value="\u200b", inline=False)
    embed.set_image(url=LOGO_URL)
    
    await log_channel.send(embed=embed)

@bot.event
async def on_member_remove(member: discord.Member):
    """Log when a member leaves or is kicked"""
    guild = member.guild
    
    if guild.id not in AUDIT_LOG_CHANNEL:
        return
    
    log_channel = guild.get_channel(AUDIT_LOG_CHANNEL[guild.id])
    if not log_channel:
        return
    
    # Check if they were kicked
    try:
        async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.kick):
            if entry.target.id == member.id:
                embed = discord.Embed(
                    title=f"{EMOJI_USER_MINUS} Member Kicked",
                    description=f"**{guild.name}**",
                    color=discord.Color(0xf39c12)
                )
                embed.add_field(name=f"{EMOJI_USER_TICKETS} User", value=f"@{member.name}", inline=True)
                embed.add_field(name=f"{EMOJI_USER_HISTORY} Kicked by", value=f"@{entry.user.name}", inline=True)
                embed.add_field(name="\u200b", value="\u200b", inline=False)
                embed.add_field(name=f"{EMOJI_INFO_TICKET} Reason", value=entry.reason or "No reason provided", inline=False)
                embed.add_field(name=f"{EMOJI_CLOCK} When?", value=datetime.now().strftime('%d/%m/%Y - %H:%M:%S'), inline=False)
                embed.set_image(url=LOGO_URL)
                
                await log_channel.send(embed=embed)
                return
    except:
        pass

@bot.event
async def on_message_delete(message: discord.Message):
    """Log when a message is deleted"""
    if message.author.bot:
        return
    
    guild = message.guild
    if not guild or guild.id not in AUDIT_LOG_CHANNEL:
        return
    
    log_channel = guild.get_channel(AUDIT_LOG_CHANNEL[guild.id])
    if not log_channel:
        return
    
    embed = discord.Embed(
        title=f"{EMOJI_TRASH_TICKET} Message Deleted",
        description=f"**{guild.name}** • {message.channel.mention}",
        color=discord.Color(0xe74c3c)
    )
    embed.add_field(name=f"{EMOJI_USER_TICKETS} Author", value=f"@{message.author.name}", inline=True)
    embed.add_field(name=f"{EMOJI_CLOCK} When?", value=datetime.now().strftime('%d/%m/%Y - %H:%M:%S'), inline=True)
    embed.add_field(name="\u200b", value="\u200b", inline=False)
    embed.add_field(name=f"{EMOJI_INFO_TICKET} Content", value=message.content[:1024] or "*(No text content)*", inline=False)
    embed.set_image(url=LOGO_URL)
    
    await log_channel.send(embed=embed)

@bot.event
async def on_message_edit(before: discord.Message, after: discord.Message):
    """Log when a message is edited"""
    if after.author.bot or before.content == after.content:
        return
    
    guild = after.guild
    if not guild or guild.id not in AUDIT_LOG_CHANNEL:
        return
    
    log_channel = guild.get_channel(AUDIT_LOG_CHANNEL[guild.id])
    if not log_channel:
        return
    
    embed = discord.Embed(
        title=f"{EMOJI_INFO_TICKET} Message Edited",
        description=f"**{guild.name}** • {after.channel.mention}",
        color=discord.Color(0x3498db)
    )
    embed.add_field(name=f"{EMOJI_USER_TICKETS} Author", value=f"@{after.author.name}", inline=True)
    embed.add_field(name=f"{EMOJI_CLOCK} When?", value=datetime.now().strftime('%d/%m/%Y - %H:%M:%S'), inline=True)
    embed.add_field(name="\u200b", value="\u200b", inline=False)
    embed.add_field(name=f"{EMOJI_MINUS} Before", value=before.content[:512] or "*(No text)*", inline=False)
    embed.add_field(name=f"{EMOJI_PLUS} After", value=after.content[:512] or "*(No text)*", inline=False)
    embed.set_image(url=LOGO_URL)
    
    await log_channel.send(embed=embed)

@bot.event
async def on_guild_update(before: discord.Guild, after: discord.Guild):
    """Log when guild is updated"""
    if before.guild_id not in AUDIT_LOG_CHANNEL:
        return
    
    log_channel = before.get_channel(AUDIT_LOG_CHANNEL[before.id])
    if not log_channel:
        return
    
    changes = []
    
    if before.name != after.name:
        changes.append(f"**Name**: {before.name} → {after.name}")
    if before.icon != after.icon:
        changes.append("**Icon**: Changed")
    if before.banner != after.banner:
        changes.append("**Banner**: Changed")
    
    if not changes:
        return
    
    embed = discord.Embed(
        title=f"{EMOJI_GEAR} Server Updated",
        description=f"**{after.name}**",
        color=discord.Color(0x9b59b6)
    )
    embed.add_field(name=f"{EMOJI_EXCLAMATION} Changes", value="\n".join(changes), inline=False)
    embed.add_field(name=f"{EMOJI_CLOCK} When?", value=datetime.now().strftime('%d/%m/%Y - %H:%M:%S'), inline=False)
    embed.set_image(url=LOGO_URL)
    
    await log_channel.send(embed=embed)

@bot.event
async def on_role_create(role: discord.Role):
    """Log when a role is created"""
    guild = role.guild
    if guild.id not in AUDIT_LOG_CHANNEL:
        return
    
    log_channel = guild.get_channel(AUDIT_LOG_CHANNEL[guild.id])
    if not log_channel:
        return
    
    embed = discord.Embed(
        title=f"{EMOJI_PLUS} Role Created",
        description=f"**{guild.name}**",
        color=discord.Color(0x2ecc71)
    )
    embed.add_field(name=f"{EMOJI_INFO_TICKET} Role", value=role.mention, inline=True)
    embed.add_field(name=f"{EMOJI_CLOCK} When?", value=datetime.now().strftime('%d/%m/%Y - %H:%M:%S'), inline=True)
    embed.add_field(name="\u200b", value="\u200b", inline=False)
    embed.set_image(url=LOGO_URL)
    
    await log_channel.send(embed=embed)

@bot.event
async def on_role_delete(role: discord.Role):
    """Log when a role is deleted"""
    guild = role.guild
    if guild.id not in AUDIT_LOG_CHANNEL:
        return
    
    log_channel = guild.get_channel(AUDIT_LOG_CHANNEL[guild.id])
    if not log_channel:
        return
    
    embed = discord.Embed(
        title=f"{EMOJI_MINUS} Role Deleted",
        description=f"**{guild.name}**",
        color=discord.Color(0xe74c3c)
    )
    embed.add_field(name=f"{EMOJI_INFO_TICKET} Role", value=role.name, inline=True)
    embed.add_field(name=f"{EMOJI_CLOCK} When?", value=datetime.now().strftime('%d/%m/%Y - %H:%M:%S'), inline=True)
    embed.add_field(name="\u200b", value="\u200b", inline=False)
    embed.set_image(url=LOGO_URL)
    
    await log_channel.send(embed=embed)

@bot.event
async def on_role_update(before: discord.Role, after: discord.Role):
    """Log when a role is updated"""
    guild = after.guild
    if guild.id not in AUDIT_LOG_CHANNEL:
        return
    
    log_channel = guild.get_channel(AUDIT_LOG_CHANNEL[guild.id])
    if not log_channel:
        return
    
    changes = []
    
    if before.name != after.name:
        changes.append(f"**Name**: {before.name} → {after.name}")
    if before.color != after.color:
        changes.append(f"**Color**: {before.color} → {after.color}")
    if before.permissions != after.permissions:
        changes.append("**Permissions**: Changed")
    
    if not changes:
        return
    
    embed = discord.Embed(
        title=f"{EMOJI_GEAR} Role Updated",
        description=f"**{guild.name}**",
        color=discord.Color(0x9b59b6)
    )
    embed.add_field(name=f"{EMOJI_INFO_TICKET} Role", value=after.mention, inline=True)
    embed.add_field(name=f"{EMOJI_EXCLAMATION} Changes", value="\n".join(changes), inline=False)
    embed.add_field(name=f"{EMOJI_CLOCK} When?", value=datetime.now().strftime('%d/%m/%Y - %H:%M:%S'), inline=False)
    embed.set_image(url=LOGO_URL)
    
    await log_channel.send(embed=embed)

# ========== WELCOME SYSTEM ==========

@bot.event
async def on_member_join(member: discord.Member):
    """Send welcome message when a member joins"""
    guild = member.guild
    
    if guild.id not in WELCOME_CHANNEL:
        return
    
    welcome_channel = guild.get_channel(WELCOME_CHANNEL[guild.id])
    if not welcome_channel:
        return
    
    embed = discord.Embed(
        title="Welcome To S.U!",
        description=f"Welcome @{member.name}! this is Skibidi Toilet, a community founded by many famous YouTubers.\n\n{EMOJI_PAPERPLANE} Don't forget to read the rules.\n\n{EMOJI_EXCLAMATION} Please keep in mind that this is one of the skibidi toilet community servers.",
        color=discord.Color(0x000000)
    )
    
    embed.add_field(name="\u200b", value="\u200b", inline=False)
    
    # Add decorative image
    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
    embed.add_field(name="\u200b", value="\u200b", inline=False)
    
    # Add welcome banner
    embed.set_image(url="https://s3.galaxybot.app/media/embeds/banner/welcome/Welcome.png")
    
    embed.set_footer(text=f"Welcome to {guild.name}! • {datetime.now().strftime('%d/%m/%Y - %H:%M:%S')}")
    
    await welcome_channel.send(f"{member.mention}", embed=embed)

@bot.tree.command(name="ticket-logs", description="Set ticket logs channel (Admin only)")
@app_commands.checks.has_permissions(administrator=True)
async def ticket_logs(interaction: discord.Interaction, channel: discord.TextChannel):
    """Setup ticket logs channel"""
    TICKET_LOG_CHANNEL[interaction.guild.id] = channel.id
    save_settings()
    
    embed = discord.Embed(
        title=f"{EMOJI_GEAR} Ticket Logs Setup",
        description=f"Ticket logs channel has been set to {channel.mention}",
        color=discord.Color(0x2ecc71)
    )
    embed.add_field(name="\u200b", value="\u200b", inline=False)
    embed.set_image(url=LOGO_URL)
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="close", description="Close a ticket")
async def close_ticket(interaction: discord.Interaction, reason: str = "No reason provided"):
    """Close a ticket"""
    channel = interaction.channel
    
    if channel.id not in TICKET_INFO:
        error_embed = discord.Embed(
            title="Error",
            description="This is not a ticket channel!",
            color=discord.Color(0xff0000)
        )
        await interaction.response.send_message(embed=error_embed, ephemeral=True)
        return
    
    ticket_data = TICKET_INFO[channel.id]
    user_id = ticket_data['user_id']
    ticket_number = ticket_data['ticket_number']
    category = ticket_data['category']
    created_at = ticket_data['created_at']
    
    guild = interaction.guild
    
    # Calculate processing time
    time_diff = datetime.now() - created_at
    hours = time_diff.seconds // 3600
    minutes = (time_diff.seconds % 3600) // 60
    processing_time = f"{hours}h {minutes}m" if hours > 0 else f"{minutes}m"
    
    # Send log message
    if guild.id in TICKET_LOG_CHANNEL:
        log_channel = guild.get_channel(TICKET_LOG_CHANNEL[guild.id])
        if log_channel:
            log_embed = discord.Embed(
                title=f"{EMOJI_LOCK} Ticket has been closed",
                description=f"**{guild.name}**",
                color=discord.Color(0xe74c3c)
            )
            log_embed.add_field(name=f"{EMOJI_TICKET} CaseID", value=f"#{ticket_number}", inline=True)
            log_embed.add_field(name=f"{EMOJI_USER_MINUS} Closed by", value=f"@{interaction.user.name}", inline=True)
            log_embed.add_field(name=f"{EMOJI_CLOCK} Processing time", value=processing_time, inline=True)
            log_embed.add_field(name="\u200b", value="\u200b", inline=False)
            log_embed.add_field(name=f"{EMOJI_CLOCK} When?", value=datetime.now().strftime('%d/%m/%Y - %H:%M:%S'), inline=False)
            log_embed.add_field(name=f"{EMOJI_TICKET} Ticket category", value=TICKET_CATEGORIES[category]['name'], inline=False)
            log_embed.set_image(url=LOGO_URL)
            await log_channel.send(embed=log_embed)
    
    # Send DM to ticket creator
    try:
        user = await bot.fetch_user(user_id)
        dm_embed = discord.Embed(
            title=f"{EMOJI_LOCK} Your ticket has been closed!",
            description=f"@Skibidi Union Bot has closed your ticket on **{guild.name}**. We hope that your issue has been resolved!",
            color=discord.Color(0xe74c3c)
        )
        dm_embed.add_field(name=f"{EMOJI_TICKET} CaseID", value=f"#{ticket_number}", inline=True)
        dm_embed.add_field(name=f"{EMOJI_LOCK} Guild", value=guild.name, inline=True)
        dm_embed.add_field(name=f"{EMOJI_CLOCK} Processing time", value=processing_time, inline=True)
        dm_embed.add_field(name="\u200b", value="\u200b", inline=False)
        dm_embed.add_field(name=f"{EMOJI_CLOCK} Created at", value=created_at.strftime('%d/%m/%Y - %H:%M:%S'), inline=False)
        dm_embed.add_field(name=f"{EMOJI_TICKET} Ticket category", value=TICKET_CATEGORIES[category]['name'], inline=False)
        dm_embed.set_image(url=LOGO_URL)
        await user.send(embed=dm_embed)
    except:
        pass
    
    # Respond to closer
    response_embed = discord.Embed(
        title=f"{EMOJI_LOCK} Ticket Closed",
        description=f"The ticket #{ticket_number} has been closed.",
        color=discord.Color(0xe74c3c)
    )
    response_embed.set_image(url=LOGO_URL)
    await interaction.response.send_message(embed=response_embed)
    
    # Delete ticket info
    del TICKET_INFO[channel.id]
    if channel.id in TICKET_CLAIMED_BY:
        del TICKET_CLAIMED_BY[channel.id]
    
    # Delete channel after 5 seconds
    await asyncio.sleep(5)
    try:
        await channel.delete(reason=f"Ticket #{ticket_number} closed")
    except:
        pass

# Start bot
if __name__ == '__main__':
    bot.run(TOKEN)

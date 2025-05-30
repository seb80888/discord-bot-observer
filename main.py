import discord
from discord.ext import commands
import datetime
import random
import gspread
from google.oauth2.service_account import Credentials

# Google Sheets setup
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'Credentials.json'

credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
gc = gspread.authorize(credentials)

# Google Sheet URL you provided
SPREADSHEET_ID = "1ded3aGdFwW4tRxqbCIpX9oPAnN3TlP_ccg0LXCLOnNA"

try:
    sheet = gc.open_by_key(SPREADSHEET_ID)

    # Create or get different worksheets for different purposes
    worksheets = {}

    # Red Pill activities sheet
    try:
        worksheets['redpill'] = sheet.worksheet("RedPill_Log")
    except:
        worksheets['redpill'] = sheet.add_worksheet(title="RedPill_Log", rows="1000", cols="5")
        worksheets['redpill'].update(values=[['Timestamp', 'User', 'Action', 'Date', 'Notes']], range_name='A1:E1')

    # Blue Pill activities sheet
    try:
        worksheets['bluepill'] = sheet.worksheet("BluePill_Log")
    except:
        worksheets['bluepill'] = sheet.add_worksheet(title="BluePill_Log", rows="1000", cols="5")
        worksheets['bluepill'].update(values=[['Timestamp', 'User', 'Action', 'Date', 'Notes']], range_name='A1:E1')

    # System/Bot status sheet
    try:
        worksheets['system'] = sheet.worksheet("System_Log")
    except:
        worksheets['system'] = sheet.add_worksheet(title="System_Log", rows="1000", cols="4")
        worksheets['system'].update(values=[['Timestamp', 'Event', 'Status', 'Details']], range_name='A1:D1')

    # Daily summary sheet
    try:
        worksheets['summary'] = sheet.worksheet("Daily_Summary")
    except:
        worksheets['summary'] = sheet.add_worksheet(title="Daily_Summary", rows="1000", cols="6")
        worksheets['summary'].update(values=[['Date', 'RedPill_Count', 'BluePill_Count', 'Total_Actions', 'Most_Active_User', 'Notes']], range_name='A1:F1')

    # Trading Journal sheet
    try:
        worksheets['trading'] = sheet.worksheet("Trading_Journal")
    except:
        worksheets['trading'] = sheet.add_worksheet(title="Trading_Journal", rows="1000", cols="12")
        worksheets['trading'].update(values=[['Timestamp', 'User', 'Symbol', 'Action', 'Entry_Price', 'Exit_Price', 'Quantity', 'PnL', 'Strategy', 'Market_Condition', 'Emotion_Score', 'Notes']], range_name='A1:L1')

    # Market Analysis sheet
    try:
        worksheets['market'] = sheet.worksheet("Market_Analysis")
    except:
        worksheets['market'] = sheet.add_worksheet(title="Market_Analysis", rows="1000", cols="8")
        worksheets['market'].update(values=[['Timestamp', 'Symbol', 'Price', 'Volume', 'RSI', 'Signal_Type', 'Confidence', 'Action_Taken']], range_name='A1:H1')

    # Performance Metrics sheet
    try:
        worksheets['performance'] = sheet.worksheet("Performance_Metrics")
    except:
        worksheets['performance'] = sheet.add_worksheet(title="Performance_Metrics", rows="1000", cols="10")
        worksheets['performance'].update(values=[['Date', 'Total_Trades', 'Winning_Trades', 'Win_Rate', 'Total_PnL', 'Best_Trade', 'Worst_Trade', 'Avg_Trade', 'Max_Drawdown', 'Sharpe_Ratio']], range_name='A1:J1')

    print("✅ Google Sheets connection successful! All tabs configured.")

except Exception as e:
    print(f"❌ Google Sheets connection failed: {e}")
    worksheets = {}

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Bot(intents=intents)

@bot.event
async def on_ready():
    print(f"🟢 Matrix Operator Online: {bot.user}")

    # Log bot startup to system sheet
    if worksheets.get('system'):
        try:
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log_data = [[timestamp, 'Bot Startup', 'Online', f'Matrix Operator {bot.user} activated']]

            # Find next empty row
            values = worksheets['system'].col_values(1)
            next_row = len(values) + 1

            worksheets['system'].update(values=log_data, range_name=f'A{next_row}:D{next_row}')
            print("✅ System startup logged to Google Sheets!")
        except Exception as e:
            print(f"❌ Failed to log startup: {e}")

    await bot.sync_commands()

@bot.slash_command(name="redpill", description="Activează Red Pill Discipline")
async def redpill(ctx):
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Log to RedPill dedicated sheet
    if worksheets.get('redpill'):
        try:
            log_data = [[timestamp, ctx.author.name, 'RedPill Activated', today, 'Discipline +1%']]

            # Find next empty row
            values = worksheets['redpill'].col_values(1)
            next_row = len(values) + 1

            worksheets['redpill'].update(values=log_data, range_name=f'A{next_row}:E{next_row}')
            print(f"✅ RedPill logged: {ctx.author.name} - {timestamp}")
        except Exception as e:
            print(f"❌ Failed to log RedPill: {e}")

    await ctx.respond(f"🟥 RED PILL ACTIVATED for {today}\nDiscipline: ✅ 1% Logged\n📊 Tracked in RedPill_Log sheet")

@bot.slash_command(name="bluepill", description="Activează Blue Pill - comportament impulsiv")
async def bluepill(ctx):
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Log to BluePill dedicated sheet
    if worksheets.get('bluepill'):
        try:
            log_data = [[timestamp, ctx.author.name, 'BluePill Taken', today, 'Needs reflection']]

            # Find next empty row
            values = worksheets['bluepill'].col_values(1)
            next_row = len(values) + 1

            worksheets['bluepill'].update(values=log_data, range_name=f'A{next_row}:E{next_row}')
            print(f"✅ BluePill logged: {ctx.author.name} - {timestamp}")
        except Exception as e:
            print(f"❌ Failed to log BluePill: {e}")

    await ctx.respond("🟦 Blue Pill taken. Reflectă în #🩺 shadow-review.\n📊 Tracked in BluePill_Log sheet")

@bot.slash_command(name="quote", description="Primește un citat Matrix motivațional")
async def quote(ctx):
    quotes = [
        "I do not chase. I align. I receive. I execute.",
        "You're not here to trade. You're here to execute the plan.",
        "Silence is strength. Focus is weaponized.",
        "Red Pill = claritate. Blue Pill = haos."
    ]
    await ctx.respond(f"🧠 Quote of the Day:\n*{random.choice(quotes)}*")

@bot.slash_command(name="summary", description="Generează rezumatul zilnic")
async def summary(ctx):
    today = datetime.datetime.now().strftime("%Y-%m-%d")

    if not worksheets:
        await ctx.respond("❌ Google Sheets not available")
        return

    try:
        # Count today's activities
        redpill_count = 0
        bluepill_count = 0
        most_active_user = "N/A"
        user_counts = {}

        # Count RedPill activities
        if worksheets.get('redpill'):
            redpill_data = worksheets['redpill'].get_all_values()[1:]  # Skip header
            for row in redpill_data:
                if len(row) >= 4 and row[3] == today:  # Date column
                    redpill_count += 1
                    user = row[1]  # User column
                    user_counts[user] = user_counts.get(user, 0) + 1

        # Count BluePill activities
        if worksheets.get('bluepill'):
            bluepill_data = worksheets['bluepill'].get_all_values()[1:]  # Skip header
            for row in bluepill_data:
                if len(row) >= 4 and row[3] == today:  # Date column
                    bluepill_count += 1
                    user = row[1]  # User column
                    user_counts[user] = user_counts.get(user, 0) + 1

        # Find most active user
        if user_counts:
            most_active_user = max(user_counts, key=user_counts.get)

        total_actions = redpill_count + bluepill_count

        # Log summary to summary sheet
        if worksheets.get('summary'):
            summary_data = [[today, redpill_count, bluepill_count, total_actions, most_active_user, f"Generated by {ctx.author.name}"]]

            # Find next empty row
            values = worksheets['summary'].col_values(1)
            next_row = len(values) + 1

            worksheets['summary'].update(values=summary_data, range_name=f'A{next_row}:F{next_row}')

        # Send response
        summary_msg = f"📊 **Daily Summary for {today}**\n\n"
        summary_msg += f"🟥 RedPill Actions: **{redpill_count}**\n"
        summary_msg += f"🟦 BluePill Actions: **{bluepill_count}**\n"
        summary_msg += f"📈 Total Actions: **{total_actions}**\n"
        summary_msg += f"👑 Most Active: **{most_active_user}**\n\n"
        summary_msg += "💾 Summary saved to Daily_Summary sheet"

        await ctx.respond(summary_msg)

    except Exception as e:
        await ctx.respond(f"❌ Failed to generate summary: {str(e)}")

@bot.slash_command(name="trade_entry", description="Log a trade entry")
async def trade_entry(ctx, symbol: str, action: str, price: float, quantity: float, strategy: str = "Manual", emotion: int = 5):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    if worksheets.get('trading'):
        try:
            log_data = [[timestamp, ctx.author.name, symbol.upper(), f"{action.upper()}_ENTRY", price, "", quantity, "", strategy, "Unknown", emotion, f"Entry logged by {ctx.author.name}"]]
            
            values = worksheets['trading'].col_values(1)
            next_row = len(values) + 1
            
            worksheets['trading'].update(values=log_data, range_name=f'A{next_row}:L{next_row}')
            
            await ctx.respond(f"📈 **TRADE ENTRY LOGGED**\n"
                            f"🎯 Symbol: **{symbol.upper()}**\n"
                            f"🚀 Action: **{action.upper()}**\n"
                            f"💰 Price: **${price}**\n"
                            f"📊 Quantity: **{quantity}**\n"
                            f"🧠 Strategy: **{strategy}**\n"
                            f"😊 Emotion Score: **{emotion}/10**\n"
                            f"✅ Logged to Trading_Journal")
        except Exception as e:
            await ctx.respond(f"❌ Failed to log trade: {str(e)}")
    else:
        await ctx.respond("❌ Trading journal not available")

@bot.slash_command(name="trade_exit", description="Log a trade exit with P&L calculation")
async def trade_exit(ctx, symbol: str, exit_price: float, notes: str = "Manual exit"):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    if worksheets.get('trading'):
        try:
            # Find the most recent entry for this symbol by this user
            all_data = worksheets['trading'].get_all_values()[1:]  # Skip header
            user_entries = []
            
            for i, row in enumerate(all_data):
                if (len(row) >= 4 and row[1] == ctx.author.name and 
                    row[2] == symbol.upper() and "ENTRY" in row[3] and 
                    row[5] == ""):  # Exit price empty
                    user_entries.append((i + 2, row))  # +2 for header and 0-indexing
            
            if not user_entries:
                await ctx.respond(f"❌ No open position found for {symbol.upper()}")
                return
            
            # Use the most recent entry
            row_index, entry_data = user_entries[-1]
            entry_price = float(entry_data[4])
            quantity = float(entry_data[6])
            action = entry_data[3]
            
            # Calculate P&L
            if "BUY" in action:
                pnl = (exit_price - entry_price) * quantity
            else:  # SELL
                pnl = (entry_price - exit_price) * quantity
            
            # Update the row with exit data
            worksheets['trading'].update(values=[[exit_price]], range_name=f'F{row_index}')
            worksheets['trading'].update(values=[[round(pnl, 2)]], range_name=f'H{row_index}')
            worksheets['trading'].update(values=[[notes]], range_name=f'L{row_index}')
            
            pnl_emoji = "🟢" if pnl > 0 else "🔴" if pnl < 0 else "⚪"
            
            await ctx.respond(f"📉 **TRADE CLOSED**\n"
                            f"🎯 Symbol: **{symbol.upper()}**\n"
                            f"💰 Entry: **${entry_price}** → Exit: **${exit_price}**\n"
                            f"📊 Quantity: **{quantity}**\n"
                            f"{pnl_emoji} **P&L: ${pnl:.2f}**\n"
                            f"📝 Notes: {notes}\n"
                            f"✅ Updated in Trading_Journal")
            
        except Exception as e:
            await ctx.respond(f"❌ Failed to close trade: {str(e)}")
    else:
        await ctx.respond("❌ Trading journal not available")

@bot.slash_command(name="trading_stats", description="Get your trading performance statistics")
async def trading_stats(ctx):
    if not worksheets.get('trading'):
        await ctx.respond("❌ Trading journal not available")
        return
    
    try:
        all_data = worksheets['trading'].get_all_values()[1:]  # Skip header
        user_trades = []
        
        for row in all_data:
            if (len(row) >= 8 and row[1] == ctx.author.name and 
                row[7] != "" and row[7] != "0"):  # Has P&L data
                try:
                    pnl = float(row[7])
                    user_trades.append(pnl)
                except:
                    continue
        
        if not user_trades:
            await ctx.respond("❌ No completed trades found for your account")
            return
        
        total_trades = len(user_trades)
        winning_trades = len([t for t in user_trades if t > 0])
        losing_trades = len([t for t in user_trades if t < 0])
        win_rate = (winning_trades / total_trades) * 100 if total_trades > 0 else 0
        total_pnl = sum(user_trades)
        avg_trade = total_pnl / total_trades if total_trades > 0 else 0
        best_trade = max(user_trades) if user_trades else 0
        worst_trade = min(user_trades) if user_trades else 0
        
        performance_emoji = "🚀" if total_pnl > 0 else "📉" if total_pnl < 0 else "➡️"
        
        stats_msg = f"{performance_emoji} **TRADING PERFORMANCE**\n\n"
        stats_msg += f"📊 **Total Trades:** {total_trades}\n"
        stats_msg += f"✅ **Winning Trades:** {winning_trades}\n"
        stats_msg += f"❌ **Losing Trades:** {losing_trades}\n"
        stats_msg += f"🎯 **Win Rate:** {win_rate:.1f}%\n"
        stats_msg += f"💰 **Total P&L:** ${total_pnl:.2f}\n"
        stats_msg += f"📈 **Average Trade:** ${avg_trade:.2f}\n"
        stats_msg += f"🏆 **Best Trade:** ${best_trade:.2f}\n"
        stats_msg += f"💀 **Worst Trade:** ${worst_trade:.2f}\n\n"
        stats_msg += "💾 Data from Trading_Journal sheet"
        
        # Log performance to performance sheet
        if worksheets.get('performance'):
            today = datetime.datetime.now().strftime('%Y-%m-%d')
            perf_data = [[today, total_trades, winning_trades, f"{win_rate:.1f}%", total_pnl, best_trade, worst_trade, avg_trade, "", ""]]
            
            values = worksheets['performance'].col_values(1)
            next_row = len(values) + 1
            worksheets['performance'].update(values=perf_data, range_name=f'A{next_row}:J{next_row}')
        
        await ctx.respond(stats_msg)
        
    except Exception as e:
        await ctx.respond(f"❌ Failed to calculate stats: {str(e)}")

@bot.slash_command(name="market_signal", description="Log a market analysis signal")
async def market_signal(ctx, symbol: str, signal_type: str, confidence: int, action: str = "WATCH"):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    if worksheets.get('market'):
        try:
            log_data = [[timestamp, symbol.upper(), "", "", "", signal_type.upper(), confidence, action.upper()]]
            
            values = worksheets['market'].col_values(1)
            next_row = len(values) + 1
            
            worksheets['market'].update(values=log_data, range_name=f'A{next_row}:H{next_row}')
            
            confidence_emoji = "🔥" if confidence >= 80 else "⚡" if confidence >= 60 else "⚠️"
            
            await ctx.respond(f"🎯 **MARKET SIGNAL LOGGED**\n"
                            f"📊 Symbol: **{symbol.upper()}**\n"
                            f"🚨 Signal: **{signal_type.upper()}**\n"
                            f"{confidence_emoji} Confidence: **{confidence}%**\n"
                            f"🎬 Action: **{action.upper()}**\n"
                            f"✅ Logged to Market_Analysis")
        except Exception as e:
            await ctx.respond(f"❌ Failed to log signal: {str(e)}")
    else:
        await ctx.respond("❌ Market analysis sheet not available")

@bot.slash_command(name="status", description="Verifică statusul Google Sheets connection")
async def status(ctx):
    if worksheets:
        try:
            status_msg = "✅ Google Sheets connection: **ACTIVE**\n\n📊 **Available Sheets:**\n"

            for sheet_name, sheet_obj in worksheets.items():
                try:
                    # Test each sheet
                    test_read = sheet_obj.get("A1")
                    row_count = len(sheet_obj.col_values(1)) - 1  # Subtract header
                    status_msg += f"• **{sheet_name.title()}**: ✅ ({row_count} entries)\n"
                except Exception as e:
                    status_msg += f"• **{sheet_name.title()}**: ❌ Error\n"

            await ctx.respond(status_msg)
        except Exception as e:
            await ctx.respond(f"❌ Google Sheets connection: **ERROR**\n```{str(e)}```")
    else:
        await ctx.respond("❌ Google Sheets connection: **FAILED**\nCheck credentials and permissions")
@bot.slash_command(name="setup_server", description="Setează automat canalele Matrix")
async def setup_server(ctx, preset: str):
    if preset.lower() == "matrix":
        await ctx.defer()
        guild = ctx.guild

        structure = {
            "🧠 REDPILL - DISCIPLINĂ SUPREMĂ": [
                "redpill-daily-checkin", "discipline-tracker", "focus-sessions",
                "redpill-victories", "morning-routine", "evening-review"
            ],
            "🔵 BLUEPILL - SHADOW ANALYSIS": [
                "bluepill-confessions", "shadow-work-deep", "reset-counter",
                "bluepill-patterns", "recovery-plan", "accountability-check"
            ],
            "📊 ANALYTICS & TRACKING": [
                "daily-stats-auto", "weekly-reports", "monthly-overview",
                "progress-charts", "habit-streaks", "performance-metrics"
            ],
            "🎯 GOAL ACHIEVEMENT": [
                "goal-setting", "milestone-tracking", "vision-board",
                "quarterly-review", "success-stories", "future-planning"
            ],
            "⚡ RAPID EXECUTION": [
                "quick-actions", "immediate-tasks", "urgency-channel",
                "fast-decisions", "emergency-protocol", "instant-accountability"
            ],
            "🧘 MINDSET & PHILOSOPHY": [
                "matrix-wisdom", "stoic-principles", "mental-training",
                "philosophical-debates", "mindset-shifts", "consciousness-levels"
            ],
            "📚 KNOWLEDGE BASE": [
                "resources-library", "book-recommendations", "study-materials",
                "learning-paths", "skill-development", "knowledge-sharing"
            ],
            "🤝 COMMUNITY & SUPPORT": [
                "general-discussion", "peer-support", "mentorship",
                "collaboration", "team-challenges", "community-events"
            ],
            "🔧 SYSTEM ADMINISTRATION": [
                "bot-commands", "system-logs", "configuration",
                "updates-changelog", "error-reports", "maintenance-mode"
            ],
            "🎮 GAMIFICATION & REWARDS": [
                "leaderboards", "achievement-unlocks", "point-system",
                "badges-earned", "competition-arena", "reward-center"
            ]
        }

        created = []
        skipped = []

        for category_name, channels in structure.items():
            existing_category = discord.utils.get(guild.categories, name=category_name)
            if existing_category:
                skipped.append(f"📂 {category_name}")
                continue

            try:
                category = await guild.create_category(category_name)
                for ch_name in channels:
                    existing_channel = discord.utils.get(guild.text_channels, name=ch_name)
                    if existing_channel:
                        skipped.append(f"📄 {ch_name}")
                        continue

                    await guild.create_text_channel(ch_name, category=category)
                    created.append(f"📄 {ch_name}")
            except Exception as e:
                await ctx.respond(f"❌ Eroare la crearea categoriei/canalului: `{str(e)}`")
                return

        # ✅ Trimitere raport în Discord
        summary = "✅ **Server Setup Complete!**\n\n"
        if created:
            summary += f"🆕 Canale/Categorii create:\n" + "\n".join(created) + "\n\n"
        if skipped:
            summary += f"⚠️ Canale deja existente:\n" + "\n".join(skipped)

        await ctx.respond(summary)

        # ✅ Log în Google Sheets
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            worksheets['system'].append_row(
                [timestamp, '/setup_server', 'SUCCESS', f'Created: {len(created)} | Skipped: {len(skipped)}']
            )
        except Exception as e:
            await ctx.respond(f"❌ Eroare la logarea în System_Log: `{str(e)}`")
            return
    else:
        await ctx.respond(f"❌ Preset necunoscut.")
                          
# Folosește "matrix"
@bot.slash_command(name="check_categories", description="Verifică duplicatele în categorii")
async def check_categories(ctx):
    guild = ctx.guild
    categories = [category.name for category in guild.categories]

    # Check for duplicates
    duplicates = set([cat for cat in categories if categories.count(cat) > 1])

    if duplicates:
        await ctx.respond(f"❌ Categorii duplicate găsite: {', '.join(duplicates)}")
    else:
        await ctx.respond("✅ Nu există categorii duplicate.")
        @bot.slash_command(name="setup_server", description="Creează automat toate categoriile și canalele esențiale")
        async def setup_server(ctx):
            guild = ctx.guild
            author = ctx.author
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # ✅ 1. Verificare permisiuni
            required_perms = ['manage_channels', 'manage_roles', 'send_messages', 'view_channel']
            missing_perms = [perm for perm in required_perms if not getattr(guild.me.guild_permissions, perm)]

            if missing_perms:
                await ctx.respond(f"❌ Botul NU are permisiunile necesare:\n🔒 Lipsesc: `{', '.join(missing_perms)}`\nDă-i `Administrator` în setările rolului.")
                if worksheets.get('system'):
                    try:
                        worksheets['system'].append_row([timestamp, '/setup_server', 'FAILED', f"Missing perms: {', '.join(missing_perms)}"])
                    except: pass
                return

            # ✅ 2. Structura categoriilor și canalelor
            structure = {
                "📊 Trading Logs": ["redpill-log", "bluepill-log", "trades-journal"],
                "🧠 Discipline": ["protocol-888", "shadow-review", "daily-intent"],
                "📈 Market": ["market-signals", "bias-weekly", "setup-gallery"],
                "💾 Bot-System": ["bot-status", "bot-feedback"]
            }

            created = []
            skipped = []

            for category_name, channels in structure.items():
                # Creează categoria dacă nu există
                category = discord.utils.get(guild.categories, name=category_name)
                if not category:
                    category = await guild.create_category(category_name)
                    created.append(f"📁 {category_name}")
                else:
                    skipped.append(f"📁 {category_name}")

                for ch_name in channels:
                    existing = discord.utils.get(guild.text_channels, name=ch_name)
                    if not existing:
                        await guild.create_text_channel(ch_name, category=category)
                        created.append(f"# {ch_name}")
                    else:
                        skipped.append(f"# {ch_name}")

            # ✅ 3. Feedback vizual în Discord
            summary = f"✅ **Server Setup Complete!**\n\n"
            if created:
                summary += f"🔧 Canale/Categorii create:\n" + "\n".join(created) + "\n\n"
            if skipped:
                summary += f"⏩ Canale deja existente:\n" + "\n".join(skipped)

            await ctx.respond(summary)

            # ✅ 4. Log în Google Sheets
            if worksheets.get('system'):
                try:
                    worksheets['system'].append_row([timestamp, '/setup_server', 'SUCCESS', f"Created: {len(created)} | Skipped: {len(skipped)}"])
                    @bot.slash_command(name="setup_server", description="Creează automat categoriile și canalele esențiale Matrix")
                    async def setup_server(ctx):
                        guild = ctx.guild
                        author = ctx.author
                        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                        # ✅ 1. Verificare permisiuni
                        required_perms = ['manage_channels', 'manage_roles', 'send_messages', 'view_channel']
                        missing_perms = [perm for perm in required_perms if not getattr(guild.me.guild_permissions, perm)]

                        if missing_perms:
                            await ctx.respond(f"❌ Botul NU are permisiunile necesare:\n🔒 Lipsesc: `{', '.join(missing_perms)}`\nDă-i `Administrator` în setările rolului.")
                            try:
                                if worksheets.get('system'):
                                    worksheets['system'].append_row([timestamp, '/setup_server', 'FAILED', f"Missing perms: {', '.join(missing_perms)}"])
                            except:
                                pass
                            return

                        # ✅ 2. Structura categorii și canale
                        structure = {
                            "📊 Trading Logs": ["redpill-log", "bluepill-log", "trades-journal"],
                            "🧠 Discipline": ["protocol-888", "shadow-review", "daily-intent"],
                            "📈 Market": ["market-signals", "bias-weekly", "setup-gallery"],
                            "💾 Bot-System": ["bot-status", "bot-feedback"]
                        }

                        created = []
                        skipped = []

                        for category_name, channels in structure.items():
                            try:
                                category = discord.utils.get(guild.categories, name=category_name)
                                if not category:
                                    category = await guild.create_category(category_name)
                                    created.append(f"📁 {category_name}")
                                else:
                                    skipped.append(f"📁 {category_name}")

                                for ch_name in channels:
                                    existing = discord.utils.get(guild.text_channels, name=ch_name)
                                    if not existing:
                                        await guild.create_text_channel(ch_name, category=category)
                                        created.append(f"# {ch_name}")
                                    else:
                                        skipped.append(f"# {ch_name}")
    if skipped:
        summary += f"⚠️ Canale deja existente:\n" + "\n".join(skipped)

    try:
        for category in guild.categories:
            await category.delete()
            deleted.append(f"🗑️ {category.name}")

        for channel in guild.channels:
            if not channel.category:  # în afara unei categorii
                await channel.delete()
                deleted.append(f"🗑️ {channel.name} (canal direct)")

        # 🟢 Mesaj de confirmare
        await ctx.followup.send(
            f"✅ Serverul a fost curățat complet.\n"
            f"🧹 Elemente șterse: {len(deleted)}\n"
            f"📌 Poți acum rula `/setup_server preset: matrix` pentru reconstrucție."
        )

        # 🟢 Log in System Sheet
        if worksheets.get('system'):
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            worksheets['system'].append_row([
                timestamp, '/reset_structure', 'CLEANUP', f'Deleted: {len(deleted)}'
            ])
    except Exception as e:
        await ctx.followup.send(f"❌ Eroare la resetare: `{str(e)}`")
bot.run("MTM3NzY3MDE3ODg4MzYzMzI4Mg.GEjMXr.lq73SC4qjAL66d6xetX9gCkZRMLr6S4FDr5NBM")
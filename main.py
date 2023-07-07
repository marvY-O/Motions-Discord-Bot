from keep_alive import keep_alive
import discord
import os
#import random
os.system("pip install --upgrade google-cloud-bigquery")
from google.cloud import bigquery
import google.auth
from discord.ext import commands

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/runner/motionsbot/snappy-attic-334609-b29283a461a9.json"



token = os.environ['TOKEN']

bot = commands.Bot(command_prefix='$')

credentials, project = google.auth.default(
    scopes=[
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/bigquery",
    ]
)

client = discord.Client()
#token = os.environ['TOKEN']

BigQuery_client = bigquery.Client(credentials=credentials, project=project)

def generate(motion_type, count,filter_result):

    name_group_query = """
        SELECT motion, info 
        FROM `snappy-attic-334609.debate_topics.{}`
        WHERE motion LIKE "%{}%"
        ORDER BY RAND()
        LIMIT {};
    """.format(motion_type,count,filter_result)

    query_results = BigQuery_client.query(name_group_query)  

    result_motion = []
    result_info = ""

    query_results = list(query_results)
    for i in range(len(query_results)):
        #print(query_results[i][0]+"\n")
        result_motion.append("`{}. ".format(i+1)+query_results[i][0]+"`\n")

    return result_motion

def generate_custom(keyword = "", count = 1 ):
  name_group_query = """
        SELECT motion, info 
        FROM `snappy-attic-334609.debate_topics.custom`
        WHERE motion LIKE "%{}%"
        ORDER BY RAND()
        LIMIT {};
  """.format(keyword, count)

  query_results = BigQuery_client.query(name_group_query)  

  result_motion = []
  result_info = ""

  query_results = list(query_results)
  for i in range(len(query_results)):
      #print(query_results[i][0]+"\n")
      result_motion.append("`{}. ".format(i+1)+query_results[i][0]+"`\n")

  return result_motion

@bot.command(name = 'spank', help = 'to spank eachother')
async def fetch_custom(ctx, arg2):
    await ctx.send("{} spanked {}! How does your booty feel {}? lmao".format(ctx.message.author, arg2, arg2) )

@bot.command(name = 'custom', help = 'Fetch through custom motions')
async def fetch_custom(ctx, arg2 = 1, arg1 = ""):
    for e in generate_custom(arg1, arg2):
        await ctx.send(e)

@bot.command(name = "motion_search", help = "Search for motion(s) using a keyword")
async def test(ctx, arg1):
    for e in generate("all_motions",arg1, 10):
        await ctx.send(e)

@bot.command(name = "motion", help = "Pick random motion(s). format $motion_thw <count>; default count=1")
async def test(ctx, arg2=1):
    for e in generate("all_motions","",arg2):
        await ctx.send(e)

"""
@bot.command(name = "motion_thbt", help = "Pick random motion(s) of THBT type. \n\t\tformat: $motion_thbt <count>; default count=1")
async def test(ctx, arg2=1):
    for e in generate("THBT_motions","",arg2):
        await ctx.send(e)

@bot.command(name = "motion_thb", help = "Pick random motion(s) of THB type. \n\t\tformat $motion_thb <count>; default count=1")
async def test(ctx, arg2=1):
    for e in generate("THB_motions","",arg2):
        await ctx.send(e)

@bot.command(name = "motion_th", help = "Pick random motion(s) of TH type. format $motion_th <count>; default count=1")
async def test(ctx, arg2=1):
    for e in generate("TH_motions","",arg2):
        await ctx.send(e)

@bot.command(name = "motion_ths", help = "Pick random motion(s) of THS type. format $motion_ths <count>; default count=1")
async def test(ctx, arg2=1):
    for e in generate("THS_motions","",arg2):
        await ctx.send(e)

@bot.command(name = "motion_tho", help = "Pick random motion(s) of THO type. format $motion_tho <count>; default count=1")
async def test(ctx, arg2=1):
    for e in generate("THO_motions","",arg2):
        await ctx.send(e)

@bot.command(name = "motion_thw", help = "Pick random motion(s) of THW type. format $motion_thw <count>; default count=1")
async def test(ctx, arg2=1):
    for e in generate("THW_motions","",arg2):
        await ctx.send(e)
"""




@bot.event
async def on_ready_command():
    print('We have logged in as {0.user} for bot'.format(client))


keep_alive()
bot.run(token)



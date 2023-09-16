from nonebot import get_driver
from nonebot.internal.adapter import message
from nonebot.plugin import PluginMetadata

from .config import Config
from nonebot import on_command,require,get_bots
from nonebot.rule import to_me
from nonebot_plugin_apscheduler import scheduler
from apscheduler.triggers.interval import IntervalTrigger
import requests
import json





bootcode = on_command("sboot",rule=to_me(),block=True)   #启动matcher

@bootcode.handle()
async def send_message_bot():
    await bootcode.send("booting") #启动开始提示

    config = get_driver().config
    gameinfo = config.gameinfo   #获取config中的gameinfo列表
    groupid = config.groupid     #获取config中的群号
    
    gameinfo = {"moli1":"8623324930326","moli2":"8623724390687","moli3":"8623324730316","moli4":"8622724750452"} #测试用gameinfo列表
    
    url_common = "https://api.gametools.network/bf1/detailedserver/?gameid="    #公共api
    
    gamename = list(gameinfo.keys())
    gameid = list(gameinfo.values()) #将info中的信息裁切
    
    gameurl = []
    for i in range(len(gamename)):
        url_temp = url_common + gameid[i]
        gameurl.append(url_temp)  #将id转化为api的url

    headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    }
    
    old_PlayerAmount = []
    for i in range(len(gamename)):
        content = requests.get(gameurl[i],headers=headers).text
        dic_content = json.loads(content)
        old_player = dic_content["playerAmount"]
        old_PlayerAmount.append(old_player)      #初始化人数列表

    @scheduler.scheduled_job("interval", seconds=10)
    async def _():
        bot, = get_bots().values()
        for i in range(len(gamename)):
            content = requests.get(gameurl[i],headers=headers).text
            dic_content = json.loads(content)
            new_Amount = dic_content["playerAmount"]
            if new_Amount != old_PlayerAmount[i]:
                if new_Amount <= 55:
                    message_send = "{} {}->{}".format(gamename[i],old_PlayerAmount[i],new_Amount)
                    await bot.send_msg(
                            message_type="group",
                          # 群号
                            group_id=groupid,
                            message=message_send
                    )   
                old_PlayerAmount[i] = new_Amount


        
        
        




    


















__plugin_meta = PluginMetadata(
    name="test-plugin_2",
    description="",
    usage="",
    config=Config,
)

global_config = get_driver().config
config = Config.parse_obj(global_config)


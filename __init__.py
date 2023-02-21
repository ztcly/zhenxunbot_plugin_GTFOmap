from nonebot import on_command
from nonebot.params import CommandArg, ArgStr
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Message, Event, PrivateMessageEvent, GroupMessageEvent, \
    MessageSegment
from nonebot.log import logger
import os

__zx_plugin_name__ = "GTFO地图查询"
__plugin_usage__ = """
usage：
    查询GTFO地图捏
    指令：
        gtfo [地图] 例：gtfo r1a1  /  gtfo R7C1
    地图来源：https://steamcommunity.com/sharedfiles/filedetails/?id=2828458886
    作者：Hunter48RUS,Artefas,livinghell
""".strip()
__plugin_des__ = "查询GTFO地图"
__plugin_cmd__ = ["gtfo [地图编号]"]
__plugin_version__ = 1.0
__plugin_author__ = "ztcly"
__plugin_settings__ = {
    "cmd": ["gtfo"]
}


gtfomap = on_command("gtfo", priority=5, block=True)


Tool_Path = os.path.dirname(__file__)
Tool_Assets_Path = f"{Tool_Path}/Assets"
Map_Path = f"{Tool_Assets_Path}/Maps"

async def SendMsg(bot: Bot, event, msg):
    if isinstance(event, PrivateMessageEvent):
        await bot.send_private_msg(user_id=event.user_id, message=msg)
    elif isinstance(event, GroupMessageEvent):
        await bot.send_group_msg(group_id=event.group_id, message=msg)
    else:
        bot.send(event,msg)

@gtfomap.handle()
async def sendmapimage(bot: Bot, event: Event, text: Message = CommandArg()):
    args = []
    if len(text) > 0:
        args = text[0].data['text'].split(' ')
    if len(args) < 1:
        await gtfomap.send('地图查询方式：gtfo [地图名称]')
        return

    levelname = args[0].upper()
    maps=[]

    logger.info(f"[gtfomap]准备开始查询,查询关卡{levelname},地图路径:{Map_Path}")

    for root, dirs, files in os.walk(Map_Path):
        for file in files:
            if file[0:4] == levelname:
                logger.info(f"查询关卡名：{levelname} 与地图 {file} 通过比较")
                path = os.path.join(root, file)
                maps.append(path)

    logger.info(f"[gtfomap]准备开始发送")
    for mappath in maps:
        mapimage = f"file:///{mappath}"
        msg = Message.template("{}{}").format(f"查询地图：{levelname}",MessageSegment.image(f'{mapimage}'))
        try:
            logger.info(f"[gtfomap]发送地图路径【{mappath}】")
            await SendMsg(bot, event, msg)
        except Exception as e:
            await SendMsg(bot, event, f"出错啦!\n错误信息：{e}")
            logger.error(e)









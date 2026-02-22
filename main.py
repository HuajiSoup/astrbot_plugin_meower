from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger

import random

quotes = [
    "滑稽是人类进步的阶梯。",
    "滑而不稽则罔，稽而不滑则殆。",
    "真是滑天下之大稽。",
    "稽稽稽墨稽墨，稽稽墨稽墨稽~",
    "武装直升稽！！",
    "恐怖稽器人！！",
    "读万卷书，不如滑万里稽。",
]

@register("astrbot_plugin_meower", "HuajiSoup", "AstrBot Meower 插件，纯粹用来测试。", "0.0.3")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""

    @filter.command_group("huaji")
    def huaji_group(self):
        """huaji组命令"""
        pass

    @huaji_group.command("random")
    async def huaji_random_int(self, event: AstrMessageEvent, max_value: int = 100):
        """随机整数，可指定上限。"""
        rand_int = random.randint(0, max_value)
        yield event.plain_result(f"{rand_int}")
    
    @huaji_group.command("meow")
    async def huaji_meow(self, event: AstrMessageEvent):
        """喵~"""
        yield event.plain_result("喵~")
    
    @huaji_group.command("quote")
    async def huaji_quote(self, event: AstrMessageEvent, new_quote: str = ""):
        """输出已记录的名言警句，或添加新名言"""
        stored_quotes = await self.get_kv_data("quotes", quotes)
        if stored_quotes is None:
            stored_quotes = list(quotes)
        
        if (new_quote != ""):
            # 添加新名言
            if "稽" not in new_quote:
                yield event.plain_result("不是滑稽的名言不加哦喵")
                return
            stored_quotes.append(new_quote)
            await self.put_kv_data("quotes", stored_quotes)
            yield event.plain_result(f"滑稽水怪记住了喵，{new_quote}")
        else:
            # 输出随机名言
            yield event.plain_result(random.choice(stored_quotes))

    # @filter.command("helloworld")
    # async def helloworld(self, event: AstrMessageEvent):
    #     """repeat your msg""" # 这是 handler 的描述，将会被解析方便用户了解插件内容。建议填写。
    #     user_name = event.get_sender_name()
    #     message_str = event.message_str # 用户发的纯文本消息字符串
    #     message_chain = event.get_messages() # 用户所发的消息的消息链 # from astrbot.api.message_components import *
    #     logger.info(message_chain)
    #     yield event.plain_result(f"Hello, {user_name}, 你发了 {message_str}!") # 发送一条纯文本消息

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""

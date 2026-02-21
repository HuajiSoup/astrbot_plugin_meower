from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger

@register("astrbot_plugin_meower", "HuajiSoup", "AstrBot Meower 插件，纯粹用来测试。", "0.0.2")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""

    @filter.command("random")
    async def random_int(self, event: AstrMessageEvent):
        """生成一个随机整数，范围是 0-100"""
        import random
        rand_int = random.randint(0, 100)
        yield event.plain_result(f"{rand_int}")

    @filter.command("helloworld")
    async def helloworld(self, event: AstrMessageEvent):
        """repeat your msg""" # 这是 handler 的描述，将会被解析方便用户了解插件内容。建议填写。
        user_name = event.get_sender_name()
        message_str = event.message_str # 用户发的纯文本消息字符串
        message_chain = event.get_messages() # 用户所发的消息的消息链 # from astrbot.api.message_components import *
        logger.info(message_chain)
        yield event.plain_result(f"Hello, {user_name}, 你发了 {message_str}!") # 发送一条纯文本消息

    @filter.regex(r".*草.*")
    async def grass_cn(self, event: AstrMessageEvent):
        """匹配到草时回复我"""
        yield event.plain_result("我")
    
    @filter.regex(r".*grass.*")
    async def grass_en(self, event: AstrMessageEvent):
        """匹配到grass时回复me"""
        yield event.plain_result("me")

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""

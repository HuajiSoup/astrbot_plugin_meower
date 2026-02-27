from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger

import random
import aiohttp

quotes = [
    "滑稽是人类进步的阶梯。",
    "滑而不稽则罔，稽而不滑则殆。",
    "真是滑天下之大稽。",
    "稽稽稽墨稽墨，稽稽墨稽墨稽~",
    "武装直升稽！！",
    "恐怖稽器人！！",
    "读万卷书，不如滑万里稽。",
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://image.baidu.com'
}

async def urlAccessible(session: aiohttp.ClientSession, url: str, timeout: int = 10):
    try:
        timeoutObj = aiohttp.ClientTimeout(timeout)
        async with session.head(url, timeout=timeoutObj, allow_redirects=True) as response:
            return response.status == 200
    except:
        return False

@register("astrbot_plugin_meower", "HuajiSoup", "AstrBot Meower 插件，纯粹用来测试。", "0.0.3")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""

    @filter.command_group("huaji", alias={"滑稽"})
    def huaji_group(self):
        """huaji组命令"""
        pass


    @huaji_group.command("random", alias={"rand", "随机数"})
    async def huaji_random_int(
        self, 
        event: AstrMessageEvent, 
        max_value: int = 100
    ):
        """随机整数，可指定上限。"""
        rand_int = random.randint(1, max_value)
        yield event.plain_result(f"{rand_int}")
    

    @huaji_group.command("meow", alias={"喵"})
    async def huaji_meow(
        self, 
        event: AstrMessageEvent
    ):
        """喵~"""
        yield event.plain_result("喵~")
    
    
    @huaji_group.group("quote", alias={"名言", "名言警句"})
    def huaji_quote_group(self):
        """名言警句组命令"""
        pass

    @huaji_quote_group.command("add", alias={"添加"})
    async def huaji_quote_add(
        self, 
        event: AstrMessageEvent, 
        new_quote: str
    ):
        """添加新名言"""
        if "稽" not in new_quote:
            yield event.plain_result("不是滑稽的名言不加哦喵")
            return
        stored_quotes = await self.get_kv_data("quotes", quotes)
        if stored_quotes is None:
            stored_quotes = list(quotes)
        stored_quotes.append(new_quote)
        await self.put_kv_data("quotes", stored_quotes)
        yield event.plain_result(f"滑稽水怪记住了喵，{new_quote}")

    @huaji_quote_group.command("say", alias={"说"})
    async def huaji_quote_random(
        self, 
        event: AstrMessageEvent
    ):
        """输出随机名言"""
        stored_quotes = await self.get_kv_data("quotes", quotes)
        if stored_quotes is None or len(stored_quotes) == 0:
            stored_quotes = list(quotes)
        yield event.plain_result(random.choice(stored_quotes))

    @huaji_quote_group.command("clear", alias={"remove", "清除"})
    async def huaji_quote_clear(
        self, 
        event: AstrMessageEvent
    ):
        """清除所有名言"""
        await self.put_kv_data("quotes", [])
        yield event.plain_result("滑稽水怪把添加的名言都忘了喵")
    

    @huaji_group.command("image", alias={"pic", "搜图", "图片"})
    async def huaji_image(
        self,
        event: AstrMessageEvent, 
        keyword: str = "香蕉", 
    ):
        """搜索关键词图片"""
        page = random.randint(0, 200)
        url = f"https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&word={keyword}&pn={page}&rn=15"

        try:
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.get(url, timeout=15) as response:
                    if (response.status != 200):
                        logger.error(f"GET失败，状态码：{response.status}")
                        yield event.plain_result("555，滑稽水怪搜索失败了喵")
                        return
                    data = await response.json(content_type=None)
            
                # get all available possible images
                images = [{
                    "low": img.get("middleURL"),
                    "high": img.get("replaceUrl")[0].get("ObjUrl", ""),
                } for img in data.get("data") if img.get("middleURL") and img.get("replaceUrl")]

                result = random.choice(images)
                res_high = result.get("high", "")
                res_low = result.get("low", "")

                if (res_high != "" and await urlAccessible(session, res_high)):
                    yield event.image_result(res_high)
                    return
                yield event.image_result(res_low)
            
        except aiohttp.ClientError as e:
            logger.error(f"网络请求出现异常，报错信息如下：{e}")
            yield event.plain_result("555，滑稽水怪断网了喵")
        except Exception as e:
            logger.error(f"插件运行出现异常，报错信息如下：{e}")
            yield event.plain_result("555，滑稽水怪被玩坏了喵")

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

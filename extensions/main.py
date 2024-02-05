"""
The MIT License (MIT)

Copyright (c) 2022-present cardboard box

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.


An extension to the discord.py library, bringing some features that do not
exist, or may not be included in the library. extDPY uses asynchronous code with 
modules aiohttp and requests to efficiently PATCH, POST, GET, and DELETE content.


 -> future content will introduce ability to manipulate text channels and servers themselves
    to further the accessiblity of the discord API to everyone.

"""
from .moderation import moderation
from .events import guild_events
from .webhooks import discord_webhooks

def ext_setup(client,token):
    return moderation(client,token), guild_events(client,token), discord_webhooks(client,token)
    


if __name__ != '__main__':
    print("cardboard box extDPY extension, so you won't have to code it.")
    print("aiohttp clientsessions autoclosed once bot is finished, just have to be initialised beforehand.")


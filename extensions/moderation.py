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
exist, or may not be included in the library. 
"""


import requests, aiohttp, datetime
from errors import raise_error, read_json_for_errors


class moderation:

    '''Functional. Manages users in any guild connected to application.'''


    def __init__(self,client,token):
        self.client = client
        self.token = token
        self.client.session = aiohttp.ClientSession()
    
    def __repr__(self) -> str:
        return f'moderation(client={self.client}, token={self.token}, session={self.client.session})'
    
    def _toiso(seconds:float=0,minutes:float=0,hours:float=0,days:float=0) -> str:
        return (datetime.datetime.utcnow()+datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)).isoformat()

    #patches
    async def timeout_user(self,*, user_id: int, guild_id: int, days:float=0, hours:float=0, minutes:float=0):

        '''Patch subroutine
        params:
        user_id = user to affect by timeout
        guild_id = guild to affet user in
        days = self explanatory
        hours = self explanatory
        minutes = self explanatory'''
        

        
        headers = {"Authorization": f"Bot {self.token}"}
        url = f"https://discord.com/api/v9/guilds/{guild_id}/members/{user_id}"
        timeout = moderation._toiso(days=days, hours=hours, minutes=minutes)
        json = {'communication_disabled_until': timeout}
        async with self.client.session.patch(url, json=json, headers=headers) as session:
            if session.status in range(200, 299):
                
                return      
            raise_error(session.status)
        

        #second delay, fix in next release
    async def untimeout_user(self,*,user_id: int, guild_id: int):

        '''Patch subroutine
        params same as timeout_user, without addition of any timeout length.'''

        
        headers = {"Authorization": f"Bot {self.token}"}
        url = f"https://discord.com/api/v9/guilds/{guild_id}/members/{user_id}"
        timeout = moderation._toiso(seconds=1)
        json = {'communication_disabled_until': timeout}
        async with self.client.session.patch(url, json=json, headers=headers) as session:
            if session.status in range(200, 299):
                
                return 
            raise_error(session.status)
        

    async def nickname_user(self,*,user_id:int, guild_id:int, nickname:str):

        '''Patch subroutine
        params:
        user_id = user to affect by nickname
        guild_id = guild to affect user in
        nickname = "something to call the user" '''

        
        headers = {"Authorization": f"Bot {self.token}"}
        url = f"https://discord.com/api/v9/guilds/{guild_id}/members/{user_id}"
        json = {'nick': nickname}
        async with self.client.session.patch(url,json=json,headers=headers) as session:
            if session.status in range(200,299):
                
                return 
            raise_error(session.status)
        

    async def move_member(self,*,user_id:int, guild_id:int, channel_id:int):

        '''Patch subroutine
        params:
        user_id= user to move
        guild_id = guild to affect user in
        channel_id = channel to move user to'''

        
        headers = {"Authorization": f"Bot {self.token}"}
        url = f"https://discord.com/api/v9/guilds/{guild_id}/members/{user_id}"
        json = {'channel_id':channel_id}
        async with self.client.session.patch(url,json=json,headers=headers) as session:
            if session.status in range(200,299):
                return
            raise_error(session.status)
        
    
    async def disconnect_member(self,*,user_id:int,guild_id:int):

        '''Patch subroutine
        params:
        user_id= user to move
        guild_id = guild to affect user in'''

        self.client.session = aiohttp.ClientSession()
        headers = {"Authorization": f"Bot {self.token}"}
        url = f"https://discord.com/api/v9/guilds/{guild_id}/members/{user_id}"
        json = {'channel_id':None}
        async with self.client.session.patch(url,json=json,headers=headers) as session:
            if session.status in range(200,299):
                
                return
            raise_error(session.status)
        


    #gets, return str 
    async def get_invites(self,*,guild_id:int):

        '''Get subroutine
        params:
        guild_id = guild
        '''

        headers = {"Authorization": f"Bot {self.token}"}
        r=requests.get(f"https://discord.com/api/v9/guilds/{guild_id}/invites",headers=headers)
        if r.status_code in range(200,299):
            return r.text
        read_json_for_errors(r.json)
        
    async def get_audit(self,*,guild_id:int):

        '''Get subroutine
        params:
        guild_id = guild
        '''

        headers = {"Authorization": f"Bot {self.token}"}
        r=requests.get(f"https://discord.com/api/v9/guilds/{guild_id}/audit-logs",headers=headers)
        if r.status_code in range(200,299):
            return r.text
        read_json_for_errors(r.json)
    
    

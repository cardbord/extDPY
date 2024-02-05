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



import aiohttp, requests, datetime
from errors import raise_error

class EventClass:

    '''Represents a channel scheduled event

    uses POST, PATCH, DELETE requests to manipulate a specific event from discord's API
    requires full ownership of the event and administrator permissions

    EventClass.modify(channel_id,name,start_time,end_time,description,event_type) -> new EventClass
    - EventClass.modify functions without all parameters, replacing those not filled with the original value.
    
    EventClass.delete()
    
    '''

    def __init__(self,
        id,
        guild_id,
        channel_id,
        name,
        start_time,
        end_time,
        description,
        event_type,
        image
    ):
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.name = name
        self.start_time = start_time
        self.end_time = end_time
        self.description = description
        self.event_type = event_type
        self.image = image
        self.event_id = id
        self.token = tooken
        self.client = sessions



    async def modify(self,channel_id:int=None,name:str=None,start_time:int=None,end_time:int=None,description:str=None,event_type=None):
        '''
        Sends a PATCH request to modify the data of the current event.

        All parameters are unrequired, simply select the necessary ones you want to change.
        
        '''
        
        
        self.client.session = aiohttp.ClientSession
        headers = {"Authorization": f"Bot {self.token}"}
        url=f"https://discord.com/api/v9/guilds/{self.guild_id}/scheduled-events/{self.event_id}"
        if start_time != None and end_time != None:

            starttime = (datetime.datetime.utcnow() + datetime.timedelta(minutes=start_time)).isoformat()
            endtime = (datetime.datetime.utcnow() + datetime.timedelta(minutes=end_time)).isoformat()
        else:
            starttime = None
            endtime = None
        
        params = [channel_id,name,starttime,endtime,description,event_type]

        if params[0] is None:
            params[0] = self.channel_id
        if params[1] is None:
            params[1] = self.name
        if params[2] is None:
            params[2] = self.start_time
        if params[3] is None:
            params[3] = self.end_time
        if params[4] is None:
            params[4] = self.description
        if params[5] is None:
            params[5] = self.event_type



        json = {
            'channel_id':params[0],
            'entity_metadata':None,
            'name':params[1],
            'privacy_level':2,
            'scheduled_start_time':params[2],
            'scheduled_end_time':params[3],
            'description':params[4],
            'entity_type':params[5],
            'status':'SCHEDULED',
            'image':None
        }
        async with self.client.session.patch(url=url,headers=headers,json=json) as session:
            if session.status in range(200,299):
                text = await session.text()
                eventstatus = eval(text.replace('null','None'))
                await self.client.session.close()
                return EventClass(
                    id=eventstatus['id'],
                    guild_id=eventstatus['guild_id'],
                    channel_id=eventstatus['channel_id'],
                    name=eventstatus['name'],
                    start_time=eventstatus['scheduled_start_time'],
                    end_time=eventstatus['scheduled_end_time'],
                    description=eventstatus['description'],
                    image=eventstatus['image'],
                    event_type=eventstatus['entity_type']
                )
                
                
                
        raise_error(status_code=session.status)
        await self.client.session.close()
        return


    async def delete(self):
        self.client.session = aiohttp.ClientSession()
        headers = {"Authorization": f"Bot {self.token}"}
        url = f"https://discord.com/api/v9/guilds/{self.guild_id}/scheduled-events/{self.event_id}"
        async with self.client.session.delete(headers=headers) as session:
            if session.status in range(200,299):
                await self.client.session.close()
                return
        await self.client.session.close()
        return




class guild_events:

    '''Creates and finds guild events
    
    guild_events.create_event(guild_id,channel_id,name,start_time,end_time,description,event_type,image) -> EventClass
    guild_events.find_guild_events(guild_id) -> dict
    guild_events.get_event(guild_id,event_id) -> EventClass

    '''

    def __init__(self,client,token):
        self.client = client
        self.token = token
        global tooken
        tooken = self.token
        global sessions
        sessions = self.client
        
    
    async def create_event(self,
    *,
    guild_id:int,
    channel_id:int,
    name:str,
    start_time:int,
    end_time:int,
    description:str,
    event_type:int,
    image:str=None,
    ) -> EventClass:
        self.client.session = aiohttp.ClientSession()
        headers = {"Authorization": f"Bot {self.token}"}
        url=f"https://discord.com/api/v9/guilds/{guild_id}/scheduled-events"
        starttime = (datetime.datetime.utcnow() + datetime.timedelta(minutes=start_time)).isoformat()
        endtime = (datetime.datetime.utcnow() + datetime.timedelta(minutes=end_time)).isoformat()
        json = {
        'channel_id':channel_id,
        'entity_metadata':None,
        'name':name,
        'privacy_level':2,
        'scheduled_start_time':starttime,
        'scheduled_end_time':endtime,
        'description':description,
        'entity_type':event_type,
        'status':'SCHEDULED',
        'image':image
        }
        async with self.client.session.post(url, json=json, headers=headers) as session:
            if session.status in range(200, 299):
                text = await session.text()
                eventstatus = eval(text.replace('null',"None"))
                await self.client.session.close()
                return EventClass(
                    id=eventstatus['id'],
                    guild_id=guild_id,
                    channel_id=channel_id,
                    name=name,
                    start_time=eventstatus['scheduled_start_time'],
                    end_time=eventstatus['scheduled_end_time'],
                    description=eventstatus['description'],
                    image=eventstatus['image'],
                    event_type=event_type
                )
                
                
                
        raise_error(status_code=session.status)
        await self.client.session.close()
        return




    async def find_guild_events(self,*,guild_id:int):
        self.client.session = aiohttp.ClientSession()
        headers = {"Authorization": f"Bot {self.token}"}
        r=requests.get(f"https://discord.com/api/v9/guilds/{guild_id}/scheduled-events",headers=headers)
        if r.status_code in range(200,299):
            await self.client.session.close()
            return r.text
        await self.client.session.close()
        return

    async def get_event(self,*,guild_id:int,event_id:int) -> EventClass:
        self.client.session = aiohttp.ClientSession()
        headers = {"Authorization": f"Bot {self.token}"}
        r= requests.get(f"https://discord.com/api/v9/guilds/{guild_id}/scheduled-events/{event_id}",headers=headers)
        if r.status_code in range(200,299):
            eventstatus = eval(r.text.replace('null','None'))
            return EventClass(
                id=eventstatus['id'],
                guild_id=guild_id,
                channel_id=eventstatus['channel_id'],
                name=eventstatus['name'],
                start_time=eventstatus['scheduled_start_time'],
                end_time=eventstatus['scheduled_end_time'],
                description=eventstatus['description'],
                image=eventstatus['image'],
                event_type=eventstatus['event_type']
            )
        raise_error(r.status_code)
        return None
    
    
    
    






    
    async def pin_message(self,*,channel_id:int,message_id:int):
        self.client.session = aiohttp.ClientSession()
        headers = {"Authorization": f"Bot {self.token}"}
        url = f"https://discord.com/api/v9/channels/{channel_id}/pins/{message_id}"
        async with self.client.session.put(url=url,headers=headers) as session:
            if session.status == 204:
                await self.client.session.close()
        
        raise_error(session.status)
        await self.client.session.close()
        return
import logging

from opsdroid.skill import Skill
from opsdroid.matchers import match_event, match_crontab, match_regex
from opsdroid.events import Message

from opsdroid.connector.twitch.events import (
    UserFollowed,
    UserJoinedChat,
    UserSubscribed,
    UserGiftedSubscription
        )


_LOGGER = logging.getLogger(__name__)


class TwitchSkill(Skill):
    """Opsdroid skill to integrate with twitch and game."""
    def __init__(self, opsdroid, config, *args, **kwargs):
        super().__init__(opsdroid, config, *args, **kwargs)
        self.connector = self.opsdroid.get_connector('shell')
        self.joined_users = []

    async def create_character(self, name):
        """Creates character for user."""
        character = {
                "name": name, 
                "class": "adventurer", 
                "gold": 0, 
                "inventory": {
                    "head": None,
                    "body": None,
                    "r-hand": None,
                    "l-hand": None,
                    "legs": None,
                    "feet": None,
                    "items": {"potion": 1}
                    } 
                }

        characters_list = await self.opsdroid.memory.get("characters")
        characters_list[name] = character

        await self.opsdroid.memory.put("characters", characters_list)

    async def add_gold(self, name, amount=1):
        """Add gold to the user character sheet."""
        characters = await self.opsdroid.memory.get("characters")

        if characters.get(name):
            characters[name]["gold"] += amount
            return
        await self.create_character(name)

    @match_event(UserJoinedChat)
    async def user_joined(self, event):
        """User joined channel, add to the list and give points."""
        user = event.user
        await self.add_gold(user, 2)
        self.joined_users.append(user)
    
    @match_event(UserLeftChat)
    async def user_left(self, event):
        """Remove user from list when user leaves chat."""
        user = event.user
        self.joined_users.remove(user)

    @match_crontab('* * * * *')
    async def reward_view(self, event):
        """Reward users for viewing."""
        for user in self.joined_users:
            await self.add_gold(user)

    @match_regex('.*')
    async def talked(self, message):
        user = message.user

        if user not in self.joined_users:
            await self.add_gold(user)

    @match_event(UserFollowed)
    async def reward_follow(self, event):
        """Reward users for viewing."""
        await self.add_gold(event.follower, 100)

    @match_event(UserSubscribed)
    async def reward_sub(self, event):
        """Reward users for viewing."""
        await self.add_gold(event.user, 500)
    
    @match_event(UserSubscribed)
    async def reward_gift_sub(self, event):
        """Reward users for viewing."""
        await self.add_gold(event.gifter_name, 500)
        await self.add_gold(event.gifted_name, 250)
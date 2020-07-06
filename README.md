# opsdroid skill Twitch Game

A skill for [opsdroid](https://github.com/opsdroid/opsdroid) to work together with the Twitch Connector.

This skill was created to interact with a game to be played with Twitch and uses the opsdroid Twitch Connector. This skill
will create a character sheet for users that are on the chat and reward them for interacting with the streamer.

## Requirements

An active Twitch Connector.

## Configuration

```yaml
skills:
  game: {}

```

## Usage

### Reward every minute

Reward a user every minute with 1 gold for staying in chat.


### Reward each chat line

Reward a user with 1 gold for each message sent to the channel.


### Reward subscription

Reward a user with 500 gold for subscribing to the channel.

### Reward gifted subscription

Rewards the user that gifted the subscription with 500 gold and 250 gold to the gifted user.


### Reward user follows

Rewards a user with 100 gold for following the channel.
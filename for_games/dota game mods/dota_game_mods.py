#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


def parse(s):
    if s[0] == "-":
        s = s[1:]

    mod_list = list()

    # Вроде бы, единственная короткая комманда, длинной в 3 символа
    if "wtf" in s:
        mod_list.append("wtf")
        s.replace("wtf", "")

    for i in range(0, len(s), 2):
        mod_list.append(s[i] + s[i + 1])

    return mod_list


if __name__ == "__main__":
    import json

    game_mods = json.load(open("game_mods.json", encoding="utf-8"))

    mods = "-aremnpakulsc"
    mods = "-apemomsc"

    print("game mods:", mods)
    for gm in parse(mods):
        try:
            print(gm, game_mods[gm]["en"])
        except KeyError:
            print(f'Could not find the game mode: "{gm}".')


# Game Commands
#
#     -repick: Repick Gives you a new hero instead of the one you already have, at a cost. Can only be used once, in the first minute, but not in league mode. Repick costs 150 gold normally, but in -ar and -tr it costs 400 gold.
#     -ma: Matchup Displays which opponent controls which hero.
#     -ms: Move Speed Displays your heroes movement speed.
#     -unstuck: Unstuck Channels for 60 seconds, then moves your hero back to your base.
#     -recreate: Recreate Available for N’aix, Terrorblade, Dragon Knight and Banehallow. Use when close to the fountain if you have lost control of your hero (metamorphosis problem). 200 seconds channeling.
#     -deathon/off: Death Timer Toggles on and off a new death timer to show you your respawn without needing to open the scoreboard.
#     -disablehelp: Disable Help Disable help: Makes Chen’s Test of Faith (teleports you back to base) unable to teleport you.
#     -enablehelp: Enable Help Enable help: If -disablehelp has been activated, -enablehelp will make Chen’s Test of Faith able to teleport you again.
#     -cs: Creep Stats Shows how many creeps you have killed, as well as how many you have denied.
#     -cson: Creep Stat Scoreboard On Shows a scoreboard for creep stats
#     -csoff: Creep Stat Scoreboard Off Hides the scoreboard for creep stats
#     -fleshstr: Flesh Strength Command for Pudge to view how much str has been gained from the ability.
#     -gameinfo: Game Info Displays some information on the different game modes that are used.
#     -hidemsg/unhidemsg: Toggle Hero Death Message Turn on/off the Hero death message spam.
#     -refresh: Refresh Refreshes PA’s blur so that if you were visible you will become transparent again. This does not affect evasion in any way.
#     -showdeny: Show Deny Show denies.
#     -swaphero: Swap Hero Only usable once, and only in the first 90 seconds. Brings up a menu where you can select a teammate whom you would like to change hero with. The player you choose will get a menu where he can either accept or decline your offer.
#
#
#
#
# Commands
# tips 	Gives you various helpful pointers about your hero throughout the game.
# random 	Random. Gives you a random hero in modes like All Pick. You get 250 extra gold.
# random int 	Random. Gives you a random Intelligence hero in modes like All Pick. You get 150 extra gold.
# random str 	Random. Gives you a random Strength hero in modes like All Pick. You get 150 extra gold.
# random agi 	Random. Gives you a random Agility hero in modes like All Pick. You get 150 extra gold.
# ma 	Displays the heroes your opponents control and their levels. Alias: -matchup.
# ms 	Displays your hero's current movement speed. Alias: -movespeed.
# apm 	Displays apm ( actions per minute ) of all players.
# cs 	Displays your creep kills, denies, and neutral kills.
# switch # 	Allows you to switch teams with another player. Other players vote with -ok or -no after this command is entered.
# cson 	Activates the cs display to display your creep kills and denies.
# es 	Enables selection helper. This is enabled by default. Alias: -enableselection
# es 	Disables selection helper. Alias: -disableselection
# csoff 	Deactivates the cs display.
# c 	Center. Locks the camera on your hero.
# co 	Centeroff. Turns center mode off.
# disablehelp 	Prevents certain spells, such as Test of Faith cast by an allied Holy Knight, from affecting you. Also prevents allies from picking up your items in the fountain area.
# enablehelp 	Re-enables effects from certain allied spells and allows allies to pick up your items in the fountain area.
# unstuck 	Pauses your hero for 60 seconds, after which you are teleported to your base.
# recreate 	Sometimes rare glitches occur with certain heroes, recreate can fix those glitches. Recreate takes about 2 minutes to complete, and only works on Lycanthrope, Lifestealer, Dragon Knight, Soul Keeper, and Tormented Soul.
# swap # 	Offers to swap your hero with another player's. -swaphero # can also be used.
# showmsg 	Shows messages.
# hidemsg 	Hides messages.
# showdeny 	Shows a '!' above a creep when it is denied.
# hidedeny 	Hides the '!'.
# quote # 	Plays a hero quote. Writing it without a number will play a random hero quote.
# weather rain 	Switches weather to rain.
# weather snow 	Switches weather to snow.
# weather moonlight 	Switches weather to moonlight.
# weather wind 	Switches weather to wind.
# weather random 	Switches to random weather.
# weather off 	Turns weather off.
# di 	Enables -cson and -showdeny. Alias: -denyinfo. -di is initially enabled.
# don 	Shows the death timer. Alias: -deathon
# doff 	Hides the death timer. -deathoff
# roll # 	Shows a random number between 1 and the number entered, max of 2000. Default of 100.
# rollon 	Enables roll command. This is initially enabled.
# rolloff 	Disables roll command.
# hhn 	Hides the hero name portion of player's names. Alias: -hideheronames.
# test 	Enables single player commands.
# mute 	Toggles sounds on and off.
# clear 	Clears the messages.
# ii 	Item info. Shows items of allied heroes on multiboard.
# gameinfo 	Displays information about the current game modes.
# kickafk # 	Used to kick a player who has been AFK for a long period of time.
# mines 	Shows you how many Land Mines you have placed with Goblin Techies.
# mc 	Shows how many times you have Multicast with Ogre Magi.
# fs 	Shows how much bonus Strength you have gained from Flesh Heap with Pudge. Alias: -fleshstr
# int 	Shows how much bonus Intelligence you have gained from Last Word with Silencer.
# ha 	Shows your average accuracy with Meat Hook or Hookshot.
# aa 	Shows your average accuracy with Elune's Arrow.
# invokelist 	Displays all of Invoker's spells, and what reagents are needed to use them.
# water red 	Makes the water red.
# water green 	Makes the water green.
# water blue 	Makes the water blue.
# water default 	Makes the water the default color.
# water r g b 	Sets the water color to the color specified by r, g, and b. Example: "-water 255 0 0" is the same as "-water red".
# water random 	Sets the water to a random color.
# gg 	Displays bonus gold gained from Alchemist's Goblin Greed ability.
# rh 	Displays a random hero name. Alias: -rollhero.
#
# Single Player Commands
# lvlup # 	Increases level of your hero by entered value.
# refresh 	Resets ability cooldowns, sets health and mana of your hero to 100%.
# spawncreeps 	Spawns creeps from all lanes.
# powerup 	Spawns runes.
# neutrals 	Forces neutral spawn.
# kill 	Kills your last picked hero. This kill will be considered as a suicide.
# gold # 	Increases your gold by entered value.
# time # 	Sets time of day. Values should be between 0 and 24.
# killsent 	Kills sentinel creeps.
# killscourge 	Kills scourge creeps.
# killall 	Kills all creeps.
# noherolimitt 	Allows you to pick multiple heroes.
# trees 	Forces a tree spawn.
# killwards 	Removes wards from the map.
# spawnon 	Enables creep spawn. This is enabled initially.
# spawnoff 	Disables creep spawn.
#
#
#
#
# Single Player Commands
# lvlup # 	Increases level of your hero by entered value.
# refresh 	Resets ability cooldowns, sets health and mana of your hero to 100%.
# spawncreeps 	Spawns creeps from all lanes.
# powerup 	Spawns runes.
# neutrals 	Forces neutral spawn.
# kill 	Kills your last picked hero. This kill will be considered as a suicide.
# gold # 	Increases your gold by entered value.
# time # 	Sets time of day. Values should be between 0 and 24.
# killsent 	Kills sentinel creeps.
# killscourge 	Kills scourge creeps.
# killall 	Kills all creeps.
# noherolimitt 	Allows you to pick multiple heroes.
# trees 	Forces a tree spawn.
# killwards 	Removes wards from the map.
# spawnon 	Enables creep spawn. This is enabled initially.
# spawnoff 	Disables creep spawn.

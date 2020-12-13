import json
import nbt
import time

HIGHLIGHT_TIME = 15
CacheFile = 'server/usercache.json'
DatPath = 'server/world/playerdata/'
UUID = {}
Color = {
    "minecraft:overworld": "\"§a\"",
    "minecraft:the_nether": "\"§4\"",
    "minecraft:the_end": "\"§5\""
}
Text = {
    "minecraft:overworld": "{\"translate\": \"createWorld.customize.preset.overworld\"}",
    "minecraft:the_nether": "{\"translate\": \"advancements.nether.root.title\"}",
    "minecraft:the_end": "{\"translate\": \"advancements.end.root.title\"}"
}


def ReadPos(server, name):
    for i in UUID:
        if i["name"] == name:
            New = i["uuid"]
    nbtFile = nbt.nbt.NBTFile(DatPath + New + '.dat', 'rb')
    X = nbtFile["Pos"].tags[0].value
    Y = nbtFile["Pos"].tags[1].value
    Z = nbtFile["Pos"].tags[2].value
    Dim = str(nbtFile["Dimension"])
    Command = '{\"text\":\"[x:' + str(int(X)) + ', y:' + str(int(Y)) + ' ,z:' + str(int(Z)) + ']\"}'
    if Dim == 'minecraft:overworld':
        NetherPos = '(x:{},y:{},z:{})'.format(int(X/8), int(Y), int(Z/8))
        server.execute('tellraw @a ' + '["§e{} ","@ ",{},{}," ",{}," §7-> ",{},{},"{}"]'.format(name, Color[Dim], Text[Dim], Command, Color["minecraft:the_nether"], Text["minecraft:the_nether"], NetherPos))
    if Dim == 'minecraft:the_nether':
        OverworldPos = '(x:{},y:{},z:{})'.format(int(X*8), int(Y), int(Z*8))
        server.execute('tellraw @a ' + '["§e{} ","@ ",{},{}," ",{}," §7-> ",{},{},"{}"]'.format(name, Color[Dim], Text[Dim], Command, Color["minecraft:overworld"], Text["minecraft:overworld"], OverworldPos))
    if Dim == 'minecraft:the_end':
        server.execute('tellraw @a ' + '["§e{} ","@ ",{},{}," ",{}]'.format(name, Color[Dim], Text[Dim], Command))
    if not HIGHLIGHT_TIME == 0:
        server.execute('effect give {} minecraft:glowing {} 0 true'.format(name, HIGHLIGHT_TIME))


def ReadUUID():
    global UUID
    with open(CacheFile, 'r') as f:
        UUID = json.load(f)


def on_load(server, old_module):
    server.add_help_message('!!here', '广播坐标并高亮玩家')
    ReadUUID()


def on_user_info(server, info):
    content = info.content
    if content == '!!here':
        server.execute('save-all')
        time.sleep(0.1)
        ReadPos(server, info.player)


def on_player_joined(server, player, info):
    ReadUUID()

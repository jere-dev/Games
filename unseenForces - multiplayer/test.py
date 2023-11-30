def pos(mes):
    return [int(i) for i in mes.split(";")]

networkCommands = {
    'pos':pos
}

message = "pos:6;6"
spl = message.split(":")

print(networkCommands[spl[0]](spl[1]))
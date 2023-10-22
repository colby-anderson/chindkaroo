import random


def readchinpin(chinfile, pinfile, filter=None):
    filter = [f.lower() for f in (filter or [])]
    source = {}
    with open(chinfile, "r") as chin, open(pinfile, "r") as pin:
        for ctr, (c, p) in enumerate(zip(chin, pin)):
            p = p.lower().strip()
            c = c.strip()
            for f in filter:
                if f in c or f in p:
                    source.setdefault(f, []).append((c, p))
            if filter is None or len(filter) == 0:
                source.setdefault(ctr, []).append((c, p))
    return source


def present(source):
    key, tups = random.choice(list(source.items()))
    # to_show, to_reveal = zip(*[(elt[0], elt[1]) if random.choice([True, False]) else (elt[1], elt[0]) for elt in tups])
    to_show, to_reveal = zip(*[(elt[0], elt[1]) for elt in tups])
    source.pop(key)
    return list(to_show), list(to_reveal)


def updatedict(source, new):
    for key, value in new.items():
        source.setdefault(key, []).extend(value)
    return source


def process_level(coms):
    if len(coms) > 1:
        return list(range(int(coms[0]), int(coms[2]) + 1))
    else:
        return [int(coms[0])]


def get_source(levels, further_commands):
    source = {}
    for l in levels:
        for file_type in ["mandarincorner_sentences"]: # TODO
            source = updatedict(source, readchinpin(f"data/hsk{l}/hsk{l}_{file_type}.chinese", f"data/hsk{l}/hsk{l}_{file_type}.pinyin", further_commands))
    return source


def cli2():
    source = {}
    to_reveal = []
    while True:
        command = str(input('> '))
        # command = "start 3"
        if command == "exit":
            print("Exiting")
            return
        elif command in ["next", "n"]:
            to_show, to_reveal = present(source)
            print("\n".join(to_show))
        elif command in ["reveal", "r"]:
            print("\n".join(to_reveal))
        elif command.split(" ")[0] == "start":
            further_commands = command.split(" ")[1:]
            levels = process_level(further_commands[0])
            source = get_source(levels, further_commands[1:])
            to_show, to_reveal = present(source)
            print("\n".join(to_show))
        else:
            print("Invalid command. Exiting.")
            return




def opp(inp):
    if inp == "pinyin":
        return "chinese"
    else:
        return "pinyin"
# TODO: HEAVILY NOT PINYIN COMPATIBLE WITH "SHOWN"
def select_next(file_to_show, file_to_reveal, shown, num):
    with open(file_to_show, "r") as shows:
        with open(file_to_reveal, "r") as reveals:
            to_show_b4 = []
            to_reveal_b4 = []
            for s, r in zip(shows, reveals):
                if s not in shown:
                    to_show_b4.append(s.strip())
                    to_reveal_b4.append(r.strip())
            c = list(zip(to_show_b4, to_reveal_b4))
            random.shuffle(c)
            to_show, to_reveal = zip(*c)
                #     to_show.append(s.strip())
                #     to_reveal.append(r.strip())
                # if len(to_show) == num:
                #     return to_show, to_reveal
            to_show = list(to_show)
            to_reveal = list(to_reveal)
            if len(to_show) < num:
                return to_show, to_reveal
            else:
                return to_show[:5], to_reveal[:5]



def cli():
    exit = False
    shown = []
    to_reveal = []
    file_to_show = ""
    file_to_reveal = ""
    while True:
        command = str(input('> '))
        if command == "exit":
            print("Exiting")
            return
        else:
            params = command.split(" ")
            if params[0] in ["next", "n"]:
                to_show, to_reveal = select_next(file_to_show, file_to_reveal, shown, 5)
                print("\n".join(to_show))
                shown = shown + to_show
                if len(to_show) < 5:
                    print("Nothing left. Exiting after reveal.")
                    exit = True
            elif params[0] in ["reveal", "r"]:
                print("\n".join(to_reveal))
                to_reveal = []
                if exit:
                    print("Exiting")
                    return
            elif params[0] in ["sentences", "chars", "words"] and params[1] in ["pinyin", "chinese"] and params[2] in ["2", '3', '4', '5', '6']:
                to_reveal = []
                shown = []
                val = params[0]
                if params[0] == "sentences":
                    val = "mandarincorner_sentences"
                file_to_show = f"data/hsk{params[2]}/hsk{params[2]}_{val}.{params[1]}"
                file_to_reveal = f"data/hsk{params[2]}/hsk{params[2]}_{val}.{opp(params[1])}"
                to_show, to_reveal = select_next(file_to_show, file_to_reveal, shown, 5)
                print("\n".join(to_show))
                shown = shown + to_show
            else:
                print("Invalid command. Exiting.")



if __name__ == "__main__":
    cli2()
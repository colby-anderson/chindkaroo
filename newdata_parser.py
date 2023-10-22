def MandarinCornerQuizletParser():
    with open("hsk.txt", 'r', encoding='UTF-8') as original:
        with open("data/hsk6/hsk6_mandarincorner_sentences.pinyin", "a") as pinyin:
            with open("data/hsk6/hsk6_mandarincorner_sentences.chinese", "a") as chinese:
                currently_answer = False
                answer_line = 0
                while line := original.readline():
                    if line == "$$$\n":
                        currently_answer = False
                        answer_line = 0
                        continue
                    elif line == "&&&\n":
                        currently_answer = True
                        continue
                    elif currently_answer:
                        answer_line = answer_line + 1
                        if answer_line == 3:
                            pinyin.write(line[1:-2] + "\n")
                        elif answer_line == 4:
                            chinese.write(line)

def CharacterSeparateLineCreator():
    with open("hsk1_chars.chinese", 'r', encoding='UTF-8') as original:
        with open("hsk1_characters.chinese", "a") as chinese:
            while line := original.readline():
                chars = line.split()
                for char in chars:
                    chinese.write(char + "\n")


def SplitCharacterCSV():
    with open("hsk_csv/hsk6.csv", 'r', encoding='UTF-8') as original:
        with open("data/hsk6/hsk6_words.chinese", "a") as chinese:
            with open("data/hsk6/hsk6_words.pinyin", "a") as pinyin:
                with open("data/hsk6/hsk6_words.english", "a") as english:
                    while line := original.readline():
                        elements = line.split(",")
                        chinese.write(elements[0].strip() + "\n")
                        pinyin.write(elements[1].strip() + "\n")
                        english.write(elements[2].strip() + "\n")

def FromWordsToChars():
    with open("data/hsk6/hsk6_words.pinyin", 'r', encoding='UTF-8') as from_pinyin:
        with open("data/hsk6/hsk6_words.chinese", "r") as from_chinese:
            with open("data/hsk6/hsk6_chars.pinyin", "a") as to_pinyin:
                with open("data/hsk6/hsk6_chars.chinese", "a") as to_chinese:
                    with open("data/hsk1/hsk1_chars.chinese", "r") as hsk1:
                        with open("data/hsk2/hsk2_chars.chinese", "r") as hsk2:
                            with open("data/hsk3/hsk3_chars.chinese", "r") as hsk3:
                                with open("data/hsk4/hsk4_chars.chinese", "r") as hsk4:
                                    with open("data/hsk5/hsk5_chars.chinese", "r") as hsk5:
                                        processed = [char.strip() for char in hsk1]
                                        processed = processed + [char.strip() for char in hsk2]
                                        processed = processed + [char.strip() for char in hsk3]
                                        processed = processed + [char.strip() for char in hsk4]
                                        processed = processed + [char.strip() for char in hsk5]
                                        for fp, fc in zip(from_pinyin, from_chinese):
                                            pchars = fp.strip().split(" ")
                                            cchars = list(fc.strip())
                                            for cchar, pchar in zip(cchars, pchars):
                                                if cchar not in processed:
                                                    to_chinese.write(cchar + "\n")
                                                    to_pinyin.write(pchar + "\n")
                                                    processed.append(cchar)



if __name__ == "__main__":
    MandarinCornerQuizletParser()
"""
(adjective: strong / firm / staunch)

Even strong people have a weak side. - 
&&&
(坚强 jiānqiáng)

(Zài jiānqiáng de rén yě yǒu cuìruò de yī miàn.)
再坚强的人也有脆弱的一面。
$$$
(interjection: used to express surprise or dissatisfaction)

Hey? Why are you here? - 
&&&
(哎 āi)

(Āi? Nǐ zěnme huì zài zhèr?)
哎？你怎么会在这儿？
$$$
(interjection: sighing sound indicating sadness or regret)
"""
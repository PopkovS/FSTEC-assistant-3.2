import random
import re
import string


def create_sequence(*args):
    sequence = []
    for i in args:
        x, y = i
        sequence = sequence + [chr(i) for i in range(x, y)]
    return "".join(sequence)


def gen_rand_sting(chr_str, len_srt):
    if str(type(len_srt)) == "<class 'int'>":
        rand_str = "".join([random.choice(chr_str) for _ in range(len_srt)])
    elif str(type(len_srt)) == "<class 'tuple'>":
        rand_str = "".join([random.choice(chr_str) for _ in range(random.randint(*len_srt))])
    else:
        assert False, f"Указанна некоррктная длинна: {len_srt}"
    return rand_str


def zzuf(text, chr_seq, pr=int(random.randint(1, 100))):
    answer = int(len(text) / 100 * pr)
    rand_index = [random.choice([i for i in range(len(text))]) for x in range(answer)]
    text_list = list(text)
    for i in rand_index:
        text_list[i] = random.choice(chr_seq)
    fuzz_text = ''.join(text_list)
    return fuzz_text


def str_in_email(text):
    assert len(text) >= 5, f'В тексте должно быть минимум 5 символов, два из них будут заменены на "@" и "."'
    list_text = list(text)
    one_index = random.randint(1, len(text[1:-3]))
    two_index = random.randint(one_index + 2, len(text[:-2]))
    for i, j in zip(["@", "."], [one_index, two_index]):
        list_text[j] = i
    return "".join(list_text)


def str_in_access_token(text):
    assert len(text) >= 5, f'В тексте должно быть минимум 7 символов, три из них будут заменены на "."'
    list_text = list(text)
    one_index = random.randint(1, len(text[1:-3]))

    two_index = random.randint(one_index + 2, len(text[:-2]))

    for i in [one_index, two_index]:
        list_text[i] = "."
    return "".join(list_text)


def str_in_access_token_one_dots(text):
    assert len(text) >= 3, f'В тексте должно быть минимум 3 символов, три из них будут заменены на "."'
    list_text = list(text)
    one_index = random.randint(1, len(text[1:-1]))
    list_text[one_index] = "."
    return "".join(list_text)


def str_in_access_token_four_dots(text):
    assert len(text) >= 9, f'В тексте должно быть минимум 9 символов, три из них будут заменены на "."'
    list_text = list(text)
    one_index = random.randint(1, len(text[1:-7]))
    two_index = random.randint(one_index + 2, len(text[:-6]))
    thrid_index = random.randint(two_index + 2, len(text[:-4]))
    fourth_index = random.randint(thrid_index + 2, len(text[:-2]))
    for i in [one_index, two_index, thrid_index, fourth_index]:
        list_text[i] = "."
    return "".join(list_text)


def str_in_mac(text):
    return "-".join([text[i:i + 2] for i in range(0, len(text), 2)])


def str_in_hash(text):
    return " ".join(text)


def str_in_id(text):
    return " ".join([text[i:i + 3] for i in range(0, len(text), 3)])


def create_empty_field_in_list(lst):
    res = []
    for i in range(len(lst)):
        l = lst.copy()
        l[i] = chr(0)
        res.append(tuple(l))
    return res


# print(string.ascii_lowercase)
# print(string.ascii_letters)
# print(string.ascii_uppercase)
# print(string.digits)
# print(string.octdigits)
# print(string.whitespace)
# print(string.punctuation)
# print(string.printable)
# print(string.hexdigits)

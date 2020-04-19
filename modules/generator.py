import random


def create_sequence(*args):
    sequence = []
    for i in args:
        x, y = i
        sequence = sequence + [chr(i) for i in range(x, y)]
    return sequence


def gen_rand_sting(chr_str, len_srt):
    # print(f"test test:  {random.randint(*len_srt)}")
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
    assert len(text) >= 5, f'В тесте должно быть минимум 5 символов, два из них будут заменены на "@" и "."'
    list_text = list(text)
    one_index = random.randint(1, len(text[1:-3]))
    two_index = random.randint(one_index + 2, len(text[:-2]))
    for i, j in zip(["@", "."], [one_index, two_index]):
        list_text[j] = i
    return "".join(list_text)

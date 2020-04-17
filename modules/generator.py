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


# a = 9
# a = (4,9)

[print(gen_rand_sting("fsdfsdfsd", (4, 9))) for i in range(30)]

FLAGS_VALID = []
FLAGS_VALID_ARGUMENT = ["time"]


def argparse(text):
    args = text.split(' ')

    flags = set()
    arguments = dict()

    text = []

    for arg in range(len(args)):
        if args[arg - 1].startswith('--'):
            if args[arg - 1][2:] in FLAGS_VALID_ARGUMENT:
                continue
        if args[arg].startswith('--'):
            flag = args[arg][2:]
            if flag not in FLAGS_VALID and flag not in FLAGS_VALID_ARGUMENT:
                continue
            if flag in FLAGS_VALID_ARGUMENT:
                arguments[flag] = args[arg + 1]
            else:
                flags.add(flag)
            continue
        text.append(args[arg])

    return ' '.join(text), flags, arguments

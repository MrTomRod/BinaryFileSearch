import string
import subprocess
import random


def sort_bash(lines: [str], field_sep_arg: str):
    with open('/tmp/file.txt', 'wb') as f:
        f.write('\n'.join(lines).encode())
        f.flush()
        subprocess.run(
            f"sort --key=1,1 --field-separator={field_sep_arg} --output=/tmp/test_file.txt.sorted /tmp/file.txt",
            env={'LC_ALL': 'C'},
            shell=True,
            universal_newlines=True
        )
        with open('/tmp/test_file.txt.sorted', 'r') as f:
            res = f.read().strip('\n').split('\n')
    return res


def sort_python(lines: [str], sep: str):
    return sorted(lines, key=lambda x: x.split(sep)[0])


def generate_random_strings(sep: str, size: int):
    alphabet = ('\t¨\'azAZ049èèéöü°øÃÃÃ¬Ã²Ã¹Ã§@àèìòùç🤔' + string.punctuation)

    if sep in alphabet:
        alphabet = alphabet.replace(sep, '')

    # create a list of random strings of random length
    random_strings = [
        ''.join(random.choices(alphabet, k=random.randint(1, 10)))
        + sep
        + ''.join(random.choices(alphabet, k=random.randint(1, 5)))
        for _ in range(size)
    ]

    return random_strings


def check_equality(bash_sorted: [str], python_sorted: [str], sep: str):
    """
    Check if the two lists are equal. If not, print the first lines that are different.
    """
    # Print the first lines that are different
    for i, (bash_line, python_line) in enumerate(zip(bash_sorted, python_sorted)):
        if bash_line.split(sep)[0] != python_line.split(sep)[0]:
            # show surrounding lines
            for j in range(max(0, i - 5), min(i + 5, len(bash_sorted))):
                msg = '!' if bash_sorted[j] != python_sorted[j] else ' '
                print(f"{j}{msg}\tbash:   {repr(bash_sorted[j])}")
                print(f" {msg}\tpython: {repr(python_sorted[j])}")
            raise Exception(f'Lists are not the same! Error on line {i}')
    print(f"Lists are equal! Length: {len(bash_sorted)}")


# test with different separators
for sep, field_sep_arg in [
    (',', ','),
    ('\t', "$'\t'")
]:
    print(f"Testing with {sep=} and {field_sep_arg=}")
    random_strings = generate_random_strings(sep, 100_000)
    # sort the list with bash and python
    bash_sorted = sort_bash(random_strings, field_sep_arg)
    python_sorted = sort_python(random_strings, sep=sep)
    # check if the two lists are equal
    check_equality(bash_sorted, python_sorted, sep)

#
# This utility helps to find the common lines between two given files
#
# File1: This
#        is
#        a
#        great
#        match
#
# File2: The
#        match
#        is
#        great
#
# Output: great
#         match
#         is
#
def find_common_lines():
    with open("file1.txt", "r") as ins1:
        set1 = set()
        for line in ins1:
            set1.add(line)

    with open("file2.txt", "r") as ins2:
        set2 = set()
        for line in ins2:
            set2.add(line)

    for item in (set1 & set2):
        print item,


def main():
    find_common_lines()


if __name__ == '__main__':
    main()

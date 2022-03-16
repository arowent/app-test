def get_result(phrases: tuple) -> str:
    line = []
    for i in phrases:
        if 'right' in i:
            line.append(i.replace('right', 'left'))
        else:
            line.append(i)
    return ",".join(line)


if __name__ == '__main__':
    print('Example:')
    print(get_result(("left", "right", "left", "stop")))

    # #These "asserts" using only for self-checking and not necessary for auto-testing
    assert get_result(("left", "right", "left", "stop")) == "left,left,left,stop", "All to left"
    assert get_result(("bright aright", "ok")) == "bleft aleft,ok", "Bright Left"
    assert get_result(("brightness wright",)) == "bleftness wleft", "One phrase"
    assert get_result(("enough", "jokes")) == "enough,jokes", "Nothing to replace"
    print("Coding complete? Click 'Check' to review your tests and earn cool rewards!")

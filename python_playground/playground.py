from collections import deque


def decodeString(s: str) -> str:
    stack = deque()
    curr_n = 0
    curr_str = ""

    for c in s:
        if c.isdigit():
            curr_n += int(c)
        elif c == "[":
            stack.append(curr_str)
            stack.append(curr_n)
            curr_n = 0
            curr_str = ""
        elif c == "]":
            num = stack.pop()
            prev_str = stack.pop()
            curr_str = prev_str + num * curr_str
        else:
            curr_str += c
        print(stack)
        print(curr_n)
        print(curr_str)

    return curr_str


decodeString("3[a]2[bc]")

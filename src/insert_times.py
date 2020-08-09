from api_stuff import PGN

def run() -> None:

    def parens_at_start(token: str) -> int:
        for i, ch in enumerate(token):
            if ch not in "({":
                return i
        return len(token)
            
    def parens_at_end(token: str) -> int:
        for i in range(len(token)):
            if token[-i - 1] not in ")}":
                return i
        return len(token)
    
    annotated = PGN(open(input("Enter the annotated file name:\n")).read())
    timed = PGN(open(input("Enter the file name with times:\n")).read()).game.split()
    i = 1
    answer = ""
    in_parens = 0
    for j, token in enumerate(annotated.game.split()):
        answer += token + " "
        if token[-1] in ")}":
            in_parens -= parens_at_end(token)
            continue
        if token[0] in "({":
            in_parens += parens_at_start(token)
        if token[0].isdigit():
            continue
        while token[-1] in "?!":
            token = token[:-1]
        if in_parens == 0:
            answer += timed[i + 1] + " " + timed[i + 2] + " "
            i += 4
    annotated.game = answer
    print(annotated.pgn())

def remove_parens(pgn: str) -> str:
    answer = ""
    in_parens = 0
    for ch in pgn:
        if ch == "(":
            in_parens += 1
        elif ch == ")":
            in_parens -= 1
        else:
            if in_parens == 0:
                answer += ch
    return answer

if __name__ == "__main__":
    run()

import urllib.request

class PGN:
    
    def __init__(self, raw: str):
        raw = raw.split("\n")
        self.tags = {}
        for line in raw:
            if line.startswith("[Event "):
                self.tags["Event"] = line[8:-2]
            elif line.startswith("[Site "):
                self.tags["Site"] = line[7:-2]
            elif line.startswith("[Date "):
                self.tags["Date"] = line[7:-2]
            elif line.startswith("[Round "):
                self.tags["Round"] = line[8:-2]
            elif line.startswith("[Termination "):
                self.tags["Termination"] = line[14:-2]
            elif line.startswith("[ECO "):
                self.tags["ECO"] = line[6:-2]
            elif line.startswith("[Variant "):
                self.tags["Variant"] = line[10:-2]
            elif line.startswith("[Opening "):
                self.tags["Opening"] = line[10:-2]
            elif line.startswith("[Annotator "):
                self.tags["Annotator"] = line[12:-2]
            elif line.startswith("[White "):
                self.tags["White"] = line[8:-2]
            elif line.startswith("[Black "):
                self.tags["Black"] = line[8:-2]
            elif line.startswith("[Result "):
                self.tags["Result"] = line[9:-2]
            elif line.startswith("[WhiteElo "):
                self.tags["WhiteElo"] = line[11:-2]
            elif line.startswith("[BlackElo "):
                self.tags["BlackElo"] = line[11:-2]
            elif line.startswith("[TimeControl "):
                self.tags["TimeControl"] = line[14:-2]
            elif line.startswith("[Link "):
                self.tags["Link"] = line[7:-2]
            elif not line.startswith("["):
                if "game" in self.__dict__:
                    self.game += line + "\n"
                else:
                    self.game = line + "\n"

    def pgn(self) -> str:
        return "\n".join(f"[{k} \"{v}\"]" for k, v in self.tags.items()) + "\n\n" + self.game

def get_most_recent_game(username: str, year: str, month: str) -> PGN:
    url = "https://api.chess.com/pub/player/{}/games/{}/{}/pgn".format(username, year, month)
    response = urllib.request.urlopen(url)
    pgns = response.read().decode(encoding = 'utf-8')
    pgn = pgns[:pgns.find("[Event ", 1)]
    return PGN(pgn)

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

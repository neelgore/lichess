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

def get_chesscom_games(username: str, year: str, month: str) -> [PGN]:
    url = "https://api.chess.com/pub/player/{}/games/{}/{}/pgn".format(username, year, month)
    response = urllib.request.urlopen(url)
    pgns = response.read().decode(encoding = 'utf-8')
    answer = []
    while pgns:
        if "[Event" in pgns[1:]:
            end = pgns.find("[Event ", 1)
            answer.append(PGN(pgns[:end]))
            pgns = pgns[end:]
        else:
            answer.append(PGN(pgns))
            break
    return answer

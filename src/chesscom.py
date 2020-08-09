from api_stuff import PGN, get_chesscom_games
from datetime import datetime


def get_recent_tpr(username: str, games: int, time_control: str):

    def tpr_of_game(pgn: PGN, username: str) -> int:
        if pgn.tags["White"] == username:
            if pgn.game.rstrip("\n").endswith("1/2-1/2"):
                return int(pgn.tags["BlackElo"])
            elif pgn.game.rstrip("\n").endswith("1-0"):
                return int(pgn.tags["BlackElo"]) + 400
            else:
                return int(pgn.tags["BlackElo"]) - 400
        else:
            if pgn.game.rstrip("\n").endswith("1/2-1/2"):
                return int(pgn.tags["WhiteElo"])
            elif pgn.game.rstrip("\n").endswith("0-1"):
                return int(pgn.tags["WhiteElo"]) + 400
            else:
                return int(pgn.tags["WhiteElo"]) - 400

        
    now = str(datetime.now())
    pgns = get_chesscom_games(username, now[0:4], now[5:7])
    count = 0
    elo_sum = 0
    for pgn in pgns:
        if pgn.tags["TimeControl"] == time_control:
            count += 1
            elo_sum += tpr_of_game(pgn, username)
            if count == games: break
    return elo_sum/count
            
def run():
    print("TPR is:", get_recent_tpr(input("chess.com username:\n"), int(input("number of games:\n")), input("time control:\n")))

if __name__ == "__main__":
    run()

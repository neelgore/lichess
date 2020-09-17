from api_stuff import PGN, get_chesscom_games
from datetime import datetime


def get_recent_tpr(username: str, games: int, time_control: str):

    def tpr_of_game(pgn: PGN, username: str) -> (int, int):
        if pgn.tags["White"] == username:
            if pgn.tags["Result"] == "1/2-1/2":
                return (int(pgn.tags["BlackElo"]), 0)
            elif pgn.tags["Result"] == "1-0":
                return (int(pgn.tags["BlackElo"]) + 400, 1)
            else:
                return (int(pgn.tags["BlackElo"]) - 400, -1)
        else:
            if pgn.game.rstrip("\n").endswith("1/2-1/2"):
                return (int(pgn.tags["WhiteElo"]), 0)
            elif pgn.game.rstrip("\n").endswith("0-1"):
                return (int(pgn.tags["WhiteElo"]) + 400, 1)
            else:
                return (int(pgn.tags["WhiteElo"]) - 400, -1)

        
    now = str(datetime.now())
    pgns = get_chesscom_games(username, now[0:4], now[5:7])
    if now[5:7] != "01":
        pgns += get_chesscom_games(username, now[0:4], "0" + str(int(now[5:7]) - 1))
    else:
        pgns += get_chesscom_games(username, str(int(now[0:4]) - 1), "12")
    count = 0
    elo_sum = 0
    wins = 0
    losses = 0
    for pgn in pgns:
        if pgn.tags["TimeControl"] == time_control:
            if count == 0:
                last = pgn.tags["White"] if pgn.tags["Black"] == username else pgn.tags["Black"]
            count += 1
            result = tpr_of_game(pgn, username)
            elo_sum += result[0]
            if result[1] == 1:
                wins += 1
            elif result[1] == -1:
                losses += 1
            if count == games: break
    draws = games - wins - losses
    return (elo_sum/count, wins, draws, losses, last)
            
def run():
    answer = get_recent_tpr(input("chess.com username:\n"), int(input("number of games:\n")), input("time control:\n"))
    print("Last game opponent: " + answer[4])
    print("Performance rating is:", round(answer[0]))
    print(f"{answer[1]}W {answer[2]}D {answer[3]}L")

if __name__ == "__main__":
    run()

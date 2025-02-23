class Player:

    def __init__(self, player_name, team_name):
        self.player_name = player_name
        self.xp = 50
        self.team_name = team_name

    def introduce(self):
        print(f"Hello I'm {self.player_name} and I play for {self.team_name}")

class Team:

    def __init__(self, team_name):
        self.team_name = team_name
        self.players = []

    def add_player(self, player_name):
        new_player = Player(player_name, self.team_name)
        self.players.append(new_player)

    def introduce_players(self):
        for player in self.players:
            player.introduce()

    def list_players_by_name(self):
        players_name = []
        for player in self.players:
            players_name.append(player.player_name)
        print(f"{self.team_name} players list: {', '.join(players_name)}")

    def remove_player(self, player_name):
        remove_success = False
        for player in self.players:
            if player.player_name == player_name:
                self.players.remove(player)
                remove_success = True
                break
        if (remove_success):
            print(f"Player '{player_name}' was removed from Team '{self.team_name}'.")
        else:
            print(f"Player '{player_name}' was not found in Team '{self.team_name}'.")

    def show_total_xp(self):
        total_xp = 0
        for player in self.players:
            total_xp += player.xp
        print(f"{self.team_name}'s total xp: {total_xp}")


team_x = Team(
    "Team X"
)

team_x.add_player("nico")
team_x.add_player("mike")
team_x.add_player("olaf")
team_x.add_player("polly")
team_x.list_players_by_name()
team_x.remove_player("olaf")
team_x.remove_player("sarah")
team_x.list_players_by_name()


team_y = Team(
    "Team Y"
)

team_y.add_player("lynn")

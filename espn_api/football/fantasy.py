from espn_api.football import League
from operator import attrgetter
from collections import defaultdict

# Flatten list of team scores as they come in box_score format
class Score:
	def __init__(self, team_name, owner, score, point_differential, vs_team_name, vs_owner):
		self.team_name = team_name
		self.owner = owner
		self.score = score
		self.diff = point_differential
		self.vs = vs_team_name
		self.vs_owner = vs_owner

class Team_Awards:
	def __init__(self):
		self.awards = []
		self.total_money = 0

	# Add award to dict of teams
	def award(self, award_string, amount):
		self.awards.append(award_string)
		self.total_money += amount

	# Print all awards for each team
	def print_awards(self):
		for award in self.awards:
			print(award)
		print(f'Total money payout: {total_money}')
		print()

class Fantasy_Service:
	def __init__(self):
		# Hardcode league ID and year
		self.league = League(404665, 2024)
		self.team_awards = defaultdict(Team_Awards)
		self.scores = []
		self.weeks = [1, 2, 3, 4, 5, 6, 7]
		self.eliminated_teams = []

	def generateAwards(self):
		for team in self.league.teams:
			self.team_awards[team.team_name].append(Team_Awards())

		for week in weeks:
			# Iterating over matchups
			for matchup in self.league.box_scores(week=week):

				diff = max([matchup.home_score, matchup.away_score]) - min([matchup.home_score, matchup.away_score])
			
				# Make new list of matchups to iterate over
				self.scores.append(Score(matchup.home_team.team_name, matchup.home_team.owners[0]['firstName'], matchup.home_score, diff, matchup.away_team.team_name, matchup.away_team.owners[0]['firstName']))
				self.scores.append(Score(matchup.away_team.team_name, matchup.away_team.owners[0]['firstName'], matchup.away_score, (0-diff), matchup.home_team.team_name, matchup.home_team.owners[0]['firstName']))

			# 1) Compute highest score of the week
			highest = max(self.scores, key=attrgetter('score'))
			self.team_awards[highest.team_name].award(f'Highest weekly score ({highest.score}) +$5', 5)
			# self.award(highest.team_name, f'Highest weekly score ({highest.score}) +$5')

			# 2) Compute lowest score of the week 
			lowest = min(self.scores, key=attrgetter('score'))
			self.team_awards[lowest.team_name].award(f'Lowest weekly score ({lowest.score}) +$5', 5)
			# self.award(lowest.team_name, f'Lowest weekly score ({lowest.score}) +$5')
			
			# 3) Compute team eliminated via Survivor 
			survivor = min(self.scores, key=lambda score: score.team_name not in self.eliminated_teams)
			self.team_awards[survivor.team_name].award(f'ELIMINATED SURVIVOR ({survivor.score})', 5)
			self.eliminated_teams.append(survivor.team_name)
			# self.award(lowest.team_name, f'ELIMINATED SURVIVOR ({lowest.score})')
	
			# 4) Compute lowest scoring winner
			fort_son = min([x for x in self.scores if x.diff > 0], key=attrgetter('score'))
			self.team_awards[fort_son.team_name].award(f'Lowest scoring winner ({fort_son.score}) +$5', 5)
			# self.award(fort_son.team_name, f'Lowest scoring winner ({fort_son.score})')

			# 5) Compute largest margin of victory
			big_margin = max(self.scores, key=attrgetter('diff'))
			self.team_awards[big_margin.team_name].award(f'Beat opponent by largest margin ({big_margin.vs_owner} by {round(big_margin.diff, 2)}) + $5', 5)
			# self.award(big_margin.team_name, f'Beat opponent by largest margin ({big_margin.vs_owner} by {round(big_margin.diff, 2)}) + $5')
		
			# 6) Compute team that won with smallest margin of victory
			small_margin = min([x for x in self.scores if x.diff > 0], key=attrgetter('diff'))
			self.team_awards[small_margin.team_name].award(f'Beat opponent by slimmest margin ({small_margin.vs_owner} by {round(small_margin.diff, 2)}) +$5', 5)
			# self.award(small_margin.team_name, f'Beat opponent by slimmest margin ({small_margin.vs_owner} by {round(small_margin.diff, 2)}) +$5')

		for team_name, awards in self.team_awards.items() :
    		print(team_name)
    		awards.print_awards()

Fantasy_Service().generateAwards()

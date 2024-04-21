import random
import csv
import time
from collections import Counter

# in rounds
tournament_rounds = 4
simulations = 10

class GolfMonteCarloSimulation():    
    def run_simulation(self, ratings_file):
        start_timer = time.perf_counter()
        ratings = self.__import_ratings(ratings_file) # list of dictionaries with name, mean score and std of score: [{'name': 'Player 1', 'mean' = 0.5, 'std' = 0.5}]
        players = [item['name'] for item in ratings] # list of names: ['Player 1', 'Player 2']
        win_points = {player: 0 for player in players} # dictionary of player name and win points: {'Player 1': 0} - win points are allocated as 1/N of winners per tournament
        top_5_points = {player: 0 for player in players} # dictionary of player name and top_5 points: {'Player 1': 0} - top_5 points are allocated as remaining top 5 places available / players with tied score competing for it
        
        for x in range(simulations):
            # random scoring of tournament section
            tournament_scores = []
            for player in players:
                player_tournament_score = 0  
                player_score_mean = [rating['mean'] for rating in ratings if rating['name'] == player][0]
                player_score_std = [rating['std'] for rating in ratings if rating['name'] == player][0]
                for x in range(tournament_rounds):
                    player_random_score = random.normalvariate(player_score_mean,player_score_std)
                    player_tournament_score += player_random_score
                    
                player_tournament_result = (player, round(player_tournament_score)) # tuple with with name and tournament score: ('Player 1', 288) 
                tournament_scores.append(player_tournament_result) # list of such tuples for all players
            
            sorted_scores = sorted(tournament_scores, key=lambda x: x[1]) # tournament_scores sorted by score in ascending order
        
            # win points allocation section
            winners = self.__get_top_n_tuples(1, sorted_scores)
            for winner in winners:
                win_points[winner[0]] += (1/len(winners)) 
            
            # top 5 points allocation section                
            top_5 = self.__get_top_n_tuples(5, sorted_scores)
            score_frequencies = dict(Counter(x[1] for x in top_5))
            remaining_places = 5
            for player_result in top_5:
                if score_frequencies[player_result[1]] == 1:
                    top_5_points[player_result[0]] += 1
                    remaining_places -= 1
                elif score_frequencies[player_result[1]] < remaining_places:
                    top_5_points[player_result[0]] += 1
                    remaining_places -= 1
                    score_frequencies[player_result[1]] = score_frequencies[player_result[1]] - 1
                else:
                    top_5_points[player_result[0]] += (remaining_places / score_frequencies[player_result[1]])
            breakpoint()
                    
        win_probabilities = {k: round((v / simulations) * 100, 1) for k, v in win_points.items()} # win probabilities are calculated as win points per player / number simulations
        top_5_probabilities = {k: round((v / simulations) * 100, 1) for k, v in top_5_points.items()} # win probabilities are calculated as win points per player / number simulations
        end_timer = time.perf_counter()
        runtime = end_timer - start_timer
        self.__report_output(simulations, runtime, win_probabilities, top_5_probabilities)

    def __report_output(self, simulations, runtime, win_probabilities, top_5_probabilities):
        '''Prints win and top_5 probabilities for each player to STDOUT, together with an execution timer'''
        print(f'Execution time for {simulations} simulations: {runtime:0.2f}s')
        print('Win probabilities for each player are:')
        print(win_probabilities)
        print('\n')
        print('Top 5 probabilities for each player are:')
        print(top_5_probabilities)
        
        
    
    def __import_ratings(self, file):
        '''Given a path to a text file with rows and and columns Golfer, Mean and Standard Deviations (delimited with \t characters), it returns an in-memory object of the same'''
        output = []
        with open(file) as ratings:                                                                                          
            reader = csv.DictReader(ratings, delimiter='\t')
            for rating in reader:
                rating = dict((k.strip(), v.strip()) for k, v in rating.items())
                rating['name'] = rating.pop('Golfer')
                rating['mean'] = float(rating.pop('Mean'))
                rating['std'] = float(rating.pop('Standard deviation'))
                output.append(rating)
                
        return output # list of dictionaries with name, mean score and std of score: [{'name': 'Player 1', 'mean' = 0.5, 'std' = 0.5}]
    
    def __get_top_n_tuples(self, n, sorted_list_of_tuples):
        '''Given a sorted list of tuples, it returns all tuples for which the second element is one of the top n. If there's a tie in values, it returns more than n tuples'''
        res = [x[1] for x in sorted_list_of_tuples]
        i = res[n-1]
        output = [tup for tup in sorted_list_of_tuples if tup[1] <= i]
        
        return output

simulation = GolfMonteCarloSimulation()
simulation.run_simulation('ratings.txt')
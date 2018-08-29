import pandas
import math

# import and parse file
def parse_file(fileName):
    movies_df = pandas.read_csv(fileName)
    return movies_df.to_dict('records')

movies = parse_file('https://raw.githubusercontent.com/fivethirtyeight/data/master/bechdel/movies.csv')



# parsing data
def remove_movies_missing_data(movies):
    return list(filter(lambda movie: not math.isnan(movie['domgross_2013$']) ,movies))

parsed_movies = remove_movies_missing_data(movies)

def scale_down_movie(movie):
    result = {
        **movie,
        'budget': divide_and_round(movie['budget']),
        'budget_2013$': divide_and_round(movie['budget_2013$']),
        'domgross': divide_and_round(movie['domgross']),
        'domgross_2013$': divide_and_round(movie['domgross_2013$']),
        'intgross': divide_and_round(movie['intgross_2013$']),
        'intgross_2013$': divide_and_round(movie['intgross_2013$'])
        }
    return result
# helper function for scale down movie
def divide_and_round(num):
    return round((num / 1000000), 2)

def scale_down_movies(movies):
    return list(map(lambda el: scale_down_movie(el) ,movies))
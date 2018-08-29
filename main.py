import pandas
import math

#import and parse file
def parse_file(fileName):
    movies_df = pandas.read_csv(fileName)
    return movies_df.to_dict('records')

movies = parse_file('https://raw.githubusercontent.com/fivethirtyeight/data/master/bechdel/movies.csv')


#parsing data
def remove_movies_missing_data(movies):
    return list(filter(lambda movie: not math.isnan(movie['domgross_2013$']) ,movies))

parsed_movies = remove_movies_missing_data(movies)
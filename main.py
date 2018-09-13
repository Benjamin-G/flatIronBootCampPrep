import pandas
import math
import plotly as py
import plotly.graph_objs as go

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


# simple function to return the highest grossing movie
def highest_domestic_gross(movies):
    maxGrossMovie = max(movies, key=lambda x:x['domgross_2013$'])
    return maxGrossMovie


# consultants algorithm ans stats
def outside_consultant_predicted_revenue(budget):
    return (1.5*budget + 10)

def error_for_consultant_model(movie):
    return movie['domgross_2013$'] - outside_consultant_predicted_revenue(movie['budget_2013$'])

def rss_consultant(movies):
    return sum(list(map(lambda el: round(error_for_consultant_model(el)**2,2),movies)))

# our model
def revenue_with_year(budget, year):
    return (budget*1.1)+(year-1965)*1.5

def error_revenue_with_year(movie):
    return movie['domgross_2013$']-revenue_with_year(movie['budget_2013$'], movie['year'])

def rss_revenue_with_year(movies):
    return round(sum(list(map(lambda el: error_revenue_with_year(el)**2,movies))),2)

initial_regression_line = {'b': 0.5, 'm': 1.79}
def expected_revenue_per_budget(budget):
    return 1.79*budget + 0.5

def regression_revenue_error(m, b, movie):
    return round(movie['domgross_2013$']-(m*movie['budget']+b),2)

def b_gradient(m, b, movies):
    resultSum = 0
    for movie in movies:
        resultSum += regression_revenue_error(m, b, movie)
    return -2 * resultSum

def generate_steps(m, b, number_of_steps, movies, learning_rate):
    iterations = []
    for i in range(number_of_steps):
        iteration = step_gradient(b,m,movies,learning_rate)
        b = iteration['b']
        m = iteration['m']
        iterations.append(iteration)
    return iterations


# DATA
# set movie list to scaled down
scaled_movies = scale_down_movies(parsed_movies)
budgets = list(map(lambda movie: movie['budget_2013$'], scaled_movies))
domestic_revenues = list(map(lambda movie: movie['domgross_2013$'], scaled_movies))
titles = list(map(lambda movie: movie['title'], scaled_movies))

consultant_estimated_revenues = list(map(lambda budget: outside_consultant_predicted_revenue(budget),budgets))
internal_consultant_estimated_revenues = list(map(lambda movie: revenue_with_year(movie['budget_2013$'], movie['year']),scaled_movies))
#internal_consultant_estimated_trace = trace_values(budgets, internal_consultant_estimated_revenues, mode='markers', name = 'internal consultant estimate')

# PLOTLY outputs in seperate html files
trace1 = go.Scatter(x=budgets, y=domestic_revenues, text = titles, mode="markers", name="revenues")
trace2 = go.Scatter(x=budgets, y=consultant_estimated_revenues, text = titles, mode="lines")
trace3 = go.Scatter(x=budgets, y=internal_consultant_estimated_revenues, text = titles, mode="markers")

data=go.Data([trace1, trace2, trace3])
layout=go.Layout(title="Movies", xaxis={'title':'Budget', 'range':[0,300]}, yaxis={'title':'Revenue','range':[0,1000]}, )
figure=go.Figure(data=data, layout=layout)
py.offline.plot(figure, filename='file.html')

# New Model
years = list(map(lambda movie: movie['year'],movies))
years_and_revenues = go.Scatter(x=years, y=domestic_revenues, text = titles, mode="markers")
data1 = go.Data([years_and_revenues])
layout1 = go.Layout(title="New Model")
figure1 = go.Figure(data=data1, layout=layout1)
#py.offline.plot(figure1, filename='file1.html')
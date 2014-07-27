__author__ = 'Jus'
# toolkits
# import matplotlib.pyplot as plt
import json
# import math as mt
# import numpy as np

# def scoring_function(list1_author, list1_list2_sentiment, list1_list2_relevance, stock_tuples) - deleted
# bas_object = [ ['Company_name1-string', 'sentiment_score1-float', 'relevance_score1-float', 'stock_score1-float'],
#   ['Company_name2-string', 'sentiment_score2-float', 'relevance_score2-float', 'stock_score2-float'],
#   ...
#        ]
# My output would be a list of strings (you'll see why strings, and not floats), where each string is a score. Therefore
# each element in the list would be a score to the company it corresponds to.
# So output -> return_value = ['score_company_1-string', 'score_company_2-string', ......]
# sentiment = [-1,1]
# relevance = [0,1]
# After the normalized stock score is computed, given to me as an input, I will use whether it is
# a net positive, or net negative to see whether it agrees with the sentiment.

# In general, the more positive the score, the higher we should rank the document. As a lot of
# the ranking depends on the interval we choose to return the results in, it would be best to
# run a trial version of the scoring function and compare how each data set was scored. That would
# allow me to make modifications to the scoring function for any bugs, as required.

# In order to visualize the data and see the edge cases of our scoring function, I also decided to plot two graphs.
# The first graph is mainly a curve of the score of the companies, as calculated by the scoring function (1)
# The second graph is a plot of the stock scores over the number of companies. I will refine this graph by taking
# stock values used to compute the score, and seeing if I can get some previous data and extrapolate the future stock
# value as a fourier (next line)
# analysis combined with a sort of HMM (for which Connor already wrote some code.) =)
# Mainly, these graphs are for us, but maybe we could extend them to use ideas to plot predicted stock behavior (in
# a very elementary way), or show the accuracy of an author, and plot his accuracy vs. time, assuming he has more
# than one article. Or, if that proposal is not good, we could just plot the accuracy as a score, for each company.
# Juspreet Sandhu


def scoring_function(base_object):
    num_companies = len(base_object)
    alpha = float(.4)
    return_value = []
    stock_value_score = []
    for i in range(num_companies):
        curr_object = base_object[i]
        # if (len(curr_object) == 4):
        if curr_object[3] != 0:
            stock_value_score.append(float(curr_object[3]))
            # company_name = curr_object[0]
            sentiment_value = float(curr_object[1])
            relevance_value = float(curr_object[2])
            stock_value = float(curr_object[3])
            if (stock_value > 0 and sentiment_value > 0) or (stock_value < 0 and sentiment_value < 0):
                return_value.append(str(alpha*(sentiment_value/stock_value) + (1 - alpha)*relevance_value))
            elif (stock_value > 0 > sentiment_value) or (stock_value < 0 < sentiment_value):
                if -.5 < stock_value < .5:  # Even if the sentiment is opposite to the reality, I want to punish less
                    return_value.append(str(alpha*(sentiment_value/(2*stock_value)) + (1 - alpha)*relevance_value))
                else:
                    return_value.append(str(alpha*(sentiment_value/stock_value) + (1 - alpha)*relevance_value))
            else:
                    stock_score = "-12.5 , Available data does not fit parameters"
                    return_value.append(stock_score)
        else:
            stock_value_score.append(float(0))
            sentiment_value = float(curr_object[1])
            relevance_value = float(curr_object[2])
            beta = sentiment_value/(1 + sentiment_value)
            gamma = relevance_value/(1 + relevance_value)
            if (sentiment_value > .5) and (relevance_value > .5):
                return_value.append(str(beta + relevance_value/2))
            elif (sentiment_value > .5) and (relevance_value < .5):
                return_value.append(str(gamma + relevance_value/1.5))
            elif (sentiment_value < .5) and (relevance_value > .5):
                return_value.append(str(beta*relevance_value))
            else:
                return_value.append(str(sentiment_value*relevance_value))
    num_processed = len(return_value)
    if num_companies == num_processed:
        json_string_list = json.dumps(return_value, separators=',')
        return json_string_list
    else:
        return "Error in computing scores for DataSet !"


# x = []
# y = []


# def plotting_function1(list_scores):
#    for i in range(len(list_scores)):
#        x.append(i)
#        y.append(list_scores[i])


# plt.xlabel(' Number of Companies')
# plt.ylabel(' Scores')
# plt.plot(x, y)
# plt.show()


# def plotting_function2(list_stock_scores):
#    for i in range(len(list_stock_scores)):
#        x.append(i)
#        y.append(list_stock_scores[i])


# plt.xlabel(' Number of Companies')
# plt.ylabel(' Stock Behavior Scores')
# plt.plot(x, y)
# plt.show()

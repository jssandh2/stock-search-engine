# This file is for the purposes of calling all the necessary the functions, including the one in final_call.py, and 
# finally running the query.
__author__ = 'Jus'

import json, requests, math, csv, urllib, urllib2, datetime, logging, base64

BingKey = "jpADODPO6cElNoSZefCKhWntzIuoN27NWTN+pU0rltc"
womi = 2
time_delta = 10

def basicNewSearch(query, skip):
    username = '9adffa4f-0bb2-4a22-a308-aa2d36ba0435'
    password = 'jpADODPO6cElNoSZefCKhWntzIuoN27NWTN+pU0rltc'
    url = "https://api.datamarket.azure.com/Bing/Search/v1/News?Query=%27"+query+"%27&Market=%27en-US%27&NewsCategory=%27rt_Business%27&NewsSortBy=%27Relevance%27&$format=json&$skip="+str(skip)
    request = urllib2.Request(url)
    base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)   
    result = urllib2.urlopen(request).read()
    return result

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
        json_string_list = json.dumps(return_value)
        return json_string_list
    else:
        return "Error in computing scores for DataSet !"

def Stocks_search(company):
    with open('WIKI_tickers.csv', 'rU') as f:  # s for static
        reader = csv.reader(f, delimiter=',')
        ret_vals = []
        for row in reader:
            if company in row[1]:
                return row[0]
    with open('Stocks.csv', 'rU') as f:  # s for static
        reader = csv.reader(f, delimiter=',')
        ret_vals = []
        for row in reader:
            if company in row[2]:
                return row[1]
    return 'None'

def alpha_t(t):
    T = t/womi
    a = math.exp(-1 * T ^ 2)
    b = 1 / (math.log(t,2) + 1)
    c = 2 * math.sqrt(2 / math.pi)
    d = T ^ 2
    return a * b * c * d

def Stocks(company, date):
    url_base = "http://www.quandl.com/api/v1/datasets/"
    url_data = Stocks_search(company)
    url_settings = "?auth_token=ySxVLLUoX6Pzff6DArmm&column=4&sort_order=asc&collapse=daily&transformation=rdiff" # formating
    url_timeframe = "&trim_start=" + date  # time frame for retrieval
    ret_val = 0.0
    if url_data != 'None':
        url = url_base + url_data + url_settings + url_timeframe
        r = requests.get(url)
        result = json.loads(r.text)
        t = 1
        if result['data'] != None:
            for line in result['data']:
                ret_val = ret_val + line[1] * alpha_t(t)
                t = t + 1
    return ret_val

def Entities(url):
    url_base = 'http://access.alchemyapi.com/calls/url/URLGetRankedNamedEntities'
    url_settings_1 = '?apikey=979e3fc42bc01cce4549f93c1e5ef3311665ecc4&outputMode=json'
    url_settings_2 = '&disambiguate=1&coreference=1&quatations=1&sentiment=1&showSourceText=0'
    url_source = '&url=' + url
    r = requests.get(url_base + url_settings_1 + url_settings_2 + url_source)
    result = json.loads(r.text)
    ret_val = []
    for entity in result['entities']:
        if entity['type'] == 'Company':
            if entity['sentiment']['type'] != 'neutral':
                ret_val.append([entity['text'], entity['sentiment']['score'], entity['relevance']])
    return ret_val

def data_prep(url, date):
    ret_data = []
    e_data = Entities(url)
    for line in e_data:
        s_data = Stocks(line[0], date)
        if s_data != 0:
            ret_data.append([line[0], line[1], line[2], s_data])
    return ret_data

def date_calc(date):
    date = str(date.split('T')[0])
    date_op = datetime.date(int(date[0:4]), int(date[5:7]), int(date[8:10]))
    time_delt = datetime.timedelta(time_delta)
    return str(date_op - time_delt)

def final_call(query):
    calculated_dates = []
    data_input = []
    scores_avg = []
    ret_val = []
    news_result = basicNewSearch(query, 0)
    i = 0
    news_result_json = json.loads(news_result)
    for result in news_result_json['d']['results']:
        calculated_dates.append(date_calc(str(result['Date'])))
        data_input.append(data_prep(result['Url'], calculated_dates[i]))
        single_scores = json.loads(scoring_function(data_input[i]))
        sum_scores = 0.0
        vals = 0
        for score in single_scores:
            if score != '-12.5, Available data does not fit parameters':
                sum_scores += float(score)
                vals += 1
            else:
                continue
        if vals != 0:
            scores_avg.append(sum_scores/vals)
        else:
            scores_avg.append(0)
        temp_dict = {'Title':result['Title'], 'Url':result['Url'], 'Score':scores_avg[i]}
        ret_val.append(temp_dict)
        i += 1
    return json.dumps(ret_val)

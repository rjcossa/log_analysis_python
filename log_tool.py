#!/usr/bin/env python3
import datetime
import psycopg2

"""
This application is used to collect aggregated information from
an sql database and displaying in the terminal output
"""


def get_query_results(query):
    """
    Helper query to perform a database query towards the
    postgreSQL database
    """
    db = psycopg2.connect(database="news")
    c = db.cursor()
    c.execute(query)
    result = c.fetchall()
    db.close()
    return result


"""
The Functions below are responsible for querying the database and
formatting and printing the information collected from the SQL database
"""


def print_error_ratio_days():
    query = """select to_char(daily_requests.f_date, 'FMMonth FMDD, YYYY') as date_1,
                 round(
                 (daily_errors.error_count * 100. /
                 daily_requests.request_count)::numeric,1
                 ) as error_perc
                 from daily_requests, daily_errors
                 where daily_requests.f_date = daily_errors.f_date
                 and round(
                 (daily_errors.error_count * 100. /
                 daily_requests.request_count)::numeric,1
                 ) >= 1.0;"""
    rows = get_query_results(query)
    print("****** Biggest Error Ratio ******")
    for date, perc in rows:
        print("{} -- {}% errors".format(date, perc))
    print("\n")


def print_most_popular_authors():
        query = """select authors.name,count(articles_log.article_title) as views
                 from articles_log ,authors
                 where authors.id = articles_log.articles_author
                 group by authors.name
                 order by views desc;"""
        rows = get_query_results(query)
        print("****** Most Popular Authors ******")
        for author, views in rows:
            print("{} -- {} views".format(author, views))
        print("\n")


def print_most_viewed_articles():
    query = """select article_title,count(article_title) as views
                  from articles_log
                  group by article_title
                  order by views desc limit 3;"""
    rows = get_query_results(query)
    print("****** Most Viewed Articles ******")
    for title, views in rows:
        print("{} -- {} views".format(title, views))
    print("\n")


if __name__ == "__main__":
    print_most_viewed_articles()
    print_most_popular_authors()
    print_error_ratio_days()

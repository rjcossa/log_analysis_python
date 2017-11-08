import datetime
import psycopg2

"""
This application is used to collect aggregated information from
an sql database and displaying in the terminal output
"""


def get_most_viewed_articles():
    """
    This function is responsible for getting information about
    the most viewed articles from an sql database and returning
    a list of the most viewed articles
    """
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    # Query Execution
    c.execute("""select article_title,count(article_title) as views
                  from articles_log
                  group by article_title
                  order by views desc limit 3;""")
    rows = c.fetchall()
    db.close()
    return rows


def get_most_popular_authors():
    """
    This function is responsible for getting information about
    the most popular artists from an sql database and returning
    a list of the most popular authors
    """
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    # Query Execution
    c.execute("""select authors.name,count(articles_log.article_title) as views
                 from articles_log ,authors
                 where authors.id = articles_log.articles_author
                 group by authors.name
                 order by views;""")
    rows = c.fetchall()
    db.close()
    return rows


def big_error_ratio_days():
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    # Query Execution
    c.execute("""select daily_requests.f_date as date_1,
                 round(
                 (daily_errors.error_count * 100. /
                 daily_requests.request_count)::numeric,1
                 ) as error_perc
                 from daily_requests, daily_errors
                 where daily_requests.f_date = daily_errors.f_date
                 and round(
                 (daily_errors.error_count * 100. /
                 daily_requests.request_count)::numeric,1
                 ) >= 1.0;""")
    rows = c.fetchall()
    db.close()
    return rows

"""
The Functions below are responsible for formatting and printing
the information collected from the SQL database
"""


def print_error_ratio_days():
    print("****** Biggest Error Ratio ******")
    for row in big_error_ratio_days():
        print(row[0].strftime('%B %d,%Y') + " -- " + str(row[1]) + "% errors")
    print("\n")


def print_most_popular_authors():
    print("****** Most Popular Authors ******")
    for row in get_most_popular_authors():
        print(row[0] + " -- " + str(row[1]) + " views")
    print("\n")


def print_most_viewed_articles():
    print("****** Most Viewed Articles ******")
    for row in get_most_viewed_articles():
        print(row[0] + " -- " + str(row[1]) + " views")
    print("\n")

print_most_viewed_articles()
print_most_popular_authors()
print_error_ratio_days()

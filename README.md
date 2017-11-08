# Log Analysis Tool

This project entails a log analysis tool that works from the command line and analyses data from an SQL Database to answer a group of questions for a newspaper website

## SQL Database Structure

The SQL Database is made out of three tables:

* Log - That contains information about the hits to the website
* Authors - That contains the name and id of every authors
* Articles - That contains information about newspaper articles


## What questions are answered

The questions that are currently answered by this log analysis tool are:

* What are the three most popular articles? (Articles with the most views)
* What are the most popular artists ?
* On which days did more than 1% of requests lead to errors?



## Installation

In order to install this application you need to perform the following steps:

* Download and install [VirtualBox](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1)
* Download and install [Vagrant](https://www.vagrantup.com/downloads.html)
* Fork [this](https://github.com/udacity/fullstack-nanodegree-vm) Github Repository that has the VM Configuration
* Change Directory to the vagrant folder in the repository
* Type the command `vagrant up` to start the VM
* After the vm starts successfully type the command `vagrant ssh`
* Download `newsdata.sql` [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)
* Place `newsdata.sql` in the /vagrant/ directory which is shared with your virtual machine
* Change into the /vagrant/ directory
* Run the command `psql -d news -f newsdata.sql` to import the data into the database

The following sql commands must be executed in the  news database:

#### Log entries of the articles

```
create view articles_log as
select articles.title as article_title,
articles.author as articles_author,
articles.slug as articles_slug from articles,
(select substring(path  from 10) as post_slug
from log where path like '/article/%') as slugs
where slugs.post_slug = articles.slug;

```
#### Daily Error Count

```
create view daily_errors as
select time::date as f_date, count(*) as error_count
from log where status like '4%' or status like '5%'
group by f_date
order by error_count desc;
```

#### Daily Request Count

```
create view daily_requests
as select time::date as f_date, count(*) as request_count
from log
group by f_date
order by request_count desc;
```

## Running the application

In order to run the application it is only required to run the
log_tool.py python file

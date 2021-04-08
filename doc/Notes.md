https://habr.com/ru/post/418281/
# Engine:
- web: flask/[/webpy]
- db: tc, bdb, sqlite

# Stores:

# Settings:
- per_page
- similarity (0..1)

# Filters:
- area
- created_at
- employment
- schedule
- specializations

# Compare vacancies:
- employer.id
----
List:
- found
- page
- pages
- per_page
- items:
	- id
	- area.id|name
	- created_at
	- published_at
	- employer.id|name
	- name
	- type.id
	- snippet.requirement,responsibility (enable_snipets=true)
	- salary...
----
# DB structure

## Employer
ID: ID

## Vacancy
'''
'''
ID: ID # => URL

## Refs:
### schedule	
### experience
### employment
### specializations	specializations
====
* chk py - flake8, pep8
request example:
https://spb.hh.ru/search/vacancy?
area=2
employment=full+part+project+volunteer
schedule=flexible+remote
specialization=25.383+25.386+25.381+1.273+1.272+1.211+1.82+1.113
search_period=1
clusters=true	# false is better
no_magic=true
enable_snippets=true
items_on_page=20
....
https://spb.hh.ru/search/vacancy?st=searchVacancy&text=&specialization=6&area=2&salary=&currency_code=RUR&experience=doesNotMatter&order_by=relevance&search_period=1&items_on_page=20&no_magic=true
====
Vacancy states:
- new (empty)
- in favorite
- Я откликнулся
- Rejected by me
- Rejected by employer
- Doubled new/rejected by ...
- ?Archived
Vacancy set to:
- favorite
- reject


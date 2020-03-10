-- check how many rows were originally in the table
select count(*) from users;

insert into users 
values ('2a2b89b9-d8b3-46d9-8a84-e8c1de3c76cc','test',111111);

-- test if we successfully insert the row into the table
select count(*) from users;

-- test if we successfully delete the row inserted into the table
delete from users 
where uid = '2a2b89b9-d8b3-46d9-8a84-e8c1de3c76cc';

select count(*) from users;

-- select the most popular movie wrt genre
-- will rank by num_voted_user

select movie_title, movies.genres 
	from test.movies as movies,
	(select genres, max(num_voted_users) as num_voted_users
	from test.movies
	group by genres) a
where movies.genres = a.genres
and movies.num_voted_users = a.num_voted_users
order by movie_title
limit 5
;

-- select the highest rating movie wrt genre
-- will rank by imdb_score
select movie_title, movies.genres, movies.imdb_score
        from test.movies as movies,
        (select genres, max(imdb_score) as imdb_score
        from test.movies
        group by genres) a
where movies.genres = a.genres
and movies.imdb_score = a.imdb_score
order by movie_title
limit 5
;

-- select the highest rating movie wrt director
-- will rank by imdb_score
select movie_title, a.director_name, movies.imdb_score
        from test.movies as movies,
	test.movie2director as t2,
	(select d.did, d.director_name, max(b.imdb_score) as imdb_score
        from test.movies b, test.movie2director as c, test.directors as d where
	b.mid = c.mid and
	c.did = d.did
        group by d.did, d.director_name) as a
where movies.mid = t2.mid and
t2.did = a.did
and movies.imdb_score = a.imdb_score
order by a.imdb_score
limit 5
;

-- select the most popular movie wrt director
-- will rank by num_voted_user

select movie_title, a.director_name
        from test.movies,
	(select d.did, d.director_name, max(b.num_voted_users) as  num_voted_users
        from test.movies b, test.movie2director as c, test.directors as d where
	b.mid = c.mid and
	c.did = d.did
        group by d.did, d.director_name) as a
where movies.director_name = a.director_name
and movies.num_voted_users = a.num_voted_users
order by a.director_name
limit 5
;

-- select the highest rating movie wrt year
-- will rank by imdb_score
select movie_title, movies.title_year, movies.imdb_score
        from test.movies as movies,
        (select title_year, max(imdb_score) as imdb_score
        from test.movies
        group by title_year) a
where movies.title_year = a.title_year
and movies.imdb_score = a.imdb_score
order by a.title_year
limit 5
;

-- select the most popular movie wrt year
-- will rank by num_voted_user

select movie_title, movies.title_year
        from test.movies as movies,
        (select title_year, max(num_voted_users) as num_voted_users
        from test.movies
        group by title_year) a
where movies.title_year = a.title_year
and movies.num_voted_users = a.num_voted_users
order by a.country
limit 5
;

-- select the highest rating movie wrt country
-- will rank by imdb_score
select movie_title, movies.country, movies.imdb_score
        from test.movies as movies,
        (select country, max(imdb_score) as imdb_score
        from test.movies
        group by country) a
where movies.country = a.country
and movies.imdb_score = a.imdb_score
order by a.country
limit 5
;

-- select the most popular movie wrt country
-- will rank by num_voted_user

select movie_title, movies.country
        from test.movies as movies,
        (select country, max(num_voted_users) as num_voted_users
        from test.movies
        group by country) a
where movies.country = a.country
and movies.num_voted_users = a.num_voted_users
order by a.country
limit 5
;

-- select distinct contries within the database
select distinct country from movies
order by country
limit 5;

-- select all movies satisfying score requirements
select movie_title, genres from movies
where title_year = 2010
and country = 'USA'
and imdb_score > 8
order by movie_title
limit 5;

-- select the number of users for a specific 
-- user_name and password
select count(*) from users
where user_name = 'test'
and password = '111111';

-- insert a user into the user table if the user
-- name does not exist
insert into users
values ('74ee7bdd-68b4-4532-ad80-5fe89fa5bb3c','test1',111111)
on duplicate key update user_name = 'test1';




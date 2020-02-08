-- select the most popular movie wrt genre
-- will rank by num_voted_user

select movie_title, movies.genres 
	from movies,
	(select genres, max(num_voted_users) as num_voted_users
	from movies
	group by genres) a
where movies.genres = a.genres
and movies.num_voted_users = a.num_voted_users
;

-- select the highest rating movie wrt genre
-- will rank by imdb_score
select movie_title, movies.genres, movies.imdb_score
        from movies,
        (select genres, max(imdb_score) as imdb_score
        from movies
        group by genres) a
where movies.genres = a.genres
and movies.imdb_score = a.imdb_score
;

-- select the highest rating movie wrt director
-- will rank by imdb_score
select movie_title, movies.director_name, movies.imdb_score
        from movies,
        (select director_name, max(imdb_score) as imdb_score
        from movies
        group by director_name) a
where movies.director_name = a.director_name
and movies.imdb_score = a.imdb_score
order by a.imdb_score
;

-- select the most popular movie wrt director
-- will rank by num_voted_user

select movie_title, movies.director_name
        from movies,
        (select director_name, max(num_voted_users) as num_voted_users
        from movies
        group by director_name) a
where movies.director_name = a.director_name
and movies.num_voted_users = a.num_voted_users
;

-- select the highest rating movie wrt year
-- will rank by imdb_score
select movie_title, movies.title_year, movies.imdb_score
        from movies,
        (select title_year, max(imdb_score) as imdb_score
        from movies
        group by title_year) a
where movies.title_year = a.title_year
and movies.imdb_score = a.imdb_score
order by a.title_year
;

-- select the most popular movie wrt year
-- will rank by num_voted_user

select movie_title, movies.title_year
        from movies,
        (select title_year, max(num_voted_users) as num_voted_users
        from movies
        group by title_year) a
where movies.title_year = a.title_year
and movies.num_voted_users = a.num_voted_users
;


-- recommends top 5 movies based on most wishlisted genre 
-- order by imdb_score 
-- added

select movie_title, movies.title_year, imdb_score
        from movies where
	genre in
	(select genre, 
	 count(genre) c 
	 from wishlist group by genre
	 order by c
	 limit 1) t1
order by imdb_score limit 5
;

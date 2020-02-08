create table MOVIE_USER ( 
        color VARCHAR(6), 
        director_name VARCHAR(255), 
        num_critic_for_reviews DECIMAL(4,0),
        duration DECIMAL(4,0), 
        actor_2_name VARCHAR(255),
        gross DECIMAL(10,0), 
        genres VARCHAR(255), 
        actor_1_name VARCHAR(255),
        movie_title VARCHAR(255), 
        num_voted_users DECIMAL(8,0),
        actor_3_name VARCHAR(255),   
        plot_keywords VARCHAR(255),  
        movie_imdb_link VARCHAR(255) NOT NULL PRIMARY KEY,
        language VARCHAR(20),
        country VARCHAR (20),
        budget DECIMAL(12), 
        title_year DECIMAL(4), 
        imdb_score DECIMAL(2,1)
);

create table users (
        uid VARCHAR(36) not null primary key,
        user_name VARCHAR(200),
        password VARCHAR(200)
);

create table wishlist (
        uid VARCHAR(36) not null,
        mid VARCHAR(9) not null,
        date_created TIMESTAMP,
        primary key(uid,mid),
	foreign key (mid) references movies(mid),
	foreign key (uid) references users(uid)
);

update MOVIE_USER
set movie_imdb_link = SUBSTRING(movie_imdb_link,27,9);

create table movies like MOVIE_USER;
insert into movies select * from MOVIE_USER;

alter table movies
        change movie_imdb_link mid VARCHAR(9);

alter table movies
        drop color,
        drop num_critic_for_reviews,
        drop plot_keywords;

create table actors
( aid INT(11) NOT NULL AUTO_INCREMENT,
  actor_name VARCHAR(30) NOT NULL,
  primary key (aid)
);

create table directors
( did INT(11) NOT NULL AUTO_INCREMENT,
  director_name VARCHAR(50) NOT NULL,
  primary key (did)
);

insert into actors(actor_name)
        select * from
        ((select actor_1_name as actor_name from movies)
        union
        (select actor_2_name as actor_name from movies)
        union
        (select actor_3_name as actor_name from movies)) a;

insert into directors(director_name)
        select distinct director_name from movies;
	 
create table movie2director
(
        mid VARCHAR(9) not null,
        did INT(11) not null,
        primary key (mid,did)
);

create table movie2actor
(
        mid VARCHAR(9) not null,
        aid INT(11) not null,
        primary key (mid,aid)
);

insert into movie2director select * from
        (select distinct mid, did from
        movies, directors
        where movies.director_name = directors.director_name) l;

insert into movie2actor select * from
        (select mid, aid from
        ((select mid, actor_1_name as actor_name from movies)
        union
        (select mid, actor_2_name as actor_name from movies)
        union
        (select mid, actor_3_name as actor_name from movies)) l, actors
        where l.actor_name = actors.actor_name) m;

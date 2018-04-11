-- sqlite3 only allows one drop at a time
drop table if exists posts;
drop table if exists users;
drop table if exists bids;
drop table if exists accepted_bids;
drop table if exists notifications;
drop view if exists user_activity;

create table users (
    email char(100) primary key,
    'name' char(100) not null,
    password_hash text
);

create table posts (
    id integer primary key, -- default autoincrements, so no need to supply a value. See https://sqlite.org/autoinc.html. 
    title char(100) not null,
    'description' text not null,
    user_email char(100) not null,
    price numeric not null,
    foreign key (user_email) references users (email)
    on delete cascade
    on update cascade
);

create table accepted_bids (
    user_email char(100),
    post_id integer unique, 
    primary key (user_email, post_id),
    foreign key (user_email, post_id) references bids (user_email, post_id)
    on delete cascade
    on update cascade
);

create table bids (
    user_email char(100),
    post_id integer,
    offer numeric not null,
    primary key (user_email, post_id),
    foreign key (user_email) references users (email)
    on delete cascade
    on update cascade,
    foreign key (post_id) references posts (id)
    on delete cascade
    on update cascade
);

create table notifications (
    bidder char(100),
    post_id integer,
    primary key (bidder, post_id),
    foreign key (bidder, post_id) references bids (user_email, post_id)
    on delete cascade
    on update cascade
);

create trigger check_if_already_accepted before insert on bids
when exists (select * from accepted_bids where post_id = new.post_id) 
  begin
      select raise(FAIL, "Post has been closed.");
  end;

create trigger check_bid_own_post before insert on bids
when new.user_email = (select user_email from posts where id = new.post_id)
  begin
      select raise(FAIL, "You cannot bid on your own post.");
  end;

create trigger created_bid_notif after insert on bids
  begin
    insert into notifications values ((select name from users where email = new.user_email), new.post_id);
  end;

create view user_activity as 
with num_posts as (select count(*) post_count, user_email as poster
                   from posts group by user_email),
user_accepted_bids as (select post_id,
                      (select user_email from posts where post_id = id) as poster
                      from accepted_bids),
num_accepted_bids as (select count(*) ab_count, poster 
                      from user_accepted_bids group by poster)
select poster, post_count, 
case when ab_count is Null then 0 else ab_count end ab_count
from num_posts left natural outer join num_accepted_bids
order by (post_count + ab_count) desc;

insert into notifications
(bidder, post_id)
values
('Haroun@gmail.com', 1);

insert into users
(email, name)
values
('Barack@gmail.com', 'Barack Obama'),
('Haroun@gmail.com', 'Haroun Chahed'),
('Jeremy@gmail.com', 'Jeremy Yew'),
('Ewelina@gmail.com', 'Ewelina'),
('Geoffery@gmail.com', 'Goeffery'),
('suzan@gmail.com', 'suzan lim'),
('nathanial@yahoo.com' , 'Nathanial Mah'),
('joeyeo@yahoo.com' , 'Joe Yeo'),
('jonathanlim@gmail.com' , 'Jonathan Lim'),
('russelcrow@gmail.com' , 'Russel Crow'),
('stephenieteng@yahoo.com' , 'Stephenie Teng'),
('tiongley@yahoo.com' , 'Tion Ley'),
('isabelletan@yahoo.com' , 'Isabelle Tan'),
('xuekai@gmail.com' , 'Xue Kai'),
('abhiparikh@gmail.com' , 'Abhi Parikh'),
('gracelim@yahoo.com' , 'Grace Lim'),
('deandramuliawan@gmail.com' , 'Deandra Muliawan');

insert into posts
(id,title, description, user_email, price) -- id should not be supplied
values
(1,'football', 'adidas white football', 'Barack@gmail.com' , 10),
(2,'guitar', '2-year guitar', 'Barack@gmail.com' , 90),
(3,'microwave', 'super powerful microwave', 'Barack@gmail.com' , 30),
(4,'oven', 'oven from your dreams', 'Haroun@gmail.com' , 301),
(5,'fridge', 'smallest fridge in the world', 'Haroun@gmail.com' , 305),
(6,'tv set', 'tv with highest quality on the market!', 'Haroun@gmail.com' , 310),
(7,'headphones', 'brand new, great quality of sound', 'Jeremy@gmail.com' , 340),
(8,'water bottle', 'best bottle for the gym and sports!', 'Jeremy@gmail.com' , 360),
(9,'iPhone X', 'bought just two months ago, unused', 'Ewelina@gmail.com' , 3000),
(10,'calendar', 'make your year organised with this super calendar', 'Ewelina@gmail.com' , 31),
(11,'table', 'great design for any kitchen', 'Ewelina@gmail.com' , 420),
(12,'hp printer', 'brand new printer', 'Geoffery@gmail.com' , 430),
(13,'iTv', 'best apple tv set on the market', 'Geoffery@gmail.com' , 450),
(14,'chair set', 'milti-purpose set, for any kind of interior', 'suzan@gmail.com' , 480),
(15,'toaster', 'super powerful toaster', 'suzan@gmail.com' , 500),
(16,'oculus', 'newest tech gadet ever', 'nathanial@yahoo.com' , 530),
(17,'portable charger', 'super powerful charger for your phonw', 'nathanial@yahoo.com' , 550),
(18,'phone case', 'cse for samsung galaxy phone', 'joeyeo@yahoo.com' , 580),
(19,'samsung galaxy', 'used only for 5 months, new samsung galaxy s6', 'joeyeo@yahoo.com' , 600),
(20,'piano', 'brand new piano', 'jonathanlim@gmail.com' , 630),
(21,'flute', 'brand new flute', 'isabelletan@yahoo.com' , 650),
(22,'ski set', 'best ski set on the market', 'deandramuliawan@gmail.com' , 680),
(23,'tennis racket', 'willson, new!', 'abhiparikh@gmail.com' , 730);

insert into bids
(user_email, post_id, offer) -- accepted is 0 by default
values
('Jeremy@gmail.com', 1, 90),
('Haroun@gmail.com', 1, 90),
('Haroun@gmail.com', 2, 92),
('Haroun@gmail.com',3,32 ),
('Jeremy@gmail.com',3, 33),
('Ewelina@gmail.com',4,302 ),
('Geoffery@gmail.com',4,303 ),
('suzan@gmail.com',4,304 ),
('nathanial@yahoo.com' ,5, 306),
('joeyeo@yahoo.com' ,6, 311 ),
('jonathanlim@gmail.com' ,6, 312),
('russelcrow@gmail.com' ,7,341 ),
('stephenieteng@yahoo.com' ,7,342 ),
('tiongley@yahoo.com' ,7,343 ),
('isabelletan@yahoo.com' ,8,361 ),
('xuekai@gmail.com' ,8,362 ),
('abhiparikh@gmail.com' ,9,3001 ),
('gracelim@yahoo.com' ,9,3100 ),
('deandramuliawan@gmail.com' ,9, 3200),
('Jeremy@gmail.com', 10, 90),
('Haroun@gmail.com', 11, 490),
('Haroun@gmail.com', 12, 490),
('Barack@gmail.com', 13,460 ),
('Haroun@gmail.com',14, 490),
('Jeremy@gmail.com', 15,510 ),
('Ewelina@gmail.com',16,540 ),
('Geoffery@gmail.com',17,570 ),
('suzan@gmail.com',18,600),
('nathanial@yahoo.com',18,610),
('jonathanlim@gmail.com' ,18,630 ),
('russelcrow@gmail.com' ,18,640 ),
('stephenieteng@yahoo.com' ,18,650 ),
('tiongley@yahoo.com' ,18,660 ),
('isabelletan@yahoo.com' ,18,670 ),
('xuekai@gmail.com' ,19,680 ),
('abhiparikh@gmail.com' ,19,700 ),
('gracelim@yahoo.com' ,19,710 ),
('deandramuliawan@gmail.com' ,19,720 ),
('Geoffery@gmail.com',20,640 ),
('suzan@gmail.com',20,650 ),
('nathanial@yahoo.com' ,20,660 ),
('joeyeo@yahoo.com' ,20,670 ),
('russelcrow@gmail.com' ,20,690 ),
('stephenieteng@yahoo.com' ,20,700 ),
('tiongley@yahoo.com' ,21, 660),
('xuekai@gmail.com' ,21,680 ),
('abhiparikh@gmail.com' ,21,690 ),
('gracelim@yahoo.com' ,21,700 ),
('deandramuliawan@gmail.com' ,21,720 );

insert into accepted_bids
(user_email, post_id) -- accepted is 0 by default
values
('Jeremy@gmail.com', 1),
('Haroun@gmail.com', 2),
('Haroun@gmail.com', 3),
('Ewelina@gmail.com', 4),
('nathanial@yahoo.com', 5),
('joeyeo@yahoo.com', 6),
('russelcrow@gmail.com', 7),
('isabelletan@yahoo.com', 8),
('abhiparikh@gmail.com', 9),
('Jeremy@gmail.com', 10),
('Haroun@gmail.com', 11),
('Haroun@gmail.com', 12),
('Barack@gmail.com', 13),
('Haroun@gmail.com',14),
('Jeremy@gmail.com', 15),
('Ewelina@gmail.com', 16),
('Geoffery@gmail.com', 17),
('isabelletan@yahoo.com', 18);



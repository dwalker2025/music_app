create table Artist (
 id	        integer primary key autoincrement,
 artistName 	varchar(64) not null,
 hometown 		varchar(128),
 bio 			varchar(250)
);

create table Venue (
    id      integer primary key autoincrement,
    capacity    integer not null,
    city    varchar(64),
    state   varchar(64),
    address varchar(150),
    eventID integer not null,
        foreign key (eventID) references Event(id)
)

create table Event (
 id	        integer primary key autoincrement,
 eventName 	varchar(64) not null,
 time           datetime,
 venueID        integer not null,
        foreign key (venueID) references Venue(id)
);

create table ArtistToEvent (
	id	      integer primary key autoincrement,
 	artistID integer not null,
	eventID  integer not null,
	    foreign key (artistID) references Artist(id),
	    foreign key (eventID) references Event(id)
);
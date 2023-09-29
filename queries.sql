SELECT Event.eventName, Event.time
FROM Event
INNER JOIN Artist ON Artist.id = Artist.id
WHERE Artist.artistName = 'Drake';

SELECT Artist.artistName
FROM Artist
INNER JOIN Event ON Artist.id = Event.id
INNER JOIN Venue ON Event.venueID = Venue.id
WHERE Venue.id = 'Trey Songz';


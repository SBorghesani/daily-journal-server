CREATE TABLE `Entries` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`concept` TEXT NOT NULL,
	`entry`	TEXT NOT NULL,
	`mood_id`	INTEGER NOT NULL,
	`date`	DATE NOT NULL,
    FOREIGN KEY (`mood_id`) REFERENCES `Moods`(`id`)
);


CREATE TABLE `Moods` (
    `id`    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `mood`    TEXT NOT NULL
);

CREATE TABLE 'Tags' (
	'id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	'name' TEXT NOT NULL
);

DROP TABLE 'Entry-tags';

CREATE TABLE 'Entry_tags' (
	'id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	'entry_id' INTEGER NOT NULL,
	'tag_id' INTEGER NOT NULL,
	FOREIGN KEY ('entry_id') REFERENCES 'Entries'('id'),
	FOREIGN KEY ('tag_id') REFERENCES 'Tags'('id')
);

ALTER TABLE 'Entries' ADD 'tag_ids' VARCHAR(20) ;

INSERT INTO 'Tags' VALUES (null, 'JavaScript');
INSERT INTO 'Tags' VALUES (null, 'Python');
INSERT INTO 'Tags' VALUES (null, 'SQL');
INSERT INTO 'Tags' VALUES (null, 'Django');
INSERT INTO 'Tags' VALUES (null, 'HTML');
INSERT INTO 'Tags' VALUES (null, 'CSS');


INSERT INTO `Entries` VALUES (null, 'Javascript', 
'I learned about loops today. They can be a lot of fun.\nI 
learned about loops today. They can be a lot of fun.\nI learned about 
loops today. They can be a lot of fun.', 1, "Wed Sep 15 2021 10:10:47 ");
INSERT INTO `Entries` VALUES (null, 'Python', 
"Python is named after the Monty Python comedy group from the UK. 
I'm sad because I thought it was named after the snake", 4, "Wed Sep 15 2021 10:11:33 ");
INSERT INTO `Entries` VALUES (null, 'Python', "Why did it take so long for python to have a switch statement? 
It's much cleaner than if/elif blocks", 3, "Wed Sep 15 2021 10:13:11 ");
INSERT INTO `Entries` VALUES (null, 'Javascript', "Dealing with Date is terrible. Why do you have 
to add an entire package just to format a date. It makes no sense.", 3, "Wed Sep 15 2021 10:14:05 ");

INSERT INTO `Moods` VALUES (null, "Happy");
INSERT INTO `Moods` VALUES (null, "Sad");
INSERT INTO `Moods` VALUES (null, "Angry");
INSERT INTO `Moods` VALUES (null, "Ok");

SELECT * FROM Entries;
SELECT * FROM tags;
SELECT * FROM Entry_tags;

SELECT
	e.id,
	e.concept,
	e.entry,
	e.mood_id,
	e.date,
	e.tag_ids,
	m.id m_id,
	m.mood,
	t.id t_id,
	t.name
FROM entries e
JOIN moods m
	ON m.id = e.mood_id
JOIN Entry_tags et ON e.id = et.entry_id
JOIN Tags t ON t_id = et.tag_id
WHERE e.id = 16;

SELECT t.id, t.name
FROM Entries e
JOIN Entry_tags et on e.id = et.entry_id
JOIN Tags t on t.id = et.tag_id
WHERE e.id = 18;



CREATE TABLE `artls` (
	`title`			TEXT,
	`url`			TEXT 	NOT NULL PRIMARY KEY UNIQUE,
	`domain`		TEXT 	NOT NULL,
	`domain_url` 	TEXT	NOT NULL,
	`date`			INTEGER	NOT NULL,
	`time`			INTEGER NOT NULL
);

CREATE TABLE `artls_tags` (
	`artl_url`	INTEGER NOT NULL,
	`tag`		TEXT 	NOT NULL,
	PRIMARY KEY(artl_url,tag),
	FOREIGN KEY(`artl_url`) REFERENCES artls(url)
);
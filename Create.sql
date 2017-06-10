CREATE TABLE users (
	user_id integer(12) NOT NULL,
	username varchar(50),
	first_name varchar(50) NOT NULL,
	last_name varchar(50),
	registed TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY(user_id)
);


CREATE TABLE pictures (
	id integer PRIMARY KEY AUTOINCREMENT,
	user_id integer(12) NOT NULL,
	slide_id integer(12) NOT NULL,
	name varchar(25) NOT NULL UNIQUE,
	created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY (user_id)
      REFERENCES users(user_id)
	  ON UPDATE CASCADE
	  ON DELETE CASCADE
	FOREIGN KEY (slide_id)
	  REFERENCES slideshows(id)
	  ON UPDATE CASCADE
	  ON DELETE CASCADE
);


CREATE TABLE slideshows (
	id integer PRIMARY KEY AUTOINCREMENT,
	name varchar(50) NOT NULL,
	user_id integer(12) NOT NULL,
	private integer(1) NOT NULL DEFAULT 0,
	effect integer(1) NOT NULL DEFAULT 0,
	duration integer(10) NOT NULL DEFAULT 5,
	FOREIGN KEY (user_id)
	  REFERENCES users(user_id)
	  ON UPDATE CASCADE
	  ON DELETE CASCADE
);
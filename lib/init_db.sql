\c portofolio

CREATE TABLE users(
            user_id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            password TEXT NOT NULL,
			isCurrentUser integer,
			score integer
        );
INSERT INTO users(
	name, password, iscurrentuser, score)
	VALUES ('jcc', '123',0,0);
      
CREATE TABLE words(
            word_id SERIAL PRIMARY KEY,
            word TEXT NOT NULL,
			wasProsessed integer,
			urserId integer,
			difficulty integer
        )
        
CREATE TABLE wordsGuessed(
            wordGuessed_id SERIAL PRIMARY KEY,
            wordid integer NOT NULL,
			letter TEXT,
			guessed integer
        )
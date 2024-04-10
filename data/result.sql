CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT,
    full_name TEXT,
    first_name TEXT,
    last_name TEXT,
    headline TEXT,
    skills TEXT,
    projects_count INTEGER,
    city TEXT,
    country TEXT,
    resume_url TEXT,
    twitter_url TEXT,
    facebook_url TEXT,
    tumblr_url TEXT,
    deviantart_url TEXT,
    linkedin_url TEXT,
    instagram_url TEXT,
    pinterest_url TEXT,
    youtube_url TEXT,
    vimeo_url TEXT,
    behance_url TEXT,
    steam_url TEXT,
    sketchfab_url TEXT,
    twitch_url TEXT,
    imdb_url TEXT,
    website_url TEXT
);

CREATE TABLE software_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    icon_url TEXT,
    name TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE social_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    url TEXT,
    social_network TEXT,
    position INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE artist_urls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT,
    scrapped BOOLEAN
);

CREATE TABLE skills (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	user_id INTEGER NOT NULL,
	name text,
	FOREIGN KEY (user_id) REFERENCES users(id)
);

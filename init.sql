
CREATE TABLE IF NOT EXISTS dbupdate (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key char(40) NOT NULL,
    value text NOT NULL,
    attime timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS logs (
    ref char(40) PRIMARY KEY,
    json text NOT NULL,
    gameat timestamp NOT NULL,
    rulecode char(4) NOT NULL,
    lobby char(4) NOT NULL,
    createat timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS logs_ref_index on logs(ref);
CREATE INDEX IF NOT EXISTS logs_gameat_index on logs(gameat);
CREATE INDEX IF NOT EXISTS logs_rulecode_index on logs(rulecode);
CREATE INDEX IF NOT EXISTS logs_lobby_index on logs(lobby);
CREATE INDEX IF NOT EXISTS logs_createat_index on logs(createat);

CREATE TABLE IF NOT EXISTS logs_name (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ref char(40) NOT NULL,
    name char(40) NOT NULL,
    sex char(1) NOT NULL,
    rate float NOT NULL,
    dan char(16) NOT NULL,
    score INTEGER NOT NULL,
    point INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS logs_name_id_index on logs_name(id);
CREATE INDEX IF NOT EXISTS logs_name_ref_index on logs_name(ref);
CREATE INDEX IF NOT EXISTS logs_name_name_index on logs_name(name);

CREATE TABLE IF NOT EXISTS statistics_cache (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name char(40) NOT NULL,
    hash char(64) NOT NULL,
    json text NOT NULL,
    updated INTEGER NOT NULL DEFAULT 0,
    global boolean DEFAULT false
);

CREATE INDEX IF NOT EXISTS statistics_cache_name_index on statistics_cache(name);
CREATE INDEX IF NOT EXISTS statistics_cache_hash_index on statistics_cache(hash);

CREATE TABLE IF NOT EXISTS dbupdate (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key char(40) NOT NULL,
    value text NOT NULL,
    attime timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username char(40) NOT NULL,
    password char(64) NOT NULL,
    id_role INTEGER NOT NULL DEFAULT 0,
    des  text NOT NULL DEFAULT ""
);

CREATE INDEX IF NOT EXISTS user_username_index on user(username);
CREATE INDEX IF NOT EXISTS user_id_role_index on user(id_role);

CREATE TABLE IF NOT EXISTS role (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name char(40)
); 

CREATE INDEX IF NOT EXISTS role_name_index on role(name);

CREATE TABLE IF NOT EXISTS right (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name char(40)
);

CREATE TABLE IF NOT EXISTS roleRight (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_role INTEGER NOT NULL,
    id_right INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS roleRight_id_role_index on roleRight(id_role);
CREATE INDEX IF NOT EXISTS roleRight_id_right_index on roleRight(id_right);

CREATE TABLE IF NOT EXISTS game (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name char(128) NOT NULL,
    url char(128) NOT NULL,
    id_statue INTEGER NOT NULL DEFAULT 0,
    id_user_creator INTEGER NOT NULL,
    des text NOT NULL DEFAULT ""
);

CREATE TABLE IF NOT EXISTS gameStatue (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name char(40)
);

CREATE TABLE IF NOT EXISTS gameUser (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_game INTEGER NOT NULL,
    id_user INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS gameUser_id_game_index on gameUser(id_game);
CREATE INDEX IF NOT EXISTS gameUser_id_user_index on gameUser(id_user);

CREATE TABLE IF NOT EXISTS round (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_game INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS round_id_game_index on round(id_game);

CREATE TABLE IF NOT EXISTS roundRef (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_round INTEGER NOT NULL,
    ref char(40) NOT NULL
);

CREATE INDEX IF NOT EXISTS roundRef_id_round_index on roundRef(id_round);
CREATE INDEX IF NOT EXISTS roundRef_ref_index on roundRef(ref);

CREATE TABLE IF NOT EXISTS team (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name char(80),
    id_user_leader INTEGER,
    id_game INTEGER NOT NULL,
    des text NOT NULL DEFAULT ""
);

CREATE INDEX IF NOT EXISTS team_id_game_index on team(id_game);

CREATE TABLE IF NOT EXISTS teamUser (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_team INTEGER NOT NULL,
    id_user INTEGER NOT NULL,
    id_teamrole INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS teamUser_id_team_index on teamUser(id_team);
CREATE INDEX IF NOT EXISTS teamUser_id_user_index on teamUser(id_user);

CREATE TABLE IF NOT EXISTS teamRole (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name char(40) NOT NULL
);
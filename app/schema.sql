drop table if exists user;
create table user (
  user_id integer primary key autoincrement,
  username text not null,
  email text not null,
  pw_hash text not null
);

drop table if exists app;
create table app (
  app_id integer primary key autoincrement,
  app_token text not null,
  app_api_key text not null,
  app_package text not null
);

drop table if exists build;
create table build (
  build_id integer primary key autoincrement,
  app_id integer,
  pub_date text not null,
  version text not null,
  release_notes text not null,
  url text not null
);

drop table if exists user_apps;
create table user_apps (
  app_id integer not null,
  user_id integer not null
);

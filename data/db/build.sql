CREATE TABLE IF NOT EXISTS users (
  ReminderAuthor VARCHAR PRIMARY KEY,
  ReminderChannel NUMERIC,
  ReminderHours VARCHAR
);

CREATE TABLE IF NOT EXISTS reminders (
  ReminderTime DATE,
  InternalID VARCHAR PRIMARY KEY,
  ReminderID NUMERIC,
  ReminderText VARCHAR,
  ReminderAuthor VARCHAR,
  ReminderChannel NUMERIC
);

CREATE TABLE IF NOT EXISTS amounts (
  ReminderDate VARCHAR,
  InternalID VARCHAR PRIMARY KEY,
  ReminderAuthor VARCHAR,
  ReminderID NUMERIC,
  WaterAmount NUMERIC DEFAULT 0
);

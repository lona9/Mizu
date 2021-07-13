CREATE TABLE IF NOT EXISTS users (
  ReminderAuthor VARCHAR PRIMARY KEY,
  ReminderChannel NUMERIC,
  ReminderHours VARCHAR
);

CREATE TABLE IF NOT EXISTS reminders (
  ReminderTime DATE,
  ReminderID VARCHAR PRIMARY KEY,
  ReminderText VARCHAR,
  ReminderAuthor VARCHAR,
  ReminderChannel NUMERIC
);

CREATE TABLE IF NOT EXISTS amounts (
  ReminderDate VARCHAR,
  ReminderAuthor VARCHAR,
  AmountID VARCHAR PRIMARY KEY,
  WaterAmount NUMERIC DEFAULT 0
);

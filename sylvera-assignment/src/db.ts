import sqlite3 from 'sqlite3';
import { open, Database } from 'sqlite';

const dbPromise: Promise<Database<sqlite3.Database, sqlite3.Statement>> = open({
  filename: './sylvera-programming-task.db', // Path to SQLite database file
  driver: sqlite3.Database,
});

export default dbPromise;
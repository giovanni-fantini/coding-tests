import { Database } from 'sqlite';
import sqlite3 from 'sqlite3';

// Example model for a 'Project' entity
export interface Project {
  id: string;
  url: string;
  status: string;
  country: string;
}

// Example DAO (Data Access Object) for interacting with SQLite3
import dbPromise from '../db';

export async function getAllProjects(): Promise<Project[]> {
  const db: Database<sqlite3.Database, sqlite3.Statement> = await dbPromise;
  const rows: Project[] = await db.all('SELECT * FROM projects');
  return rows;
}

export async function getProjectById(id: string): Promise<Project> {
  const db: Database<sqlite3.Database, sqlite3.Statement> = await dbPromise;
  const row: Project = await db.all('SELECT * FROM projects WHERE id = ?', id);
  return row;
}

export async function getAllProjectsGroupedBy(group_by_column: string): Promise<Project> {
  const db: Database<sqlite3.Database, sqlite3.Statement> = await dbPromise;
  const row: Project = await db.all('SELECT * FROM projects GROUP_BY', group_by_column);
  return row;
}
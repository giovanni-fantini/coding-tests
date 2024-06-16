import { Request, Response } from 'express';
import * as project from '../models/project';

export async function getAllProjectsHandler(req: Request, res: Response): Promise<void> {
  try {
    const projects = await project.getAllProjects();
    res.json(projects);
  } catch (error) {
    console.error('Error fetching projects:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
}

export async function getProjectByIdHandler(req: Request, res: Response): Promise<void> {
  const { id } = req.params;
  try {
    const project_object = await project.getProjectById(id);
    if ( project_object ) {
      res.json(project_object);
    }
    else {
      console.error('Project not found');
      res.status(404).json({ error: 'Project not found' });
    }
  } catch (error) {
    console.error('Error fetching projects:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
}
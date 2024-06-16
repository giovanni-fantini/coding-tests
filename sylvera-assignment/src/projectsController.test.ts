// Jest test file for projectsController.ts
import request from 'supertest';
import express from 'express';
import { getAllProjectsHandler } from './controllers/projectsController';
import * as projectModel from './models/project';

const app = express();
app.use(express.json());
// app.post('/projects', createProjectHandler);
app.get('/projects', getAllProjectsHandler);
// app.get('/projects/:id', getProjectByIdHandler);
// app.put('/projects/:id', updateProjectHandler);
// app.delete('/projects/:id', deleteProjectHandler);

// Mock the database calls to avoid interaction with the real database
jest.mock('./models/project');

const mockProject = {
  id: 'cfafa6a2-6bca-45d1-9ae3-8ed7bc01d99d',
  url: 'https://registry.verra.org/app/projectDetail/VCS/4699',
  status: 'Under development',
  country: 'South Africa'
};

const mockProject2 = {
  id: 'b22abb14-9976-4b28-a0fe-51265b104d33',
  url: 'some_url',
  status: 'Live',
  country: 'Argentina'
}

describe('Projects Controller', () => {
  afterEach(() => {
    jest.clearAllMocks();
  });

  test('should get all projects', async () => {
    const response = await request(app).get('/projects');

    expect(response.status).toBe(200);
    expect(response.body).toEqual([mockProject, mockProject2]);
  });

  // test('should get a project', async () => {
  //   (projectModel.getProjectById as jest.Mock).mockResolvedValue(mockProject);

  //   const response = await request(app).get('/projects/b22abb14-9976-4b28-a0fe-51265b104d33')

  //   expect(response.status).toBe(200)
  //   expect(response)
  // }
});
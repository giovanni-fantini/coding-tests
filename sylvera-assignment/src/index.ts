import express, { Request, Response, NextFunction } from 'express';
import dbPromise from './db'; // Import SQLite3 database connection
import { getAllProjectsHandler, getProjectByIdHandler } from './controllers/projectsController';

const app = express();
const port = 3000;

// Middleware to parse JSON bodies
app.use(express.json());

// SQLite initialization
(async () => {
  const db = await dbPromise;
  // Perform any initialization queries if needed
  // Example: Run migrations if you have them
  // await db.migrate(); 
})();

// Routes
app.get('/projects', getAllProjectsHandler);
app.get('/projects/:id', getProjectByIdHandler);

// Error handling middleware
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Internal Server Error' });
});

// Start server
app.listen(port, () => {
  console.log(`Server is listening on http://localhost:${port}`);
});

GET http://localhost:3000/projects HTTP/1.1
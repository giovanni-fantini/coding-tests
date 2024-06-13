"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = __importDefault(require("express"));
const db_1 = __importDefault(require("./db")); // Import SQLite3 database connection
const projectsController_1 = require("./controllers/projectsController");
const app = (0, express_1.default)();
const port = 3000;
// Middleware to parse JSON bodies
app.use(express_1.default.json());
// SQLite initialization
(async () => {
    const db = await db_1.default;
    // Perform any initialization queries if needed
    // Example: Run migrations if you have them
    // await db.migrate(); 
})();
// Routes
app.get('/projects', projectsController_1.getAllProjectsHandler);
app.get('/projects/:id', projectsController_1.getProjectByIdHandler);
// Error handling middleware
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({ error: 'Internal Server Error' });
});
// Start server
app.listen(port, () => {
    console.log(`Server is listening on http://localhost:${port}`);
});

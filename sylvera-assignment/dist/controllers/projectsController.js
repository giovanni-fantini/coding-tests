"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.getProjectByIdHandler = exports.getAllProjectsHandler = void 0;
const project = __importStar(require("../models/project"));
async function getAllProjectsHandler(req, res) {
    try {
        const projects = await project.getAllProjects();
        res.json(projects);
    }
    catch (error) {
        console.error('Error fetching projects:', error);
        res.status(500).json({ error: 'Internal Server Error' });
    }
}
exports.getAllProjectsHandler = getAllProjectsHandler;
async function getProjectByIdHandler(req, res) {
    const { id } = req.params;
    try {
        const projectDetails = await project.getProjectById(id);
        if (projectDetails) {
            res.json(projectDetails);
        }
        else {
            res.status(404).json({ error: 'Project not found' });
        }
    }
    catch (error) {
        console.error(`Error fetching project with id ${id}:`, error);
        res.status(500).json({ error: 'Internal Server Error' });
    }
}
exports.getProjectByIdHandler = getProjectByIdHandler;

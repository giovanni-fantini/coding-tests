"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.getProjectById = exports.getAllProjects = void 0;
// Example DAO (Data Access Object) for interacting with SQLite3
const db_1 = __importDefault(require("../db"));
async function getAllProjects() {
    const db = await db_1.default;
    const rows = await db.all('SELECT * FROM projects');
    return rows;
}
exports.getAllProjects = getAllProjects;
async function getProjectById(id) {
    const db = await db_1.default;
    const row = await db.get('SELECT * FROM projects WHERE id = ?', id);
    return row;
}
exports.getProjectById = getProjectById;

import express from "express";
import { getStatus } from "../controllers/controllers.js";

const router = express.Router();

router.get("/", getStatus);

export default router;
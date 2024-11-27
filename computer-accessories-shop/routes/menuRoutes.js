const express = require('express');
const router = express.Router();
const menuController = require('../controllers/menuController');
const isLoggedIn = require('../middleware/isLoggedIn');

router.get('/Processors', isLoggedIn, menuController.getProcessors);
router.get('/Gpus', isLoggedIn, menuController.getGpus);
router.get('/Motherboards', isLoggedIn, menuController.getMotherboards);
router.get('/Monitors', isLoggedIn, menuController.getMonitors);

module.exports = router;
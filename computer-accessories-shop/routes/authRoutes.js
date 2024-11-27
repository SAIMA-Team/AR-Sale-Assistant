const express = require('express');                     //imports the express packaage
const router = express.Router();                        //creates a express router object to handle the routes related to authentication
const authController = require('../controllers/authController');                    //imports the controller logic for the auth routes

router.get('/login', authController.getLogin);                //get the login route with the imported methods               
router.get('/register', authController.getRegister);
router.post('/register', authController.registerUser);
router.post('/login', authController.loginUser);
router.get('/logout', authController.logoutUser);

module.exports = router;                //export the router object
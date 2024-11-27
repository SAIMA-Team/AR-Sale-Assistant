const express = require('express');
const router = express.Router();
const cartController = require('../controllers/cartController');
const isLoggedIn = require('../middleware/isLoggedIn');                              //imports the middleware for check user is logged in or not

router.get('/cart', isLoggedIn, cartController.getCart);                             //router for get the cart route with the modules imported
router.post('/addToCart/:itemId/:category', isLoggedIn, cartController.addToCart);   //router for add items to the cart

module.exports = router;   //exports the module
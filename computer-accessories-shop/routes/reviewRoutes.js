const express = require('express');               
const router = express.Router();
const reviewController = require('../controllers/reviewController');
const isLoggedIn = require('../middleware/isLoggedIn');                            //imports the middleware for check user is logged in or not

router.get('/Reviews', reviewController.getReviews);                              //gets the reviews route with support methods
router.post('/Reviews', isLoggedIn, reviewController.postReview);                 //route for post a review  with support methods

module.exports = router;
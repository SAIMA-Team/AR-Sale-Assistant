const Review = require('../models/Review');                           //imports the review model from the database
const User = require('../models/User');                               //imports the user model from the database

exports.getReviews = async (req, res) => {                            //exports the function for get reviews
  try {
    const allReviews = await Review.find({}).populate('user');       //find all the review objects in the database and fill the user field in each review with the relavent user information
    res.render('reviews', { reviews: allReviews });                  //render the reviews ejs template with passing the review parameter to render all reviews
  } catch (error) {
    console.error(error);                                            //error handling
    res.status(500).send('Internal Server Error');
  }
};

exports.postReview = async (req, res) => {                           //exports the function for post the reviews which the user submits
  try {
    const { review } = req.body;                                     //get the review text 
    const userId = req.user._id;                                     //get the user_id
    const newReview = await Review.create({ text: review, user: userId });               //creates a new review object in the database using the data
    const user = await User.findById(userId);
    if (!user) {                                                     //validate the user
      throw new Error('User not found');
    }
    if (!user.reviews) {                                             //initialize the user's reviews array
      user.reviews = [];
    }
    user.reviews.push(newReview);                                    //push the review to the relevent user's review array
    await user.save();
    res.redirect('/Reviews');
  } catch (error) {
    console.error(error);
    res.status(500).send('Internal Server Error');
  }
};
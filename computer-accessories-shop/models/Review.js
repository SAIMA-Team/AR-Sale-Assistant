const mongoose = require('mongoose');                      //imports the mogoose package

const reviewSchema = new mongoose.Schema({                 //creates the schema for reviews model
  text: String,
  user: { type: mongoose.Schema.Types.ObjectId, ref: 'User' },      //populate the user field with the relevant user data that caused to the review
  createdAt: { type: Date, default: Date.now },
});

const Review = mongoose.model('Review', reviewSchema);     //creates the review model using the reviews schema

module.exports = Review;              //exports the review model
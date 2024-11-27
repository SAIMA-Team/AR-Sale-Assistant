const passport = require('passport');                        //imports passport package 
const User = require('../models/User');                      //imports the user model from the models directory

passport.use(User.createStrategy());                         //use passport package to create a strategy in user model

passport.serializeUser(User.serializeUser());                //stores the user data in the session using user_id
passport.deserializeUser(User.deserializeUser());            //retrives the user data from the session using user-id

module.exports = passport;                                   //exports the passport object
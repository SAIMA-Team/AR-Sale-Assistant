const passport = require('passport');                   //imports the passport PACKAGE
const User = require('../models/User');                 //imports the user database modle

exports.getLogin = (req, res) => {                      //exports the function for get the login page 
  res.render('login', { showPassword: false });         //renders the login ejs template
};

exports.getRegister = (req, res) => {                   //exports the function for get the register page      
  res.render('register');                               //renders the register ejs template
};

exports.registerUser = async (req, res) => {            //exports the function for register a new user
  try {
    const user = await User.register({ username: req.body.username }, req.body.password);     //saves the user data in the database using passport-local-mongoose package
    passport.authenticate('local')(req, res, () => {                      //authenticate the user using passport local strategy
      res.redirect('/');
    });
  } catch (error) {
    console.log(error);                                                   //error handling
    res.redirect('/register');
  }
};

exports.loginUser = (req, res) => {                     //exports the function for logs a new user    
  const user = new User({
    username: req.body.username,                        //gets the username and password from the page
    password: req.body.password,
  });
  req.login(user, (err) => {                            //passport method for logs the user in
    if (err) {
      console.log(err);
    } else {
      passport.authenticate('local')(req, res, () => {      //check if the user is authenticated using the passport local strategy and starts a new session for the user
        res.redirect('/catelog');                           //upon successfull authentication redirect the user to the catelog page
      });
    }
  });
};

exports.logoutUser = async (req, res) => {                 //exports the function for logout process
  try {
    await User.findByIdAndUpdate(req.user._id, {           //checks the user ID and clear the cart of the user
      $set: {
        gpusCart: [],
        monitorsCart: [],
        motherboardsCart: [],
        processorsCart: [],
      },
    });

    const logoutPromise = () => new Promise((resolve, reject) => {     //implements a promise to handle the logout
      req.logout((err) => {                                            //passport method for logs out the user and destroy the session
        if (err) {
          reject(err);                                                //reject the promise
        } else {
          resolve();
        }
      });
    });

    await logoutPromise();                                           //wait until the logout promise finishes
    res.redirect('/');
  } catch (error) {                                                  //error handling
    console.error('Error during logout process:', error);
    res.status(500).send('Internal Server Error');
  }
};
const session = require('express-session');  //imports the session package

//is used to manage user sessions in an Express.js application. Sessions allow you to store user data between HTTP requests, providing a way to maintain state across multiple interactions with the user.

const sessionConfig = {
  secret: process.env.SESSION_SECRET,              //secret key for session
  resave: false,                                   //resave: When set to false, this option prevents the session from being saved back to the session store if it was never modified during the request. This can reduce session store usage and improve performance.
  saveUninitialized: false,                        //saveUninitialized: When set to false, this option prevents a session that is new but not modified from being saved to the session store. This can be useful to avoid creating empty sessions and saving resources.
};

module.exports = sessionConfig;                    //exports the sessionConfig object
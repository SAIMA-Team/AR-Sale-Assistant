require('dotenv').config();                                         //imports and configure the dotenv package for environmental variables

const express = require('express');                                 //imports the express package
const bodyParser = require('body-parser');                          //imports the body-parser package(use to access the form data)
const ejs = require('ejs');                                         //imports the ejs templates package
const session = require('express-session');                         //imports the express-session middleware object for handle session
const passport = require('./utils/passportConfig');                 //imports the passportConfig object to authenticate user
const mongoose = require('./config/database');                      //imports the mongoose.connection object
const sessionConfig = require('./config/session');                  //imports the sessionConfig object

const app = express();                                              //use express to create the application(app)

app.use(express.static('public'));                                   //use a directory called public for store the static content like images
app.set('view engine', 'ejs');                                       //set the ejs templates inside the app
app.use(bodyParser.urlencoded({ extended: true }));                  //use the body parser package inside the app

app.use(session(sessionConfig));                                     //use the sessionconfig object inside the app and integrates the express-session middleware into your Express application:           

app.use(passport.initialize());                                      //initialize the passport object inside the app
app.use(passport.session());                                         //integrates Passport with the session management middleware inside the app

const authRoutes = require('./routes/authRoutes');                   //imports the router object for handle authroutes
const cartRoutes = require('./routes/cartRoutes');                   //imports the router object for handle cartroutes
const menuRoutes = require('./routes/menuRoutes');                   //imports the router object for handle menuroutes
const reviewRoutes = require('./routes/reviewRoutes');               //imports the router object for handle reviewroutes

app.use('/', authRoutes);                                            //use the router objects inside the express application to access all routes from the root route
app.use('/', cartRoutes);
app.use('/', menuRoutes);
app.use('/', reviewRoutes);

app.get('/', (req, res) => {                                         //route for render the home page
  res.render('home');
});

app.get('/catelog', (req, res) => {                                 //get the catelog page
  if (req.isAuthenticated()) {                                      // check if the user is authentiacated or not
    res.render('catelog');
  } else {
    res.redirect('/login');
  }
});

app.get('/Contacts', (req, res) => {
  res.render('Contacts');
});

const PORT = process.env.PORT || 3000;                             //initailize the local port of the app

app.listen(PORT, () => {                                           // check if the port listen to out requests
  console.log(`Server started on port ${PORT}`);
});
















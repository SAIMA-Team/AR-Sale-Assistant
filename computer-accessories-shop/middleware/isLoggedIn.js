module.exports = (req, res, next) => {   //middleware for check user is logged in or not
    if (req.isAuthenticated()) {
      return next();
    }
    res.redirect('/login');
  };
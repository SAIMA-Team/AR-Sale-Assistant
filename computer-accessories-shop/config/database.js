const mongoose = require('mongoose');  //require mongoose package


mongoose.connect(process.env.MONGO_URI, { useNewUrlParser: true, useUnifiedTopology: true })   //connect mongoose with mongodb
  .then(() => console.log('MongoDB connected'))               //error handling
  .catch((err) => console.error('MongoDB connection error:', err));

module.exports = mongoose.connection;     //exports the module 
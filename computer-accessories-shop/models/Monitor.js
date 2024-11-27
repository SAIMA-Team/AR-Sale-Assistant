const mongoose = require('mongoose');

const MonitorsSchema = new mongoose.Schema({//creates a new schema for the Monitor collection
  name: String,
  price: Number,
  image: String
});

const Monitor = mongoose.model('Monitor', MonitorsSchema);// Monitor is the name of the collection in the database

module.exports = Monitor;
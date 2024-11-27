const mongoose = require('mongoose');

const MotherboardsSchema = new mongoose.Schema({//creates a new schema for the Motherboard collection
  name: String,
  price: Number,
  image: String
});

const Motherboard = mongoose.model('Motherboard', MotherboardsSchema);// Motherboard is the name of the collection in the database

module.exports = Motherboard;
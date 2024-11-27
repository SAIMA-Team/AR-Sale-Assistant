const mongoose = require('mongoose');

const ProcessorsSchema = new mongoose.Schema({//creates a new schema for the Processor collection
  name: String,
  price: Number,
  image: String,
  cpu_cores: Number,
  threads: Number,
  base_clock: String,
  warranty: String

});

const Processor = mongoose.model('Processor', ProcessorsSchema);// Processor is the name of the collection in the database



module.exports = Processor;
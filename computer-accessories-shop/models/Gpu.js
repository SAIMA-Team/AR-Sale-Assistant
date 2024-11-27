const mongoose = require('mongoose');

const GpusSchema = new mongoose.Schema({//creates a new schema for the GPU collection
  name: String,
  price: Number,
  image: String,
  boost_clock: String,
  memory_size: String,
  memory_type: String,
  cuda_cores: Number

});

const Gpu = mongoose.model('Gpu', GpusSchema);// Gpu is the name of the collection in the database



module.exports = Gpu;
const mongoose = require('mongoose');                                //imports the mongoose package to provide MongoDB object modeling for Node.js.
const passportLocalMongoose = require('passport-local-mongoose');    //imports the passport-local-mongoose package to creaet the user model using it

const userSchema = new mongoose.Schema({
  email: String,
  password: String,
  gpusCart: [{
    itemId: { type: mongoose.Schema.Types.ObjectId, ref: 'Gpu' },   //stores the referenced document data
    name: String,
    amount: Number,
    price: Number,
  }],
  monitorsCart: [{
    itemId: { type: mongoose.Schema.Types.ObjectId, ref: 'Monitor' },//
    name: String,
    amount: Number,
    price: Number,
  }],
  motherboardsCart: [{
    itemId: { type: mongoose.Schema.Types.ObjectId, ref: 'Motherboard' },
    name: String,
    amount: Number,
    price: Number,
  }],
  processorsCart: [{
    itemId: { type: mongoose.Schema.Types.ObjectId, ref: 'Processor' },
    name: String,
    amount: Number,
    price: Number,
  }],
});

userSchema.plugin(passportLocalMongoose);

const User = mongoose.model('User', userSchema);

module.exports = User;
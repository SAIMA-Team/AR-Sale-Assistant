const Gpu = require('../models/Gpu');                            //importing the product database models
const Monitor = require('../models/Monitor');
const Motherboard = require('../models/Motherboard');
const Processor = require('../models/Processor');

exports.getProcessors = async (req, res) => {                   //exports the function for get the processor items to the page
  try {
    const processors = await Processor.find({});                //render the processors ejs template and pass the processors parameter to fill it with the processor items
    res.render('Processors', { processors });
  } catch (error) {
    console.error(error);
    res.status(500).send('Internal Server Error');
  }
};

exports.getGpus = async (req, res) => {
  try {
    const gpus = await Gpu.find({});
    res.render('Gpus', { gpus });
  } catch (error) {
    console.error(error);
    res.status(500).send('Internal Server Error');
  }
};

exports.getMotherboards = async (req, res) => {
  try {
    const motherboards = await Motherboard.find({});
    res.render('Motherboards', { motherboards });
  } catch (error) {
    console.error(error);
    res.status(500).send('Internal Server Error');
  }
};

exports.getMonitors = async (req, res) => {
  try {
    const monitors = await Monitor.find({});
    res.render('Monitors', { monitors });
  } catch (error) {
    console.error(error);
    res.status(500).send('Internal Server Error');
  }
};


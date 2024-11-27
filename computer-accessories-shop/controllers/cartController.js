const User = require('../models/User');
const Gpu = require('../models/Gpu');
const Monitor = require('../models/Monitor');
const Motherboard = require('../models/Motherboard');
const Processor = require('../models/Processor');

exports.getCart = async (req, res) => {
  try {
    const user = req.user;

    // Combine all cart items into a single array
    const allCartItems = [
      ...user.gpusCart,
      ...user.monitorsCart,
      ...user.motherboardsCart,
      ...user.processorsCart
    ].filter(item => item); // Remove any undefined or null items

    // Calculate the grand total
    const grandTotal = allCartItems.reduce((total, item) => {
      return total + (item.price * item.amount);
    }, 0);

    res.render('cart', {
      allCartItems,
      grandTotal,
      user,
    });
  } catch (error) {
    console.error(error);
    res.status(500).send('Internal Server Error');
  }
};

exports.addToCart = async (req, res) => {
  try {
    const { itemId, category } = req.params;// Get the item ID and category from the request parameters
    const user = req.user;

    console.log(`Adding item ${itemId} from category ${category} to cart for user ${user._id}`);

    let itemModel;
    switch (category) {
      case 'gpus':
        itemModel = Gpu;
        break;
      case 'monitors':
        itemModel = Monitor;
        break;
      case 'motherboards':
        itemModel = Motherboard;
        break;
      case 'processors':
        itemModel = Processor;
        break;
      default:
        console.log(`Invalid category: ${category}`);
        return res.status(400).json({ error: 'Invalid category' });
    }

    const selectedItem = await itemModel.findById(itemId);

    if (!selectedItem) {
      console.log(`Item not found: ${itemId}`);
      return res.status(404).json({ error: 'Item not found' });
    }

    // Check if the item already exists in the cart
    const existingItem = user[`${category}Cart`].find(cartItem => cartItem.itemId.equals(selectedItem._id));

    if (existingItem) {
      // If item already exists, increase the amount
      existingItem.amount += 1;
      console.log(`Increased amount of item: ${existingItem.name} to ${existingItem.amount}`);
    } else {
      // If item does not exist, add as a new entry
      const cartItem = {
        itemId: selectedItem._id,
        name: selectedItem.name,
        amount: 1,
        price: selectedItem.price,
      };
      user[`${category}Cart`].push(cartItem);
      console.log(`Item added successfully: ${JSON.stringify(cartItem)}`);
    }

    // Save the updated user cart
    await user.save();

    res.status(200).json({ message: 'Item added to cart successfully' });
  } catch (error) {
    console.error('Error in addToCart:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
};
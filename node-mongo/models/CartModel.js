const mongoose = require('mongoose');

const cartSchema = mongoose.Schema(
  {
    total: {
      type: Number,
      required: true,
      default: 0,
    },
    user: {
      type: mongoose.Schema.ObjectId,
      ref: 'User',
    },
    amount: {
      type: Number,
      required: true,
      default: 0,
    },
    category: {
        type: String,
        required: true,
        enum: ['grocery', 'electrical', 'plumbing'],
    },
    prods: [
      {
        quantity: Number,
        prod: {
            prod_id: String
        },
      },
    ],
  },
  {
    toJSON: { virtuals: true },
    toObject: { virtuals: true },
  }
);

const Cart = mongoose.model('Cart', cartSchema);
module.exports = Cart;
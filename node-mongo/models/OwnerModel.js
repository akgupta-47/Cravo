const mongoose = require('mongoose');

const ownerSchema = mongoose.Schema(
  {
    fname: {
      type: String,
      required: true,
    },
    lname: {
        type: String,
    },
    phone: {
        type: Number,
        required: true,
    },
    shop: {
        type: mongoose.Schema.ObjectId,
        ref: 'Shop',
    },
    address1: {
        type: String,
        required: true,
    },
    city: {
        type: String,
        required: true,
    },
    state: {
        type: String,
        required: true,
    },
    adhaar: {
        type: Number,
        required: true,
    }
  },
  {
    toJSON: { virtuals: true },
    toObject: { virtuals: true },
  }
);

const Owner = mongoose.model('Owner', ownerSchema);
module.exports = Owner;
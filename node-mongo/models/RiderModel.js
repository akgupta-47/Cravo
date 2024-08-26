const mongoose = require('mongoose');

const riderSchema = mongoose.Schema(
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
    adhaar: {
        type: Number,
        required: true,
    },
    driver_liscense: {
      type: Number,
      required: true,
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
    salary: {
        type: String,
        required: true,
    },
    rides: [
      {
        order: String,
        id: String
      },
    ],
  },
  {
    toJSON: { virtuals: true },
    toObject: { virtuals: true },
  }
);

const Rider = mongoose.model('Rider', riderSchema);
module.exports = Rider;
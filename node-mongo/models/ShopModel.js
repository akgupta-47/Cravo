const mongoose = require('mongoose');

const userSchema = mongoose.Schema(
  {
    name: {
      type: String,
      required: true,
    },
    phone_1: {
        type: Number,
        required: true,
    },
    phone_2: {
        type: Number,
        required: true,
    },
    email: {
        type: String,
        required: true,
    },
    address1: {
        type: String,
        required: true,
    },
    address2: {
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
    premium: {
        type: Boolean,
        default: true
    }
  },
  {
    toJSON: { virtuals: true },
    toObject: { virtuals: true },
  }
);

const User = mongoose.model('User', userSchema);
module.exports = User;
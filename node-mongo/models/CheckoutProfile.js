const mongoose = require('mongoose');

const cProfileSchema = mongoose.Schema(
  {
    name: {
      type: String,
      required: true,
    },
    type: {
        type: String,
        required: true,
        enum: ['home','work','other'],
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
    pincode: {
        type: String,
        required: true
    },
    default_payment_method: {
        type: String,
    }
  },
  {
    toJSON: { virtuals: true },
    toObject: { virtuals: true },
  }
);

const CProfile = mongoose.model('CProfile', cProfileSchema);
module.exports = CProfile;
const mongoose = require('mongoose');

const issueSchema = mongoose.Schema(
  {
    order: {
      type: String,
      required: true,
    },
    shop: {
      type: mongoose.Schema.ObjectId,
      ref: 'Shop',
    },
    user: {
        type: mongoose.Schema.ObjectId,
        ref: 'User',
    },
    description: {
        type: String,
        required: true,
    },
    category: {
        type: String,
        required: true,
        enum: ['wrong', 'incomplete', 'quality'],
    },
    status: {
        type: String,
        required: true,
        enum: ['resolved','in progress','initiated']
    },
    prods: [
        {
          prod_id: String
        },
    ],
  },
  {
    toJSON: { virtuals: true },
    toObject: { virtuals: true },
  }
);

const Issue = mongoose.model('Issue', issueSchema);
module.exports = Issue;
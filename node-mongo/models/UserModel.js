const crypto = require('crypto');
const mongoose = require('mongoose');
const validator = require('validator');
const bcrypt = require('bcryptjs');

const userSchema = new mongoose.Schema({
  name: {
    type: String,
    required: [true, 'Every User must have a name'],
    validate: [
      validator.isAlpha,
      'name should only have characters not numbers or symbols',
    ],
  },
  email: {
    type: String,
    required: [true, 'every user must have an email'],
    unique: true,
    lowercase: true,
    validate: [validator.isEmail, 'Please enter a valid email!!'],
  },
  photo: {
    type: String,
    default:
      'https://res.cloudinary.com/flyingbing/image/upload/v1631215449/defaultImage_mmxazq.png',
  },
  idd: {
    type: String,
    unique: true,
    required: true,
  },
  password: {
    type: String,
    required: [true, 'Please enter a password'],
    minlength: 8,
    // adding select: false will not show password property anytime a document is requested, until specified in the code to select the password
    select: false,
  },
  premium: {
    type: Boolean,
    default: false,
  },
  passwordConfirm: {
    type: String,
    required: [true, 'Please confirm your a password'],
    validate: {
      // This only works on SAVE
      // this is because the this keyword only points to the newley created documents
      validator: function (el) {
        return el === this.password;
      },
      message: 'password must be same',
    },
  },
  phone_1: {
    type: Number,
    required: true,
    maxlength: [10, 'The maximum length of phone number is 10 characters'],
    minlength: [10, 'The minimum length of phone number is 10 characters'],
  },
  phone_2: {
    type: Number,
    required: true,
    maxlength: [10, 'The maximum length of phone number is 10 characters'],
    minlength: [10, 'The minimum length of phone number is 10 characters'],
  },
  sex: {
    type: String,
    lowercase: true,
    default: 'other',
    enum: ['male', 'female', 'other'],
  },
  passwordChangedAt: Date,
  passwordResetToken: String,
  passwordResetExpires: Date,
  active: {
    type: Boolean,
    default: true,
    select: false,
  },
  validated: {
    type: Boolean,
    default: false,
    select: false,
  },
});

const User = mongoose.model('User', userSchema);

module.exports = User;

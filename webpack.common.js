const path = require('path');
const webpack = require('webpack');
const CleanWebpackPlugin = require('clean-webpack-plugin');
const ManifestPlugin = require('webpack-manifest-plugin');

const distPath = path.resolve(__dirname, 'app', 'static', 'dist')

module.exports = {
  entry: {
    index: './src/js/index.js',
  },
  plugins: [
    new CleanWebpackPlugin([distPath]),
    new ManifestPlugin({
      writeToFileEmit: true,
    }),
  ],
  output: {
    filename: '[name]-[hash].bundle.js',
    path: distPath,
  },
  module: {
    rules: [
      {
        enforce: 'pre',
        test: /\.jsx?$/,
        exclude: /node_modules/,
        loader: 'eslint-loader',
      },
      {
        test: /\.jsx?$/,
        exclude: /node_modules/,
        loader: 'babel-loader',
      },
      {
        test: /\.css$/,
        exclude: /node_modules/,
        use: [
          'style-loader',
          'css-loader',
        ],
      },
    ],
  },
};

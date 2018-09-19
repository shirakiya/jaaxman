const path = require('path');
const webpack = require('webpack');
const CleanWebpackPlugin = require('clean-webpack-plugin');
const ManifestPlugin = require('webpack-manifest-plugin');

const distPath = path.resolve(__dirname, 'app', 'static', 'dist')

module.exports = {
  entry: {
    app: './src/js/entry.js',
    style: './src/css/entry.js',
  },
  plugins: [
    new CleanWebpackPlugin([distPath]),
    new ManifestPlugin({
      writeToFileEmit: true,
    }),
  ],
  output: {
    filename: '[name]-[hash].js',
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
        test: /\.vue$/,
        exclude: /node_modules(?![\\/]vue-awesome[\\/])/,
        loader: 'vue-loader',
      },
      {
        test: /\.jsx?$/,
        exclude: /node_modules/,
        loader: 'babel-loader',
      },
      {
        test: /\.(sass|scss)$/,
        use: [
          'style-loader',
          'css-loader',
          'sass-loader',
        ],
      },
      {
        test: /\.css$/,
        use: [
          'style-loader',
          'css-loader',
        ],
      },
    ],
  },
  resolve: {
    alias: {
      'vue$': 'vue/dist/vue.esm.js',
    }
  },
};

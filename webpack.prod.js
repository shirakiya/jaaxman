const merge = require('webpack-merge');
const common = require('./webpack.common.js');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const UglifyJsPlugin = require('uglifyjs-webpack-plugin');

module.exports = merge.smart(common, {
  mode: 'production',
  plugins: [
    new UglifyJsPlugin(),
    new MiniCssExtractPlugin({
      filename: '[name]-[hash].css',
    }),
  ],
  module: {
    rules: [
      {
        test: /\.(sass|scss|css)$/,
        use: [
          MiniCssExtractPlugin.loader,
          'css-loader?url=false',
          'sass-loader',
        ],
      },
    ],
  },
});

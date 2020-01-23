const merge = require('webpack-merge');
const common = require('./webpack.common.js');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const TerserPlugin = require('terser-webpack-plugin');

module.exports = merge.smart(common, {
  mode: 'production',
  plugins: [
    new MiniCssExtractPlugin({
      filename: '[name]-[hash].css',
    }),
  ],
  optimization: {
    minimize: true,
    minimizer: [
      new TerserPlugin({
        parallel: true,
        sourceMap: true,
      }),
    ],
  },
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

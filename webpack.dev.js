const merge = require('webpack-merge');
const common = require('./webpack.common.js');

module.exports = merge.smart(common, {
  mode: 'development',
  devtool: 'inline-source-map',
  devServer: {
    compress: false,
    publicPath: '/assets/',
    host: '0.0.0.0',
    port: 8001,
  },
});

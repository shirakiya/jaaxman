/* global __dirname */
const path = require('path');
const CleanWebpackPlugin = require('clean-webpack-plugin');
const ManifestPlugin = require('webpack-manifest-plugin');
const VueLoaderPlugin = require('vue-loader/lib/plugin');

const distPath = path.resolve(__dirname, 'app', 'static', 'dist');

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
    new VueLoaderPlugin(),
  ],
  output: {
    filename: '[name]-[hash].js',
    path: distPath,
  },
  module: {
    rules: [
      {
        enforce: 'pre',
        test: /\.(js|vue)$/,
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
        options: {
          'presets': [
            [
              '@babel/preset-env',
              {
                targets: {
                  browsers: [
                    'last 2 versions',
                    'Chrome >= 41',
                  ],
                },
                modules: false,
                useBuiltIns: 'usage',
              },
            ],
          ],
        },
      },
      {
        test: /\.(sass|scss|css)$/,
        use: [
          'style-loader',
          'css-loader',
          'sass-loader',
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

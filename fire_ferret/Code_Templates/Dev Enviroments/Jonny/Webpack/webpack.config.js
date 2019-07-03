module.exports = {
  entry: {
    V1: "./src/v1/_v1.js"
  },
  output: {
    filename: "[name].js"
  },
  module: {
    rules: [{
      test: /\.css$/,
      use: [
        'style-loader',
        'css-loader'
      ]
    }]
  }
}
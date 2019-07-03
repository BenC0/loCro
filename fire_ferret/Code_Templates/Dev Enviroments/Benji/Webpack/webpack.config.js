const path = require('path');
const CleanWebpackPlugin = require("clean-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const UglifyJsPlugin = require("uglifyjs-webpack-plugin");
const OptimizeCSSAssetsPlugin = require("optimize-css-assets-webpack-plugin");
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;

const build_folder = "./build/"
const production_folder = "../site/locro/"

const config = {
	entry: {
		control: `${build_folder}control.js`,
		v1: `${build_folder}v1.js`
	},
	output: {
		filename: '[name].js',
		path: path.resolve(__dirname, production_folder)
	},
	mode: 'production',
	devtool: false,
	optimization: {
		minimizer: [
			new UglifyJsPlugin({
				cache: true,
				parallel: true
			  })
		],
		splitChunks: {
			chunks: 'all'
		}
	},
	module: {
		rules: [
			{
				test: /\.js$/,
				exclude: /node_modules\/(?!icarus).*/,
				use: {
					loader: 'babel-loader'
				}
			},
			{
				test: /\.scss$/,
				use: [
					MiniCssExtractPlugin.loader,
					'css-loader',
					'sass-loader',
					'postcss-loader'
				]
			}
		]
	},
	plugins: [
		new MiniCssExtractPlugin({
			filename: "[name].css",
			chunkFilename: "[name].css"
		}),
		new CleanWebpackPlugin([production_folder])
		//new BundleAnalyzerPlugin()
	]
};

module.exports = config;
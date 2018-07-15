const path = require('path');
const webpack = require('webpack');
const UglifyJsPlugin = require('uglifyjs-webpack-plugin');
const HardSourceWebpackPlugin = require('hard-source-webpack-plugin');
const ExtractTextPlugin = require('extract-text-webpack-plugin');
const { VueLoaderPlugin } = require('vue-loader');

module.exports = {
    context: __dirname,

    entry: {
        main: ['babel-polyfill', './app/static/javascript/main.js']
    },

    output: {
        path: path.resolve('./app/static/assets/'),
        filename: '[name].js',
    },

    devtool: 'cheap-eval-source-map',

    module: {
        rules: [
            {
                test: /\.vue$/,
                loader: 'vue-loader',
                options: {
                    loaders: {
                        js: 'babel-loader'
                    }
                }
            },
            {
                test: /\.js$/,
                loader: "babel-loader",
                exclude: file => {
                    /node_modules/.test(file) &&
                    !/\.vue\.js/.test(file)
                }
            },
            {
                test: /\.css$/,
                use: [
                    'vue-style-loader',
                    'css-loader'
                ]
            }
        ]
    },

    resolve: {
        alias: {
            vue: vueScript()
        }
    },

    plugins: [
        new VueLoaderPlugin(),

        // Cache processed files to reduce build time
        new HardSourceWebpackPlugin(),

        // Constant for API URL
        new webpack.DefinePlugin({
            'process.env': {
                'API_URL': apiUrl()
            }
        })
    ],

    optimization: {
        minimizer: [
            // Minimize JavaScript output
            new UglifyJsPlugin({
                sourceMap: true,
                parallel: true,
                cache: true
            })
        ]
    }
};


function vueScript() {
    return process.env.NODE_ENV === 'production'
        ? 'vue/dist/vue.min.js'
        : 'vue/dist/vue.js';
}

function apiUrl() {
    return JSON.stringify(process.env.NODE_ENV === 'production'
        ? 'https://nathanclonts.com/contact-manager/api/'
        : 'http://127.0.0.1:5000/api/'
    );
}

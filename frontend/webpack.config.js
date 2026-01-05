const Path = require("path");
const Webpack = require('webpack');
const BundleTracker = require('webpack-bundle-tracker');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

module.exports = {
    // Disable production-specific optimizations by default
    // They can be re-enabled by running the cli with `--mode=production` or making a
    // separate webpack config for production.
    mode: "development",

    // Every source path are resolved from current directory
    context: __dirname,

    // Entrypoint JS sources to build
    entry: {
        "main": "./js/main.js",
        "bundle-tiptap": "./js/bundles/tiptap.js",
        "bundle-suneditor": "./js/bundles/suneditor.js",
    },

    // Built JS files goes into sandbox staticfile directory
    output: {
        path: Path.resolve("../sandbox/static-sources/js"),
        //filename: "[name]-[contenthash].js",
        filename: "[name].js",
        publicPath: "/static/js/",
        // Ensure previous bundle builds are cleaned and do not stack forever
        clean: true,
    },

    // Modules rules
    module: {
        rules: [
            // Babel ES6 inspection watch for every JS sources changes
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: "babel-loader",
                    options: {
                        presets: ["@babel/preset-env"]
                    },
                }
            },
            {
                test: /\.css$/,
                use: [MiniCssExtractPlugin.loader, 'css-loader']
            }
        ]
    },

    // Enabled webpack plugins with their config
    plugins: [
        new BundleTracker({
            path: Path.join(__dirname, '../sandbox/static-sources'),
            filename: 'webpack-stats.json'
        }),
        new MiniCssExtractPlugin({
            filename: 'suneditor.min.css'
        })
    ],
};

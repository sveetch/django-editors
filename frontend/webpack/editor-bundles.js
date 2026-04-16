/**
 * Configuration to build editor bundles to ship in django-editors application
 */
import path from "node:path";
import { fileURLToPath } from "node:url";
import MiniCssExtractPlugin from "mini-css-extract-plugin";
import { merge } from "webpack-merge";
import base from './_base.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export default merge(base, {
    // Disable production-specific optimizations by default
    // They can be enabled by running the cli with `--mode=production` or making a
    // separate webpack config for production.
    mode: "development",

    // Every source path are resolved from current directory
    context: __dirname,

    // Entrypoint JS sources to build
    entry: {
        "bundle-tiptap": "../js/bundles/tiptap.js",
        "bundle-suneditor": "../js/bundles/suneditor.js",
        "bundle-codemirror": "../js/bundles/codemirror.js",
    },

    // Built JS files goes into sandbox staticfile directory
    output: {
        path: path.resolve(__dirname, "../../django_editors/static/js"),
        filename: "[name].js",
        publicPath: "/static/js/",
        // Ensure previous bundle builds are cleaned and do not stack forever
        clean: true,
    },

    // Enabled webpack plugins with their config
    plugins: [
        new MiniCssExtractPlugin({
            filename: "suneditor.min.css"
        })
    ],
});

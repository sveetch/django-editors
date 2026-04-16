/**
 * Configuration to build sandbox assets
 */
import path from "node:path";
import { fileURLToPath } from "node:url";
import BundleTracker from "webpack-bundle-tracker";
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
        "main": "../js/main.js",
    },

    // Built JS files goes into sandbox staticfile directory
    output: {
        path: path.resolve(__dirname, "../../sandbox/static-sources/js"),
        filename: "[name].js",
        publicPath: "/static/js/",
        // Ensure previous bundle builds are cleaned and do not stack forever
        clean: true,
    },

    // Enabled webpack plugins with their config
    plugins: [
        new BundleTracker({
            path: path.join(__dirname, "../../sandbox/static-sources"),
            filename: "webpack-stats.json"
        })
    ],
});

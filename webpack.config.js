var path = require("path");
var webpack = require("webpack");

module.exports = {
    entry: {
        "flask-example": path.join(__dirname, 'src', 'main.jsx'),
    },
    output: {
        filename: "dist/[name].js"
    },
    module: {
        loaders: [
            { 
                test: /\.jsx$/, 
                exclude: /node_modules/, 
                loader: "babel-loader", 
                query: {
                    plugins:['transform-runtime'],
                    presets:['es2015','stage-0','react']
                }
            },
            { test: /\.css$/, loader: "style!css" },
            { test: /\.scss$/, loader: "style!css!sass" },
            { test: /\.less$/, loader: "style!css!less" },
            { test: /\.(ttf|eot|svg|woff(2)?)(\?[a-z0-9\.=]+)?$/,loader: 'url?limit=100000'}
        ]
    }
};

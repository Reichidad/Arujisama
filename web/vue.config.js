const path = require('path');

module.exports = {
  assetsDir: '../static',
  publicPath: '',       // = baseURL (deprecated)
  outputDir: path.resolve(__dirname, '../arujisama_flask/app/templates'),
  runtimeCompiler: undefined,
  productionSourceMap: false,
  parallel: undefined,
  css: undefined,
  // chainWebpack: (config) => {
  //   config.plugin('html').tap((opts) => {
  //     opts[0].filename = './main.html';
  //     return opts;
  //   });
  // }
  pages: {
    main: {
      entry: "src/main.js",
      filename: "main.html"
    },
    validation: {
      entry: "src/validation/validation_main.js",
      filename: "validation.html"
    }
  }
}
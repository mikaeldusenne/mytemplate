module.exports = {
  publicPath: '{{ cookiecutter.root_url }}', // process.env.NODE_ENV === 'production' ? '/subpath/' : '/',
  assetsDir: "./static",
  outputDir: "./dist/dist/",
  devServer: {
    proxy: "http://{{ cookiecutter.project_name }}_app_1:5000"
  },
  lintOnSave: true
};

module.rules = {
  test: /\.pug$/,
  loader: "pug-plain-loader"
};

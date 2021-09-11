module.exports = {
    publicPath:  (e => e.startsWith('/')?e:'/'+e)('{{ cookiecutter.root_url }}'),
    assetsDir: "./static",
    outputDir: "./dist/",
    devServer: {
        proxy: "http://{{ cookiecutter.project_name }}_app:5000"
    },
    lintOnSave: true
};

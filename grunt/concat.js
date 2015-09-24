/**
 * Created by Stan on 05.09.2015.
 */
module.exports = {
    development: {},
    productionStyles: {
        src: [
            'app/static/dist/css/font-awesome.css',
            'app/static/dist/css/normalize.css',
            'app/static/dist/css/foundation-custom-min.css',
            'app/static/dist/css/custom.css'
        ],
        dest: 'app/static/production.css'
    },
    productionScripts: {
        src: [
            'app/static/dist/js/json2.js',
            'app/static/dist/js/jquery-1.js',
            'app/static/dist/js/underscore-min.js',
            'app/static/dist/js/backbone-min.js',
            'app/static/dist/js/foundation-custom-min.js',
            'app/static/dist/js/jquery-cookie.js',
            'app/static/dist/js/modernizr.js',
            'app/static/dist/js/placeholder.js',
            //'app/static/dist/js/upload.js',
            'app/static/dist/js/coffee.js',
            'app/static/dist/js/custom.js'
        ],
        dest: 'app/static/production.js'
    }
};
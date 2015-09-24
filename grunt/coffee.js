/**
 * Created by Stan on 05.09.2015.
 */
module.exports = {
    development: {
        options: {
            join: true,
            bare: true
        },
        files: {
            'app/static/dist/js/coffee.js': ['app/static/coffee/*.coffee']
        }
    },
    production: {
        options: {
            join: true,
            bare: true
        },
        files: {
            'app/static/dist/js/coffee.js': ['app/static/coffee/*.coffee']
        }
    }
};
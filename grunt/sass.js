/**
 * Created by Stan on 05.09.2015.
 */
module.exports = {
    development: {
        options: {
            outputStyle: 'nested',
            sourceMap: true
        },
        files: [{
            expand: true,
            cwd: 'app/static/css',
            src: ['*.css'],
            dest: 'app/static/dist/css',
            ext: '.css'
        }, {
            expand: true,
            cwd: 'app/static/sass',
            src: ['*.scss'],
            dest: 'app/static/dist/css',
            ext: '.css'
        }]
    },
    production: {
        options: {
            outputStyle: 'compressed',
            sourceMap: false
        },
        files: [{
            expand: true,
            cwd: 'app/static/css',
            src: ['*.css'],
            dest: 'app/static/dist/css',
            ext: '.css'
        }, {
            expand: true,
            cwd: 'app/static/sass',
            src: ['*.scss'],
            dest: 'app/static/dist/css',
            ext: '.css'
        }]
    }
};
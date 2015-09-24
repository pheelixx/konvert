/**
 * Created by Stan on 05.09.2015.
 */
module.exports = {
    all: {
        files: [{
            expand: true,
            cwd: 'app/static/js',
            src: '*.js',
            dest: 'app/static/dist/js/',
            ext: '.js'
        }]
    }
};
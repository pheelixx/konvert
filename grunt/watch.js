/**
 * Created by Stan on 05.09.2015.
 */
module.exports = {
    options: {
        spawn: false,
        livereload: true
    },
    scripts: {
        files: [
            'app/static/*.js'
        ],
        tasks: [
            'uglify'
        ]
    },
    styles: {
        files: [
            'app/static/css/*.scss'
        ],
        tasks: [
            'sass:development'
        ]
    }
};
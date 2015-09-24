/**
 * Created by Stan on 05.09.2015.
 */
module.exports = {
    options: {
        limit: 3
    },
    developmentFirst: [
        'clean'/*,
        'jshint'*/
    ],
    developmentSecond: [
        'sass:development',
        'coffee:development',
        'uglify'
    ],
    productionFirst: [
        'clean'/*,
        'jshint'*/
    ],
    productionSecond: [
        'sass:production',
        'coffee:production',
        'uglify'
    ],
    productionThird: [
        'concat:productionStyles',
        'concat:productionScripts'
    ],
    coffeeCompile: [
        'coffee:compltf'
    ]
};
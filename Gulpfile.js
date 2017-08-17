/**
 * Created by gaspar on 01/05/15.
 */
// File: Gulpfile.js
'use strict';

var gulp      = require('gulp'),
    wiredep   = require('wiredep').stream;



// Inyecta las librerias que instalemos vía Bower
gulp.task('wiredep', function () {
  gulp.src('./pythonizame/apps/blog/templates/*.html')
    .pipe(wiredep({
      directory: './pythonizame/static/app/lib'
    }))
    .pipe(gulp.dest('./pythonizame'));
});

// Vigila cambios que se produzcan en el código
// y lanza las tareas relacionadas
gulp.task('watch', function() {
  gulp.watch( ['wiredep']);
});


gulp.task('default', ['wiredep','watch']);

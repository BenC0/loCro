const gulp = require('gulp'),
  autoprefixer = require('gulp-autoprefixer'),
  babel = require('gulp-babel'),
  sass = require('gulp-sass'),
  runSequence = require('run-sequence'),
  Prod = '../site/locro/',
  Build = 'build/'
 
gulp.task('babel', () => {
  gulp.src([
      Build+'*.js',
      Build+'*/*.js'
    ])
    .pipe(babel({
        presets: ['env']
    }).on('error', console.error.bind(console)))
    .pipe(gulp.dest(Prod))
})

gulp.task('sass', () => {
  gulp.src([
      Build+'*.scss',
      Build+'*/*.scss'
    ])
    .pipe(sass().on('error', sass.logError))
    .pipe(autoprefixer({
        browsers: ['last 2 versions'],
        cascade: false
    }))
    .pipe(gulp.dest(Prod))
})

gulp.task('watch', ['build'], () => {
  gulp.watch(Build+'*.scss', ['sass'])
  gulp.watch(Build+'*/*.scss', ['sass'])
  gulp.watch(Build+'*.js', ['babel'])
  gulp.watch(Build+'*/*.js', ['babel'])
})

gulp.task('build', () => {
  runSequence('sass', 'babel')
})

gulp.task('default', ['build'])
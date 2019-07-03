const gulp = require('gulp')
const browserSync = require('browser-sync')
const Prod = '../site/locro/'
const Build = 'build/'

gulp.task('migrate_variations', () => {
  gulp.src([
      Build+'**.scss',
      Build+'**.js'
    ])
    .pipe(gulp.dest(Prod))
})

gulp.task('start_server', ['migrate_variations'], () => {
  browserSync.init({
    server: {
      baseDir: '../site',
      port: 3000
    }
  }),
  gulp.watch(Build+'*.scss', ['migrate_variations']).on('change', browserSync.reload);
  gulp.watch(Build+'*.js', ['migrate_variations']).on('change', browserSync.reload);
})

gulp.task('default', ['start_server'])
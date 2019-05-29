const gulp = require('gulp');
const sass = require('gulp-sass');

const compileSass = () => {
    return gulp.src('assets/scss/**/*.scss')
        .pipe(sass({
            outputStyle: 'compressed'
        }))
        .pipe(gulp.dest('app/static/css'));
};

const compileJs = () => {};

const watchSass = () => {
    gulp.watch('assets/scss/**/*.scss', compileSass);
};

const watchJs = () => {};

const compile = gulp.parallel(compileSass, compileJs);
compile.description = 'Compile Sass and JS';

const watch = gulp.parallel(watchSass, watchJs);
watch.description = 'Watch for changes to *.sass and *.js files';

// eventually might have more tasks as default, but only watch for now
gulp.task('default', gulp.parallel(watch));

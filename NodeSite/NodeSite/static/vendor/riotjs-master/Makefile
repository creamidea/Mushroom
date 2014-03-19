init:
	bower install

jshint:
	./node_modules/jshint/bin/jshint lib/*.js

riot:
	@ cat license.js > riot.js
	@ echo '(function($$) { "use strict";' >> riot.js
	@ cat lib/* >> riot.js
	@ echo '})(typeof top == "object" ? window.$$ || (window.$$ = {}) : exports);' >> riot.js

min: riot
	./node_modules/uglify-js/bin/uglifyjs riot.js --comments --mangle -o riot.min.js

test: min
	node test/node.js

.PHONY: test compare

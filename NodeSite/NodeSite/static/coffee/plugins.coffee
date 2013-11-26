# Avoid `console` errors in browsers that lack a console.
(->
    noop = () ->
      
    methods = [
        'assert', 'clear', 'count', 'debug', 'dir', 'dirxml', 'error',
        'exception', 'group', 'groupCollapsed', 'groupEnd', 'info', 'log',
        'markTimeline', 'profile', 'profileEnd', 'table', 'time', 'timeEnd',
        'timeStamp', 'trace', 'warn'
    ]
    length = methods.length;
    console = (window.console = window.console || {});

    while (length--)
        method = methods[length];

        # Only stub undefined methods.
        if !console[method]
            console[method] = noop;
    this
)();

# Place any jQuery/helper plugins in here.

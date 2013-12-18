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

  ##############################################################
  # Ajax  请求
  class Ajax
    constructor: (@url, @success, @fail) ->
    getCookie: (name) ->
        cookieValue = null
        if (document.cookie && document.cookie != '')
            cookies = document.cookie.split(';')
            length = cookies.length
            for i in [0...length]
                cookie = jQuery.trim(cookies[i])
                if cookie.substring(0, name.length+1) == (name + '=')
                    cookieValue = \
                      decodeURIComponent(cookie.substring(name.length+1))
                    break
        return cookieValue;
    csrfSafeMethod: (method) ->
        # these HTTP methods do not require CSRF protection
        (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));

    beforeSend: (xhr, settings) =>
        if (!@csrfSafeMethod(settings.type))
            xhr.setRequestHeader("X-CSRFToken", @getCookie('csrftoken'))
        return
    crossDomain: false
    type: 'POST'
    send: (data)->
      try
        $.ajax
          crossDomain: @crossDomain
          beforeSend: @beforeSend
          url: @url
          type: @type
          data: data
          success: @success
          error: @fail
      catch error
        throw error
      return
      
  class Post extends Ajax
    type: 'POST'
    send: (data)->
      super(data)
      
  class Get extends Ajax
    type: 'GET'
    send: (data)->
      super(data)
  ##############################################################
)();

# Place any jQuery/helper plugins in here.

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
  # Place any jQuery/helper plugins in here.

  ##############################################################
  # 核心组件
  ##############################################################
  # Pub/Sub 订阅/发布系统
  # 使用示例
  # 订阅
  # $.subscribe '/error', (e, error) ->
  #   alert error
  # 发布
  # $.publish '/error', [{status: 500, error: '[Ponds.save]执行失败'}]
  subpub = ($) ->
    o = $({})
    $.subscribe = ->
      o.on.apply(o, arguments);
    $.unsubscribe = ->
      o.off.apply(o, arguments);
    $.publish = ->
      o.trigger.apply(o, arguments);
  subpub $                      #启动sub/pub系统
  ############################################################## 

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
    type: 'GET'
    _success: (data) =>
      try
          data = JSON.parse(data)
          code = data.code
          definition = data.definition
          # console.log definition
          # console.log data
          if code is "-1"
            $.publish "/echo/", [{code: -1, definition: definition}]
          else
            if typeof @success is "function"
              @success(data)          
      catch error
          $.publish "/echo/", [{code: -1, definition: error || "JSON解析错误"}]
    _fail: (jqXHR, textStatus, errorThrown) =>
      # console.log arguments
      $.publish "/echo/", [{code: -1, definition: errorThrown || "通讯错误
"}]
      if typeof @fail is "function"
        @fail(jqXHR, textStatus, errorThrown)
    send: (data)->
      try
        $.ajax
          crossDomain: @crossDomain
          beforeSend: @beforeSend
          url: @url
          type: @type
          data: data
          success: @_success
          error: @_fail
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
      
  class Delete extends Ajax
    type: 'DELETE'
    send: (data) ->
      super(data)
      
  class Put extends Ajax
    type: 'PUT'
    send: (data) ->
      super(data)
  ##############################################################

  ##############################################################
  # 内建组件
  ##############################################################
  # 信息提示
  # error = {code: [:code], definition: [:definition]}
  class Echo
    constructor: (uri) ->
      @uri = uri || "/echo/"
      @$echo = $echo = $('#echo')
      $.subscribe @uri, $.proxy(@subscribe, this)
    show: (definition) ->
      $echo = @$echo
      $echo.html(definition)
      $echo.fadeIn(500)
    hide: ->
      # @$echo.hide()
      @$echo.fadeOut(1000)
    subscribe: (e, error) ->
      # alert error
      code = error.code || "unknow code"
      definition = error.definition || "unknow definition"
      @show(definition)
      setTimeout =>
        @hide()
      , 4000
      return
  ##############################################################
)();

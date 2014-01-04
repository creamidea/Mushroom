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


  # 监听hashchange事件，然后利用sub/pub系统简单的实现一个路由功能
  class Router
    # exclue: []
    constructor: (@id) ->
      
    start: ->
      # 全局简单路由信号发送器
      $(window).on "hashchange", ->
        signal = window.location.hash
        $.publish "#{signal}", [arguments]
        # console.log signal

    # 这个函数暂时没有使用，外部在食用时仍然使用的是
    # $.subscribt uri, func
    on: (uri, func)->
      $.subscribe uri, func
      

  # $(window).on "hashchange", ->
  #   console.log arguments
  
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
          # console.log data
      # try
          console.log data
          data = JSON.parse(data)
          code = data.code || "0"
          # definition = data.definition
          # console.log definition
          # console.log data
          if code is "-1"
            # $.publish "#echo/", [{code: -1, definition: definition}]
            $.publish "#echo/", [data]
          if typeof @success is "function"
            @success(data)          
      # catch error
      #     $.publish "#echo/", [{code: -1, definition: error || "JSON解析错误"}]
    _fail: (jqXHR, textStatus, errorThrown) =>
      # console.log arguments
      $.publish "#echo/", [{code: -1, definition: errorThrown || "通讯错误"}]
      console.log @fail, typeof @fail
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
  # 全局视图框架类
  class Frame
    constructor: (@templateName) ->
      # 这里面的@$el要不要做判断？
      # 后期解决，前期暂时不在任何判断是否被赋值
      @$el = $({})
      @isShow = false
    fill: (context, helper) ->
      # 填充数据，生成最终html
      # @param {object} 数据
      # @param {function} Handlebars.registerHelper
      # console.log context, @templateName
      source = $(@templateName).html()
      template = Handlebars.compile(source)
      # console.log helper
      # Handlebars.registerHelper helper.tag, helper.fun
      if $.isArray helper
        Handlebars.registerHelper h.tag, h.fun for h in helper
      else if $.isPlainObject helper
        Handlebars.registerHelper helper.tag, helper.fun
        # console.log helper
        # helper()
      @html = template(context)
      this
    render: (context, target) ->
      # @param {string} 加载到那个node里面去，如果不存在则加到自己el下面
      if !target
        @fill(context, helper)
        html = @html
        @$el.append html       #不知这里是否是原子操作
        el = $.parseHTML(html)[1] #text, li#room-1.room, text
        @$el = $(el)              #绑定元素，如果绑定错误，后面修改
      else
        @renderTo(target, context)
      this
    renderTo: (target, context, helper) ->
      # console.log typeof helper
      # console.log target, context
      # 这里是因为没有给出该元素的id，只能在这里增加了
      @fill(context, helper)
      html = @html
      if _.isElement(target)
        # 已经是jQuery对象
        target.append html
      else
        $(target).append html
      el = $.parseHTML(html)[1] #text, li#room-1.room, text
      id = el.id
      @$el = $("##{id}")              #绑定元素，如果绑定错误，后面修改
      # console.log el.id, @$el
      @
    show: () ->
      @$el.show()
      @isShow = true
    hide: () ->
      @$el.hide()
      @isShow = false
    remove: () ->
      @$el.remove()
      @isShow = false

  ##############################################################
  # 内建组件
  ##############################################################
  # 信息提示
  # error = {code: [:code], definition: [:definition]}
  class Echo
    constructor: (uri) ->
      @uri = uri || "#echo/"
      @$echoList = $echo = $('#echo-list') #存放错误的容器
      #理论上需要ubsubscribe，但是这里就不做了
    start: ->
      $.subscribe @uri, $.proxy(@subscribe, this)
    show: (definition) ->
      $echoList = @$echoList
      $echo = $("<li class='alert alert-success' hide>#{definition}</li>")
      $echo.appendTo($echoList).fadeIn(500)
      setTimeout =>
        $echo.fadeOut(1000).remove()
      , 4000
    hide: ->
      # @$echo.hide()
      @$echo.fadeOut(1000)
    subscribe: (e, error) ->
      # alert error
      code = error.code || "未知错误码"
      definition = error.definition || "未知错误定义"
      @show(definition)
      return
    hint: (info) =>
      {code, definition} = info
      @show(definition||"未知错误定义")
  ##############################################################
)();

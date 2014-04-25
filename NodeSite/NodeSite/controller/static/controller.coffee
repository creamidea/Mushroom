'use strict'

# 使用方式
# 记得还有一个模板文件 
# @cl = new ControllerList
#   $renderTo: $renderTo
#   roomId: @roomId

class ControllerList
  constructor: (params) ->
    {$renderTo, @roomId} = params
    # console.log "[controller.coffee]", $renderTo
    $renderTo.on "click", "input[type=checkbox]", $.proxy @clickEvent, @

    @$renderTo = $renderTo
    @intervalTime = 4000       # 1 minitus
    templateName = "#controller-list-template"
    source = $(templateName).html()
    @template = Handlebars.compile(source)
    # 这里是handlebars帮助函数 
    Handlebars.registerHelper "cn_name", (info) ->
      # this执行的是context中的每一条数据，arguments指向什么，我也不知道。
      # console.log arguments, this
      dict =
        "yello_light": "黄灯"
        "blue_light": "蓝灯"
        "red_light": "红灯"
        "paifeng_fan": "排风扇"
        "yasuoji": "压缩机"
        "xunhuan_fan": "循环风"
        "jinfeng_fan": "进风扇"
        "jiashiqi": "加湿器"
        "neiji": "内机"
      enName = info.data.key
      cnName = dict[enName]
    Handlebars.registerHelper "checked", () ->
      # this执行的是context中的每一条数据，arguments指向什么，我也不知道。
      # console.log arguments, this
      state = @state
      if state is 1
        checked = "checked"
      else
        checked = ""
      return checked

    # 初次运行
    getControllerList @roomId, (data) =>
      # console.log ">>>data:", data
      @render data.body
      
    # @sync()                 # 启动更新器
    # @stop()
    
  clickEvent: (e) ->
    $elt = $(e.target)
    answer =  $elt.prop('checked')
    if answer is true           #打开设备
      action = "on"
    else if answer is false
      action = "off"
    controllerId = $elt.attr("cid")
    # alert action+":"+controllerId
    $elt.parent().append("<p>这在处理中。。。</p>")
    putController controllerId, action, {cl: this, $elt:$elt}

  update: (cid, value) ->
    if not cid or not value then return
    $switch = @$renderTo.find "input[cid=#{cid}]"
    if value is "on"
      $switch.attr("checked", "checked")
    else
      $switch.removeAttr("checked")
      
  render: (context) ->
    if context is undefined
      context = @context
    {$renderTo, template} = @
    clHTML = template {context: context}
    # console.log context, clHTML
    @context = context
    $renderTo.html clHTML
    
  sync: () ->
    @timer = setInterval () =>
      if not @roomId then return
      getControllerList @roomId, (data) =>
        @render data.body
    , @intervalTime
    
  stop: () ->
    clearInterval @timer
  
renderControllerList = (params) ->
  # 渲染控制器列表
  # renderTo: controller-list
  {renderTo, templateName, context} = params
  source = $(templateName).html()
  console.log source
  template = Handlebars.compile(source)
  clHTML = template {context: context}
  $(renderTo).html clHTML

getControllerList = (roomId, callback) ->
  if arguments.length is 1
    callback = roomId
    url = "/controller/list/"
  else
    # url = "/controller/list/room/1/"
    url = "/controller/list/room/#{roomId}/"
  $.ajax
    url: url
    type: "GET"
    success: (data) ->
      if _.isFunction(callback)
        callback data
    fail: () ->
      alert "Get controller List Fail"

getController = (controllerId, callback) ->
  return

putController = (cid, action, extra) ->
  # cid就是控制器的编号
  $.ajax
    url: "/controller/#{cid}/"
    type: "PUT"
    context: extra
    data:
      action: action
    success: (data) ->
      # console.log ">>>[controller]data:", data
      if data.code is 0
        $('p', @$elt.parent()).remove()
      else
        @cl.render()
        alert data.body
    fail: () ->
      # alert "PUT CONTROLLER CONNECTION FAIL!"
      alert "请检查网络连接！"

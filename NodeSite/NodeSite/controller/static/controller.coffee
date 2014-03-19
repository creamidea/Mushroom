'use strict'

class ControllerList
  constructor: (params) ->
    {renderTo, @templateName} = params
    console.log "[controller.coffee]", renderTo
    @$renderTo = $renderTo = $(renderTo)
    $renderTo.on "click", "input[type=checkbox]", $.proxy @clickEvent, @

    @intervalTime = 60000       # 1 minitus
    @interval()                 # 启动更新器
    @roomId = null              # null值时说明没有
  clickEvent: (e) ->
    $elt = $(e.target)
    answer =  $elt.prop('checked')
    if answer is true           #打开设备
      action = "on"
    else if answer is false
      action = "off"
    controllerId = $elt.attr("cid")
    # alert action+":"+controllerId
    putController controllerId, action

  update: (cid, value) ->
    if not cid or not value then return
    $switch = @$renderTo.find "input[cid=#{cid}]"
    if value is "on"
      $switch.attr("checked", "checked")
    else
      $switch.removeAttr("checked")
      
  render: (context) ->
    {$renderTo, templateName} = @
    @roomId = context[0].roomId
    source = $(templateName).html()
    # console.log source
    template = Handlebars.compile(source)
    # 这里是handlebars帮助函数 
    Handlebars.registerHelper "checked", () ->
      # this执行的是context中的每一条数据，arguments指向什么，我也不知道。
      # console.log arguments, this
      state = @state
      if state is "on"
        checked = "checked"
      else
        checked = ""
      return checked
    clHTML = template {context: context}
    @context = context
    $renderTo.html clHTML
    
  interval: () ->
    setInterval () =>
      if not @roomId then return
      $.ajax
        url: "/controller/update/room/#{@roomId}/"
        type: "GET"
        success: (data) =>
          @render data.body
        fail: () ->
          alert "controller update failed"
    , @intervalTime
  
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

putController = (cid, action) ->
  # cid就是控制器的编号
  $.ajax
    url: "/controller/#{cid}/"
    type: "PUT"
    data:
      action: action
    success: (data) ->
      alert data.body
    fail: () ->
      alert "PUT CONTROLLER CONNECTION FAIL!"

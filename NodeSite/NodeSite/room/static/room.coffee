'use strict'

# ####################################################
# $("#create-new-policy-model").on 'shown.bs.modal', (e) ->
#   getPolicyList
#     $renderTo: $("#create-new-policy-model .modal-body")

sensorEnToCn =
  "temperature": "温度"
  "co2": "二氧化碳"
  "humidity": "湿度"
  "light": "光照"

# 渲染成HTML，返回HTML
render = (tplName, context, tag, helper) ->
  # console.log tplName
  # console.log context
  source   = $(tplName).html()
  template = Handlebars.compile(source)
  if _.isString(tag) and _.isFunction(helper)
    Handlebars.registerHelper tag, helper
  html = template(context)

# 渲染静态的html，意思是没有事件
renderStatic = (tplName, context, $renderTo) ->
  html = render tplName, context
  $renderTo.html html if $renderTo
  return html

# 渲染房间的meta信息
renderRoomMeta = (context, $renderTo) ->
  html = render "#room-meta-template", context
  $renderTo.html html if $renderTo
  return html

renderSensorsList = (context, $renderTo) ->
  html = render "#room-sensors-list-template", context,
    "cn-name", (param) ->
      # console.log @, arguments
      key = param.data.key
      sensorEnToCn[key] + "传感器"

  $renderTo.html html if $renderTo
  return html

class AverageUI
  constructor: (@$renderTo) ->
  render: (context) ->
    $renderTo = @$renderTo
    html = render "#room-env-average-template", context,
      "cn-name", (param) ->
        # console.log @, arguments
        key = param.data.key
        sensorEnToCn[key] + "传感器"

    $renderTo.html html if $renderTo
    @update()
    return html
  update: () ->
    console.log this

renderRoom = (context, $renderTo) ->
  # html = render "#room-template", context, "room-info", () ->
  #   # console.log "[render room]", context
  #   ahtml = []
  #   ahtml.push renderRoomMeta(this)
  #   avgUI = new AverageUI
  #   ahtml.push avgUI.render(this)
  #   # ahtml.push renderStatic "#room-env-average-template", this
  #   ahtml.push renderStatic "#room-policy-now-template", this
  #   ahtml.push renderSensorsList(this)
  #   ahtml.push renderStatic "#room-controller-list-template", this
  #   ret = ahtml.join("")
  #   # console.log this, html, ret
  #   new Handlebars.SafeString ret
  html = render "#room-template", context
  $renderTo.html html if $renderTo
  return html

renderRoomList = (context, $renderTo) ->
  # console.log "[render room list]", context
  html = render "#room-list-template", {context: context},
    'room-list', () ->
      # console.log this, context, options
      new Handlebars.SafeString renderRoom(this)
      # console.log "renderRoomList:", html
  $renderTo.html html if $renderTo
  return html
  
# renderRoomList context, $('#room-list')

$averages = $('.average')
# console.log $averages

# $.ajax
#   url: "/sensor/average/"
#   type: "GET"
#   success: (data) ->
#     # console.log data
#     $averages.each (index, $elt) ->
#       console.log "hello"
#       # $elt.find(".average")
#   fail: () ->
#     alert "SENSOR AVERAGE FAIL"
# ;
# renderRoomList = (context)->
#   source   = $("#room-template").html()
#   template = Handlebars.compile(source)
#   html = template(context)
#   # return html
#   $(html).on "click", "button[name=create-new-policy]", (e) ->
#     # 这里渲染创建策略的视图
#     getPolicyList
#       $renderTo: $("#policy-list")

# getRoom = (roomId) ->
#   # 获取房间信息
#   $.ajax
#     url: "/room/#{roomId}/"
#     type: "GET"
#     success: (data) ->
#       body = data.body
#       roomId = body.roomId
#       # console.log roomId, body
#       renderRoom body, $("#room-#{roomId}")
#       # console.log
#       # 获取并显示现在正在执行的策略 
#       getNowPolicy
#         roomId: roomId
#         $renderTo: $("#show-room-#{roomId}-now-policy")
#       getControllerList roomId, (data) ->
#         console.log "[room.coffee]", roomId
#         controllerList = new ControllerList
#           renderTo: "#room-#{roomId}-controller-list",
#           templateName: "#controller-list-template"
#         # console.log "GET CL 2:", data
#         # 渲染控制器列表
#         controllerList.render data.body
#         return
#     fail: (data) ->
#       alert "fail"

# getRoomList = ->
#   $.ajax
#     url: "/room/list/"
#     type: "GET"
#     success: (data) ->
#       body = data.body
#       # console.log data, body
#       renderRoomList body, $("#room-list")
#       for d in body
#         roomId = d.roomId
#         # console.log
#         # 获取并显示现在正在执行的策略 
#         getNowPolicy
#           roomId: roomId
#           $renderTo: $("#show-room-#{roomId}-now-policy")

#         # 获取并显示各个房间的控制器情况获取控制器列表
#         ( (roomId) ->
#         # 使用闭包，避免都是使用最后一次roomId
#         # 因为getControllerList这个函数引用了roomId这一个「外部」变量
#         # 于是roomId会始终保持「最新」状态
#             getControllerList roomId, (data) ->
#               # console.log "[room.coffee]", roomId
#               controllerList = new ControllerList
#                 renderTo: "#room-#{roomId}-controller-list",
#                 templateName: "#controller-list-template"

#               # console.log "GET CL 2:", data
#               # 渲染控制器列表
#               controllerList.render data.body
#               return
#         )(roomId)
#       return
#     fail: (data) ->
#       alert "fail"

# class RoomUI
  # constructor: (@room, @$renderTo) ->

class RoomList
  constructor: (data) ->
  # 这个用于管理房间的列表
    @data = data || []           #这个是房间单元
    $.observable @

  add: (data) ->
  # 增加一个房间
    console.log "add a room"
    room = new Room
    room.add(data)
    @data.push room
    
  remove: (room) ->
    console.log "remove a room"
  update: (room) ->
    console.log "update a room"

class Room
  constructor: (data) ->
  # 房间的模型
  # Enable MVP pattern (this is the secret for everything)
    $.observable @
    
    @data = data || {}
    @intervalTime = 6000
    # @isSync = true
    
    # @on "add update:time update:sensors update:average update:brightness", (data) ->

    @sync()                     #开启同步
    
  init: (data) ->
    @trigger "init", data
    @data = data
    
  getLatestData: () ->
    try
      roomId = @data.roomId
    catch e
      console.log e.message
    if roomId is undefined or roomId is null then return
    $.ajax
      url: "/data/room/#{roomId}/latest_data/"
      # url: "/data/room/1/latest_data/"
      type: "GET"
      success: (data) =>
        @trigger "getLatestData", data
      fail: () ->
        alert "[room.coffee] get room sensor failed"

  update: (data) ->
  # 更新数据
    # console.log "here is update"
    trigger = @trigger
    __data = @data
    # console.log data, __data
    time = data.time
    if __data.time isnt time
      trigger "update:time", time
      
    brightness = data.brightness
    if __data.brightness isnt brightness
      trigger "update:brightness", brightness

    average = data.average
    if not _.isEqual(__data.average, average)
      trigger "update:average", average
      
    sensors = data.sensors
    if not _.isEqual(__data.sensors, sensors)
      trigger "update:sensors", sensors

    @data = data
    # console.log @data
    
  sync: () ->
    @timer = setInterval ()=>
      try
        roomId = @data.roomId
      catch e
        console.log e.message
      if roomId is undefined or roomId is null then return
      $.ajax
        url: "/room/#{roomId}"
        type: "GET"
        success: (data) =>
          # console.log data
          @update data.body
        fail: (data) ->
          alert "[room.coffee] sync room failed!"
    , @intervalTime
    
  stop: () ->
    clearInterval @timer

# Room = (data) ->
#   # 房间的模型
#   __data = data || {}
#   # console.log data

#   # Enable MVP pattern (this is the secret for everything)
#   self = $.observable @
  
#   self.update = (data) ->
#     console.log "here is update"

#     time = data.time
#     if __data.time isnt time
#       self.trigger "update:time", time
      
#     average = data.average
#     if _.isEqual(__data.average, average)
#       self.trigger "update:time", average
      
#     sensors = data.sensors
#     if _.isEqual(__data.sensors, sensors)
#       self.trigger "update:sensors", sensors

#     __data = data
#   # self.on "update:time update:sensors", () ->

class Test
  constructor: (@name) ->
    $.observable this
  update: (age) ->
    @trigger "update", age

test = new Test()
test.on "update", (age) ->
  console.log "update age: ", age

# test.update 100

# class RoomUI
#   constructor: (data, $renderTo) ->
#     @room = room = new Room(context[0])
#     @data = data
#     @$renderTo = $renderTo
#     # 外层框架
#     $renderTo.append renderStatic("#room-template", @data)    
#     renderRoomMeta(data, $('.meta-info', $renderTo))
#     renderStatic "#room-env-average-template", data
#   render: (data) ->
#     data = data || @data
#     $renderTo = @$renderTo
#     # avgUI = new AverageUI
#     # ahtml.push avgUI.render(data)

#     # ahtml.push renderStatic "#room-env-average-template", this
#     # ahtml.push renderStatic "#room-policy-now-template", data

#     # ahtml.push renderSensorsList(data)
#     # ahtml.push renderStatic "#room-controller-list-template", data
#     # ret = ahtml.join("")
#     # console.log template, @$renderTo, 
#     # @$renderTo.append ret
    
#   update: (data) ->
#     @room.update data
#   renderTime: (time) ->
  #

class RoomPresenter
  constructor: (model, @$wrpelt) ->
    # model为模型，暂时由外部传入
    # $elt为外出包裹标签
    
    model.on "init", $.proxy @render, @
    model.on "update:average", $.proxy @updateAverage, @
    model.on "update:time", $.proxy @updateTime, @
    model.on "update:brightness", $.proxy @updateBrightness, @

    model.on "getLatestData", $.proxy @renderLatestData, @
    # @tplName = tplName

    # 这里是当html渲染进document之后出发完成时间
    # @$wrpelt.on "shown.room", (e, $elt) ->
      # console.log $room
        
    source = $("#room-template").html()
    @template = Handlebars.compile(source)
    Handlebars.registerHelper 'cn-name', (param) ->
      key = param.data.key
      sensorEnToCn[key] + "传感器"

  renderLatestData: (data) ->
    # console.log data
    source = $("#room-latest-data-template").html()
    template = Handlebars.compile(source)
    # Handlebars.registerHelper ''
    html = template(data.body)
    # console.log html
    $(".latest-data", @$elt).html(html)
            
  updateAverage: (average) ->
    source = $("#room-average-template").html()
    template = Handlebars.compile(source)
    html = template {average:average}
    # console.log source, average, html
    $('.average', @$elt).html html
  updateTime: (time) ->
    $('.capture-time', @$elt).html "<p>#{time}</p>"
  updateBrightness: (brightness) ->
    $('.brightness', @$elt).html "<p class=#{brightness}>#{brightness}</p>"
    
  render: (data) ->
    {template} = @
    roomId = @roomId = data.roomId
    # console.log "???data??", data, @roomId
    html = template(data)
    $wrpelt = @$wrpelt
    @$elt = $elt = $(html).appendTo $wrpelt if $wrpelt
    # ------------------------------------------------
    # 出发房间完成渲染事件
    # $wrpelt.trigger "shown.room-#{data.roomId}", $elt

    # $("#room-id-#{roomId}", @$el).find("[action=edit-rname]").click (e)=>
    #   $elt = $(e.target)
    #   console.log $elt
    #   $.proxy @roomMetaEdit("rname"), @
    # $("#room-id-#{roomId}", @$el).find("[action=edit-pname]").click (e)=>
    #   $.proxy @roomMetaEdit("pname"), @
    
    @$widgetPanel = $('.widget-panel', @$elt)
    @closeButton = $('button.close', @$widgetPanel)
    # $elt.on "click", ".widget > a", $.proxy @clickWidget, @
    @closeButton.click $.proxy @closePanel, @

  # roomMetaEdit: (name) ->
    # $.ajax
    #   url: "/room/#{@roomId}/name"
    #   type: "PUT"
    #   data:
    #     name: "test"
    #   success: (data) ->
    #     alert "success"
    #   fail: (data) ->
    #     alert "[room.coffee] modify room meta failed!"

  closePanel: (e) ->
    $button = $(e.target).closest("button")
    $button.addClass("hide")    #隐藏图标
    $button.siblings(".active").removeClass("active") #隐藏面板 
    
  clickWidget: (e) ->
    e.preventDefault() if e
    # console.log e.target
    $link = $($(e.target).closest('a'))
    href = $link.attr("href").split("/")
    # href = href.split("/")
    name = "#{href[2]}-#{href[3]}"
    @$widgetPanel.children().removeClass("active").filter (index, elt) ->
      # console.log name, $(elt).attr("name")
      return name is $(elt).attr("name")
    .addClass("active")
    @closeButton.removeClass("hide")

    $renderTo = $("[name=#{name}]", @$elt)
    switch name
      when "policy-add"
        if @ppAdd then break
        policyAdd = new Policy
        @ppAdd = new PolicyPresenter policyAdd, $renderTo, "edit"
      when "policy-now"
        if @ppNow then break
        pid = $link.attr("pid")
        pid = 8
        policyNow = new Policy pid
        @ppNow = new PolicyPresenter policyNow, $renderTo, "view"
      when "controller-list"
        if @cl then break
        @cl = new ControllerList
          $renderTo: $renderTo
          roomId: @roomId
      else
        break

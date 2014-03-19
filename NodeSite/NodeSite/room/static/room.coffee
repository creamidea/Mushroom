'use strict'

console.log "here is room"
context = [{
  "roomId": 1,
  "roomName": "房间1",
  "plantId": 1,
  "plantName": "蘑菇",
  "time": "2013-12-25 16:41",
  "average":
    temperature:18,
    co2:24,
    humidity:150,
  "sensors": {
    'temperature': [1,2,3,4,5],
    'co2': [12,13,14,15],
    'humidity': [23,24,25,26,27],
  },
  "brightness": "yellow",
  "nowPolicy": 1,
},
{
  "roomId": 2,
  "roomName": "房间2",
  "plantId": 2,
  "plantName": "蘑菇",
  "time": "2013-12-25 16:41",
  "average":
    temperature:18,
    co2:24,
    humidity:150,
  "sensors": {
    'temperature': [1,2,3,4,5],
    'co2': [12,13,14,15],
    'humidity': [23,24,25,26,27],
  },
  "brightness": "yellow",
  "nowPolicy": 1,
},
{
  "roomId": 3,
  "roomName": "房间3",
  "plantId": 3,
  "plantName": "蘑菇",
  "time": "2013-12-25 16:41",
  "average":
    temperature:18,
    co2:24,
    humidity:150,
  "sensors": {
    'temperature': [1,2,3,4,5],
    'co2': [12,13,14,15],
    'humidity': [23,24,25,26,27],
  },
  "brightness": "yellow",
  "nowPolicy": 1,
}
]

# ####################################################
$("#create-new-policy-model").on 'shown.bs.modal', (e) ->
  # console.log arguments
  getPolicyList
    $renderTo: $("#create-new-policy-model .modal-body")
# .on 'hide.bs.modal', (e) ->
#   alert "sending..."

sensorEnToCn =
  "temperature": "温度"
  "co2": "二氧化碳"
  "humidity": "湿度"

render = (tplName, context, tag, helper) ->
# 渲染成HTML，返回HTML
  # console.log tplName
  # console.log context
  source   = $(tplName).html()
  template = Handlebars.compile(source)
  if _.isString(tag) and _.isFunction(helper)
    Handlebars.registerHelper tag, helper
  html = template(context)


renderStatic = (tplName, context, $renderTo) ->
# 渲染静态的html，意思是没有事件
  html = render tplName, context
  $renderTo.html html if $renderTo
  return html

renderRoomMeta = (context, $renderTo) ->
# 渲染房间的meta信息
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
  
renderRoomList context, $('#room-list')

$averages = $('.average')
console.log $averages

$.ajax
  url: "/sensor/average/"
  type: "GET"
  success: (data) ->
    console.log data
    $averages.each (index, $elt) ->
      console.log "hello"
      $elt.find(".average")
  fail: () ->
    alert "SENSOR AVERAGE FAIL"

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

Room = (data) ->
  __data = data || {}
  # console.log data

  # Enable MVP pattern (this is the secret for everything)
  self = $.observable @
  
  self.update = (data) ->
    console.log "here is update"

    time = data.time
    if __data.time isnt time
      self.trigger "update:time", time
      
    average = data.average
    if _.isEqual(__data.average, average)
      self.trigger "update:time", average
      
    sensors = data.sensors
    if _.isEqual(__data.sensors, sensors)
      self.trigger "update:sensors", sensors

    __data = data
  # self.on "update:time update:sensors", () ->

  return

class RoomUI
  constructor: (data, $renderTo) ->
    @room = room = new Room(context[0])
    @data = data
    @$renderTo = $renderTo
    # 外层框架
    $renderTo.append renderStatic("#room-template", @data)    
    renderRoomMeta(data, $('.meta-info', $renderTo))
    renderStatic "#room-env-average-template", data
  render: (data) ->
    data = data || @data
    $renderTo = @$renderTo
    # avgUI = new AverageUI
    # ahtml.push avgUI.render(data)

    # ahtml.push renderStatic "#room-env-average-template", this
    # ahtml.push renderStatic "#room-policy-now-template", data

    # ahtml.push renderSensorsList(data)
    # ahtml.push renderStatic "#room-controller-list-template", data
    # ret = ahtml.join("")
    # console.log template, @$renderTo, 
    # @$renderTo.append ret
    
  update: (data) ->
    @room.update data
  renderTime: (time) ->

  

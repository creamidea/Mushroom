# class RoomList
#   constructor: (el)->
#     @el = el || "#room-list"
#     @$el = $(@el)
#     @list = {}
#     @uri = "/rooms/"
#   hide: () ->
#     @$el.hide()
#   fetch: (uri) ->
#     uri = uri || @uri
#     roomFetch = new Post uri, (data) =>
#       console.log data
#       if data.code is 0
#         @appendAll(data.context)
#     roomFetch.send()

class RoomList extends Frame
  constructor: (el)->
    @el = el || "#room-list"
    @$el = $(@el)
    @list = {}
    @uri = "/rooms/"
  fetch: (opt) ->
    # 从服务器取数据
    isRender = opt.isRender
    uri = opt.uri || @uri
    roomFetch = new Post uri, (data) =>
      # console.log data
      if data.code is 0
        if isRender
          @renderAll(data.context)
        else
          $.publish opt.url, [data.context]
    roomFetch.send()
  renderAll: (context) ->
    @render c for c in context
  render: (context) ->
    roomId = context.roomId
    list = @list
    $roomList = @$el
    if list[roomId] is undefined
      room = new Room roomId, "#room-template"
      room.renderTo $roomList, context
      list[context.id] = room

class Room extends Frame
  # 这个是房间类，囊括了缩略图，数据图表，查看/设置策略和控制面板
  constructor: (@roomId, @templateName) ->
    super(@templateName)
    
    roomId = @roomId
    @showElt = undefined               #用于记录当前显示的元素
    
    # 订阅RoomThumbnail发出的信号
    $.subscribe "#data/room-#{roomId}", $.proxy(@dataHandle, this)
    $.subscribe "#policy/viewer/room-#{roomId}", $.proxy(@viewPolicy, this)
    $.subscribe "#policy/setter/room-#{roomId}", $.proxy(@setPolicy, this)
    $.subscribe "#controller/room-#{roomId}", $.proxy(@controllerHandle, this)
    
  hideElt: (elt) ->
    if elt
      elt.hide
    else
      @env.hide()
      @policyViewer.hide()
      @policySetter.hide()
      @controller.hide()
      
  dataHandle: ->
    console.log arguments
    if @showElt
      @showElt.hide()
    if !@env                    #第一次创生
      @env = new RoomEnv "#room-env-template", @roomId
      @env.renderTo @$el, @context
    else
      @env.show()
    @showElt = @env
    
  viewPolicy: ->
    if @showElt
      @showElt.hide()
    if !@policyViewer
      roomId = @roomId
      @policyViewer = new RoomPolicyViewer "#room-policy-viewer-template", @roomId
      getPolicy = new Get "/policy/now/room/#{roomId}/", (data) =>
        @policyViewer.renderTo @$el, data.data
      getPolicy.send()
      # @policyViewer.renderTo @$el, @context
    else
      @policyViewer.show()
    @showElt = @policyViewer
    
  setPolicy: ->
    if @showElt
      @showElt.hide()
    if !@policySetter
      @policySetter = new RoomPolicySetter "#room-policy-setter-template", @roomId
      @policySetter.renderTo @$el, @context
    else
      @policySetter.show()
    @showElt = @policySetter
  controllerHandle: () ->
    if @showElt
      @showElt.hide()
    if !@controller
      @controller = new RoomController "#room-controller-template", @roomId
      @controller.renderTo @$el, @context
    else
      @controller.show()
    @showElt = @controller
  renderTo: (target, context) ->
    super(target, context)
    @context = context
    # console.log target, @roomId
    # super(target, {roomId: "#{@roomId}"})
    # console.log @html
    # @$el = $("#room-#{@roomId}")
    @roomThumbnail = new RoomThumbnail "#room-thumbnail-template", @roomId
    @roomThumbnail.renderTo @$el, context
    # @roomThumbnail.fill(@context).renderTo(@$el)
    # roomThumbnail.submit()
    # @roomThumbnail.hide()

class RoomThumbnail extends Frame
  constructor: (@templateName, @roomId) ->
    super(@templateName)
    # 初始化一些变量，后期会提供修改接口
    @nav = "nav.room-menu>ul"
    @card = ".card"
    @brightness = ".room-light"
    @roomName = ".room-name"
    # @inputRoomName = "input[name=roomName]"
    @plantName = ".plant-name"
    # @inputPlantName = "input[name=plantName]"
    @searchForm = ".room-search>form"
    @searchURI = "/search/"
    
  renderTo: (target, context) ->
    # console.log target, context
    super(target, context)
    $el = @$el
    # find = $el.find
    # console.log find
    @$roomName = $el.find(@roomName)
    @$plantName = $el.find(@plantName)
    @$cards = $el.find(@card)   #保存上面需要实时跟新的信息：温度，湿度，co2
    @$brightness = $el.find(@brightness)
    @submit()                   #启动提交事件监听
    # @update(testRoomUpdate)
  update: (context) ->
    roomName = context.roomName
    plantName = context.plantName
    sensors = context.sensors
    brightness = context.brightness
    @$roomName.html(roomName)
    @$plantName.html(plantName)
    @$cards.each (index, el)->
      s = el.id.split('-')[2]
      if s                      #排除第一张卡片
        value = sensors[s]
        $(el).html("<p>#{value}</p>")
    @$brightness.attr("brightness", brightness)
  subscribe: ->
    # 这类函数放到room里面去了
    roomId = @roomId
    $.subscribe "#data/room-#{roomId}", $.proxy(@dataHandle, this)
    $.subscribe "#policy/viewer/room-#{roomId}", $.proxy(@viewPolicy, this)
    $.subscribe "#policy/setter/room-#{roomId}", $.proxy(@setPolicy, this)
    $.subscribe "#policy/controller/room-#{roomId}", $.proxy(@controllerHandle, this)
    # $.subscribe "#search/room-#{roomId}", $.proxy(@search, this)
  submit: () ->
    $form = @$el.find(@searchForm)
    # console.log $form
    $sensor = $form.find("input[name=sensor]")
    $startDate = $form.find("input[name=start-date]")
    $endDate = $form.find("input[name=end-date]")
    $form.submit (e) =>
      e.preventDefault()
      sensor = $sensor.val()
      startDate = $startDate.val()
      endDate = $endDate.val()
      roomId = @roomId || -1
      # alert @roomId
      @search
        roomId: roomId
        sensorId: sensor
        startDate: startDate
        endDate: endDate
      # alert "#{sensor}:#{startDate}:#{endDate}"
  search: (context)->
    # console.log "context", context
    searchPost = new Post @searchURI, (data) ->
      $.publish "#search/finish/", [data]
      # alert data.data
    searchPost.send(context)
    # console.log e
  fill: (context) ->
    # console.log context
    super(context)

class RoomEnv extends Frame
  constructor: (@templateName, @roomId) ->
    super(@templateName)
  renderTo: (target, context) ->
    super(target, context)

class RoomPolicyViewer extends Frame
  constructor: (@templateName, @roomId) ->
    super(@templateName)
    @timeline = '.timeline'
    @table = 'table'
  renderTo: (target, context) ->
    console.log context
    super(target, context)
    @$timeline = @$el.find(@timeline)
    @$table = @$el.find(@table)
    # @$timeline.css('top', '0')
    console.log @$table.height()
    

class RoomPolicySetter extends Frame
  constructor: (@templateName, @roomId) ->
    super(@templateName)
  renderTo: (target, context) ->
    super(target, context)

class RoomController extends Frame
  constructor: (@templateName, @roomId) ->
    super(@templateName)
  renderTo: (target, context) ->
    # console.log roomControllerData
    super(target, context)
    
context =
  "roomId": 1,
  "roomName": "房间1",
  "plantId": 1,
  "plantName": "蘑菇",
  "time": "2013-12-25 16:41",
  "sensors": 
    "temperature": 18,
    "co2": 24,
    "humidity": 150,
  "brightness": "yellow",
  "menu": 
    "data": "glyphicon-sort",
    "policy/viewer": "glyphicon-list-alt",
    "policy/setter": "glyphicon-pencil",
    "controller": "glyphicon-wrench",

testRoomUpdate =
  "roomName": "房间1-1"
  "plantName": "蘑菇2"
  "sensors":
    "temperature": 0
    "co2": 0
    "humidity": 1
  "brightness": "white"

roomControllerData =
  [
    {
      "roomId": 1
      "controllerId": 2
      "controllerType": "湿度传感器"
      "state": "on"
    }
    {
      "roomId": 2
      "controllerId": 2
      "controllerType": "湿度传感器"
      "state": "on"
    }
    {
      "roomId": 3
      "controllerId": 2
      "controllerType": "湿度传感器"
      "state": "on"
    }
  ]

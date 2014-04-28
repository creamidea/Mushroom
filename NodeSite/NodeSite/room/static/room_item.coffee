$ ->
  'use strict'
  # alert "hi"
  console.log "here is room item"
  # roomId = window.location.pathname.split("/")[2]
  roomId = (window.location.pathname).replace(/(.*)\/room\/(\d+)\//g, "$2")
  sensorEnToCn =
    "temperature": "温度"
    "co2": "二氧化碳"
    "humidity": "湿度"
    "light": "光照"

  # $("#create-new-policy-model").on 'shown.bs.modal', (e) ->
  #   # console.log arguments
  #   getPolicyList
  #     $renderTo: $("#create-new-policy-model .modal-body")

  # 这里加载房间基础信息
  # getRoom(roomId)

  # renderRoomList = (context)->
  #   source   = $("#room-template").html()
  #   template = Handlebars.compile(source)
  #   html = template(context)
  #   # return html
  #   $(html).on "click", "button[name=create-new-policy]", (e) ->
  #     # 这里渲染创建策略的视图
  #     getPolicyList
  #       $renderTo: $("#policy-list")
  $room = $("#room-#{roomId}")
  getRoom = -> 
    $.ajax
      url: "/room/#{roomId}/"
      type: "GET"
      success: (data) ->
        body = data.body
        # console.log body
        
        room = new Room
        new RoomPresenter room, $room
        room.init body
        room.stop()
        room.getLatestData()
          # showRoom(item)
          # getRoomSensors(item.roomId)
        return
      fail: (data) ->
        alert "[room_list.coffee] get room faild"
  getRoom()
  
  # 获取数据，并绘制图表
  # requestData(roomId)

  $oneHourArea = $('#realtime-chart')
  # 从服务器获取数据，并绘制一小时趋势图
  now = new Date()
  endTime = now.getTime()
  startTime = new Date(endTime-3600000)
  endTime = now
  getDataFromS
    # 从服务器获取数据 
    url: "/data/room/#{roomId}/"
    requestData:
      startTime: "2014/03/29 22:00:00"
      endTime: "2014/03/29 22:01:58"
      # startTime: "#{startTime.toLocaleDateString()} #{startTime.toLocaleTimeString()}"
      # endTime: "#{endTime.toLocaleDateString()} #{endTime.toLocaleTimeString()}"
    callback: (data) ->
      if data.code is -1
        $oneHourArea.html("<p class=error>目前还没有数据</p>")
        return 0
      console.log data.body
      datapkg =  dataPkgForD3(data.body)
      # 加载图表div
      # console.log source, html
      html = renderRTChart datapkg
      $oneHourArea.append html
      for key, data of datapkg
        console.log key, data
        # 绘制图表
        drawLineChart
          elt: "##{key} svg"
          data: data
          xLabel: sensorEnToCn[key]
          yLabel: "采集值"

  # searchChart = new SearchChart
  #   $renderTo: $("#search-chart-area")
  #   roomId: roomId
  # console.log searchChart
  # searchChart.render()

# ===========================================================
  data = ->
    stream_layers(3,10+Math.random()*200,.1).map (data, i) ->
      {
        key: 'Stream' + i
        values: data
      }
  # /* Inspired by Lee Byron's test data generator. */
  stream_layers = (n, m, o) ->
    if arguments.length < 3 then o = 0
    bump = (a) -> 
      x = 1 / (.1 + Math.random())
      y = 2 * Math.random() - .5
      z = 10 / (.1 + Math.random())
      for i in [0..m]
        w = (i / m - y) * z
        a[i] += x * Math.exp(-w * w)
        
    d3.range(n).map ->
      a = []
      for i in [0..m]
        a[i] = o + o * Math.random()
      for i in [0..5]
        bump(a)
      a.map(stream_index);

  # /* Another layer generator using gamma distributions. */
  stream_waves = (n, m) ->
    d3.range(n)
    .map (i) ->
      d3.range(m)
      .map (j) ->
          x = 20 * j / m - i / 3
          2 * x * Math.exp(-.5 * x)
      .map(stream_index)

  stream_index = (d, i) ->
    {x: i, y: Math.max(0, d)}

  data_2 =
    key: "test1"
    values: []
  for i in [1..1000]
    data_2.values.push
      x: i
      y: i * Math.random() * 100 - 20
  data_test = [data_2]
  # console.log data(), data_test
  drawLineWithFocusChart
    data:data_test
    elt: "#line-with-focus-chart svg"
    xLabel: "采集时间"
    yLabel: "采集值"

  
  # controllerList = new ControllerList
  #   renderTo: "#controller-list",
  #   templateName: "#controller-list-template"
    
  # # 获取控制器列表
  # getControllerList roomId, (data) ->
  #   console.log "GET CL 2:", data
  #   # 渲染控制器列表
  #   controllerList.render data.body
  #

  # 开启时间选择插件
  $('#datepicker0').pickadate
    today: '今日'
    clear: '清除'
    format: 'yyyy/mm/dd'
  $('#datepicker1').pickadate
    today: '今日'
    clear: '清除'
    format: 'yyyy/mm/dd'
    
  return

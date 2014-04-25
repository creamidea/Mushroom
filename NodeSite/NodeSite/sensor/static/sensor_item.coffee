'use strict'
$ ->
  console.log "here is sensor item"
  sid = window.location.pathname.split("/")[2]

  $realtimeChart = $("#realtime-chart")
  
  sensorEnToCn =
    "temperature": "温度"
    "co2": "二氧化碳"
    "humidity": "湿度"
  # 从服务器获取数据，并绘制一小时趋势图
  now = new Date()
  endTime = now.getTime()
  startTime = new Date(endTime-3600000)
  endTime = now
  getDataFromS
    # 从服务器获取数据 
    url: "/data/sensor/#{sid}/"
    requestData:
      startTime: "2014/03/27 00:00:00"
      endTime: "2014/03/30 23:59:58"
      # startTime: "#{startTime.toLocaleDateString()} #{startTime.toLocaleTimeString()}"
      # endTime: "#{endTime.toLocaleDateString()} #{endTime.toLocaleTimeString()}"
    callback: (data) ->
      # console.log data.body
      if data.code is -1
        $realtimeChart.html("<p class=error>目前还没有数据</p>")
        return 0
      datapkg =  dataPkgForD3(data.body)
      console.log datapkg
      # 加载图表div
      # console.log source, html
      html = renderRTChart datapkg
      $realtimeChart.append html
      for key, data of datapkg
        # console.log data
        # drawLineChart
        drawLineWithFocusChart
          elt: "##{key} svg"
          data: data
          xLabel: key
          yLabel: "采集值"

  source = $('#download-form-template').html()
  template = Handlebars.compile source
  html = template {sensorId: sid}
  $('#download-area').append(html)
  # $('#download-form').submit (e) ->
    # data = $(this).serialize()
    # console.log data
    

  return 


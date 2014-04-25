'use strict'
sensorEnToCn =
  "temperature": "温度"
  "co2": "二氧化碳"
  "humidity": "湿度"
  "light": "光照"

getDataFromS = (context)->
  {url, requestData, callback} = context
  $.ajax
    url: url
    type: "GET"
    data: requestData
    success: (data) ->
      callback data
    fail: (data) ->
      alert "通讯失败"
    # statusCode: 
      # 404: ->
      #   window.location.href = "/404.html"


dataPkgForD3 = (data) ->
  # 数据处理
  _sensors = {}
  for sensor in data
    sensorType = sensor.sensorType
    if _sensors[sensorType] is undefined then _sensors[sensorType] = []
    sensorTypeCN = sensorEnToCn[sensorType]
    key = "#{sensorTypeCN}-#{sensor.sensorId}-#{sensor.position}"
    values = []
    _values = sensor.values
    for v in _values
      # 这里将数据处理成D3能够使用的x和y值
      # values.push [(new Date(v[0])).getTime(), v[1]]
      values.push
        x: (new Date(v[0])).getTime()
        y: v[1]
    # console.log sensorType, key, values
    _sensors[sensorType].push
      key: key
      values: values
  _sensors

drawLineChart = (opt) ->
  {elt, data, xLabel, yLabel} = opt
  # console.log elt, datas, xLabel, yLabel
  # console.log datas
  if elt and data
    nv.addGraph ->
      chart = nv.models.lineChart().color(d3.scale.category10().range()).useInteractiveGuideline(true)
      chart.xAxis.axisLabel(xLabel).tickFormat (d)->
        d3.time.format('%X')(new Date(d))
      chart.yAxis.axisLabel(yLabel).tickFormat(d3.format('.02f'))
      d3.select(elt).datum(data).transition().duration(500).call(chart)
      nv.utils.windowResize(chart.update)
      chart
      
drawLineWithFocusChart = (opt) ->
  {elt, data, xLabel, yLabel} = opt
  chart = nv.models.lineWithFocusChart()
  chart.xAxis.axisLabel(xLabel).tickFormat (d)->
    d3.time.format('%x')(new Date(d))
  chart.yAxis
    .tickFormat(d3.format(',.2f'))
  chart.y2Axis.axisLabel(yLabel)
    .tickFormat(d3.format(',.2f'))
  d3.select(elt)
    .datum(data)
    .transition().duration(500)
    .call(chart)
  nv.utils.windowResize(chart.update)
  chart


drawCumulativeLineChart = (opt) ->
  {elt, data, xLabel, yLabel} = opt 
  chart = nv.models.cumulativeLineChart()
    .x (d) -> d[0]
    .y (d) -> d[1]/100
    .color d3.scale.category10().range()
  chart.xAxis.axisLabel(xLabel).tickFormat (d)->
    d3.time.format('%X')(new Date(d))
  chart.yAxis
    .tickFormat(d3.format(',.2f'))
  d3.select(elt)
    .datum(data)
    .transition().duration(500)
    .call(chart)
  nv.utils.windowResize(chart.update)
  chart
 
requestData = (roomId)->
  $.ajax
    url: "/data/room/#{roomId}/"
    type: "get"
    data:
      startTime: "2014-03-30 00:00:00"
      endTime: "2014-03-31 23:59:59"
    success: (data) ->
      # console.log data.body
      dataBody = data.body
      lines = []
      for sensor in dataBody
        key = "#{sensor.sensorId}-#{sensor.sensorType}-#{sensor.position}"
        values = []
        _values = sensor.values
        for v in _values
          values.push
            x: (new Date(v[0])).getTime()
            y: v[1]
        lines.push
          key: key
          values: values
      # console.log lines
      nv.addGraph ->
        chart = nv.models.lineChart().useInteractiveGuideline(true)
        chart.xAxis.axisLabel('Temperature').tickFormat (d)->
          d3.time.format('%x')(new Date(d))
        chart.yAxis.axisLabel('Voltage (v)').tickFormat(d3.format('.02f'))
        d3.select('#chart svg').datum(lines).transition().duration(500).call(chart)
        nv.utils.windowResize(chart.update)

    fail: () ->
      alert "GET ROOM DATA FAILED!"

generateData = ->
  sin = []
  cos = []
  for i in [0..100]
    sin.push {x: i, y: Math.sin(i/10)}
    cos.push({x: i, y: .5 * Math.cos(i/10)})
  return [
    {
      values: sin,
      key: 'Sine Wave',
      color: '#ff7f0e'
    },
    {
      values: cos,
      key: 'Cosine Wave',
      color: '#2ca02c'
    }
    ]

drawLine = ->
  nv.addGraph ->
    chart = nv.models.lineChart().useInteractiveGuideline(true)
    chart.xAxis.axisLabel('Time (ms)').tickFormat(d3.format(',r'))
    chart.yAxis.axisLabel('Voltage (v)').tickFormat(d3.format('.02f'))
    d3.select('#chart svg').datum(generateData()).transition().duration(500).call(chart)
    nv.utils.windowResize(chart.update)
    return chart
# drawLineChart()


getData = ->
# 一天产生一个数据
# getDate() return the day of the month
# setDate() set the day of the month
  arr = []
  theDate = new Date(2014, 1, 1, 0, 0, 0, 0)
  for i in [0..30]
    arr.push
      x: new Date theDate.getTime()
      y: Math.random() * 100
    theDate.setDate(theDate.getDate() + 1)
  return arr

data = [
  "key": "Long"
  "values": getData()
]
chart = null
duration = 20000

redraw = ->
  nv.addGraph ->
    chart = nv.models.cumulativeLineChart()
      .x (d) -> d.x
      .y (d) -> d.y / 100
      .color d3.scale.category10().range()

    chart.xAxis.tickFormat (d) ->
      d3.time.format('%x')(new Date(d))

    chart.yAxis.tickFormat d3.format(',.1%')

    d3.select('#realtime-chart-1 svg')
      .datum(data)
      .transition().duration(500)
      .call(chart)

    nv.utils.windowResize chart.update

    return chart

redraw()
# setInterval ->
#   long = data[0].values
#   # console.log long
#   next = new Date(long[long.length-1].x)
#   next.setDate next.getDate() + 1
#   long.shift()
#   long.push
#     x: next.getTime()
#     y: Math.random() * 100
#   redraw()
# , duration

renderRTChart = (datapkg) ->
  source   = $("#realtime-chart-template").html()
  template = Handlebars.compile(source)
  Handlebars.registerHelper 'cn-name', (obj) ->
    # console.log arguments
    key = obj.data.key
    sensorEnToCn[key]
  html = template {datapkg:datapkg}


# 这里是搜索结果显示图标
# 使用方式
# 
class SearchChart
  constructor: (params) ->
    {roomId, $renderTo} = params
    if $renderTo instanceof jQuery
      $renderTo.on "blur", "select", $.proxy @blurEvent, @
      $renderTo.on "blur", "input", $.proxy @blurEvent, @
      $renderTo.on "submit", "form", $.proxy @submit, @
    @data =
      roomId: roomId
      sensorType: "all"
    @$renderTo = $renderTo

    @charts = {}
    
  blurEvent: (e) ->
    # console.log e, arguments
    $elt = $(e.target)
    name = $elt.attr("name")
    value = $elt.val()
    # tagName = $elt.prop("tagName")
    # if tagName.toLowerCase() is "select"
    #   name = $elt.attr("name")
    @data[name] = value
    e.stopPropagation()
    
  submit: (e) ->
    # console.log @data
    $renderTo = @$renderTo
    data = @data
    # if not data.sensorType
    $.ajax
      url: "/search/"
      type: "GET"
      data: data
      success: (data) =>
        console.log data
        datapkg = dataPkgForD3(data.body)
        console.log datapkg
        for key, data of datapkg
          # console.log key, data
          # 绘制图表
          if @charts[key] is undefined
            id = "search-#{key}-chart"
            html ="<div id=#{id} class=chart><svg></svg></div>"
            @charts[key] = $renderTo.append html
          drawLineChart
            elt: "#search-#{key}-chart svg"
            data: data
            xLabel: "采集#{sensorEnToCn[key]}时间"
            yLabel: "采集值"
      fail: ()->
        alert "Search Fail!"
    e.preventDefault()
    
  render: () ->
    source   = $("#search-chart-template").html()
    template = Handlebars.compile(source)
    html = template {author: "icecream"}
    @$renderTo.html html if @$renderTo instanceof jQuery
    return html

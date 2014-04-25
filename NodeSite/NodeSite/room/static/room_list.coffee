'use strict'
$ ->
  # 页面载入时获取房间列表
  # getRoomList()
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
    "time": "2013-12-26 16:41",
    "average":
      temperature:180,
      co2:240,
      humidity:150,
    "sensors": {
      'temperature': [1,2,3,4,5],
      'co2': [12,13,14,15],
      'humidity': [23,24,25,26,27],
    },
    "brightness": "blue",
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

  $roomList = $("#room-list")
  
  # showError = (error) ->
  #   alert error

  # showRoom = (data)->
  #   source = $("#room-template").html()
  #   template = Handlebars.compile(source)
  #   html = template(data)
  #   $roomList.append(html)

  # showEnv = (data)->

  # getRoomSensors = (roomId) ->
  #   $.ajax
  #     url: "/sensor/list/room/#{roomId}/"
  #     type: "GET"
  #     success: (data) ->
  #       console.log data
  #     fail: () ->
  #       showError "get room sensor failed"
  
  getRoomList = () ->
    $.ajax
      url: "/room/list/"
      type: "GET"
      success: (data) ->
        body = data.body
        # console.log body
        for item in body
          room = new Room
          new RoomPresenter room, $roomList
          room.init item
          room.stop()
          room.getLatestData()
          # showRoom(item)
          # getRoomSensors(item.roomId)
        return
      fail: (data) ->
        alert "[room_list.coffee] get room list faild"
  getRoomList()
  return

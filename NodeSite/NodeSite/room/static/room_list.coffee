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
  # roomui = new RoomUI context[0], $("#room-list")
  # roomui.render()
  # roomui.update context[1]
  return

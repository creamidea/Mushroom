$ ->
  'use strict'
  # 页面载入时获取房间列表
  $roomList = $("#room-list")
  
  getRoomList = () ->
    $.ajax
      url: "/room/list/"
      type: "GET"
      success: (data) ->
        if data.code is 0
          body = data.body
          console.log body
          for item in body
            room = new Room
            new RoomPresenter room, $roomList
            room.init item
            room.stop()
            room.getLatestData()
        else
          alert data.body
        return
      fail: (data) ->
        alert "[room_list.coffee] get room list faild"
  getRoomList()
  return

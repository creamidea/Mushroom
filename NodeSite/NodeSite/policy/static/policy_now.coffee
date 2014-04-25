'use strict'

$ ->
  href = window.location.href
  roomId = href.match(/.*room\/(\d+)\//)

  $policyNow = $('#policy-now')
  if roomId
    roomId = roomId[1]
    $.ajax
      url: "/policy/now/room/#{roomId}/"
      type: 'GET'
      success: (data) ->
        console.log data
        body = data.body
        if body.length < 1
          $policyNow.html("现在还没有数据")
        else
          {policyId, roomId, roomDesc, now, rules} = data.body[0]
          source = $('#policy-now-template').html()
          template = Handlebars.compile(source)
          html = template
            roomId: roomId
            roomDesc: roomDesc
            context: rules
          $('#policy-now').html(html)

          # 标记正在执行的策略
          nowPos = 0                #使用闭包，将下面函数的值传出 
          $('table tbody', $policyNow).children()
            .each (index, elt) ->
              $elt = $(elt)
              $date = $('td.date', $elt)
              if $date.text() is now
                nowPos = index
                html = "<i class=\"glyphicon glyphicon-forward\"></i>"
                $date.prepend(html)
                $i = $date.find('i')
                $i.css("position", "absolute")
                  .css("left", "10px")
                  .css("top", "10px")


          # link = "<a href=\"/policy/#{pid}/\">#{description}</a>"
          # btnHTML = "<a href=\"/policy/create/?from-policy=#{pid}&&nowPos=#{nowPos}&&now=#{now}\"><button class=\"btn btn-success\">修改策略</button></a>"
          # $('#pid').html(description).append(btnHTML)
          $("#room-#{roomId} a").attr('href',
          encodeURI("/policy/create/?from-policy=#{policyId}&&nowPos=#{nowPos}&&now=#{now}"))

      fail: (data) ->
        alert "通信失败，请检查网络，稍微再试"

  
  return

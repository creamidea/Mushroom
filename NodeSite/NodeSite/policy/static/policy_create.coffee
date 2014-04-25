'use strict'
$ ->
  # console.log "[policy create]: ", window.location.search
  href = decodeURI(window.location.search).slice(1)
  [from, nowPos, now] = href.split("&&")
  # pid = window.location.search).replace /.*from-policy=(\d+)/, "$1"
  pid = from.split('=')[1] if from
  nowPos = parseInt nowPos.split('=')[1], 10 if nowPos
  now = now.split('=')[1] if now
  # alert "#{pid}, #{nowPos}"
  
  $renderTo = $('#policy-add')
  if pid 
    policyAdd = new Policy pid, nowPos
  else
    policyAdd = new Policy 
  @ppAdd = new PolicyPresenter policyAdd, $renderTo, "edit"

  # 根据房间号来获取策略
  # 废弃！
  href = window.location.href
  roomId = href.match(/.*\?roomId=(\d+)$/)
  if roomId
    roomId = roomId[1]
  $policyList = $('#policy-list')
  if roomId
    $.ajax
      url: "/policy/room/#{roomId}/"
      type: "GET"
      success: (data) ->
        source = $("#policy-list-template").html()
        template = Handlebars.compile(source)
        html = template {policys: data.body}
        $policyList.html(html)
      fail: () ->
        alert "获取房间#{roomId}的策略失败，请检查网络连接！"

  $('#create-policy-form').submit (e) ->
    e.preventDefault() if e
    if not confirm("提交之后不能修改，只能新建，请仔细检查。") then return 0
    $form = $(this)
    description = $('input#description', $form).val()
    rules = policyAdd.data
    if description is "" or rules.length is 0
      alert "描述，策略不能为空"
      return 0
    # console.log description, policyAdd.data
    $.ajax
      url: "/policy/create/"
      type: "POST"
      data:
        description: description
        rules: JSON.stringify rules
      success: (data) ->
        # console.log "[create policy return]: ", data
        if data.code is 0
          window.location.href = "/policy/#{data.body}/"
        else
          alert data.body
      fail: () ->
        alert "创建策略失败，请检查网络连接。"


  # 如果now存在，则说明是从正在执行的表转移过来的，那么需要做一些修正
  # 标记不能编辑的项
  
  # $('.policy tbody').on 'rendern.policy.mr', (e) ->
  #   $(this).children().each (index, tr) ->
  #     $tr = $(tr)
  #     if index < nowPos
  #       $('td:last-child', $tr).html("不能修改这项")
  #       $tr.addClass('pre-playing')
  #     else if index == nowPos
  #       $lastChild = $('td:last-child', $tr)
  #       setInterval () ->
  #          $lastChild.html("现在正在执行")
  #       , 1000
  #       $tr.addClass('now-playing')
        
  # 提示用户现在应该从那个时间开始算起
  if nowPos >= 0
    nowAlert = "<div class=\"alert alert-warning alert-dismissable\">
      <button type=\"button\" class=\"close\" data-dismiss=\"alert\" aria-hidden=\"true\">&times;</button>
      以下从可以编辑的地方开始，都是相对<strong style=\"font-size: 1.2em; color: black;\">#{now}</strong>进行的，请格外注意。
      还有请注意编辑的速度，避免造成贻误现象出现。
      </div> "
    $('.policy').prepend(nowAlert)
  
  return 

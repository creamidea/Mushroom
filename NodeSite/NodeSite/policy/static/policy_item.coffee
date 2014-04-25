$ ->

  pid = (window.location.pathname).replace(/\/policy\/(\d+)\//g, "$1")
  console.log pid

  # 这里是策略的具体情况区域 
  $renderTo = $('#policy')
  policy = new Policy pid
  new PolicyPresenter policy, $renderTo, "view"
  btnNewPolicy = "<a href=\"/policy/create/?from-policy=#{pid}\"><button class=\"btn btn-success\">在此基础上新建</button></a>"
  # 下面是使用按钮替换掉原来的那个增加表单 
  $('.policy-add', $renderTo).html(btnNewPolicy)

  # 加载正在执行的策略
  $policyNow = $('#policy-now')
  $.ajax
    url: "/policy/#{pid}/now/"
    type: "GET"
    success: (data) ->
      # console.log "[policy #{pid} now]:", data
      source = $('#policy-now-template').html()
      template = Handlebars.compile(source)
      rooms = data.body
      for room in rooms
        {roomId, roomDesc, now, rules} = room
        html = template
          roomId: roomId
          roomDesc: roomDesc
          context: rules
        
        $policyNow.append(html)

        # 标记正在执行的策略
        nowPos = 0                #使用闭包，将下面函数的值传出 
        $("#room-#{roomId} table tbody", $policyNow).children()
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
        
        $("#room-#{roomId} a").attr('href',
          encodeURI("/policy/create/?from-policy=#{pid}&&nowPos=#{nowPos}&&now=#{now}"))

    fail: () ->
      alert "获取该策略正在执行情况失败，请检查网络连接。"


  # ========================================
  # 计划列表呈现区域
  # 
  # 新建一个实例，也就是提交计划策略表
  $policyPlanSection = $('#policy-plan-section')
  $policyPlanList = $('#policy-plan-list')
  renderPlanList = (plan) ->
    if not _.isArray(plan) then return -1
    source = $('#policy-plan-template').html()
    template = Handlebars.compile(source)
    html = template {plan: plan}

  # 提交创建策略实例的表单处理逻辑
  $policyPlanForm = $('#policy-plan form')
  getData = ($elt, url, isShow) ->
    $.ajax
      url: url
      type: "GET"
      success: (data) ->
        source = $("#dropdown-template").html()
        template = Handlebars.compile source
        console.log "[room desc list]:", data
        html = template {rooms: data.body, isShow: isShow}
        $dropdown = $elt.siblings('.dropdown')
        # console.log $dropdown
        if $dropdown.length is 0
          $(html).insertAfter $elt
        else
          $dropdown.replaceWith $(html)
      fail: () ->
        alert "获取房间描述列表失败，请检查网络连接。"
  showDropdown = (e) ->
    $elt = $(this)
    target = $elt.attr("name")
    switch target
      when "roomDesc"
        url = "/room/description/list/"
        isShow = false
      when "plantName"
        url = "/plant/name/list/"
        isShow = true
    getData($elt, url, isShow)
  hideDropdown = (e) ->
    $elt = $(this)
    # $elt.siblings('div.dropdown').hide()
  getChoice = (e) ->
    console.log e
    $elt = $(this)
    name = $.trim($elt.text())
    $dropdown = $elt.closest('.dropdown')
    $input = $dropdown.siblings('input')
    $input.val(name)
    $dropdown.remove()

  plantName =
    remove: (e) ->
      if not confirm("你确定奥删除吗？") then return -1
      $button = $(this)
      $li = $button.closest('li')
      $a = $button.siblings('a')
      name = $.trim($a.text())
      plantId = $li.attr('mr-id')
      alert plantId+":"+name
      $.ajax
        url: "/plant/#{plantId}/"
        type: "DELETE"
        context: {$li: $li}
        data:
          plantName: name
        success: (data) ->
          if data.code is 0
            @$li.remove()
          else
            alert data.body
        fail: () ->
          alert "删除失败，请检查网络连接。"
    edit: (e) ->
      $i = $(e.target)
      $button = $i.parent()
      $a = $button.siblings('a')
      # 变成输入框
      input = "<input type=\"text\" name=\"plant-name\" style=\"width: 72%\" value=\"#{$.trim($a.text())}\" old-value=\"#{$.trim($a.text())}\"/>"
      $a.replaceWith $(input)
      # 变成确认
      $i.removeClass('glyphicon-pencil').addClass('glyphicon-ok')
      $button.attr("action", "edited-plantname")

    edited: (e) ->
      if e.type is "keypress"
        if e.which is 13
          $input = $(this)
          $i = $input.siblings('button').find('i')
      else
        $i = $(e.target)
        $button = $i.parent()
        $input = $button.siblings('input')
      $li = $input.closest('li')
      plant_id = $li.attr('mr-id')
      console.log e
      oldPlantName = $.trim($input.attr('old-value'))
      plantName = $.trim($input.val())

      $.ajax
        url: "/plant/#{plant_id}/name/"
        type: "PUT"
        data:
          name: plantName
        success: (data) ->
          if data.code is 0
            # 变成a
            a = "<a role=\"menuitem\" tabindex=\"-1\" href=\"javascript:void(0)\" style=\"float: left\">#{plantName}</a>"
          else
            a = "<a role=\"menuitem\" tabindex=\"-1\" href=\"javascript:void(0)\" style=\"float: left\">#{oldPlantName}</a>"
          $input.replaceWith $(a)
          # 变成编辑
          $i.removeClass('glyphicon-ok').addClass('glyphicon-pencil')
          $button.attr("action", "edit-plantname")
          e.preventDefault()
        fail: () ->
          alert "修改失败，请检查网络连接。"
      
      
  $policyPlanSection.on 'focusin', 'input[data-api=mr-dropdown]', showDropdown
  $policyPlanSection.on 'focusout', 'input[data-api=mr-dropdown]', hideDropdown
  $policyPlanSection.on 'click', '.dropdown li a', getChoice
  $policyPlanSection.on 'click', 'button[action=remove-plantname]', plantName.remove
  $policyPlanSection.on 'click', 'button[action=edit-plantname]', plantName.edit
  $policyPlanSection.on 'click', 'button[action=edited-plantname]', plantName.edited
  $policyPlanSection.on 'keypress', 'li input[name=plant-name]', plantName.edited
  
  submitPlan = (e) ->
    e.preventDefault() if e
    # console.log e
    # console.log "data: ", policy.data
    metaA = $(e.target).serializeArray()
    meta = {}
    for m in metaA
      meta[m.name] = m.value
    console.log meta
    $.ajax
      url: "/policy/instance/create/"
      type: "POST"
      data:
        pid: pid
        roomDesc: meta.roomDesc
        plantName: meta.plantName
        startDate: meta.startDate
        startTime: meta.startTime
        policy: JSON.stringify(policy.data)
      success: (data) ->
        # 成功之后在下面添加
        # console.log data
        if data.code is 0
          policyInstanceId = data.body
          meta["policyInstanceId"] = policyInstanceId
          html = renderPlanList [meta]
          $policyPlanList.append(html)
          $policyPlanList.trigger $.Event('appendn.planlist.mr')
        else
          alert data.body
      fail: () ->
        alert "创建策略实例失败，请检查网络连接。"
  $policyPlanForm.on 'submit', submitPlan

  # 获取计划列表
  $.ajax
    url: "/policy/#{pid}/plan/list/"
    type: "GET"
    success: (data) ->
      # console.log "[plan policy]:", data
      html = renderPlanList data.body
      $policyPlanList.append(html)
      
      $policyPlanList.trigger $.Event('rendern.planlist.mr')
      
    fail: (data) ->
      alert "获取计划中的策略失败，请检查网络连接。"
  pickerListen =
    add: (e) ->
      # console.log e
      console.log this
      $elt = $(e.target)
      $('.datepicker', $elt).pickadate
        today: '今日'
        clear: '清除'
        format: 'yyyy/mm/dd'
      $('.timepicker', $elt).pickatime
        format: 'HH:i'
        editable: true
    
  $policyPlanList.on 'rendern.planlist.mr', pickerListen.add
  $policyPlanList.on 'appendn.planlist.mr', pickerListen.add
  $policyPlanList.on 'update.planlist.mr', pickerListen.add

  # 修改实例部分
  editingEvent = (e) ->
    $self = $(this)
    $li = $self.closest("li")
    $li.find("input").each (index, elt) ->
      $(elt).show()
    $li.find("span").each (index, elt) ->
      $(elt).hide()
    $self.find("i").removeClass("glyphicon-pencil").addClass("glyphicon-ok")
      .end()
      .attr("action", "edited")
  editedEvent = (e) ->
    $self = $(this)
    $li = $self.closest("li")
    piid = $li.attr('policy-instance-id')
    data = {}
    $li.find("input").each (index, elt) ->
      $elt = $(elt)
      data[$elt.attr("name")] = $.trim($elt.val())
    # console.log "????", data
    data.policyInstanceId = piid
    $.ajax
      url: "/policy/instance/#{piid}/"
      type: "PUT"
      data: 
        roomDesc: data.roomDesc
        plantName: data.plantName
        startAt: "#{data.startDate} #{data.startTime}"
      context: {data: data}
      success: (data) ->
        if data.code is 0
          html = renderPlanList [@data]
          $li.replaceWith(html)
          $policyPlanList.trigger $.Event('update.planlist.mr')
        else
          alert data.body
      fail: () ->
        alert "修改实例失败，请检查网络连接。"
    
    $li.find("input").each (index, elt) ->
      $(elt).hide()
    $li.find("span").each (index, elt) ->
      $(elt).show()
    $self.find("i").removeClass("glyphicon-ok").addClass("glyphicon-pencil")
      .end()
      .attr("action", "editing")
  # 删除实例
  removeEvent = (e) ->
    $self = $(this)
    $li = $self.closest("li")
    piid = $li.attr('policy-instance-id')
    $.ajax
      url: "/policy/instance/#{piid}/"
      type: "DELETE"
      context: {"$li": $li}
      success: (data) ->
        # alert data.body
        @$li.remove()
      fail: () ->
        alert "发送删除策略实例失败， 请检查网络连接。"

  $('#policy-plan-list').on 'click', 'button[action=editing]', editingEvent
  $('#policy-plan-list').on 'click', 'button[action=edited]', editedEvent
  $('#policy-plan-list').on 'click', 'button[action=remove]', removeEvent


  # ========================================


  renderDoneList = (done) ->
    if not _.isArray(done) then return -1
    source = $('#policy-done-template').html()
    template = Handlebars.compile(source)
    html = template {done: done}
  $policyDoneList = $("#policy-done-list")
  
  # 获取已经执行的策略
  $.ajax
    url: "/policy/#{pid}/done/list/"
    type: "GET"
    success: (data) ->
      # console.log "[POLICY DONE]:", data
      html = renderDoneList data.body
      $policyDoneList.html html
    fail: (data) ->
      alert "获取完成的策略实例失败，请检查网络连接。"

  saveOutput = (e) ->
    e.preventDefault() if e
    $form = $(this)
    piid = $form.closest('li').attr('policy-instance-id')
    output = $form.find('[name=output]').val()
    $.ajax
      url: "/policy/instance/#{piid}/output/save/"
      type: "POST"
      data: {"output": output}
      success: (data) ->
        if data.code is 0
          btnEdit = '''
                    <button type="button" class="close" action="edit-output" >
                      <i class="glyphicon glyphicon-pencil"></i>
                    </button>
                    '''
          $span = $form.siblings('p.output').find("span")
          $span.html(output+btnEdit)
          $form.hide()
        else
          alert data.body
      fail: () ->
        alert "存储产量值失败，请检查网络连接。"
  editOutput = (e) ->
    $elt = $(this)
    $li = $elt.closest('li')
    $("form[action=save-output]", $li).show().find("[name=output]").focus()
  $policyDoneList.on 'submit', 'form[action=save-output]', saveOutput
  $policyDoneList.on 'click', 'button[action=edit-output]', editOutput
  
  editImage = (e) ->
    $elt = $(this)
    $li = $elt.closest('li')
    $("form[type=save-image]", $li).show()
  $policyDoneList.on 'click', 'button[action=edit-image]', editImage

  # 删除产出的一个情况（产出值和图片）
  # 暂时废弃
  ajaxDelete = (outputId, $elt) ->
    $.ajax
      url: "/policy/delete/output/"
      type: "DELETE"
      data:
        outputId: outputId
      success: (data) ->
        $elt.remove()
      fail: (data) ->
        alert "删除失败！"
  $('#output-area ul').on 'click', 'button[action=remove]', (e) ->
    answer = confirm('你确定删除吗？')
    if answer
      $elt = $(this).closest('li')
      outputId = $elt.attr('output-id')
      ajaxDelete(outputId, $elt)


  # 开启时间选择插件
  $('.datepicker').pickadate
    today: '今日'
    clear: '清除'
    format: 'yyyy/mm/dd'
  $('.timepicker').pickatime
    format: 'HH:i'
    editable: true
    
  return

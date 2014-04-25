$ ->
  $policyList = $('#policy-list')
  $.ajax
    url: "/policy/list/"
    type: "GET"
    success: (data) ->
      console.log data
      source = $("#policy-list-template").html()
      template = Handlebars.compile(source)
      html = template {policys: data.body}
      $policyList.html(html)
    failed: () ->
      alert "GET POLICY LIST FAILED!"


  $policyList.on 'click', 'button[action=remove]', (e) ->
    $elt = $(this).closest('li')
    pid = $elt.attr('policy-id')
    answer = confirm('你确定删除吗？')
    if not answer then return
    $.ajax
      url: "/policy/#{pid}/"
      type: "DELETE"
      success: (data) ->
        if data.code is 0
          $elt.animate
            width: '10px'
          , 1000, ->
            $(this).remove()
        else
          alert data.body
      fail: () ->
        alert "删除失败，请稍候再试"
    return
    
  $policyList.on 'click', 'button[action=edit]', (e) ->
    $elt = $(this).closest('li')
    $input = $elt.find('input')
    $href = $elt.find('a')
    $input.show()
    $href.hide()

    $icon = $elt.find('button[action=edit] i')
    $icon.removeClass("glyphicon-pencil").addClass("glyphicon-ok")
    
    $elt.find('button[action=edit]').attr('action', 'editing')
    return

  editedEvent = (e)->
    $elt = $(e.target).closest('li')
    pid = $elt.attr('policy-id')
    $input = $elt.find('input')
    $href = $elt.find('a')
    value = $input.val()
    oldValue = $href.text()
    console.log pid, value, oldValue

    $icon = $elt.find('button[action=editing] i')
    $icon.removeClass("glyphicon-ok").addClass("glyphicon-pencil")
    $href.show()
    $input.hide()
    $elt.find('button[action=editing]').attr('action', 'edit')
    
    if value is "" or oldValue == value then return
    $.ajax
      url: "/policy/#{pid}/description/"
      type: "PUT"
      data:
        description: value
      success: (data) ->
        if data.code is 0
          $href.html("<strong>#{value}</strong>")
        else
          alert data.body
      fail: () ->
        alert "通信失败，请稍候再试"
  keypressEvent = (e) ->
    if e.which is 13 then editedEvent(e)
  $policyList.on 'click', 'button[action=editing]', editedEvent
  $policyList.on 'keypress', 'input[type=text]', keypressEvent

  return

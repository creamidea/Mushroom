$ ->
  # ######################################################
  # 核心世界
  # ######################################################

  window.location.hash = "!#/( ^_^)／□☆□＼(^-^ )"

  # 打印基础信息
  copyright = "CIT"
  version = "v0.0.1"
  console.log "Copyright: #{copyright}, Version: #{version}"

  router = new Router           #监听url地址栏中的变化，分发信号
  router.start()
  echo = new Echo               #启动信息提示框，采用默认配置
  echo.start()
  window.hint = echo.hint
  login = new Login

  username = ""
  sidebar = new Sidebar "#sidebar-template"
  roomList = new RoomList "#room-list"

  $smartTable = $("#smart-table")
  class Table
    constructor: (option) ->
      {@templateName, @$wrapper} = option
      @context = []              #内部存储数据列表
    click: (e) ->
      $li = $(e.target)
      action = $li.attr('action')
      switch action
        when "add"
          alert "add"
          
    _merge: (thead, tbody) ->
      _tbody = []
      for tr in tbody
        _tr = []
        for th in thead
          key = th["key"]
          type = th["type"]
          value = tr[key]
          _td =
            "key": key
            "type": type
            "value": value
          _tr.push _td
        _tbody.push _tr
      return _tbody
    init: (params) ->
      {thead, tbody} = params
      # 数据融合成我想要的样子
      # 将thead中type复制一份到tbody中去
      # len = thead.length
      @thead = thead || []
      @context = tbody
      @tbody = @_merge(thead, tbody)
      console.log @thead, @tbody
      @

    render: (option) ->
      @source = source = $(@templateName).html()
      template = Handlebars.compile(source)
      html = template({thead: @thead, tbody: @tbody})
      @$wrapper.append html       #渲染table head html

      @$table = @$wrapper.find("table") #table整体索引
      @$thead = @$table.find("thead")   #table head索引
      @$tbody = @$table.find("tbody")   #table body索引
      @$btnAddRow = @$wrapper.find("button[role=add-row]")

      @$addRow = @$tbody.find("tr:last-child").clone()
      @$table.append @$addRow
      @$addRow.attr("index", "-1").find("td p").html("").end().find("td input").attr("value", "")

      # 处理checkbox被选中/反选的情况
      @$tbody.delegate "input[type=checkbox]", "change", $.proxy(@check, @)
      # 处理修改之后的处理
      @$tbody.delegate "input[key]", "focusout", $.proxy(@update, @)
      @$menu = $(".table.menu")
      @$menu.delegate "li", "click", $.proxy(@click, @)
      @$btnAddRow.unbind("click").click (e) =>
        @$addRow.children().each (index, elt) =>
          if index > 0          #第一列是checkbox
            $input = $(elt).find("input")
            key = $input.attr("key")
            value = $input.val()
            # @add [{key: key, value: value}]
      @
    add: (record) ->
      # alert "eee"
      pattern = /<tbody.*>([\s\S]*)<\/tbody>/m
      tbodySource = @source.match pattern
      tbodySource = tbodySource[1]
      template = Handlebars.compile(tbodySource)
      tbody = @_merge(@thead, record)
      html = template({tbody: tbody}) #完成第一步渲染，后面需要更改其index

      context = @context
      len = context.length
      p = /(<tr index=\")(\d)(\"[\s\S]*)/m
      html = html.replace(p, "$1#{len}$3")
      $(html).insertBefore(@$addRow)
      @$addRow.find("td p").html("").next().val("")
      # console.log html
      @context = context.concat record       #在真正加入数组之前，获得其indxe，这样就不要-1
      console.log @context
      
    update: (e) ->
      context = @context
      $input = $(e.target)
      index = $input.parent().parent().attr("index")
      key = $input.attr("key")
      context[index][key] = $input.val()
      console.log "context:", @context
    delete: () ->
    check: (e) ->
      context = @context
      $checkbox = $(e.target)
      isChecked = $checkbox.prop('checked')
      if isChecked
        $row = $checkbox.parent().parent()
        index = $checkbox.attr("index")
        answer = confirm("确定删除么？")
        if answer               #删除
          delete context[index]
          $row.remove()
          
  # t = new Table
  #   templateName: "#table-template"
  #   $wrapper: $smartTable
  # t.init
  #   thead: [
  #     {name: "时间", type: "time", key: "time"}
  #     {name: "采集值", type: "number", key: "value"}
  #   ]
  #   tbody: [{
  #     time: "22:08"
  #     value: "100"
  #   }, {
  #     time: "22:08"
  #     value: "100"
  #   }]
  # .render()
  # t.add [{
  #     time: "14:09"
  #     value: "110"
  #   }]
  #   templateName: "#table-body-template"
  # console.log "///////", t.context


  

  # 自动尝试性登录
  testLogin = new Post "/login-test/", (data) ->
    if data.code is "0"        #尝试登录失败
      $.publish "#login/", [data]
    else
      #登录界面，默认配置
      login.show()
  testLogin.send()

  # 登录成功之后发的信号，登录失败及其其他错误在login中或者Ajax中已经被处理掉了。
  $.subscribe "#login/", (e, data) ->
    context = data.definition
    username = context.username
    $.publish "#echo/", [{definition: "#{username} 欢迎回来"}]
    login.hide()

    # console.log context
    sidebar.renderTo "#sidebar", context
    # sidebar.hide()

    # 房间信息
    # roomList.fetch()
    roomList.fetch()

  # TODO: 应该使用路由，后期需要整改  
  $.subscribe "#logout/", (e) ->
    # alert "logout"
    logout = new Post "/logout/", (data) ->
      console.log "sidebar", sidebar
      sidebar.hide()
      # roomList.hide()
      $.publish "#echo/", [{definition: data.definition}]
      window.location.reload()
      # window.location.hash = ""
      # login.show()
    logout.send()

  $config = $('#config form')
  $config.submit (e) ->
    e.preventDefault()
    type = $config.find('select option:selected').val()
    # alert type
    get = new Get "/config/log/#{type}", (data) ->
      $.publish "#echo/", [data]
    get.send()

  $.subscribe "#config/", (e) ->
    alert "config"
    roomList.hide()
    
  return

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
  login = new Login

  username = ""
  sidebar = new Sidebar "#sidebar-template"
  roomList = new RoomList "#room-list"
  roomList.fetch({isRender: true})
      
  # 自动尝试性登录
  testLogin = new Post "/login-test/", (data) ->
    if data.code is "0"        #尝试登录失败
      $.publish "#login", [data]
    else
      #登录界面，默认配置
      login.show()
  testLogin.send()

  # 登录成功之后发的信号，登录失败及其其他错误在login中或者Ajax中已经被处理掉了。
  $.subscribe "#login", (e, data) ->
    context = data.definition
    username = context.username
    $.publish "#echo", [{definition: "#{username} 欢迎回来"}]
    login.hide()

    # console.log context
    sidebar.renderTo "#sidebar", context
    # sidebar.hide()

    # 房间信息
    # roomList.fetch()

  # TODO: 应该使用路由，后期需要整改  
  $.subscribe "#logout", (e) ->
    # alert "logout"
    logout = new Post "/logout/", (data) ->
      console.log "sidebar", sidebar
      sidebar.hide()
      # roomList.hide()
      $.publish "#echo", [{definition: data.definition}]
      window.location.reload()
      # window.location.hash = ""
      # login.show()
    logout.send()
    
  return

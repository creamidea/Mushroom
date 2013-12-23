$ ->
  # 打印基础信息
  copyright = "CIT"
  version = "v0.0.1"
  console.log "Copyright: #{copyright}, Version: #{version}"
  #启动信息提示框，采用默认配置
  echo = new Echo
  #登录界面，默认配置
  login = new Login
  login.show()
  
  $.subscribe "/login/", (e, data) ->
    $.publish "/echo/", [{definition: '登录成功'}]
    login.hide()

  source   = $("#entry-template").html()
  template = Handlebars.compile(source)
  context =
    "title": "My New Post"
    "body": "This is my first post!"
  html    = template(context);
  $('body').append(html)
    
  return

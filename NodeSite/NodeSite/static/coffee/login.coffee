class Login
  # alert 'ice'
  constructor: (uri) ->
    @$login = $login = $('#login')
    @$username = $login.find('input[name=username]')
    @$password = $login.find('input[name=password]')
    $btnLogin = $login.find('button[type="submit"]')
    @loginURI = uri || '/login/'
    # 单击事件处理
    $login.submit $.proxy(@handler, this)
  show: ->
    $login = @$login
    $login.show()
  hide: ->
    $login = @$login
    $login.hide()
  handler: (e) ->
    e.preventDefault()
    username = @$username.val()
    password = @$password.val()
    loginURI = @loginURI
    if username and password
      alert "#{username}: #{[password]}"
      login = new Post loginURI, (data) ->
        $.publish "/login/", [data]
      # 发送信息
      login.send
        "username": username
        "password": password
    else
      $.publish "/echo/", [{code: -1, definition: 'Error, who are you?'}]
      # alert "Some Error. Who know?"

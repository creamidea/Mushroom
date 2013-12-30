class Login
  # alert 'ice'
  constructor: (uri) ->
    @$login = $login = $('#login')
    @$username = $login.find('input[name=username]')
    @$password = $login.find('input[name=password]')
    @$remember = $login.find('input[name=remember]')
    @$btnLogin = $btnLogin = $login.find('button[type="submit"]')
    @loginURI = uri || '/login/'
    # 单击事件处理
    $login.submit $.proxy(@handler, this)
  show: ->
    $login = @$login
    $login.show()
  hide: ->
    $login = @$login
    $login.hide()
  btnDisable: ->
    @$btnLogin.html('登录中...').attr('disabled','disabled')
  btnEnable: ->
    @$btnLogin.html('登录').removeAttr('disabled')
  handler: (e) ->
    e.preventDefault()
    @btnDisable()
    username = @$username.val()
    password = @$password.val()
    if @$remember.prop('checked')
      remember = true
    else
      remember = false
    loginURI = @loginURI
    if username and password
      # alert "#{username}: #{[password]}: #{remember}"
      login = new Post loginURI, (data) =>
        if data.code is "-1"
          @btnEnable()
        else
          $.publish "#login", [data]
      , () =>
        @btnEnable()
      # 发送信息
      login.send
        "username": username
        "password": password
        "remember": remember
    else
      $.publish "#echo", [{code: -1, definition: 'Error, who are you?'}]
      @btnEnable()
      # alert "Some Error. Who know?"

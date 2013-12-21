$ ->
  # alert 'ice'
  $login = $('#login')
  $btnLogin = $login.find('button.login')
  loginURI = '/login/'
  $btnLogin.click ->
    username = $login.find('input[name=username]').val()
    password = $login.find('input[name=password]').val()
    if username and password
      alert "#{username}: #{[password]}"
      login = new Post loginURI, (data) ->
        console.log data
      login.send
        "username": username
        "password": password
    else
      alert "Some Error. Who know?"
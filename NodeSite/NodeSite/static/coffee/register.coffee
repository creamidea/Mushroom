# 用于注册的类
class Register extends Frame
  # 构造函数
  constructor: (@templateName) ->
    super(@templateName)

  # 渲染函数
  renderTo: (target, context) ->
    super(target, context)
    @submit()
    # console.log @$el
  # 表单提价事件
  submit: () ->
    $form = @$el
    $username = $form.find("input[name=username]")
    $password1 = $form.find("input[name=password1]")
    $password2 = $form.find("input[name=password2]")
    $email = $form.find("input[name=email]")
    $group = $form.find("select[name=group]")
    $form.submit (e) =>
      e.preventDefault()
      e.stopPropagation()
      username = $username.val()
      password1 = $password1.val()
      password2 = $password2.val()
      email = $email.val()
      group = $group.val()
      # alert username+password1+password2+email+group
      if password1 is password2
        post = new Post "/register/", (data) ->
          window.hint(data)
        post.send
          username: username
          password1: password1
          password2: password2
          email: email
          group: group

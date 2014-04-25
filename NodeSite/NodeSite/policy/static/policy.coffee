'use strict'
# 使用方式
# policy = new Policy [:pid]
# new PolicyPresenter policy, $renderTo, ["edit"/"view"]
# ################################
# console.log "here is show policy"

class Policy
  constructor: (@pid, @nowPos) ->
    $.observable @
    @data = []
    @syncInterval = 5000
    @saveInterval = 4000

  add: (data, insertIndex) ->
    if arguments.length > 0

      # console.log "add: ", data
      __data = @data
      
      length = __data.length

      if 0 <= insertIndex and insertIndex < length
        # 插入中间
        prefix = __data.slice(0, insertIndex)
        affix = __data.slice(insertIndex)
        @data = [].concat prefix, data, affix
        # @data = _.union prefix, records, affix
      else 
        # @data.concat records
        # console.log data, records
        # @data = _.union data, records
        @data = __data.concat data
      # @data.push [data, false]
      # console.log "after add: ", @data
      @flagEdit()                  #为每一条数据打上是否允许被编辑的标志
      @trigger "add", @data
    
  remove: (index) ->
    # console.log "remove..."
    if index isnt undefined or index isnt null
      @data.splice index, 1
      @trigger "remove", @data
      # console.log "after remove", @data

  update: (data, index) ->
    if arguments.length is 1
      # 这里说明是一个数组传入，也就是批量传入
      # console.log data, @data
      if not _.isEqual(data, @data)
        @data = data
        @trigger "update", @data
    else
      # 更改指定位置的值
      data["isEdit"] = true
      @data[index] = data
      @trigger "update", @data
    # if _.isNumber(@nowPos) and @nowPos >= 0
    #   @flagEdit()                  #为每一条数据打上是否允许被编辑的标志
    # console.log "after update:", @data

  flagEdit: () ->
    # 这里处理一下，加上是否允许被编辑的标志
    # 这里只是简单处理一下，这里如果数据变大会有性能问题
    # 这里又犯了一个错误，0是会被判为false，于是就不会被执行了！！！
    nowPos = @nowPos
    data = @data
    for item, index in data
      # console.log index, nowPos
      @data[index]["isEdit"] = true
      if _.isNumber(@nowPos) and @nowPos >= 0
        if index <= nowPos
          @data[index]["isEdit"] = false

  get: () ->
    if not @pid then return -1
    $.ajax
      url: "/policy/#{@pid}/"
      type: "GET"
      success: (data) =>
        # console.log "GET POLICY:", data
        body = data.body
        if @data.length is 0
          # console.log "BODY:", body
          @add body.policy
        else
          @update body
      fail: () ->
        alert "Policy sync failed!"

  sync: (syncInterval) ->
  # 用于查看view模式下的策略与服务器同步
    if not @pid then return
    if _.isNumber(syncInterval)
      @syncInterval = syncInterval
      setInterval =>
        @get()
      , @syncInterval

  save: () ->
  # TODO:本来是想保存用户修改的每一个版本
  # 后来想想没有必要，只保存用户最近一次的修改
    # date = new Date()
    # key = date.toLocaleString()
    key = @saveKey = "policySave"
    setInterval =>
      if @data.length > 0
        value = JSON.stringify(@data)
        # console.log "save...", @data, value
        localStorage[key] = value
    , @saveInterval

  load: (key) ->
    key = @saveKey
    @data = JSON.parse(localStorage[key])
    @add()
    # if _.isDate(new Date(key))
    #   @data = JSON.parse(localStorage[key])
    #   @add()

class PolicyPresenter
  constructor: (model, @$wrpelt, @mode) ->
    # model.on "add", $.proxy @add, @
    # model.on "remove", $.proxy @remove, @
    # model.on "update", $.proxy @update, @
    model.on "add", $.proxy @render, @
    model.on "update", $.proxy @render, @
    model.on "remove", $.proxy @render, @
    @model = model
    
    source = $("#policy-out-template").html()
    template = Handlebars.compile(source)
    html = template {title: "策略"}
    # console.log source, h
    @$wrpelt.html html

    @recordTpl= Handlebars.compile(policyRecordTpl)
    @$policy = $('tbody', @$wrpelt)

    if @mode is "view"
      @model.get()
      @isEdit = false
      # @model.sync()

    if @mode is "edit"
      @model.get()
      @isEdit = true
      # @model.save()

      # @saveUI()
      
      template = Handlebars.compile(policyAddTpl)
      html = template()
      $add = $(html).appendTo $('.policy-add', @$wrpelt)
      $add.submit $.proxy @addEvent, @

      @$policy.on "click", "button[action=remove]", $.proxy @removeEvent, @
      @$policy.on "click", "button[action=edit]", $.proxy @editEvent, @
      @$policy.on "click", "button[action=confirm]", $.proxy @updateEvent, @
      @$policy.on "keypress", "tr td input", $.proxy @updateEvent, @

      # 显示策略提交表格
      # template = Handlebars.compile(postFormTpl)
      # html = template()
      # $postForm = $(html).appendTo $('.post-form-wrapper', @$wrpelt)
      # # $postForm.submit $.proxy @postEvent, @
      # $('form[name=post-form]', @$wrpelt).submit $.proxy @postEvent, @

  postEvent: (e) ->
    e.preventDefault() if e
    # console.log e
    # console.log "data: ", @model.data
    metaA = $(e.target).serializeArray()
    meta = {}
    for m in metaA
      meta[m.name] = m.value
    $.ajax
      url: "/policy/create/"
      type: "POST"
      data:
        roomId: meta.roomId
        description: meta.description
        startDate: meta.startDate
        startTime: meta.startTime
        policy: JSON.stringify(@model.data)
      success: (data) ->
        # console.log data
        alert data.body
      fail: () ->
        alert "POST POLICY FAILED!"
        
  removeEvent: (e) ->
    # console.log "remove event:", e
    $tr = $(e.target).closest("tr")
    index = $tr.index()
    answer = confirm("你确定删除吗？")
    if answer
      @model.remove index

  updateEvent: (e) ->
    $input = $(e.target)
    $td = $input.closest("td")
    $tr = $td.closest("tr")
    if e.which is 13 or e.type is "click"
      index = $tr.index()
      data = {}
      $('input', $tr).each (index, elt) ->
        $elt = $(elt)
        name = $elt.attr("name")
        if name in ["date", "hour"]
          data[name] = parseInt($elt.val(), 10)
        else if name is "light"
          data[name] = $elt.val()
        else
          [name, index] = name.split('-')
          if data[name] is undefined
            data[name] = []
          data[name][index] = parseFloat($elt.val())
        # console.log data
      @model.update(data, index)

  editEvent: (e) ->
    $elt = $(e.target)
    $elt.removeClass("glyphicon-pencil").addClass("glyphicon-ok")
    $elt.closest("button").attr("action", "confirm")
    # console.log $elt
    $tr = $elt.closest("tr")
    $('input', $tr).show().each (index, elt) ->
      # console.log index
      $elt = $(elt)
      if index == 0 then $elt.focus().select()
      value = $elt.siblings('p').text()
      $(elt).val(value)
    $('p', $tr).hide()
    # console.log e, $tr

  # editn: (data, index) ->
  #   @
  #   $tr = $(e.target).closest("tr")
  #   $('p', )
  addEvent: (e) ->
    e.preventDefault() if e
    # console.log e
    # console.log( $( e.target ).serialize() );
    serialize = $(e.target).serializeArray()
    serializeLen = serialize.length
    insertPosition = parseInt(serialize[serializeLen-1].value, 10)
    # alert insertPosition
    # delete serialize[serializeLen-1]
    # console.log insertPosition
    if isNaN(insertPosition)
    # 无效字符插入最后一行
      insertPosition = @model.data.length
    else if insertPosition <= 0
      insertPosition = 1
    # console.log insertPosition, @model.data[insertPosition]
    # data = @model.data[insertPosition]
    # $.extend data,data
    # console.log ">>>data:", data
    preData = @model.data[insertPosition-1]
    data = {}
    # console.log "serialize: ", serialize
    for s in serialize
      # console.log s.name
      if s.name is "insertPosition" then break
      if s.name in ["date", "hour", "light"]
        if s.value is ""
          data[s.name] = preData[s.name]
        else
          data[s.name] = s.value
      else
        # console.log s.name
        [name, index] = s.name.split('-')
        if data[name] is undefined
          data[name] = []
        value = parseFloat(s.value)
        if isNaN(value)
          data[name][index] = preData[name][index]
        else
          data[name][index] = parseFloat(s.value)

    # console.log insertPosition, @model.data.length
    if insertPosition < @model.data.length
    # model内部增加时，逻辑上没有平移一个位置，这里需要修正一下
      @model.add data, insertPosition - 1
      # top = @$policy.children()[insertPosition-1].offsetTop
      # @$policy.children(":nth-child(#{insertPosition-1})")
    else
      @model.add data, insertPosition
      # top = @$policy.children()[insertPosition].offsetTop
      # @$policy.children(":nth-child(#{insertPosition-1})")
      
    # console.log "1000>>>>", @$policy.children(":nth-child(#{insertPosition-1})")
    # $('.middle', @$wrpelt).animate
    #   scrollTop: top
    # , 1000

    # console.log data
    #
    # $(window).resize () ->
      #

  reflush: () ->
  # 刷新每一行前面的序号
  # 以及充值是否可以编辑
    nowPos = @nowPos || -1
    @$policy.children().each (index, elt) ->
      $elt = $(elt)
      id = index + 1
      $elt.children(":first").html "<p>#{id}</p>"
      if index <= nowPos
        $('td:last-child', $(elt)).remove()
      
  render: (data) ->
    # console.log "render data:", data
    # if _.has(data[0], 'policy')
    #   policy = data[0].policy
    # else
    policy = data
    Handlebars.registerHelper "number", (context) ->
      return context.data.index + 1
    # console.log "POLICY:", policy
    html = @recordTpl {context: policy, isEdit: @isEdit}
    # console.log html
    @$policy.html html
    # 出发策略渲染完成事件
    @$policy.trigger($.Event("rendern.policy.mr"))
    # console.log @$policy.children(":last-child")

  saveUI: () ->
    html = []
    for key, value of localStorage
      # console.log key, value
      html.push "<p fade in><a href='#/policy/#{key}'>#{key}</a><button type='button' class='close' aria-hidden='true' action='remove-save'><i class='glyphicon glyphicon-remove'></i></button></p>"
    $el = $('.save-policy', @$wrpelt).html(html.join(''))
    $('a', $el).click (e) =>
      e.preventDefault() if e
      $elt = $(e.target) 
      key = $elt.text()
      $closest = $elt.closest('p')
      $closest.siblings('p')
        .each( -> $(this).removeClass("active"))
        .end().addClass("active")
      @model.load key
    $("button[action=remove-save]", $el).click (e) ->
      answer = confirm("你确定删除吗？")
      $button = $(e.target).closest("button")
      if answer
        key = $button.siblings("a").text()
        # console.log key
        delete localStorage[key]
        $button.alert('close')
      
    # $('p', $el).bind "close.bs.alert", (e) ->
    #   console.log "this", this, e
    #   answer = confirm("你确定删除吗？")
    #   $p = $(e.target)
    #   if answer
    #     # console.log arguments
    #     key = $('a', $p).text()
    #     # console.log key
    #     delete localStorage[key]
    #   else
    #     index = $p.index()
    #     alert index
    #     e.isDefaultPrevented = () ->
    #       return false
    #     $p.appendTo $('body')
    #     console.log $p

# savePolicyTpl = '''
#   {{#each policy}}  
#   <p fade in>
#     <a href=#/policy/{{@key}}>{{@key}}</a>
#       <button type="button" class="close" action="remove-save">
#         <i class="glyphicon glyphicon-remove"></i>
#       </button>
#   </p>
#   {{/each}}
# '''

    
# compileTemplate = (templateName) ->
#   source = $(templateName).html()
#   template = Handlebars.compile source

# RecordView =
#   # 这里用于渲染每一条记录
#   # signalton
#   templateName: "#policy-record-template"
#   render: (opt) ->
#     {records, isEdit} = opt
#     # console.log "RecordView:", isEdit
#     if not $.isArray records
#       temp = records
#       records = [temp]
#     template = compileTemplate @templateName
#     template {"policy":records, "isEdit": isEdit}

# class PolicyMetaView
#   # 这里负责策略元信息的显示
#   templateName: "#policy-meta-template"
#   constructor: (opt) ->
#     {$renderTo, isEdit} = opt
#     # @$el为外层元素，包裹信息

#     # 绑定事件
#     if isEdit
#       $renderTo.on "dblclick", "p", $.proxy @editing, @
#       $renderTo.on "blur keypress", "input", $.proxy @edited, @
#       # $renderTo.on "keypress", "input", $.proxy @keypress, @
#       @editItem = ["description"]
      
#     @$renderTo = $renderTo


#   keypress: (e) ->
#     e.stopPropagation()
#     code = e.which
#     switch code
#       when 13 then @edited e
#       else return

#   editing: (e) ->
#     $p = $(e.target)
#     $input = $p.siblings "input"
#     $input.show().val($p.text()).focus().select()
#     $p.hide()

#   edited: (e) ->
#     # console.log arguments
#     if e.type is "keypress"
#       if e.which isnt 13 then return
#     # if e.type isnt "focusout" then return
#     $input = $(e.target)
#     $p = $input.siblings "p"
#     value = $input.val()
    
#     name = $input.attr("name")
#     oldValue = @meta[name]
#     if value is "" or oldValue is value then return #与旧值比较
#     @meta[name] = value  #将其作为新值存入容器，为render提供数据
#     console.log ">>>", @meta

#     $input.hide()
#     $p.show()
#     @render()
    
#     if name is "description"
#       # 这里是更新策略描述的地方
#       policyId = $input.attr("policy-id")
#       if policyId is undefined or policyId is null then return
#       $.ajax
#         url: "/policy/#{policyId}/description/"
#         type: "PUT"
#         data:
#           description: value
#         success: (data) =>
#           alert data.body
#           @render()
#         fail: (data) ->
#           alert "更新失败，请重试"
#     # else
#     #   # 这里说明是创建一个全新的策略，而不是对其修改
#     #   @render()

#     e.stopPropagation()

#   render: (meta) ->
#     if not meta then meta = @meta else @meta = meta
#     # console.log meta
#     template = compileTemplate @templateName
#     $renderTo = @$renderTo
#     $renderTo.html template meta

# class PolicyAddView
#   # 这个是处理增加行的信息的
#   # 这个当单击增加按钮的时候会触发 add-record，这个有绑定的元素$renderTo触发
#   templateName: "#policy-add-record-template"
#   init: () ->
#     @record = 
#       date: ""
#       hour: ""
#       brightness: ""
#       humidity: []
#       temperature: []
#       co2: []
#       insertPosition: 0
#   constructor: (opt) ->
#     {$renderTo, isEdit} = opt
#     @init()
#     $renderTo.on "submit", "form", $.proxy @addEvent, @
#     $renderTo.on "blur keypress", "input", $.proxy @edited, @
#     @$renderTo = $renderTo
#     @isEdit = isEdit
#     # console.log $renderTo

#   addEvent: (e) ->
#     e.preventDefault()
#     # alert "hello"
#     record = @record
#     if record.data is "" or record.hour is ""
#       alert "间隔时间或者间隔天数不能为空"
#       return
#     selector = @$renderTo.selector
#     channel = selector.split(" ")[0]
#     # $.publish "/add/record/#{channel}"
#     @$renderTo.trigger "add-record"
#     @init()
#     _.extend @record, record    #使用underscore的extend，在保留上次值得基础之上，进行深拷贝，也就是避免直接等于时造成的引用，应为PolicyAddView在使用时使用的时同一个@record
#     e.stopPropagation()

#   edited: (e) ->
#     if e.type is "keypress"
#       if e.which isnt 13 then return
#     $input = $(e.target)
#     name = $input.attr("id")
#     value = $input.val()
#     # console.log $input, name, value
#     if name in ["date", "hour", "brightness", "insertPosition"]
#       # console.log name, value
#       @record[name] = value
#     else
#       [name, index] = name.split("-")
#       @record[name][index] = parseFloat value
#       # console.log name, index, value
#   render: () ->
#     template = compileTemplate @templateName
#     $renderTo = @$renderTo
#     $renderTo.html template {}
#     @$elt = $renderTo.find "[name=addition-form]"


# # 策略模型
# class Policy
#   # 这个是策略模型，用于对策略进行数组级别的增删改
#   constructor: () ->
#     @policys = []                 #存放记录的地方
#   check: (record) ->
#     # 这里是检查每一个传入的记录是否有置空项
#     # TODO: 如果置空，则默认是上一项的值
#     # console.log ">>>>>>", record
#     for key, value of record
#       if key in ["date", "hour", "brightness"] and value is null
#         console.log "string"
#         record[key] = "同上"
#       else if key in ["co2", "temperature", "humidity"] and value.length < 2
#         console.log "array"
#         if value[0] is undefined
#           value[0] = "同上"
#         if value[1] is undefined
#           value[1] = "同上"
#         record[key] = value
#     # console.log record
#     return [record]

#   add: (records, insertIndex=null) ->
#     policys = @policys
#     @policys = []
#     length = policys.length

#     if insertIndex isnt null and 0 <= insertIndex and insertIndex < length
#       # 插入中间
#       prefix = policys.slice(0, insertIndex)
#       affix = policys.slice(insertIndex)
#       @policys = @policys.concat prefix, records, affix
#       # @policys = _.union prefix, records, affix
#     else if insertIndex is null
#       # @policys.concat records
#       # console.log policys, records
#       # @policys = _.union policys, records
#       @policys = policys.concat records
#   remove: (index)->
#     # console.log "remove"
#     length = @policys.length
#     # alert index+" "+length
#     if index < 0 or index >= length then return
#     # delete @policys[index]
#     @policys.splice index, 1
#   update: (index, value)->
#     # console.log "policy update", index, _.isArray(value)
#     # if $.isNumeric index or value
#     # console.log "start update"
#     if _.isArray(value)
#       # console.log "array update"
#       [name, idx] = value[0].split("-")
#       _value = value[1]
#       # console.log name, index, _value
#       if name in ["temperature", "humidity", "co2"]
#         @policys[index][name][idx] = _value
#       else
#         @policys[index][name] = _value
#     else if _.isObject(value)
#       # Attention:
#       # 这里有一个「奇怪」的事情：
#       # console.log "object update"
#       @policys[index] = value
#     # console.log "end update"

# # 策略视图
# class PolicyView
#   # 这里是顶层的元素界面，或者说是外出包裹和主要的策略记录主体
#   # $el: $("#create-policy")
#   templateName: "#policy-out-template"
#   meta: null
#   isEdit: false
#   constructor: (context)->
#     {$renderTo, isEdit} = context
#     @$el = $renderTo
#     @isEdit = isEdit
#     # console.log renderTo, @$el
#   init: (context) ->
#     @model = new Policy       #写在这里是实例的属性
#     # 将数据渲染到界面
#     {roomId, policyId, description, policy} = context
#     template = compileTemplate @templateName
#     outHTML = template 
#       "title": "任务进行时"
#       "edit": @isEdit
#     $el = @$el
#     $el.html outHTML

#     # 绑定页面各个展示区域元素 
#     @$meta = $meta = $el.find "[name=meta]"
#     @$policys = $policys = $el.find "tbody"
#     @$policyAdd = $policyAdd = $el.find "[name=policy-add]"
#     # 创建meta
#     @meta = meta = new PolicyMetaView
#       $renderTo: $meta
#       isEdit: @isEdit
#     meta.render
#       "roomId": roomId
#       "policyId": policyId
#       "description": description
#       "isEdit": @isEdit
#       "today": (new Date()).toJSON()

#     # 创建增加行
#     if @isEdit
#       @addView = addView = new PolicyAddView
#         $renderTo:$policyAdd
#         isEdit: true
#       selector = $policyAdd.selector
#       addViewChannel = selector.split(" ")[0]
#       addView.render()
#       $policyAdd.on "add-record", $.proxy @addEvent, @

#       # 事件监听
#       $policys.delegate "tr td p", "dblclick", $.proxy @editing, @
#       $policys.delegate "tr td input", "blur", $.proxy @edited, @
#       $policys.delegate "tr td input", "keypress", $.proxy @keypress, @
#       $policys.delegate "tr td button", "click", $.proxy @removeEvent, @
#       # $.subscribe "/add/record/#{addViewChannel}", $.proxy @addEvent, @
#       $el.find("button[type=submit][name=post]").click $.proxy @submit, @

#   addEvent: (e) ->
#     # console.log @addView.record
#     # alert "add event"
#     record = @addView.record
#     @add record

#   keypress: (e) ->
#     e.stopPropagation()
#     # e.preventDefault();
#     code = e.which
#     switch code
#       when 13 then @edited(e)
#       else return

#   editing: (e) ->
#     # 编辑策略
#     # console.log e.target
#     elt = e.target
#     $elt = $(elt)
#     text = $elt.text()
#     $elt.siblings("input").val(text).show().focus().select()
#     $elt.hide()

#   edited: (e) ->
#     elt = e.target
#     $elt = $(elt)
#     $tr = $elt.closest("tr")
#     index = $tr.index()
#     name = $elt.attr("name")
#     if name in ["date", "hour", "brightness"]
#       value = $elt.val()
#       if value is "" then value = null
#     else
#       value = parseFloat $elt.val()
#       if isNaN(value) then value = null
#     if value isnt null
#       # console.log index, name, value
#       @update index, [name, value]
#     else
#       $elt.siblings("p").show()
#       $elt.val("").hide()
#     e.stopPropagation()

#   removeEvent: (e) ->
#     elt = e.target
#     $elt = $(elt)
#     # console.log $elt
#     index = $elt.closest("tr").index()
#     if confirm("你确定删除么？")
#       @remove(index)

#   submit: (e) ->
#     policys = @model.policys
#     $el = @$el
#     policys = JSON.stringify policys
#     meta = @meta.meta
#     {roomId, description} = meta
#     $el = @$el
#     startDate = $el.find("#start-date").val()
#     startTime = $el.find("#start-time").val()
#     time = "#{startDate} #{startTime}"
#     # $roomId = $el.find("p[name=meta]")
#     console.log roomId, description, "policys"
#     $.ajax
#       url: "/policy/"
#       type: "POST"
#       data:
#         roomId: roomId
#         description: description
#         policys: policys
#         time: time
#       success: (data) ->
#         alert data.body
#       fail: () ->
#         alert "fail"

#   check: (record) ->
#     # console.log ">>>>>>", record
#     for key, value of record
#       if key in ["date", "hour", "brightness"] and value is ""
#         record[key] = "-"
#       else if key in ["co2", "temperature", "humidity"] and value.length < 2
#         if value[0] is undefined
#           value[0] = "-"
#         if value[1] is undefined
#           value[1] = "-"
#         record[key] = value
#     # console.log record
#     return record

#   add: (records) ->
#     # 增加策略
#     # console.log "//////", records.insertPosition
#     model = @model
#     if $.isArray(records)
#       _records = []
#       for record in records
#         _records.push(@check(record))
#       records = _records
#     else
#       records = @check records
#       # console.log "<><><><>", records

#     insertPosition = parseInt(records.insertPosition, 10) - 1 #理解人类与计算机索引的区别
#     $policys = @$policys
#     length = model.policys.length
#     if insertPosition >= 0 and insertPosition < length
#       # 说明插入指定位置
#       records = [records]
#       # preRecord = model[insertPosition]
#       # 找到当前位置上的节点
#       $nowElt = $($policys[0].children[insertPosition])
#       recordsHTML = RecordView.render
#         records: records
#         isEdit: @isEdit
#       $(recordsHTML).insertBefore $nowElt
#       model.add records, insertPosition
#     else
#       # 插入末尾
#       recordsHTML = RecordView.render
#         records: records
#         isEdit: @isEdit
#       $policys.append recordsHTML
#       model.add records

#   remove: (index)->
#     # 移出策略
#     # console.log @$policys, index
#     $(@$policys[0].children[index]).remove()
#     @model.remove index
#     console.log "after remove:", @model.policys

#   update: (index, value) ->
#     # 更新策略
#     # console.log "policy view update"
#     # if @model.policys[index] is value then return
#     @model.update index, value
#     value = @model.policys[index]
#     recordsHTML = RecordView.render
#       records: value
#       isEdit: @isEdit
#     $(@$policys.children()[index]).html $(recordsHTML).children()
#     console.log "after update:", @model.policys


# PolicyList =
#   # 策略列表视图
#   templateName: "#policy-list-template"
#   # constructor: (opt) ->
#   #   {@$renderTo} = opt
#   render: (opt) ->
#     {policys, $renderTo} = opt
#     template = compileTemplate @templateName
#     $renderTo.html template {"policys": policys}

#     $renderTo.on "click", "li", $.proxy @clickEvent, @

#   clickEvent: (e) ->
#     $elt = $(e.target)
#     policyId = $elt.attr("policy-id")
#     # alert policyId
#     # 发一个GET获取具体的策略
#     getPolicyById
#       policyId: policyId

# getPolicyList = (opt) ->
#   # 获取策略列表的ajax
#   {$renderTo} = opt
#   $.ajax
#     url: "/policy/list/"
#     type: "GET"
#     success: (data) ->
#       # console.log data
#       PolicyList.render
#         policys: data.body
#         $renderTo: $renderTo
#     fail: (data) ->
#       alert "request policy fail"

# getPolicyById = (opt) ->
#   # 通过具体的policy id获得具体策略的ajax
#   {policyId, $renderTo} = opt
#   $.ajax
#     url: "/policy/#{policyId}"
#     type: "GET"
#     success: (data) ->
#       console.log data
#       policyView = new PolicyView
#         $renderTo: $("#policy-show-area")
#         isEdit: true
#       policyView.init
#         roomId: "双击编辑"
#         policyId: ""
#         description: "双击编辑"
#         policy: []
#       policyView.add data.body
#     fail: (data) ->
#       alert "request policy fail"

# getNowPolicy = (opt)->
#   # 获取正在执行的列表
#   {roomId, $renderTo} = opt
#   $.ajax
#     url: "/policy/now/room/#{roomId}/"
#     type: "GET"
#     success: (data) ->
#       policyView = new PolicyView
#         $renderTo: $renderTo
#         isEdit: false
#       policyView.init data.body
#       policyView.add data.body.policy
#     fail: (data) ->
#       alert "request policy fail"

        
#   # =================================================
#   # 链表实现的，但是暂时不这么实现
#   #   # 策略模型
#   # Policy =
#   #   # 这个是用于记录policys中每个值所在的正确排序
#   #   # key: represent now position(index) in policys
#   #   # values: the next 
#   #   position: {}                
#   #   policys: []                 #存放记录的地方
#   #   add: (records, p=null) ->
#   #     {position, policys} = @
#   #     # p 表示在那个位置后面增加
#   #     # 如果不提供，则默认插在最后面 
#   #     length = policys.length
#   #     console.log "length before:", length
#   #     if p > length then return
#   #     p2 = position[p] || null    # 插入位置原来的下一个
#   #     console.log "p2:", p2
#   #     if length is 0          #说明里面还没有记录
#   #       if $.isArray records
#   #         for value, index in records
#   #           position[index] = index + 1
#   #     else if length > 0      #说明已经有记录在里面了
#   #       if p is null then p = length - 1  #这个是用于直接插在最后
#   #       if $.isArray records
#   #         for value, index in records
#   #           console.log p+index, length+index
#   #           position[length + index] = length + index + 1
#   #         position[p] = position[length]
#   #       # else 
#   #       #   position[length + index] = length + index
#   #     if $.isArray records
#   #       @policys = policys.concat records
#   #     else
#   #       @policys.push records
#   #     position[@policys.length - 1] = p2
#   #   remove: ->
#   #   update: ->
#   # Policy.add [1,2,3,4,5]
#   # # Policy.add 100
#   # Policy.add [23,12,34,21], 0
#   # console.log Policy.position, Policy.policys


  
policyRecordTpl = '''
  {{#each context}}
    <tr>
      <td class="number"><p>{{number}}</p></td>
      <td class="date">
        <p>{{date}}</p>
        <input type="text" name="date" value="" />
      </td>
      <td class="hour">
        <p>{{hour}}</p>
        <input type="text" name="hour" value="" />
      </td>
      {{#each co2}}
      <td class="co2">
        <p>{{this}}</p>
        <input type="text" name="co2-{{@index}}" value="" />
      </td>
      {{/each}}
      {{#each temperature}}
      <td class="temperature">
        <p>{{this}}</p>
        <input type="text" name="temperature-{{@index}}" value="" />
      </td>
      {{/each}}
      {{#each humidity}}
      <td class="humidity">
        <p>{{this}}</p>
        <input type="text" name="humidity-{{@index}}" value="" />
      </td>
      {{/each}}
      {{#each brightness}}
      <td class="brightness">
        <p>{{this}}</p>
        <input type="text" name="brightness-{{@index}}" value="" />
      </td>
      {{/each}}
      <td light="{{lightColor}}">
        <p>{{lightColor}}</p>
        <input type="text" name="light" value="" />
      </td>

      <td>
      {{#if ../isEdit}}
      {{! ../isEdit是模式：edit 还是 view}}
      {{#if isEdit}}
      {{!这里的isEdit是标志每一行数据是否允许被编辑}}
        <button type="button" class="close" action="remove"><i class="glyphicon glyphicon-remove"></i></button>
        <button type="button" class="close" action="edit"><i class="glyphicon glyphicon-pencil"></i></button>
      {{else}}
        <p>不能被编辑</p>
      {{/if}}
      {{/if}}
      </td>
      
    </tr>
  {{/each}}
'''

policyAddTpl = '''
  <form class="form form-inline" role="form" name="add-record-form">
      
      <div class="form-group">
        <label class="" for="date">间隔天数/时间</label>
        <input type="number" class="form-control" id="date" name="date" placeholder="间隔天数">
        <input type="number" class="form-control" id="hour" name="hour" placeholder="间隔小时">
      </div>
        
      <div class="form-group">
        <label class="" for="co2">二氧化碳范围</label>
        <input type="number" class="form-control" id="co2-0" name="co2-0" placeholder="二氧化碳下限">
        <input type="number" class="form-control" id="co2-1" name="co2-1" placeholder="二氧化碳上限">
      </div>
        
      <div class="form-group">
        <label class="" for="temperature">温度范围</label>
        <input type="number" class="form-control" id="temperature-0" name="temperature-0" placeholder="温度下限">
        <input type="number" class="form-control" id="temperature-1" name="temperature-1" placeholder="温度上限">
      </div>
        
      <div class="form-group">
        <label class="" for="humidity">湿度范围</label>
        <input type="number" class="form-control" id="humidity-0" name="humidity-0" placeholder="湿度下限">
        <input type="number" class="form-control" id="humidity-1" name="humidity-1" placeholder="湿度上限">
      </div>
        
      <div class="form-group">
        <label class="" for="brightness">光照范围</label>
        <input type="number" class="form-control" id="brightness-0" name="brightness-0" placeholder="光照下限">
        <input type="number" class="form-control" id="brightness-1" name="brightness-1" placeholder="光照上限">
      </div>

      <div class="form-group">
        <label class="" for="light">光带颜色</label>
        <input type="text" class="form-control" id="light" name="light" placeholder="光带颜色">
      </div>
      <br />
      <div class="form-group">
        <label class="" for="insertPosition">插入位置</label>
        <input type="number" class="form-control" id="insertPosition" name="insertPosition" placeholder="插入位置">
      </div>
      <br />
      <button type="submit" class="btn btn-primary" name="add-policy">增加</button>
  </form>
'''

postFormTpl = '''
    <form class="form" role="form" name="post-form">
      <div class="form-group">
        <label class="" for="room-id">房间号</label>
        <input type="text" class="form-control" id="room-id" name="roomId" placeholder="房间号" value="{{roomId}}">
      </div>
      <div class="form-group">
        <label class="" for="description">描述</label>
        <input type="text" class="form-control" id="description" name="description" placeholder="描述" value="{{description}}">
      </div>
      <div class="form-group">
        <label class="" for="start-date">运行起始日期</label>
        <input type="date" class="form-control" id="start-date" name="startDate" placeholder="运行起始日期" style="display: block" value="{{startDate}}">
      </div>
      <div class="form-group">
        <label class="" for="start-date">运行起始时间</label>
        <input type="time" class="form-control" id="start-time" name="startTime" placeholder="运行起始时间" style="display: block" value="{{startTime}}">
      </div>
      <button type="submit" name="post" class="btn btn-success">提交</button>
    </form>
'''


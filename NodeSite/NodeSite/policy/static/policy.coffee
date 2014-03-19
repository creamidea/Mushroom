'use strict'
console.log "here is show policy"

compileTemplate = (templateName) ->
  source = $(templateName).html()
  template = Handlebars.compile source

RecordView =
  # 这里用于渲染每一条记录
  # signalton
  templateName: "#policy-record-template"
  render: (opt) ->
    {records, isEdit} = opt
    # console.log "RecordView:", isEdit
    if not $.isArray records
      temp = records
      records = [temp]
    template = compileTemplate @templateName
    template {"policy":records, "isEdit": isEdit}

class PolicyMetaView
  # 这里负责策略元信息的显示
  templateName: "#policy-meta-template"
  constructor: (opt) ->
    {$renderTo, isEdit} = opt
    # @$el为外层元素，包裹信息

    # 绑定事件
    if isEdit
      $renderTo.on "dblclick", "p", $.proxy @editing, @
      $renderTo.on "blur keypress", "input", $.proxy @edited, @
      # $renderTo.on "keypress", "input", $.proxy @keypress, @
      @editItem = ["description"]
      
    @$renderTo = $renderTo


  keypress: (e) ->
    e.stopPropagation()
    code = e.which
    switch code
      when 13 then @edited e
      else return

  editing: (e) ->
    $p = $(e.target)
    $input = $p.siblings "input"
    $input.show().val($p.text()).focus().select()
    $p.hide()

  edited: (e) ->
    # console.log arguments
    if e.type is "keypress"
      if e.which isnt 13 then return
    # if e.type isnt "focusout" then return
    $input = $(e.target)
    $p = $input.siblings "p"
    value = $input.val()
    
    name = $input.attr("name")
    oldValue = @meta[name]
    if value is "" or oldValue is value then return #与旧值比较
    @meta[name] = value  #将其作为新值存入容器，为render提供数据
    console.log ">>>", @meta

    $input.hide()
    $p.show()
    @render()
    
    if name is "description"
      # 这里是更新策略描述的地方
      policyId = $input.attr("policy-id")
      if policyId is undefined or policyId is null then return
      $.ajax
        url: "/policy/#{policyId}/description/"
        type: "PUT"
        data:
          description: value
        success: (data) =>
          alert data.body
          @render()
        fail: (data) ->
          alert "更新失败，请重试"
    # else
    #   # 这里说明是创建一个全新的策略，而不是对其修改
    #   @render()

    e.stopPropagation()

  render: (meta) ->
    if not meta then meta = @meta else @meta = meta
    # console.log meta
    template = compileTemplate @templateName
    $renderTo = @$renderTo
    $renderTo.html template meta

class PolicyAddView
  # 这个是处理增加行的信息的
  # 这个当单击增加按钮的时候会触发 add-record，这个有绑定的元素$renderTo触发
  templateName: "#policy-add-record-template"
  init: () ->
    @record = 
      date: ""
      hour: ""
      brightness: ""
      humidity: []
      temperature: []
      co2: []
      insertPosition: 0
  constructor: (opt) ->
    {$renderTo, isEdit} = opt
    @init()
    $renderTo.on "submit", "form", $.proxy @addEvent, @
    $renderTo.on "blur keypress", "input", $.proxy @edited, @
    @$renderTo = $renderTo
    @isEdit = isEdit
    # console.log $renderTo

  addEvent: (e) ->
    e.preventDefault()
    # alert "hello"
    record = @record
    if record.data is "" or record.hour is ""
      alert "间隔时间或者间隔天数不能为空"
      return
    selector = @$renderTo.selector
    channel = selector.split(" ")[0]
    # $.publish "/add/record/#{channel}"
    @$renderTo.trigger "add-record"
    @init()
    _.extend @record, record    #使用underscore的extend，在保留上次值得基础之上，进行深拷贝，也就是避免直接等于时造成的引用，应为PolicyAddView在使用时使用的时同一个@record
    e.stopPropagation()

  edited: (e) ->
    if e.type is "keypress"
      if e.which isnt 13 then return
    $input = $(e.target)
    name = $input.attr("id")
    value = $input.val()
    # console.log $input, name, value
    if name in ["date", "hour", "brightness", "insertPosition"]
      # console.log name, value
      @record[name] = value
    else
      [name, index] = name.split("-")
      @record[name][index] = parseFloat value
      # console.log name, index, value
  render: () ->
    template = compileTemplate @templateName
    $renderTo = @$renderTo
    $renderTo.html template {}
    @$elt = $renderTo.find "[name=addition-form]"


# 策略模型
class Policy
  # 这个是策略模型，用于对策略进行数组级别的增删改
  constructor: () ->
    @policys = []                 #存放记录的地方
  check: (record) ->
    # 这里是检查每一个传入的记录是否有置空项
    # TODO: 如果置空，则默认是上一项的值
    # console.log ">>>>>>", record
    for key, value of record
      if key in ["date", "hour", "brightness"] and value is null
        console.log "string"
        record[key] = "同上"
      else if key in ["co2", "temperature", "humidity"] and value.length < 2
        console.log "array"
        if value[0] is undefined
          value[0] = "同上"
        if value[1] is undefined
          value[1] = "同上"
        record[key] = value
    # console.log record
    return [record]

  add: (records, insertIndex=null) ->
    policys = @policys
    @policys = []
    length = policys.length

    if insertIndex isnt null and 0 <= insertIndex and insertIndex < length
      # 插入中间
      prefix = policys.slice(0, insertIndex)
      affix = policys.slice(insertIndex)
      @policys = @policys.concat prefix, records, affix
      # @policys = _.union prefix, records, affix
    else if insertIndex is null
      # @policys.concat records
      # console.log policys, records
      # @policys = _.union policys, records
      @policys = policys.concat records
  remove: (index)->
    # console.log "remove"
    length = @policys.length
    # alert index+" "+length
    if index < 0 or index >= length then return
    # delete @policys[index]
    @policys.splice index, 1
  update: (index, value)->
    # console.log "policy update", index, _.isArray(value)
    # if $.isNumeric index or value
    # console.log "start update"
    if _.isArray(value)
      # console.log "array update"
      [name, idx] = value[0].split("-")
      _value = value[1]
      # console.log name, index, _value
      if name in ["temperature", "humidity", "co2"]
        @policys[index][name][idx] = _value
      else
        @policys[index][name] = _value
    else if _.isObject(value)
      # Attention:
      # 这里有一个「奇怪」的事情：
      # console.log "object update"
      @policys[index] = value
    # console.log "end update"

# 策略视图
class PolicyView
  # 这里是顶层的元素界面，或者说是外出包裹和主要的策略记录主体
  # $el: $("#create-policy")
  templateName: "#policy-out-template"
  meta: null
  isEdit: false
  constructor: (context)->
    {$renderTo, isEdit} = context
    @$el = $renderTo
    @isEdit = isEdit
    # console.log renderTo, @$el
  init: (context) ->
    @model = new Policy       #写在这里是实例的属性
    # 将数据渲染到界面
    {roomId, policyId, description, policy} = context
    template = compileTemplate @templateName
    outHTML = template 
      "title": "任务进行时"
      "edit": @isEdit
    $el = @$el
    $el.html outHTML

    # 绑定页面各个展示区域元素 
    @$meta = $meta = $el.find "[name=meta]"
    @$policys = $policys = $el.find "tbody"
    @$policyAdd = $policyAdd = $el.find "[name=policy-add]"
    # 创建meta
    @meta = meta = new PolicyMetaView
      $renderTo: $meta
      isEdit: @isEdit
    meta.render
      "roomId": roomId
      "policyId": policyId
      "description": description
      "isEdit": @isEdit
      "today": (new Date()).toJSON()

    # 创建增加行
    if @isEdit
      @addView = addView = new PolicyAddView
        $renderTo:$policyAdd
        isEdit: true
      selector = $policyAdd.selector
      addViewChannel = selector.split(" ")[0]
      addView.render()
      $policyAdd.on "add-record", $.proxy @addEvent, @

      # 事件监听
      $policys.delegate "tr td p", "dblclick", $.proxy @editing, @
      $policys.delegate "tr td input", "blur", $.proxy @edited, @
      $policys.delegate "tr td input", "keypress", $.proxy @keypress, @
      $policys.delegate "tr td button", "click", $.proxy @removeEvent, @
      # $.subscribe "/add/record/#{addViewChannel}", $.proxy @addEvent, @
      $el.find("button[type=submit][name=post]").click $.proxy @submit, @

  addEvent: (e) ->
    # console.log @addView.record
    # alert "add event"
    record = @addView.record
    @add record

  keypress: (e) ->
    e.stopPropagation()
    # e.preventDefault();
    code = e.which
    switch code
      when 13 then @edited(e)
      else return

  editing: (e) ->
    # 编辑策略
    # console.log e.target
    elt = e.target
    $elt = $(elt)
    text = $elt.text()
    $elt.siblings("input").val(text).show().focus().select()
    $elt.hide()

  edited: (e) ->
    elt = e.target
    $elt = $(elt)
    $tr = $elt.closest("tr")
    index = $tr.index()
    name = $elt.attr("name")
    if name in ["date", "hour", "brightness"]
      value = $elt.val()
      if value is "" then value = null
    else
      value = parseFloat $elt.val()
      if isNaN(value) then value = null
    if value isnt null
      # console.log index, name, value
      @update index, [name, value]
    else
      $elt.siblings("p").show()
      $elt.val("").hide()
    e.stopPropagation()

  removeEvent: (e) ->
    elt = e.target
    $elt = $(elt)
    # console.log $elt
    index = $elt.closest("tr").index()
    if confirm("你确定删除么？")
      @remove(index)

  submit: (e) ->
    policys = @model.policys
    $el = @$el
    policys = JSON.stringify policys
    meta = @meta.meta
    {roomId, description} = meta
    $el = @$el
    startDate = $el.find("#start-date").val()
    startTime = $el.find("#start-time").val()
    time = "#{startDate} #{startTime}"
    # $roomId = $el.find("p[name=meta]")
    console.log roomId, description, "policys"
    $.ajax
      url: "/policy/"
      type: "POST"
      data:
        roomId: roomId
        description: description
        policys: policys
        time: time
      success: (data) ->
        alert data.body
      fail: () ->
        alert "fail"

  check: (record) ->
    # console.log ">>>>>>", record
    for key, value of record
      if key in ["date", "hour", "brightness"] and value is ""
        record[key] = "-"
      else if key in ["co2", "temperature", "humidity"] and value.length < 2
        if value[0] is undefined
          value[0] = "-"
        if value[1] is undefined
          value[1] = "-"
        record[key] = value
    # console.log record
    return record

  add: (records) ->
    # 增加策略
    # console.log "//////", records.insertPosition
    model = @model
    if $.isArray(records)
      _records = []
      for record in records
        _records.push(@check(record))
      records = _records
    else
      records = @check records
      # console.log "<><><><>", records

    insertPosition = parseInt(records.insertPosition, 10) - 1 #理解人类与计算机索引的区别
    $policys = @$policys
    length = model.policys.length
    if insertPosition >= 0 and insertPosition < length
      # 说明插入指定位置
      records = [records]
      # preRecord = model[insertPosition]
      # 找到当前位置上的节点
      $nowElt = $($policys[0].children[insertPosition])
      recordsHTML = RecordView.render
        records: records
        isEdit: @isEdit
      $(recordsHTML).insertBefore $nowElt
      model.add records, insertPosition
    else
      # 插入末尾
      recordsHTML = RecordView.render
        records: records
        isEdit: @isEdit
      $policys.append recordsHTML
      model.add records

  remove: (index)->
    # 移出策略
    # console.log @$policys, index
    $(@$policys[0].children[index]).remove()
    @model.remove index
    console.log "after remove:", @model.policys

  update: (index, value) ->
    # 更新策略
    # console.log "policy view update"
    # if @model.policys[index] is value then return
    @model.update index, value
    value = @model.policys[index]
    recordsHTML = RecordView.render
      records: value
      isEdit: @isEdit
    $(@$policys.children()[index]).html $(recordsHTML).children()
    console.log "after update:", @model.policys


PolicyList =
  # 策略列表视图
  templateName: "#policy-list-template"
  # constructor: (opt) ->
  #   {@$renderTo} = opt
  render: (opt) ->
    {policys, $renderTo} = opt
    template = compileTemplate @templateName
    $renderTo.html template {"policys": policys}

    $renderTo.on "click", "li", $.proxy @clickEvent, @

  clickEvent: (e) ->
    $elt = $(e.target)
    policyId = $elt.attr("policy-id")
    # alert policyId
    # 发一个GET获取具体的策略
    getPolicyById
      policyId: policyId

getPolicyList = (opt) ->
  # 获取策略列表的ajax
  {$renderTo} = opt
  $.ajax
    url: "/policy/list/"
    type: "GET"
    success: (data) ->
      # console.log data
      PolicyList.render
        policys: data.body
        $renderTo: $renderTo
    fail: (data) ->
      alert "request policy fail"

getPolicyById = (opt) ->
  # 通过具体的policy id获得具体策略的ajax
  {policyId, $renderTo} = opt
  $.ajax
    url: "/policy/#{policyId}"
    type: "GET"
    success: (data) ->
      console.log data
      policyView = new PolicyView
        $renderTo: $("#policy-show-area")
        isEdit: true
      policyView.init
        roomId: "双击编辑"
        policyId: ""
        description: "双击编辑"
        policy: []
      policyView.add data.body
    fail: (data) ->
      alert "request policy fail"

getNowPolicy = (opt)->
  # 获取正在执行的列表
  {roomId, $renderTo} = opt
  $.ajax
    url: "/policy/now/room/#{roomId}/"
    type: "GET"
    success: (data) ->
      policyView = new PolicyView
        $renderTo: $renderTo
        isEdit: false
      policyView.init data.body
      policyView.add data.body.policy
    fail: (data) ->
      alert "request policy fail"

        
  # =================================================
  # 链表实现的，但是暂时不这么实现
  #   # 策略模型
  # Policy =
  #   # 这个是用于记录policys中每个值所在的正确排序
  #   # key: represent now position(index) in policys
  #   # values: the next 
  #   position: {}                
  #   policys: []                 #存放记录的地方
  #   add: (records, p=null) ->
  #     {position, policys} = @
  #     # p 表示在那个位置后面增加
  #     # 如果不提供，则默认插在最后面 
  #     length = policys.length
  #     console.log "length before:", length
  #     if p > length then return
  #     p2 = position[p] || null    # 插入位置原来的下一个
  #     console.log "p2:", p2
  #     if length is 0          #说明里面还没有记录
  #       if $.isArray records
  #         for value, index in records
  #           position[index] = index + 1
  #     else if length > 0      #说明已经有记录在里面了
  #       if p is null then p = length - 1  #这个是用于直接插在最后
  #       if $.isArray records
  #         for value, index in records
  #           console.log p+index, length+index
  #           position[length + index] = length + index + 1
  #         position[p] = position[length]
  #       # else 
  #       #   position[length + index] = length + index
  #     if $.isArray records
  #       @policys = policys.concat records
  #     else
  #       @policys.push records
  #     position[@policys.length - 1] = p2
  #   remove: ->
  #   update: ->
  # Policy.add [1,2,3,4,5]
  # # Policy.add 100
  # Policy.add [23,12,34,21], 0
  # console.log Policy.position, Policy.policys


  
  

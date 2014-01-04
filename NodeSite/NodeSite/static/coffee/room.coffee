class RoomList extends Frame
  constructor: (el)->
    @el = el || "#room-list"
    @$el = $(@el)
    @list = {}                  #用于记录房间指引 
    @url = "/room/list/"        #获取房间列表服务器地址
  fetch: () ->
    # 从服务器取数据
    url = @url
    roomFetch = new Get url, (data) =>
      # console.log data
      if data.code is 0
        @renderAll(data.context)
      else
        window.hint(data)
    roomFetch.send()
  renderAll: (context) ->
    @render c for c in context
  render: (context) ->
    roomId = context.roomId
    list = @list
    $roomList = @$el
    if list[roomId] is undefined
      room = new Room
        templateName: "#room-template"
        roomId: roomId
      room.renderTo $roomList, context
      list[context.id] = room

class Room extends Frame
  # 这个是房间类，囊括了缩略图，数据图表，查看/设置策略和控制面板
  constructor: (option) ->
    {templateName, roomId} = option
    
    super(templateName)

    @showElt = undefined               #用于记录当前显示的元素
    
    # 订阅RoomThumbnail发出的信号
    $.subscribe "#data/room/#{roomId}/", $.proxy(@dataHandle, this)
    $.subscribe "#policy/viewer/room/#{roomId}/", $.proxy(@viewPolicy, this)
    $.subscribe "#policy/setter/room/#{roomId}/", $.proxy(@setPolicy, this)
    $.subscribe "#controller/room/#{roomId}/", $.proxy(@controllerHandle, this)

    @templateName = templateName
    @roomId = roomId
    
  hideElt: (elt) ->
    if elt
      elt.hide
    else
      @env.hide()
      @policyViewer.hide()
      @policySetter.hide()
      @controller.hide()
      
  dataHandle: ->
    console.log arguments
    if @showElt
      @showElt.hide()
    if !@env                    #第一次创生
      roomId = @roomId
      @env = new RoomEnv "#room-env-template", roomId
      @env.renderTo @$el, {roomId: roomId}
    else
      @env.show()
    @showElt = @env
    
  viewPolicy: ->
    if @showElt
      @showElt.hide()
    if !@policyViewer
      roomId = @roomId
      @policyViewer = new RoomPolicyViewer "#room-policy-viewer-template", @roomId
      getPolicy = new Get "/policy/now/room/#{roomId}/", (data) =>
        @policyViewer.renderTo @$el, data.data
      getPolicy.send()
      # @policyViewer.renderTo @$el, @context
    else
      @policyViewer.show()
    @showElt = @policyViewer
    
  setPolicy: ->
    if @showElt
      @showElt.hide()
    if !@policySetter
      roomId = @roomId
      @policySetter = new RoomPolicySetter "#policy-setter-template", roomId
      @policySetter.renderTo @$el
    else
      @policySetter.show()
    @showElt = @policySetter
    
  controllerHandle: () ->
    if @showElt
      @showElt.hide()
    if !@controller
      roomId = @roomId
      @controller = new RoomController "#room-controller-template", roomId
      @controller.fetch
        target: @$el
    else
      @controller.show()
    @showElt = @controller
    
  renderTo: (target, context) ->
    super(target, context)
    @context = context
    @roomThumbnail = new RoomThumbnail "#room-thumbnail-template", @roomId
    @roomThumbnail.renderTo @$el, context

class RoomThumbnail extends Frame
  constructor: (@templateName, @roomId) ->
    super(@templateName)
    # 初始化一些变量，后期会提供修改接口
    @nav = "nav.room-menu>ul"
    @card = ".card"
    @brightness = ".room-light"
    @roomName = ".room-name"
    # @inputRoomName = "input[name=roomName]"
    @plantName = ".plant-name"
    # @inputPlantName = "input[name=plantName]"
    @searchForm = ".room-search>form"
    @searchURI = "/search/"
    
  renderTo: (target, context) ->
    # console.log target, context
    timeHelper = () ->
      datetime = @time
      [date, time] = @time.split(" ")
      html = "<p class=date>#{date}</p><p class=time>#{time}</p>"
      return new Handlebars.SafeString html
    super(target, context, {tag: "datetime", fun: timeHelper})
    $el = @$el
    # find = $el.find
    # console.log find
    @$roomName = $el.find(@roomName)
    @$plantName = $el.find(@plantName)
    @$cards = $el.find(@card)   #保存上面需要实时跟新的信息：温度，湿度，co2
    @$brightness = $el.find(@brightness)
    @submit()                   #启动提交事件监听
    # @update(testRoomUpdate)
  update: (context) ->
    roomName = context.roomName
    plantName = context.plantName
    sensors = context.sensors
    brightness = context.brightness
    @$roomName.html(roomName)
    @$plantName.html(plantName)
    @$cards.each (index, el)->
      s = el.id.split('-')[2]
      if s                      #排除第一张卡片
        value = sensors[s]
        $(el).html("<p>#{value}</p>")
    @$brightness.attr("brightness", brightness)
  subscribe: ->
    # 这类函数放到room里面去了
    roomId = @roomId
    $.subscribe "#data/room/#{roomId}/", $.proxy(@dataHandle, this)
    $.subscribe "#policy/viewer/room/#{roomId}/", $.proxy(@viewPolicy, this)
    $.subscribe "#policy/setter/room/#{roomId}/", $.proxy(@setPolicy, this)
    $.subscribe "#policy/controller/room/#{roomId}/", $.proxy(@controllerHandle, this)
    # $.subscribe "#search/room-#{roomId}", $.proxy(@search, this)
  submit: () ->
    $form = @$el.find(@searchForm)
    # console.log $form
    $sensor = $form.find("input[name=sensor]")
    $startDate = $form.find("input[name=start-date]")
    $endDate = $form.find("input[name=end-date]")
    $form.submit (e) =>
      e.preventDefault()
      console.log e
      sensor = $sensor.val()
      startDate = $startDate.val()
      endDate = $endDate.val()
      roomId = @roomId || -1
      # alert @roomId
      @search
        roomId: roomId
        sensorId: sensor
        startDate: startDate
        endDate: endDate
      # alert "#{sensor}:#{startDate}:#{endDate}"
  search: (context)->
    # console.log "context", context
    searchPost = new Post @searchURI, (data) ->
      $.publish "#search/finish/", [data]
      # alert data.data
    searchPost.send(context)

class RoomEnv extends Frame
  constructor: (@templateName, @roomId) ->
    super(@templateName)
  renderTo: (target, context) ->
    super(target, context)

class RoomPolicyViewer extends Frame
  constructor: (@templateName, @roomId) ->
    super(@templateName)
    @timeline = '.timeline'
    @table = 'table'
  renderTo: (target, context) ->
    console.log "Room Policy Viewer:", context
    super(target, context)
    @$timeline = @$el.find(@timeline)
    @$table = @$el.find(@table)
    viewerHeight = @$el.height() #获得总的高度
    tableHeight = @$table.height() #获得实际表格的高度
    tbodyHeight =  @$table.find('tbody').height() #获得表格中数据区的高度
    tdHeight = @$table.find('tbody').find('tr').height() #获得每一个td的高度
    startPosition = viewerHeight - tbodyHeight           #计算时间线出现的位置
    next = startPosition + tdHeight                      #计算下一个出现的位置
    @$timeline.css('top', "#{next}px")                   #显示时间线

class RoomPolicySetter extends Frame
  
  constructor: (@templateName, @roomId) ->
    # 创建出模板指引
    super(@templateName)
    @modelList = '.model-list'           #list
    @table = 'table'
    @policy= 'tbody'
    # @$table = $
    @createPolicyURL = '/policy/'
    @listURL = '/policy/list/'
    @policyListTemp = '#policy-list-template'
    @policyInputTemp = "#policy-input-template"
    @tableTemp = '#table-template'
  renderTo: (target) ->
    policyInputTemp = @policyInputTemp
    # 初始窗口创建
    helper = ->
      source = $(policyInputTemp).html()
      html = Handlebars.compile(source)({})
      return new Handlebars.SafeString html
    super(target, {roomId: @roomId}, {tag: "tbody", fun: helper})
    @$table = @$el.find(@table)
    @$policy = @$table.find(@policy)
    @createPolicyList()
    @createPolicy()
  createPolicyList: () ->
    # #获取养殖策略的简要信息
    get = new Get @listURL, (mesg) =>
      # 用于获取所有policy的简要信息
      console.log mesg
      if mesg.code is 0
        @$modelList = @$el.find(@modelList)
        list = new Frame @policyListTemp
        list.renderTo @$modelList, {list:mesg.data}
        # 订阅事件，处理模板的生成
        @$modelList.children().each (index, elt) =>
          href = $(elt).find('a').attr("href")
          roomId = @roomId
          policyId = href.split('/')[1]
          $.subscribe href, (e, data) =>
            # console.log roomId, policyId
            # 获取指定的policy
            g = new Get "/policy/#{policyId}/", (mesg) =>
              if mesg.code is 0
                @createPolicy(mesg.policy)
              else
                $.publish "#echo/", mesg
            g.send()
      else
        $.publish "#echo/", [mesg]
    get.send()
  createPolicy: (policy) ->
    if @$policy
      @$policy.children().remove()
    source = $(@policyInputTemp).html()
    template = Handlebars.compile(source)
    Handlebars.registerHelper "modelList", ->
      # console.log this
      policy = @policy
      if policy is undefined    #这里表明创建空的东西
        policy = ["hello"]
      html = ""
      for p in policy
        {date, hour, brightness, co2, temperature, humidity} = p
        if co2
          [c1, c2] = co2
        if temperature
          [t1, t2] = temperature
        if humidity
          [h1, h2] = humidity
        light = {}
        light[brightness] = "selected"
        {blue, white, yellow} = light
        html += "
          <tr>
          <td value=input>
            <input type=date name=date class=form-control placeholder=间隔天数 value=#{date}> 
          </td>
          <td value=input>
            <input type=time name=time class=form-control placeholder=间隔小时 value=#{hour}> 
          </td>
          <td value=input>
            <input type=number name=co2 class=form-control placeholder=下限 value=#{c1}> 
          </td>
          <td value=input>
            <input type=number name=co2 class=form-control placeholder=上限 value=#{c2}> 
          </td>
          <td value=input>
            <input type=number name=temperature class=form-control placeholder=下限 value=#{t1}> 
          </td>
          <td value=input>
            <input type=number name=temperature class=form-control placeholder=上限 value=#{t2}> 
          </td>
          <td value=input>
            <input type=number name=humidity class=form-control placeholder=下限 value=#{h1}> 
          </td>
          <td value=input>
            <input type=number name=humidity class=form-control placeholder=上限 value=#{h2}> 
          </td>
          <td value=select>
            <select class=form-control name=brightness>
              <option value=blue #{blue}>蓝光</option>
              <option value=white #{white}>白光</option>
              <option value=yellow #{yellow}>黄光</option>
            </select>
          </td></tr>"
      return new Handlebars.SafeString html
    html = template({isModelList: true, policy: policy})
    @$policy.append html
    
    $submit = @$el.find("button[type=submit]")
    $submit.unbind "click"
    $submit.click (e) =>
      e.preventDefault()
      alert "hello"
      mesg = {}
      policy = []
      @$policy.children().each (index, tr) =>
        p =
          co2: []
          temperature: []
          humidity: []
        $(tr).children().each (index, td) =>
          childElt = $(td).attr("value")
          if childElt is "input"
            $input = $(td).find("input")
            name = $input.attr("name")
            value = $input.val()
            if name in ["date", "time"]
              p[name] = value
            else if name in ["co2", "temperature", "humidity"]
              p[name].push value
          else if childElt is "select"
            $select = $(td).find("select option:selected")
            name = $select.parent().attr("name")
            value = $select.val()
            p[name] = value
        policy.push p
      mesg["policy"] = policy
      mesg["roomId"] = @roomId
      description =  @$el.find("input[name=description]").val()
      startDate = @$el.find("input[name=startDate]").val()
      startTime = @$el.find("input[name=startTime]").val()
      mesg["description"] = description
      mesg["startat"] = "#{startDate} #{startTime}"
      post = new Post @createPolicyURL, (data) ->
        $.publish "#echo/", [data]
      post.send({mesg: JSON.stringify mesg})
      console.log "mesg", JSON.stringify mesg
          
class RoomController extends Frame
  constructor: (@templateName, @roomId) ->
    super(@templateName)
    @$switchers = {}
    @listURL = "controller/list/room/#{@roomId}/"
  fetch: (option) ->
    # 获取控制器列表状态
    { target } = option
    url = @listURL
    get = new Get url, (data) =>
      if data.code is 0
        @renderTo target, data.context
    get.send()
  renderTo: (target, context) ->
    # console.log target, context
    # 这里是html处理辅助函数，不知后期能否更好的处理
    freg = 0
    helper = () ->
      html = ""
      {controllerId, controllerType} = @
      console.log controllerId
      if controllerId < 100
        if this.state is "on"
          checked = "checked"
        else
          checked = ""
        label1 = "<label for=controller-#{controllerId}-switcher>#{controllerType}</label>"
        input = "<input #{checked} type=checkbox name=switcher id=controller-#{controllerId}-switcher>"
        label2 = "<label class=switcher for=controller-#{controllerId}-switcher></label>"
        html = label1 + input + label2
      else
        html = ""
        freg = @state
      return new Handlebars.SafeString html
      # console.log arguments
    super(target, {roomId: @roomId, context: context}, {tag: 'controller', fun: helper})
    
    $switchers_temp = @$el.find('input[name=switcher]')
    $switchers_temp.each (index, elt) =>
      id = elt.id.split('-')[1] #获取controller ID
      # console.log index,
      @$switchers[id] = $(elt)  #将元素指引存入容器，update时需要 

      # 绑定checkbox改变事件
      $(elt).unbind("change").change (e) ->
        e.stopPropagation()
        $switch = $(this)
        nowState = $switch[0].checked
        if nowState then action = "on" else action = "off"
        # alert nowState+" "+action
        put = new Put "/controller/#{id}/", (data) ->
          if data.code is -1
            # alert nowState
            if nowState
              # alert "开启失败"
              setTimeout ->
                # 延迟操作的原因：动画移动一次需要250ms，所以这里设置500ms
                $switch.removeAttr("checked")
              , 500
            else
              setTimeout ->
                $switch.prop("checked", true)
              , 500
            console.log nowState, $switch
          console.log data
          window.hint(data)
        put.send
          action: action

    # 等待其ID编号,假设100
    $freg = @$freg = @$el.find("input[name=freg-adjust]")
    $freg.val(freg)
    @$el.find("form[name=freg-adjust]").submit (e) =>
      e.preventDefault()
      freg = $freg.val()
      if freg
        put = new Put "/controller/100/", (data) ->
          window.hint(data)
        put.send
          freg: freg
      else
        window.hint
          code: -1
          definition: "请填写采集频率"
      
    # @update(switcherData)
  update: (context) ->
    $switchers = @$switchers
    for c in context
      if c.state is "on"
        $switchers[c.controllerId].attr("checked": true)
      else if c.state is "off"
        $switchers[c.controllerId].attr("checked": false)
      else if $.isNumeric c.state
        @$freg.val(c.state)
    
context1 =
  "roomId": 1,
  "roomName": "房间1",
  "plantId": 1,
  "plantName": "蘑菇",
  "time": "2013-12-25 16:41",
  "sensors": 
    "temperature": 18,
    "co2": 24,
    "humidity": 150,
  "brightness": "yellow",
  "menu": 
    "data": "glyphicon-sort",
    "policy/viewer": "glyphicon-list-alt",
    "policy/setter": "glyphicon-pencil",
    "controller": "glyphicon-wrench",

testRoomUpdate =
  "roomName": "房间1-1"
  "plantName": "蘑菇2"
  "sensors":
    "temperature": 0
    "co2": 0
    "humidity": 1
  "brightness": "white"

roomControllerData =
  [
    {
      "roomId": 1
      "controllerId": 2
      "controllerType": "湿度传感器"
      "state": "on"
    }
    {
      "roomId": 2
      "controllerId": 2
      "controllerType": "湿度传感器"
      "state": "on"
    }
    {
      "roomId": 3
      "controllerId": 2
      "controllerType": "湿度传感器"
      "state": "on"
    }
  ]

switcherData = [
    {
        "roomId": 1,
        "controllerId": 1,
        "controllerType": "风机",
        "state": "on",
    },
    {
        "roomId": 1,
        "controllerId": 2,
        "controllerType": "加湿器",
        "state": "on",
    },
    {
        "roomId": 1,
        "controllerId": 3,
        "controllerType": "温度控制器",
        "state": "on",
    },
    {
        "roomId": 1,
        "controllerId": 4,
        "controllerType": "LED控制",
        "state": "on",
    },
    ]


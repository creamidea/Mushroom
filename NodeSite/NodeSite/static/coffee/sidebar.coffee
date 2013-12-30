# TODO: 激活状态
class Sidebar extends Frame
  constructor: (tplName) ->
    super(tplName)
    # @el = "#sidebar"
    # @$el = $(@el)
    # console.log @el, @tplName
    # @$sidebar.find('ul').delegate "li", "click", $.proxy(@event, this)
    # $.subscribe "#"
  renderTo: (target, context) ->
    super(target, context)
    @el = target
    @$el = $(@el)

    menu = context.menu
    @subscribe menu
    elt = "nav ul"              #其实这里应该给出一个参数的
    @$nav = @$el.find(elt)
    # console.log @$nav
    @active(menu[0].url)
    @context = context
  # show: ->
  #   super()
  #   @$sidebar.show()
  # hide: ->
  #   @$sidebar.hide()
  active: (url) ->
    # alert(url)
    $nav = @$nav
    $nav.children().removeClass('active')
    $nav.find("li[url=#{url}]").addClass('active')
  fill: (context) ->
    @context = context          #记录填充的数据
    super(context)
  subscribe: (menu) ->
    # console.log menu
    # for x, y in menu
    # x is the item
    # y is the index
    $.subscribe "#{item.url}", $.proxy(@handler, this) for item in menu
    @
  handler: (e, args) ->
    # console.log arguments
    url = e.type
    @$el.find("a[href=#{url}]").parent
    @active url

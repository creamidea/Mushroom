class SettingPanel extends View
  # constructor: () ->
    # @$el = $("#setting-panel")
    # @render()
    # super()
  render: () ->
    super()
    $el = @$el
    logSetting = new LogSetting
      el: "#config"
      templateName: "#setting-log-template"
    logSetting.render()
    $tab = $el.find('>ul a').click (e)->
      e.preventDefault()
      console.log e.target
      $(this).tab('show')
    # log = new LogSetting "#setting-log-template"
    # log.renderTo @$el

class LogSetting extends View
  # constructor: (@templateName) ->

  renderTo: (target) ->
    console.log @templateName
    super(target, {})
    console.log @$el
    $form = @$el.find("form")
    $form.submit (e) ->
      e.preventDefault()
      type = $form.find('select option:selected').val()
      put = new Put "/config/log/#{type}", (data) ->
        window.hint data
      put.send()

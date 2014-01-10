class SettingPanel extends Frame
  constructor: () ->
    @$el = $("#setting-panel")
    # @render()
  render: () ->
    log = new LogSetting "#setting-log-template"
    log.renderTo @$el

class LogSetting extends Frame
  constructor: (@templateName) ->

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


        

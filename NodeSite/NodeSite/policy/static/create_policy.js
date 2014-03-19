// Generated by CoffeeScript 1.7.1
'use strict';
var Policy, PolicyAddView, PolicyList, PolicyMetaView, PolicyView, RecordView, compileTemplate, getNowPolicy, getPolicyById, getPolicyList;

console.log("here is show policy");

compileTemplate = function(templateName) {
  var source, template;
  source = $(templateName).html();
  return template = Handlebars.compile(source);
};

RecordView = {
  templateName: "#policy-record-template",
  render: function(opt) {
    var isEdit, records, temp, template;
    records = opt.records, isEdit = opt.isEdit;
    if (!$.isArray(records)) {
      temp = records;
      records = [temp];
    }
    template = compileTemplate(this.templateName);
    return template({
      "policy": records,
      "isEdit": isEdit
    });
  }
};

PolicyMetaView = (function() {
  PolicyMetaView.prototype.templateName = "#policy-meta-template";

  function PolicyMetaView(opt) {
    var $renderTo, isEdit;
    $renderTo = opt.$renderTo, isEdit = opt.isEdit;
    if (isEdit) {
      $renderTo.on("dblclick", "p", $.proxy(this.editing, this));
      $renderTo.on("blur keypress", "input", $.proxy(this.edited, this));
      this.editItem = ["description"];
    }
    this.$renderTo = $renderTo;
  }

  PolicyMetaView.prototype.keypress = function(e) {
    var code;
    e.stopPropagation();
    code = e.which;
    switch (code) {
      case 13:
        return this.edited(e);
    }
  };

  PolicyMetaView.prototype.editing = function(e) {
    var $input, $p;
    $p = $(e.target);
    $input = $p.siblings("input");
    $input.show().val($p.text()).focus().select();
    return $p.hide();
  };

  PolicyMetaView.prototype.edited = function(e) {
    var $input, $p, name, oldValue, policyId, value;
    if (e.type === "keypress") {
      if (e.which !== 13) {
        return;
      }
    }
    $input = $(e.target);
    $p = $input.siblings("p");
    value = $input.val();
    name = $input.attr("name");
    oldValue = this.meta[name];
    if (value === "" || oldValue === value) {
      return;
    }
    this.meta[name] = value;
    console.log(">>>", this.meta);
    $input.hide();
    $p.show();
    this.render();
    if (name === "description") {
      policyId = $input.attr("policy-id");
      if (policyId === void 0 || policyId === null) {
        return;
      }
      $.ajax({
        url: "/policy/" + policyId + "/description/",
        type: "PUT",
        data: {
          description: value
        },
        success: (function(_this) {
          return function(data) {
            alert(data.body);
            return _this.render();
          };
        })(this),
        fail: function(data) {
          return alert("更新失败，请重试");
        }
      });
    }
    return e.stopPropagation();
  };

  PolicyMetaView.prototype.render = function(meta) {
    var $renderTo, template;
    if (!meta) {
      meta = this.meta;
    } else {
      this.meta = meta;
    }
    template = compileTemplate(this.templateName);
    $renderTo = this.$renderTo;
    return $renderTo.html(template(meta));
  };

  return PolicyMetaView;

})();

PolicyAddView = (function() {
  PolicyAddView.prototype.templateName = "#policy-add-record-template";

  PolicyAddView.prototype.init = function() {
    return this.record = {
      date: "",
      hour: "",
      brightness: "",
      humidity: [],
      temperature: [],
      co2: [],
      insertPosition: 0
    };
  };

  function PolicyAddView(opt) {
    var $renderTo, isEdit;
    $renderTo = opt.$renderTo, isEdit = opt.isEdit;
    this.init();
    $renderTo.on("submit", "form", $.proxy(this.addEvent, this));
    $renderTo.on("blur keypress", "input", $.proxy(this.edited, this));
    this.$renderTo = $renderTo;
    this.isEdit = isEdit;
  }

  PolicyAddView.prototype.addEvent = function(e) {
    var channel, record, selector;
    e.preventDefault();
    record = this.record;
    if (record.data === "" || record.hour === "") {
      alert("间隔时间或者间隔天数不能为空");
      return;
    }
    selector = this.$renderTo.selector;
    channel = selector.split(" ")[0];
    this.$renderTo.trigger("add-record");
    this.init();
    _.extend(this.record, record);
    return e.stopPropagation();
  };

  PolicyAddView.prototype.edited = function(e) {
    var $input, index, name, value, _ref;
    if (e.type === "keypress") {
      if (e.which !== 13) {
        return;
      }
    }
    $input = $(e.target);
    name = $input.attr("id");
    value = $input.val();
    if (name === "date" || name === "hour" || name === "brightness" || name === "insertPosition") {
      return this.record[name] = value;
    } else {
      _ref = name.split("-"), name = _ref[0], index = _ref[1];
      return this.record[name][index] = parseFloat(value);
    }
  };

  PolicyAddView.prototype.render = function() {
    var $renderTo, template;
    template = compileTemplate(this.templateName);
    $renderTo = this.$renderTo;
    $renderTo.html(template({}));
    return this.$elt = $renderTo.find("[name=addition-form]");
  };

  return PolicyAddView;

})();

Policy = (function() {
  function Policy() {
    this.policys = [];
  }

  Policy.prototype.check = function(record) {
    var key, value;
    for (key in record) {
      value = record[key];
      if ((key === "date" || key === "hour" || key === "brightness") && value === null) {
        console.log("string");
        record[key] = "同上";
      } else if ((key === "co2" || key === "temperature" || key === "humidity") && value.length < 2) {
        console.log("array");
        if (value[0] === void 0) {
          value[0] = "同上";
        }
        if (value[1] === void 0) {
          value[1] = "同上";
        }
        record[key] = value;
      }
    }
    return [record];
  };

  Policy.prototype.add = function(records, insertIndex) {
    var affix, length, policys, prefix;
    if (insertIndex == null) {
      insertIndex = null;
    }
    policys = this.policys;
    this.policys = [];
    length = policys.length;
    if (insertIndex !== null && 0 <= insertIndex && insertIndex < length) {
      prefix = policys.slice(0, insertIndex);
      affix = policys.slice(insertIndex);
      return this.policys = this.policys.concat(prefix, records, affix);
    } else if (insertIndex === null) {
      return this.policys = policys.concat(records);
    }
  };

  Policy.prototype.remove = function(index) {
    var length;
    length = this.policys.length;
    if (index < 0 || index >= length) {
      return;
    }
    return this.policys.splice(index, 1);
  };

  Policy.prototype.update = function(index, value) {
    var idx, name, _ref, _value;
    if (_.isArray(value)) {
      _ref = value[0].split("-"), name = _ref[0], idx = _ref[1];
      _value = value[1];
      if (name === "temperature" || name === "humidity" || name === "co2") {
        return this.policys[index][name][idx] = _value;
      } else {
        return this.policys[index][name] = _value;
      }
    } else if (_.isObject(value)) {
      return this.policys[index] = value;
    }
  };

  return Policy;

})();

PolicyView = (function() {
  PolicyView.prototype.templateName = "#policy-out-template";

  PolicyView.prototype.meta = null;

  PolicyView.prototype.isEdit = false;

  function PolicyView(context) {
    var $renderTo, isEdit;
    $renderTo = context.$renderTo, isEdit = context.isEdit;
    this.$el = $renderTo;
    this.isEdit = isEdit;
  }

  PolicyView.prototype.init = function(context) {
    var $el, $meta, $policyAdd, $policys, addView, addViewChannel, description, meta, outHTML, policy, policyId, roomId, selector, template;
    this.model = new Policy;
    roomId = context.roomId, policyId = context.policyId, description = context.description, policy = context.policy;
    template = compileTemplate(this.templateName);
    outHTML = template({
      "title": "任务进行时",
      "edit": this.isEdit
    });
    $el = this.$el;
    $el.html(outHTML);
    this.$meta = $meta = $el.find("[name=meta]");
    this.$policys = $policys = $el.find("tbody");
    this.$policyAdd = $policyAdd = $el.find("[name=policy-add]");
    this.meta = meta = new PolicyMetaView({
      $renderTo: $meta,
      isEdit: this.isEdit
    });
    meta.render({
      "roomId": roomId,
      "policyId": policyId,
      "description": description,
      "isEdit": this.isEdit,
      "today": (new Date()).toJSON()
    });
    if (this.isEdit) {
      this.addView = addView = new PolicyAddView({
        $renderTo: $policyAdd,
        isEdit: true
      });
      selector = $policyAdd.selector;
      addViewChannel = selector.split(" ")[0];
      addView.render();
      $policyAdd.on("add-record", $.proxy(this.addEvent, this));
      $policys.delegate("tr td p", "dblclick", $.proxy(this.editing, this));
      $policys.delegate("tr td input", "blur", $.proxy(this.edited, this));
      $policys.delegate("tr td input", "keypress", $.proxy(this.keypress, this));
      $policys.delegate("tr td button", "click", $.proxy(this.removeEvent, this));
      return $el.find("button[type=submit][name=post]").click($.proxy(this.submit, this));
    }
  };

  PolicyView.prototype.addEvent = function(e) {
    var record;
    record = this.addView.record;
    return this.add(record);
  };

  PolicyView.prototype.keypress = function(e) {
    var code;
    e.stopPropagation();
    code = e.which;
    switch (code) {
      case 13:
        return this.edited(e);
    }
  };

  PolicyView.prototype.editing = function(e) {
    var $elt, elt, text;
    elt = e.target;
    $elt = $(elt);
    text = $elt.text();
    $elt.siblings("input").val(text).show().focus().select();
    return $elt.hide();
  };

  PolicyView.prototype.edited = function(e) {
    var $elt, $tr, elt, index, name, value;
    elt = e.target;
    $elt = $(elt);
    $tr = $elt.closest("tr");
    index = $tr.index();
    name = $elt.attr("name");
    if (name === "date" || name === "hour" || name === "brightness") {
      value = $elt.val();
      if (value === "") {
        value = null;
      }
    } else {
      value = parseFloat($elt.val());
      if (isNaN(value)) {
        value = null;
      }
    }
    if (value !== null) {
      this.update(index, [name, value]);
    } else {
      $elt.siblings("p").show();
      $elt.val("").hide();
    }
    return e.stopPropagation();
  };

  PolicyView.prototype.removeEvent = function(e) {
    var $elt, elt, index;
    elt = e.target;
    $elt = $(elt);
    index = $elt.closest("tr").index();
    if (confirm("你确定删除么？")) {
      return this.remove(index);
    }
  };

  PolicyView.prototype.submit = function(e) {
    var $el, description, meta, policys, roomId, startDate, startTime, time;
    policys = this.model.policys;
    $el = this.$el;
    policys = JSON.stringify(policys);
    meta = this.meta.meta;
    roomId = meta.roomId, description = meta.description;
    $el = this.$el;
    startDate = $el.find("#start-date").val();
    startTime = $el.find("#start-time").val();
    time = "" + startDate + " " + startTime;
    console.log(roomId, description, "policys");
    return $.ajax({
      url: "/policy/",
      type: "POST",
      data: {
        roomId: roomId,
        description: description,
        policys: policys,
        time: time
      },
      success: function(data) {
        return alert(data.body);
      },
      fail: function() {
        return alert("fail");
      }
    });
  };

  PolicyView.prototype.check = function(record) {
    var key, value;
    for (key in record) {
      value = record[key];
      if ((key === "date" || key === "hour" || key === "brightness") && value === "") {
        record[key] = "-";
      } else if ((key === "co2" || key === "temperature" || key === "humidity") && value.length < 2) {
        if (value[0] === void 0) {
          value[0] = "-";
        }
        if (value[1] === void 0) {
          value[1] = "-";
        }
        record[key] = value;
      }
    }
    return record;
  };

  PolicyView.prototype.add = function(records) {
    var $nowElt, $policys, insertPosition, length, model, record, recordsHTML, _i, _len, _records;
    model = this.model;
    if ($.isArray(records)) {
      _records = [];
      for (_i = 0, _len = records.length; _i < _len; _i++) {
        record = records[_i];
        _records.push(this.check(record));
      }
      records = _records;
    } else {
      records = this.check(records);
    }
    insertPosition = parseInt(records.insertPosition, 10) - 1;
    $policys = this.$policys;
    length = model.policys.length;
    if (insertPosition >= 0 && insertPosition < length) {
      records = [records];
      $nowElt = $($policys[0].children[insertPosition]);
      recordsHTML = RecordView.render({
        records: records,
        isEdit: this.isEdit
      });
      $(recordsHTML).insertBefore($nowElt);
      return model.add(records, insertPosition);
    } else {
      recordsHTML = RecordView.render({
        records: records,
        isEdit: this.isEdit
      });
      $policys.append(recordsHTML);
      return model.add(records);
    }
  };

  PolicyView.prototype.remove = function(index) {
    $(this.$policys[0].children[index]).remove();
    this.model.remove(index);
    return console.log("after remove:", this.model.policys);
  };

  PolicyView.prototype.update = function(index, value) {
    var recordsHTML;
    this.model.update(index, value);
    value = this.model.policys[index];
    recordsHTML = RecordView.render({
      records: value,
      isEdit: this.isEdit
    });
    $(this.$policys.children()[index]).html($(recordsHTML).children());
    return console.log("after update:", this.model.policys);
  };

  return PolicyView;

})();

PolicyList = {
  templateName: "#policy-list-template",
  render: function(opt) {
    var $renderTo, policys, template;
    policys = opt.policys, $renderTo = opt.$renderTo;
    template = compileTemplate(this.templateName);
    $renderTo.html(template({
      "policys": policys
    }));
    return $renderTo.on("click", "li", $.proxy(this.clickEvent, this));
  },
  clickEvent: function(e) {
    var $elt, policyId;
    $elt = $(e.target);
    policyId = $elt.attr("policy-id");
    return getPolicyById({
      policyId: policyId
    });
  }
};

getPolicyList = function(opt) {
  var $renderTo;
  $renderTo = opt.$renderTo;
  return $.ajax({
    url: "/policy/list/",
    type: "GET",
    success: function(data) {
      return PolicyList.render({
        policys: data.body,
        $renderTo: $renderTo
      });
    },
    fail: function(data) {
      return alert("request policy fail");
    }
  });
};

getPolicyById = function(opt) {
  var $renderTo, policyId;
  policyId = opt.policyId, $renderTo = opt.$renderTo;
  return $.ajax({
    url: "/policy/" + policyId,
    type: "GET",
    success: function(data) {
      var policyView;
      console.log(data);
      policyView = new PolicyView({
        $renderTo: $("#policy-show-area"),
        isEdit: true
      });
      policyView.init({
        roomId: "双击编辑",
        policyId: "",
        description: "双击编辑",
        policy: []
      });
      return policyView.add(data.body);
    },
    fail: function(data) {
      return alert("request policy fail");
    }
  });
};

getNowPolicy = function(opt) {
  var $renderTo, roomId;
  roomId = opt.roomId, $renderTo = opt.$renderTo;
  return $.ajax({
    url: "/policy/now/room/" + roomId + "/",
    type: "GET",
    success: function(data) {
      var policyView;
      policyView = new PolicyView({
        $renderTo: $renderTo,
        isEdit: false
      });
      policyView.init(data.body);
      return policyView.add(data.body.policy);
    },
    fail: function(data) {
      return alert("request policy fail");
    }
  });
};
